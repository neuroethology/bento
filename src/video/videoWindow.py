# videoWindow.py

from video.videoWindow_ui import Ui_videoFrame
import video.seqIo as seqIo
import video.mp4Io as mp4Io
from qtpy.QtCore import Signal, Slot, QMargins, Qt
from qtpy.QtGui import QBrush, QFontMetrics, QPixmap, QImage
from qtpy.QtWidgets import QFrame, QGraphicsScene
from timecode import Timecode
import os
import time

class VideoScene(QGraphicsScene):
    """
    A scene that knows how to draw annotations text into its foreground
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.annots = None

    def setAnnots(self, annots):
        self.annots = annots

    def drawForeground(self, painter, rect):
        # add annotations
        font = painter.font()
        pointSize = font.pointSize()+10
        font.setPointSize(pointSize)
        painter.setFont(font)
        margins = QMargins(10, 10, 0, 0)
        fm = QFontMetrics(font)
        flags = Qt.AlignLeft | Qt.AlignTop
        rectWithMargins = rect.toRect()
        rectWithMargins -= margins
        whiteBrush = QBrush(Qt.white)
        blackBrush = QBrush(Qt.black)
        for annot in self.annots:
            painter.setBrush(whiteBrush if annot[2].lightnessF() < 0.5 else blackBrush)
            text = annot[0] + ": " + annot[1]
            bounds = fm.boundingRect(rectWithMargins, flags, text)
            painter.setPen(Qt.NoPen)
            painter.drawRect(bounds)
            painter.setPen(annot[2])
            painter.drawText(bounds, text)
            margins.setTop(margins.top() + pointSize + 3)
            rectWithMargins = rect.toRect()
            rectWithMargins -= margins

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
        bento.quitting.connect(self.close)

        self.reader = None
        self.scene = VideoScene()
        self.ui.videoView.setScene(self.scene)
        self.pixmap = QPixmap()
        self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.active_annots = []
        self.aspect_ratio = 1.

    def resizeEvent(self, event):
        self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)

    def mouseReleaseEvent(self, event):
        viewport = self.ui.videoView.viewport()
        viewAspectRatio = viewport.height() / viewport.width()
        if viewAspectRatio == self.aspect_ratio:
            print("just right")
            return
        elif viewAspectRatio < self.aspect_ratio:
            # too wide
            print("too wide")
        else:
            # too tall
            print("too tall")

    def load_video(self, fn):
        self.ext = os.path.basename(fn).rsplit('.',1)[-1]
        if self.ext=='mp4' or self.ext=='avi':
            self.reader = mp4Io.mp4Io_reader(fn)
        elif self.ext=='seq':
            self.reader = seqIo.seqIo_reader(fn)
        else:
            raise Exception(f"video format {self.ext} not supported.")
        frame_width = self.reader.header['width']
        frame_height = self.reader.header['height']
        self.aspect_ratio = float(frame_height) / float(frame_width)
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.updateFrame(self.bento.current_time)
        self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)

    def sample_rate(self):
        if not self.reader:
            return 30.0
        else:
            return self.reader.header['fps']

    def running_time(self):
        if not self.reader:
            return 0.
        return float(self.reader.header['numFrames']) / float(self.reader.header['fps'])

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
        myTc = Timecode(self.reader.header['fps'], start_seconds=t.float)
        i = min(myTc.frames, self.reader.header['numFrames']-1)
        image, _ = self.reader.getFrame(i, decode=False)
        if self.ext=='seq':
            self.pixmap.loadFromData(image.tobytes())
            self.pixmapItem.setPixmap(self.pixmap)
        elif self.ext=='mp4' or self.ext=='avi':
            h, w, ch = image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            convert_to_Qt_format = QPixmap.fromImage(convert_to_Qt_format)
            self.pixmapItem.setPixmap(convert_to_Qt_format)
        else:
            raise Exception(f"video format {self.ext} not supported")

        if isinstance(self.scene, VideoScene):
            self.scene.setAnnots(self.active_annots)
        self.show()

    @Slot(list)
    def updateAnnots(self, annots):
        self.active_annots = annots
