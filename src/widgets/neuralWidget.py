# neuralWidget.py
"""
"""

from os import X_OK
from qtpy.QtCore import Qt, QPointF, QRectF, Signal, Slot
from qtpy.QtWidgets import (QGraphicsItem, QGraphicsItemGroup, QGraphicsPathItem, QGraphicsPixmapItem,
    QGraphicsScene, QGraphicsView, QMessageBox)
from qtpy.QtGui import (QBrush, QColor, QImage, QKeyEvent, QMouseEvent, QPainterPath, QPen,
    QPixmap, QTransform, QWheelEvent, QPolygonF)
from qtpy.QtCharts import QtCharts
import numpy as np
import pymatreader as pmr
from qimage2ndarray import gray2qimage
from timecode import Timecode
from utils import get_colormap, padded_rectf, quantizeTicksScale
from pynwb import NWBFile, TimeSeries
import warnings
import shiboken2 as shiboken
import ctypes

class QGraphicsSubSceneItem(QGraphicsItem):
    """
    A class that implements a custom QGraphicsItem which
    allows a potentially dynamically changing QGraphicsScene
    item to be added to another scene. For example, this
    allows annotations to be overlaid on top of other data.
    """

    def __init__(self, subScene, parentScene, annotations):
        super().__init__()
        self.subScene = subScene
        self.parentScene = parentScene
        self.annotations = annotations
        self.activeItem = 0.
        duration = min(self.parentScene.sceneRect().right(), self.subScene.sceneRect().right())
        targetRectF = QRectF(0., 0., duration, self.parentScene.height())
        sourceRectF = QRectF(0., 0., duration, 1.)
        self.transform = QTransform()
        self.transform.scale(1., targetRectF.height() / sourceRectF.height())
        self.subScene.changed.connect(self.updateScene)

    @Slot(str)
    def setActiveItem(self, chan):
        if chan=='':
            self.activeItem = 0.
        else:
            self.activeItem = self.annotations.channel(chan).top()

        self.update()

    def boundingRect(self):
        rect = self.transform.mapRect(self.subScene.sceneRect()) if self.subScene else QRectF()
        return rect

    def paint(self, painter, option, widget=None):
        if self.subScene:
            duration = min(self.parentScene.sceneRect().right(), self.subScene.sceneRect().right())
            targetRectF = QRectF(0., 0., duration, self.parentScene.height())
            sourceRectF = QRectF(0., float(self.activeItem), duration, 1.)
            self.subScene.render(painter, target=targetRectF, source=sourceRectF, aspectRatioMode=Qt.IgnoreAspectRatio)

    @Slot()
    def updateScene(self):
        self.update()

