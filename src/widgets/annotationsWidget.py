# annotationWidget.py
"""
"""

from PySide2.QtCore import Qt, QPointF, Signal, Slot
from PySide2.QtGui import QBrush, QColor, QPen, QMouseEvent, QPaintEvent
from PySide2.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem
from timecode import Timecode
from annot.annot import Bout

class AnnotationsView(QGraphicsView):
    """
    AnnotationsView is a Qt viewer class that supports horizontal display
    of annotation bouts along a timeline.  The scale of the timeline and the
    position in time can be changed by pinch gestures and mouse drags respectively,
    as well as external input via setters.
    The annotation bouts themselves are represented in an AnnotationsScene, derived
    from QtGraphicsScene
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bento = None
        self.start_x = 0.
        self.scale_h = 1.
        self.sample_rate = 30.
        self.time_x = Timecode(str(self.sample_rate), '0:0:0:1')
        self.horizontalScrollBar().sliderReleased.connect(self.updateFromScroll)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_bento(self, bento):
        self.bento = bento
    
    @Slot(float)
    def updateScene(self):
        self.sample_rate = self.scene().sample_rate
        self.scale_h = self.height() / self.scene().height
        self.scale(10., self.scale_h)
        # self.time_x.framerate(self.sample_rate)
        self.updatePosition(self.bento.current_time)

    @Slot(Timecode)
    def updatePosition(self, t):
        pt = QPointF(t.float, self.scene().height/2.)
        self.centerOn(pt)
        self.show()

    def mousePressEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        assert not self.transform().isRotating()
        self.scale_h = self.transform().m11()
        self.start_x = event.localPos().x() / self.scale_h
        self.time_x = self.bento.get_time()

    def mouseMoveEvent(self, event):
        assert isinstance(event, QMouseEvent)
        assert self.bento
        x = event.localPos().x() / self.scale_h
        self.bento.set_time(Timecode(
            self.time_x.framerate,
            start_seconds=self.time_x.float + (self.start_x - x)
        ))

    def updateFromScroll(self):
        assert self.bento
        center = self.viewport().rect().center()
        sceneCenter = self.mapToScene(center)
        self.bento.set_time(Timecode(
            self.time_x.framerate,
            start_seconds=sceneCenter.x()
        ))
        
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
    
    def addBout(self, bout, chan):
        """
        Add a bout to the scene according to its timecode and channel name or number.
        """
        if isinstance(chan, int):
            chan_num = chan
        elif isinstance(chan, str):
            chan_num = self.chan_map[chan]
        else:
            raise RuntimeError(f"addBout: expected int or str, but got {type(chan)}")
        color = bout.color
        self.addRect(bout.start().float, float(chan_num), bout.len().float, 1., QPen(QBrush(), 0, s=Qt.NoPen), QBrush(color()))
    
    def loadAnnotations(self, annotations, activeChannels, sample_rate):
        self.setSampleRate(sample_rate)
        self.height = float(len(activeChannels))
        for ix, chan in enumerate(activeChannels):
            self.chan_map[chan] = ix
            self.loadBouts(annotations.channel(chan),  ix)

    def loadBouts(self, channel, chan_num):
        print(f"Loading bouts for channel {chan_num}")
        for bout in channel:
            self.addBout(bout, chan_num)

    def setSampleRate(self, sample_rate):
        self.sample_rate = sample_rate