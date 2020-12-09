# videoWindow.py

from video.videoWindow_ui import Ui_videoDockWidget
import video.seqIo as seqIo
from PySide2.QtCore import Signal, Slot, QRect, QPoint, Qt, QObject
from PySide2.QtGui import QColor, QPixmap, QPainter
from PySide2.QtWidgets import QDockWidget, QFileDialog
import time
from timecode import Timecode

class VideoDockWidget(QDockWidget):

    openReader = Signal(str)
    quitting = Signal()

    def __init__(self, bento):
        super(VideoDockWidget, self).__init__()
        self.bento = bento
        self.ui = Ui_videoDockWidget()
        self.ui.setupUi(self)
        self.ui.openButton.clicked.connect(self.openFile)
        self.quitting.connect(self.bento.quit)

        self.reader = None
        self.pixmap = QPixmap()
        self.active_annots = []

    def load_video(self, fn):
        self.reader = seqIo.seqIo_reader(fn)
        frame_width = self.reader.header['width']
        frame_height = self.reader.header['height']
        self.resize(frame_width, frame_height)
        self.ui.label.setGeometry(QRect(0, 0, frame_width, frame_height))
        self.updateFrame(self.bento.current_time)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.skipBackward()
            else:
                self.bento.decrementTime()
        elif event.key() == Qt.Key_Right:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.skipForward()
            else:
                self.bento.incrementTime()
        elif event.key() == Qt.Key_Up:
            self.bento.toPrevEvent()
        elif event.key() == Qt.Key_Down:
            self.bento.toNextEvent()
        elif event.key() == Qt.Key_Q:
            self.quitting.emit()
        elif event.key() == Qt.Key_Space and self.bento.player:
            self.bento.player.togglePlayer()
        else:
            return
        event.accept()

    @Slot(Timecode)
    def updateFrame(self, t):
        if not self.reader:
            return
        i = min(t.frames, self.reader.header['numFrames']-1)
        image, _ = self.reader.getFrame(i, decode=False)
        self.pixmap.loadFromData(image.tobytes())
        # add annotations
        painter = QPainter(self.pixmap)
        font = painter.font()
        pointSize = font.pointSize()+10
        font.setPointSize(pointSize)
        painter.setFont(font)
        margin = QPoint(10, 30)
        for annot in self.active_annots:
            label = annot[0] + ": " + annot[1]
            painter.setPen(annot[2])
            painter.drawText(self.ui.label.rect().topLeft() + margin, label)
            margin.setY(margin.y() + pointSize + 3)
        self.ui.label.setPixmap(self.pixmap)
        self.show()

    @Slot(list)
    def updateAnnots(self, annots):
        self.active_annots = annots

    @Slot()
    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self,
            "Open Video", "", "Video Files (*.seq)")
        print(f"filename: {filename}")
        if filename:
            self.load_video(filename)