class NeuralView(QGraphicsView):
    """
    NeuralView is a Qt viewer class that supports horizontal display
    of neural data along a timeline.
    The neural channel data themselves are represented in a NeuralScene, derived
    from AnnotationsScene so that annotation data can be overlayed.
    """

    hScaleChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.start_transform = None
        self.start_x = 0.
        self.scale_h = 1.
        self.center_y = 0.
        self.horizontalScrollBar().sliderReleased.connect(self.updateFromScroll)
        self.verticalScrollBar().sliderReleased.connect(self.updateFromScroll)
        self.ticksScale = 1.
        self.setInteractive(False)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def set_bento(self, bento):
        self.bento = bento

    def setScene(self, scene):
        # give the sceneRect some additional padding
        # so that the start and end can be centered in the view
        super().setScene(scene)
        self.time_x = Timecode(str(scene.sample_rate), '0:0:0:1')
        self.center_y = float(scene.num_chans) / 2.

    def setTransformScaleV(self, t, scale_v: float):
        t.setMatrix(
                t.m11(),
                t.m12(),
                t.m13(),
                t.m21(),
                scale_v,
                t.m23(),
                t.m31(),
                t.m32(),
                t.m33()
            )
        self.setTransform(t, combine=False)

    def setTransformScaleH(self, t, scale_h: float):
        t.setMatrix(
            scale_h,
            t.m12(),
            t.m13(),
            t.m21(),
            t.m22(),
            t.m23(),
            t.m31(),
            t.m32(),
            t.m33()
        )
        self.setTransform(t, combine=False)

    def resizeEvent(self, event):
        oldHeight = float(event.oldSize().height())
        if oldHeight < 0.:
            return
        newHeight = float(event.size().height())
        min_scale_v = newHeight / self.sceneRect().height()
        t = self.transform()
        if t.m22() < min_scale_v:
            self.setTransformScaleV(t, min_scale_v)
        self.updatePosition(self.bento.current_time())
        self.synchronizeHScale()

    @Slot()
    def updateScene(self):
        self.sample_rate = self.scene().sample_rate

        self.center_y = self.scene().height() / 2.
        scale_v = self.viewport().height() / self.scene().height()
        self.scale(10., scale_v)
        self.updatePosition(self.bento.current_time())

    @Slot(Timecode)
    def updatePosition(self, t):
        pt = QPointF(t.float, self.center_y)
        self.centerOn(pt)
        self.update()

    def synchronizeHScale(self):
        self.hScaleChanged.emit(self.transform().m11())

    def mousePressEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        t = self.transform()
        assert not t.isRotating()
        self.start_transform = QTransform(t)
        self.scale_h = t.m11()
        self.start_x = event.localPos().x()
        self.start_y = event.localPos().y()
        self.time_x = self.bento.get_time()
        self.center_y_start = self.center_y

    def mouseMoveEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        if event.modifiers() & Qt.ShiftModifier:
            factor_x = max(0.1, event.localPos().x()) / self.start_x
            factor_y = event.localPos().y() / self.start_y
            t = QTransform(self.start_transform)
            t.scale(factor_x, factor_y)
            min_scale_v = self.viewport().rect().height() / self.sceneRect().height()
            self.setTransformScaleV(t, max(min_scale_v, t.m22()))
            min_scale_h = self.viewport().rect().width() / self.sceneRect().width()
            h_scale = max(min_scale_h, t.m11())
            initialTicksScale = 100./h_scale
            self.ticksScale = quantizeTicksScale(initialTicksScale)
            self.setTransformScaleH(t, h_scale)
            self.synchronizeHScale()
        else:
            x = event.localPos().x() / self.scale_h
            start_x = self.start_x / self.scale_h
            self.center_y = self.center_y_start + (self.mapToScene(self.start_x, self.start_y).y()
                - self.mapToScene(event.x(), event.y()).y())
            self.bento.set_time(Timecode(
                self.time_x.framerate,
                start_seconds=self.time_x.float + (start_x - x)
            ))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Override the widget behavior on key strokes
        # to let the parent window handle the event
        event.ignore()
    
    def updateFromScroll(self):
        assert self.bento
        center = self.viewport().rect().center()
        sceneCenter = self.mapToScene(center)
        self.center_y = sceneCenter.y()
        self.bento.set_time(Timecode(
            self.time_x.framerate,
            start_seconds=sceneCenter.x()
        ))

    def drawForeground(self, painter, rect):
        now = self.bento.get_time().float
        pen = QPen(Qt.white if self.scene().heatmap.isVisible() else Qt.black)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.drawLine(
            QPointF(now, rect.top()),
            QPointF(now, rect.bottom())
            )
        pen.setDashPattern((4, 20))
        pen.setCapStyle(Qt.FlatCap)
        painter.setPen(pen)
        offset = self.ticksScale
        while now + offset < rect.right():
            painter.drawLine(
                QPointF(now + offset, rect.top()),
                QPointF(now + offset, rect.bottom())
            )
            painter.drawLine(
                QPointF(now - offset, rect.top()),
                QPointF(now - offset, rect.bottom())
            )
            offset += self.ticksScale

class NeuralColorMapper():
    """
    Apply the selected color map to scalar image data
    """

    def __init__(self, min_val: float, max_val: float, colormap_name = "viridis"):
        self.data_min = min_val
        self.data_max = max_val
        self.data_ptp = max_val - min_val
        self.cv_colormap = colormap_name
        self.colormap = get_colormap(colormap_name)

    def mappedImage(self, scalar_image_data: np.ndarray):
        # we use Indexed8 color, which is what gray2qimage returns, and then
        # change the colorTable from the default gray (as RGB) to the requested
        # colormap, e.g. parula, turbo (jet-like, but better) or viridis
        qImage = gray2qimage(scalar_image_data, normalize = (self.data_min, self.data_max))
        qImage.setColorTable(self.colormap)
        return qImage

