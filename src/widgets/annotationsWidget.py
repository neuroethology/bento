# annotationWidget.py
"""
"""

from qtpy.QtCore import Qt, QMargins, QPointF, QRectF, Slot
from qtpy.QtGui import (QBrush, QFontMetrics, QPen, QKeyEvent, QMouseEvent,
    QTransform, QWheelEvent)
from qtpy.QtWidgets import QGraphicsScene, QGraphicsView
from timecode import Timecode
from utils import quantizeTicksScale, round_to_3

class AnnotationsView(QGraphicsView):
    """
    AnnotationsView is a Qt viewer class that supports horizontal display
    of annotation bouts along a timeline.  The scale of the timeline and the
    position in time can be changed by pinch gestures and mouse drags respectively,
    as well as external input via setters.
    The annotation bouts themselves are represented in an AnnotationsScene, derived
    from QtGraphicsScene
    """

    def __init__(self, parent=None, showTickLabels = True):
        super().__init__(parent)
        self.bento = None
        self.start_x = 0.
        self.scale_h = 1.
        self.scale_v = 10.
        #self.v_factor = self.height()
        self.scale(self.scale_v, self.scale_h)
        self.sample_rate = 30.
        self.disablePositionUpdates = False
        self.time_x = Timecode(str(self.sample_rate), '0:0:0:1')
        # NB: Unfortunately, we can't turn on scrollBar tracking, because it causes
        # an infinite loop setting the current time -> moving the scroll bar ->
        # updating the time, etc.
        self.horizontalScrollBar().sliderPressed.connect(self.startHScroll)
        self.horizontalScrollBar().sliderMoved.connect(self.updateFromScroll)
        self.horizontalScrollBar().sliderReleased.connect(self.endHScroll)
        self.horizontalScrollBar().setTracking(True)
        self.ticksScale = 1.
        self.setInteractive(False)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.showTickLabels = showTickLabels

    def set_bento(self, bento):
        self.bento = bento

    def set_showTickLabels(self, showTickLabels):
        self.showTickLabels = showTickLabels

    #def set_v_factor(self, v_factor):
    #    self.v_factor = self.height

    @Slot(Timecode)
    def updatePosition(self, t):
        if self.disablePositionUpdates:
            # break infinite signal loop when we're the source of the
            # time update
            return
        pt = QPointF(t.float, self.scene().height/2.)
        self.centerOn(pt)
        self.show()

    def setTransformScale(self, t, scale_h: float=None, scale_v: float=None):
        if scale_h == None:
            scale_h = t.m11()
        if scale_v == None:
            scale_v = t.m22()
        t.setMatrix(
                scale_h,
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

    def setScale(self, hScale: float, vScale: float) -> None:
        self.setTransformScale(self.transform(), scale_h=hScale, scale_v=vScale)

    def setHScale(self, hScale):
        self.setTransformScale(self.transform(), scale_h=hScale)
        initialTicksScale = 100./hScale
        self.ticksScale = quantizeTicksScale(initialTicksScale)

    def setVScale(self, vScale):
        self.setTransformScale(self.transform(), scale_v=vScale)

    @Slot(float)
    def setHScaleAndShow(self, hScale):
        self.scale_h = hScale
        self.setHScale(hScale)
        self.updatePosition(self.bento.current_time()) # calls show()

    @Slot(float)
    def setVScaleAndShow(self, v_factor):
        self.scale_v = self.height()/v_factor
        self.setVScale(self.scale_v)
        self.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Override the widget behavior on key strokes
        # to let the parent window handle the event
        event.ignore()

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Override the widget behavior on wheel events
        # (including "magic mouse" and trackpad gestures)
        if event.phase() == Qt.ScrollUpdate:
            self.bento.change_time(int(event.angleDelta().x() / 2))
            event.accept()
        else: # ignores wheel "momentum" among other things
            event.ignore()
        # super().wheelEvent(event)

    def mousePressEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        assert not self.transform().isRotating()
        self.scale_h = self.transform().m11()
        self.start_x = event.localPos().x() / self.scale_h
        self.time_x = self.bento.get_time()
        event.accept()

    def mouseMoveEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        x = event.localPos().x() / self.scale_h
        self.bento.set_time(Timecode(
            self.time_x.framerate,
            start_seconds=self.time_x.float + (self.start_x - x)
        ))
        event.accept()

    @Slot()
    def startHScroll(self):
        self.disablePositionUpdates = True

    @Slot(int)
    def updateFromScroll(self):
        assert self.bento
        viewrect = self.viewport().rect()
        print(f"viewrect width: {viewrect.width()}")
        center = self.viewport().rect().center()
        sceneCenter = self.mapToScene(center)
        newTime = Timecode(
            framerate=self.time_x.framerate,
            start_seconds=sceneCenter.x())
        self.bento.set_time(newTime)

    @Slot()
    def endHScroll(self):
        self.disablePositionUpdates = False
        self.updateFromScroll()

    def maybeDrawPendingBout(self, painter, rect):
        bout = self.bento.pending_bout
        if not bout:
            return
        now = self.bento.get_time().float
        brush = QBrush(bout.color(), bs=Qt.DiagCrossPattern)
        painterTransform = painter.transform()
        brushTransform = QTransform.fromScale(
            1./painterTransform.m11(),
            1./painterTransform.m22())
        brush.setTransform(brushTransform)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(QRectF(QPointF(bout.start().float, rect.top()), QPointF(now, rect.bottom())))
        painter.setBrush(Qt.NoBrush)

    def drawForeground(self, painter, rect):
        """
        drawForeground
        Draws a pending annotation bout, if one is in the process of being added, deleted or changed,
        and timing tick marks and labels, if enabled.  Overrides the default drawForeground, which
        does nothing.

        In order to draw the tick labels, we need to change the transform to identity so that
        the labels (and tick amrks themselves) don't scale when the user changes
        the view's horizontal scale.  To figure out where to draw the ticks and labels,
        we need to get their positions in pixels before we change the transform, do the drawing
        in pixel coordinates, and finally restore the transform.
        """
        self.maybeDrawPendingBout(painter, rect)

        # gather the position data we need in pixel coordinates
        # Note that mapFromScene requires both x and y coordinates, expressed in one of several ways,
        # and also returns a QPointF
        now = self.bento.get_time().float
        pen = QPen(Qt.black)
        pen.setWidth(0)
        painter.setPen(pen)
        nowTop = QPointF(now, rect.top())
        nowBottom = QPointF(now, rect.bottom())
        device_nowTop = self.mapFromScene(nowTop)
        device_nowBottom = self.mapFromScene(nowBottom)
        device_now = device_nowTop.x()
        device_left, device_top = self.mapFromScene(rect.topLeft()).toTuple()
        device_right, device_bottom = self.mapFromScene(rect.bottomRight()).toTuple()
        device_ticksScale = self.mapFromScene(QPointF(now + self.ticksScale, rect.top())).x() - device_now

        # transform to identity to facilitate drawing tick labels that don't scale
        savedTransform = painter.transform()
        painter.setTransform(QTransform())
        painter.drawLine(
            device_nowTop,
            device_nowBottom
            )
        # draw the time label
        if self.showTickLabels:
            font = painter.font()
            fm = QFontMetrics(font)
            text = '0.0'
            tickLabelY = device_top + fm.ascent() + 2
            painter.drawText(device_now + 4, tickLabelY, text)
        # draw tick marks
        if self.scene().loaded:
            eighth = (device_bottom - device_top) / 8.
            eighthDown = device_top + eighth
            eighthUp = device_bottom - eighth
            device_offset = device_ticksScale
            offset = self.ticksScale
            while device_now + device_offset < device_right:
                painter.drawLine(
                    QPointF(device_now + device_offset, device_top),
                    QPointF(device_now + device_offset, eighthDown)
                )
                painter.drawLine(
                    QPointF(device_now + device_offset, eighthUp),
                    QPointF(device_now + device_offset, device_bottom)
                )
                painter.drawLine(
                    QPointF(device_now - device_offset, device_top),
                    QPointF(device_now - device_offset, eighthDown)
                )
                painter.drawLine(
                    QPointF(device_now - device_offset, eighthUp),
                    QPointF(device_now - device_offset, device_bottom)
                )
                if self.showTickLabels:
                    text = str(round_to_3(offset))
                    painter.drawText(device_now + device_offset + 4, tickLabelY, text)
                    text = "-" + text
                    painter.drawText(device_now - device_offset + 4, tickLabelY, text)
                    offset += self.ticksScale
                device_offset += device_ticksScale
        # restore original transform
        painter.setTransform(savedTransform)

class AnnotationsScene(QGraphicsScene):
    """
    AnnotationsScene is a class to contain annotation bouts for display in an
    AnnotationsView widget.  The horizontal axis is scaled in seconds, represented
    as a float, which can be produced directly by the timecode class.
    Multiple views of the AnnotationsScene can be supported, so that the annotation
    bouts can easily be shown against a variety of data, as well as separately in
    the main annotations view.
    """

    def __init__(self, sample_rate=30.):
        super().__init__()
        self.setBackgroundBrush(QBrush(Qt.white))
        self.height = 1.
        self.sample_rate = sample_rate
        self.chan_map = {}
        self.loaded = False

    # def addBout(self, bout, chan):
    #     """
    #     Add a bout to the scene according to its timecode and channel name or number.
    #     """
    #     if isinstance(chan, int):
    #         chan_num = chan
    #     elif isinstance(chan, str):
    #         if chan not in self.chan_map.keys():
    #             self.chan_map[chan] = len(self.chan_map.keys()) # add the new channel
    #         chan_num = self.chan_map[chan]
    #     else:
    #         raise RuntimeError(f"addBout: expected int or str, but got {type(chan)}")
    #     color = bout.color
    #     self.addRect(bout.start().float, float(chan_num), bout.len().float, 1., QPen(QBrush(), 0, s=Qt.NoPen), QBrush(color()))
    #     self.loaded = True

    def loadAnnotations(self, annotations, activeChannels, sample_rate):
        self.setSampleRate(sample_rate)
        self.height = float(len(activeChannels))
        for ix, chan in enumerate(activeChannels):
            self.chan_map[chan] = ix
            channel = annotations.channel(chan)
            channel.set_top(float(ix))
            self.addItem(channel)
            # channel.contentChanged.connect(self.sceneChanged)
            # self.loadBouts(annotations.channel(chan),  ix)
        self.loaded = True


    # def loadBouts(self, channel, chan_num):
    #     print(f"Loading bouts for channel {chan_num}")
    #     for bout in channel:
    #         self.addBout(bout, chan_num)

    def setSampleRate(self, sample_rate):
        self.sample_rate = sample_rate

    @Slot(float, float)
    def sceneChanged(self, start, end):
        self.invalidate(start, 0., end - start, self.height)
