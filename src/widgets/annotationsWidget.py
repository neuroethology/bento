# annotationWidget.py
"""
"""

from PySide2.QtCore import Qt, QPointF, Signal, Slot
from PySide2.QtGui import QBrush, QColor, QPen, QMouseEvent
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

    def __init__(self, annotationsScene, parent=None):
        super(AnnotationsView, self).__init__(annotationsScene, parent)
        self.bento = None
        self.start_x = 0.
        self.scale_h = 1.
        self.time_x = Timecode('30.0', '0:0:0:1')

    def set_bento(self, bento):
        self.bento = bento
    
    @Slot(Timecode)
    def updatePosition(self, t):
        pt = QPointF(t.float, 0.)
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

class AnnotationsScene(QGraphicsScene):
    """
    AnnotationsScene is a class to contain annotation bouts for display in an
    AnnotationsView widget.  The horizontal axis is scaled in seconds, represented
    as a float, which can be produced directly by the timecode class.
    Multiple views the AnnotationsScene can be supported, so that the annotation
    bouts can easily be shown against a variety of data, as well as separately in
    the main annotations view.
    """

    def __init__(self):
        super(AnnotationsScene, self).__init__()
        self.setBackgroundBrush(QBrush(Qt.white))
        self.height = 1.
    
    def addBout(self, bout):
        """
        Add a bout to the scene according to its timecode.
        For now, put it vertically at (0, 1).  Eventually, we will probably want to
        place it depending on which channel it is in.
        """
        color = bout.color
        self.addRect(bout.start().float, 0., bout.len().float, self.height, QPen(QBrush(), 0, s=Qt.NoPen), QBrush(color()))
    
    def loadBouts(self, channel):
        for bout in channel:
            self.addBout(bout)