class NeuralScene(QGraphicsScene):
    """
    Object allowing display of Calcium data along with annotations
    """

    active_channel_changed = Signal(str)
    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QBrush(Qt.white))
        self.sample_rate = 30.
        self.num_chans = 0
        self.traces = QGraphicsItemGroup()
        self.data_min = None
        self.data_max = None
        self.colorMapper = None
        self.heatmapImage = None
        self.heatmap = None
        self.annotations = None
        self.activeChannel = None
        self.tracesCache = dict()
        self.tracesOrder = None

    """
    .mat files can be either old-style (MatLab 7.2 and earlier), in which case we need to use
    scipy.io.loadmat(), or h5 files, in which case we need to use h5py.File().
    However, the result of scipy.io.loadmat is a numpy array, while the result of h5py.File()
    is an h5 object, e.g. h5.DataSet or h5.Group.  The operations available on these two
    different data types are not the same, so the code cannot be common unless one is
    converted to the other.  Thankfully, pymatreader handles which reader
    to call and the conversion for us. However, it throws a UserWarning during a check of the
    data when the MatLab data type is "Opaque", which happens with our data.
    As far as I've been able to determine, the conversion proceeds correctly, so we simply
    suppress the warning.
    """
    def loadNeural(self, ca_file, sample_rate, start_frame, stop_frame, time_start,
            showTraces, showHeatmap, showAnnotations):
        self.time_start = time_start
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            mat = pmr.read_mat(ca_file)
        try:
            self.data = mat['results']['C_raw']
        except Exception as e:
            QMessageBox.about(self, "Load Error", f"Error loading neural data from file {ca_file}: {e}")
            return
        self.range = self.data.max() - self.data.min()
        # Provide for a little space between traces
        self.minimum = self.data.min() + self.range * 0.05
        self.range *= 0.9

        self.sample_rate = sample_rate
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.num_chans = self.data.shape[0]
        self.data_min = self.data.min()
        self.data_max = self.data.max()
        self.colorMapper = NeuralColorMapper(self.data_min, self.data_max, "parula")
        # for chan in range(self.num_chans):
        t_values = ((np.arange(self.data.shape[1]) - self.start_frame)/self.sample_rate) + self.time_start.float
        y_values = np.arange(self.num_chans).reshape(-1,1) + 0.5 + self.normalize(self.data)
        self.tracesOrder = y_values[:, self.start_frame]
        self.drawTraces(t_values[self.start_frame:self.stop_frame], 
                        y_values[:,self.start_frame:self.stop_frame])
        #for chan in range(self.num_chans):
        #    self.loadChannel(self.data, chan)
        self.addTraces()
        # create heatmap
        self.createHeatmap(np.arange(self.num_chans))
        # finally, add the traces on top of everything
        self.addItem(self.traces)
        # pad some time on left and right to allow centering
        sceneRect = padded_rectf(self.sceneRect())
        sceneRect.setHeight(float(self.num_chans) + 1.)
        self.setSceneRect(sceneRect)
        self.setVisibility(showTraces, showHeatmap, showAnnotations)

    def setVisibility(self, showTraces, showHeatmap, showAnnotations):
        if isinstance(self.traces, QGraphicsItem):
            self.traces.setVisible(showTraces)
        if isinstance(self.heatmap, QGraphicsItem):
            if showAnnotations:
                self.heatmap.setOpacity(0.5)
            else:
                self.heatmap.setOpacity(1.)
            self.heatmap.setVisible(showHeatmap)
        if isinstance(self.annotations, QGraphicsItem):
            self.annotations.setVisible(showAnnotations)
    
    def createHeatmap(self, order):
        self.heatmapImage, self.heatmap = None, None
        # Image has a pixel for each frame for each channel
        self.heatmapImage = self.colorMapper.mappedImage(self.data[order,self.start_frame:self.stop_frame])
        self.heatmap = self.addPixmap(QPixmap.fromImageInPlace(self.heatmapImage, Qt.NoFormatConversion))

        # Scale the heatmap's time axis by the 1 / sample rate so that it corresponds correctly
        # to the time scale
        transform = QTransform()
        transform.scale(1. / self.sample_rate, 1.)
        self.heatmap.setTransform(transform)
        self.heatmap.setOpacity(0.5)
    
    def drawTraces(self, t_values, y_values):
        for chan in range(self.num_chans):
            trace = QPainterPath()
            trace.reserve(self.stop_frame - self.start_frame)
            trace.addPolygon(self.createPoly(t_values, y_values[chan, :]))
            self.tracesCache[str(chan)] = trace

    def createPoly(self, x_values, y_values):
        if not (x_values.size == y_values.size == x_values.shape[0] == y_values.shape[0]):
            raise ValueError("Arguments must be 1D NumPy arrays with same size")
        size = x_values.size
        poly = QPolygonF(size)
        address = shiboken.getCppPointer(poly.data())[0]
        buffer = (ctypes.c_double * 2 * size).from_address(address)
        memory = np.frombuffer(buffer, np.float64)
        memory[: (size - 1) * 2 + 1 : 2] = np.array(x_values, dtype=np.float64, copy=False)
        memory[1 : (size - 1) * 2 + 2 : 2] = np.array(y_values, dtype=np.float64, copy=False)
        
        return poly

    def addTraces(self):
        self.traces = QGraphicsItemGroup()
        pen = QPen()
        pen.setWidth(0)
        for k in list(self.tracesCache.keys()):
            traceItem = QGraphicsPathItem(self.tracesCache[k])
            traceItem.setPen(pen)
            self.traces.addToGroup(traceItem)

    def reorderTracesAndHeatmap(self, showTraces, showHeatmap, showAnnotations):
        for item in self.items():
            if isinstance(item, QGraphicsItemGroup):
                self.removeItem(item)
            elif isinstance(item, QGraphicsPixmapItem):
                self.removeItem(item)
        newOrder = np.array([4,3,2,1,0])
        self.createHeatmap(newOrder)
        offset = (self.tracesOrder[newOrder] - self.tracesOrder)
        self.tracesOrder = self.tracesOrder + offset
        for chan in list(self.tracesCache.keys()):
            self.tracesCache[chan] = self.tracesCache[chan].translated(0., offset[int(chan)])
        self.addTraces()
        self.addItem(self.traces)
        self.setVisibility(showTraces, showHeatmap, showAnnotations)
    
    def normalize(self, y_val):
        return 1.0 - (y_val - self.minimum) / self.range

    def overlayAnnotations(self, annotationsScene, parentScene, annotations):
        self.annotations = QGraphicsSubSceneItem(annotationsScene, parentScene, annotations)
        self.annotations.setZValue(-1.) # draw below neural data
        self.active_channel_changed.connect(self.annotations.setActiveItem)
        self.addItem(self.annotations)
        transparentWhite = QColor(Qt.white)
        transparentWhite.setAlphaF(0.7)
        rectItem = self.addRect(QRectF(self.sceneRect()), brush=QBrush(transparentWhite))
        rectItem.setZValue(-1.) # draw below neural data

    @Slot(str)
    def setActiveChannel(self, chan):
        self.activeChannel = chan
        self.active_channel_changed.emit(self.activeChannel)

    @Slot(bool)
    def showTraces(self, enabled):
        if isinstance(self.traces, QGraphicsItem):
            self.traces.setVisible(enabled)

    @Slot(bool)
    def showHeatmap(self, enabled):
        if isinstance(self.heatmap, QGraphicsItem):
            self.heatmap.setVisible(enabled)

    @Slot(bool)
    def showAnnotations(self, enabled):
        if isinstance(self.annotations, QGraphicsItem):
            self.annotations.setVisible(enabled)
        if isinstance(self.heatmap, QGraphicsItem):
            self.heatmap.setOpacity(0.5 if enabled else 1.)
    
    def exportToNWBFile(self, nwbFile: NWBFile):
        neuralData = TimeSeries(name=f"neural_data",
                                data = self.data[:,self.start_frame+1:self.stop_frame],
                                rate=self.sample_rate,
                                starting_time = self.time_start.float,
                                unit = "None",
                                )
        nwbFile.add_acquisition(neuralData)

        return nwbFile
