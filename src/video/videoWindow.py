# videoWindow.py

from video.videoWindow_ui import Ui_videoFrame
import video.seqIo as seqIo
from PySide2.QtCore import Signal, Slot, QRect, QPoint, Qt
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtWidgets import QFrame, QGraphicsScene
from timecode import Timecode

class VideoFrame(QFrame):

    openReader = Signal(str)
    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.sizePolicy().setHeightForWidth(True)
        self.ui = Ui_videoFrame()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.reader = None
        self.scene = QGraphicsScene()
        self.ui.videoView.setScene(self.scene)
        self.pixmap = QPixmap()
        self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.active_annots = []
        self.aspect_ratio = 1.
    
    def hasHeightForWidth(self):
        print("called hasHeightForWidth")
        return False

    def heightForWidth(self, width):
        print(f"called heightForWidth, returning {int(float(width) * self.aspect_ratio)} for width {width}")
        return int(float(width) * self.aspect_ratio)

    def resizeEvent(self, event):
        self.ui.videoView.fitInView(self.pixmapItem, aspectRatioMode=Qt.KeepAspectRatio)

    def load_video(self, fn):
        self.reader = seqIo.seqIo_reader(fn)
        frame_width = self.reader.header['width']
        frame_height = self.reader.header['height']
        self.aspect_ratio = float(frame_height) / float(frame_width)
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.updateFrame(self.bento.current_time)
        self.ui.videoView.resize(frame_width, frame_height)
        self.ui.videoView.fitInView(self.pixmapItem, aspectRatioMode=Qt.KeepAspectRatio)

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
        # for annot in self.active_annots:
        #     label = annot[0] + ": " + annot[1]
        #     painter.setPen(annot[2])
        #     painter.drawText(self.ui.label.rect().topLeft() + margin, label)
        #     margin.setY(margin.y() + pointSize + 3)
        # self.ui.label.setPixmap(self.pixmap.scaled(self.size(), aspectMode=Qt.KeepAspectRatio))
        self.pixmapItem.setPixmap(self.pixmap)
        self.show()

    @Slot(list)
    def updateAnnots(self, annots):
        self.active_annots = annots
