# annotationWidget.py
"""
"""

from qtpy.QtCore import Qt, QPointF, QRectF, Signal, Slot
from qtpy.QtGui import (QBrush, QPen, QKeyEvent, QMouseEvent,
    QTransform, QWheelEvent)
from qtpy.QtWidgets import QGraphicsScene, QGraphicsView
from timecode import Timecode

class AnnotationsView(QGraphicsView):
    """
    AnnotationsView is a Qt viewer class that supports horizontal display
    of annotation bouts along a timeline.  The scale of the timeline and the
    position in time can be changed by pinch gestures and mouse drags respectively,
    as well as external input via setters.
    The annotation bouts themselves are represented in an AnnotationsScene, derived
    from QtGraphicsScene
    """

    hScaleChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bento = None
        self.start_x = 0.
        self.scale_h = 1.
        self.scale_v = 10.
        #self.v_factor = self.height()
        self.scale(self.scale_v, self.scale_h)
        self.sample_rate = 30.
        self.time_x = Timecode(str(self.sample_rate), '0:0:0:1')
        self.horizontalScrollBar().setTracking(True)
        self.connectScrollBarSignal()
        self.horizontalScrollBar().sliderReleased.connect(self.updateFromScroll)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ticksScale = 1.
        self.setInteractive(False)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def set_bento(self, bento):
        self.bento = bento

    def connectScrollBarSignal(self):
        self.horizontalScrollBar().valueChanged.connect(self.updateFromScroll)

    def disconnectScrollBarSignal(self):
        self.horizontalScrollBar().valueChanged.disconnect(self.updateFromScroll)

    @Slot(Timecode)
    def updatePosition(self, t):
        # We need to prevent the update of the horizontal scroll bar when
        # triggered by the centerOn() call from emitting the valueChanged
        # signal.  We do this by disconnecting the scroll bar's valueChanged
        # signal, and reconnecting it when we're done.  Note that this is not
        # safe in the face of exceptions, but no exceptions are expected here.
        self.disconnectScrollBarSignal()
        pt = QPointF(t.float, self.scene().height/2.)
        self.centerOn(pt)
        self.update()
        self.connectScrollBarSignal()

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

    def setVScale(self, vScale):
        self.setTransformScale(self.transform(), scale_v=vScale)

    @Slot(float)
    def setHScaleAndUpdate(self, hScale):
        self.scale_h = hScale
        self.setHScale(hScale)
        self.updatePosition(self.bento.current_time()) # calls update()

    @Slot(float)
    def setVScaleAndUpdate(self, v_factor):
        self.scale_v = self.height()/v_factor
        self.setVScale(self.scale_v)
        self.update()

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

    # def mousePressEvent(self, event):
    #     assert isinstance(event, QMouseEvent)
    #     assert self.bento
    #     assert not self.transform().isRotating()
    #     self.scale_h = self.transform().m11()
    #     self.start_x = event.localPos().x() / self.scale_h
    #     self.time_x = self.bento.get_time()
    #     event.accept()

    def mousePressEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        t = self.transform()
        assert not t.isRotating()
        self.start_transform = QTransform(t)
        self.scale_h = t.m11()
        self.start_x = event.localPos().x()
        self.time_x = self.bento.get_time()
        event.accept()

    def mouseMoveEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        if event.modifiers() & Qt.ShiftModifier:
            factor_x = event.localPos().x() / self.start_x
            t = QTransform(self.start_transform)
            t.scale(factor_x, 1.)
            self.setTransform(t, combine=False)
            self.synchronizeHScale()
        else:
            x = event.localPos().x() / self.scale_h
            start_x = self.start_x / self.scale_h
            self.bento.set_time(Timecode(
                self.time_x.framerate,
                start_seconds=self.time_x.float + (start_x - x)
            ))
        event.accept()

    # def mouseMoveEvent(self, event):
    #     assert isinstance(event, QMouseEvent)
    #     assert self.bento
    #     x = event.localPos().x() / self.scale_h
    #     self.bento.set_time(Timecode(
    #         self.time_x.framerate,
    #         start_seconds=self.time_x.float + (self.start_x - x)
    #     ))
    #     event.accept()

    def synchronizeHScale(self):
        self.hScaleChanged.emit(self.transform().m11())

    def updateFromScroll(self):
        assert self.bento
        center = self.viewport().rect().center()
        sceneCenter = self.mapToScene(center)
        self.bento.set_time(Timecode(
            self.time_x.framerate,
            start_seconds=sceneCenter.x()
        ))

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
        self.maybeDrawPendingBout(painter, rect)
        # draw current time indicator
        now = self.bento.get_time().float
        pen = QPen(Qt.black)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.drawLine(
            QPointF(now, rect.top()),
            QPointF(now, rect.bottom())
            )
        # draw tick marks
        if self.scene().loaded:
            offset = self.ticksScale
            eighth = (rect.bottom() - rect.top()) / 8.
            eighthDown = rect.top() + eighth
            eighthUp = rect.bottom() - eighth
            while now + offset < rect.right():
                painter.drawLine(
                    QPointF(now + offset, rect.top()),
                    QPointF(now + offset, eighthDown)
                )
                painter.drawLine(
                    QPointF(now + offset, eighthUp),
                    QPointF(now + offset, rect.bottom())
                )
                painter.drawLine(
                    QPointF(now - offset, rect.top()),
                    QPointF(now - offset, eighthDown)
                )
                painter.drawLine(
                    QPointF(now - offset, eighthUp),
                    QPointF(now - offset, rect.bottom())
                )
                offset += self.ticksScale

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

    def addBout(self, bout, chan):
        """
        Add a bout to the scene according to its timecode and channel name or number.
        """
        if isinstance(chan, int):
            chan_num = chan
        elif isinstance(chan, str):
            if chan not in self.chan_map.keys():
                self.chan_map[chan] = len(self.chan_map.keys()) # add the new channel
            chan_num = self.chan_map[chan]
        else:
            raise RuntimeError(f"addBout: expected int or str, but got {type(chan)}")
        color = bout.color
        self.addRect(bout.start().float, float(chan_num), bout.len().float, 1., QPen(QBrush(), 0, s=Qt.NoPen), QBrush(color()))
        self.loaded = True

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

    def loadBouts(self, channel, chan_num):
        print(f"Loading bouts for channel {chan_num}")
        for bout in channel:
            self.addBout(bout, chan_num)

    def setSampleRate(self, sample_rate):
        self.sample_rate = sample_rate

    @Slot(float, float)
    def sceneChanged(self, start, end):
        self.invalidate(start, 0., end - start, self.height)
