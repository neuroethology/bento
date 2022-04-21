# videoWindow.py

from pose.pose import PoseBase
from video.videoWindow_ui import Ui_videoFrame
import video.seqIo as seqIo
import video.mp4Io as mp4Io
from video.videoScene import VideoSceneAbstractBase, VideoSceneNative, VideoSceneSeq
from qtpy.QtCore import QEvent, QMargins, QObject, QPointF, QRectF, Qt, QUrl, Signal, Slot
from qtpy.QtGui import QBrush, QColor, QFontMetrics, QPen, QPainter, QPixmap, QImage, QPolygonF
from qtpy.QtWidgets import QFrame, QGraphicsScene, QGraphicsItem
from qtpy.QtMultimedia import QMediaPlayer, QVideoSurfaceFormat
from qtpy.QtMultimediaWidgets import QGraphicsVideoItem
from timecode import Timecode
import numpy as np
import os
import time

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

        # data related to video
        self.running = False
        self.reader = None
        self.scene = VideoSceneNative(self.bento)
        self.ui.videoView.setScene(self.scene)
        self.ui.showPoseCheckBox.stateChanged.connect(self.showPoseDataChanged)

        # self.pixmap = QPixmap()
        # self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.active_annots = []
        self.aspect_ratio = 1.

    def resizeEvent(self, event):
        # self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)
        self.ui.videoView.fitInView(self.scene.playerItem, aspectRadioMode=Qt.KeepAspectRatio)

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
            self.scene.setVideoPath(fn)
            self.ui.videoView.show()
            # self.reader = mp4Io.mp4Io_reader(fn)
        # elif self.ext=='seq':
        #     self.reader = seqIo.seqIo_reader(fn)
        else:
            raise Exception(f"video format {self.ext} not supported.")
        frame_size = self.scene.playerItem.nativeSize()
        self.aspect_ratio = frame_size.height() / frame_size.width()
        # frame_width = self.reader.header['width']
        # frame_height = self.reader.header['height']
        # self.aspect_ratio = float(frame_height) / float(frame_width)
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.updateFrame(self.bento.current_time)
        self.ui.videoView.fitInView(self.scene.playerItem, aspectRadioMode=Qt.KeepAspectRatio)
        # self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)

    def set_pose_class(self, pose_class):
        self.scene.setPoseClass(pose_class)
        self.ui.showPoseCheckBox.setEnabled(bool(pose_class))
        self.scene.setShowPoseData(bool(pose_class) and self.ui.showPoseCheckBox.isChecked())

    def sample_rate(self):
        if not self.reader:
            return 30.0
        else:
            return self.reader.header['fps']

    def running_time(self):
        # if not self.reader:
        #     return 0.
        # return float(self.reader.header['numFrames']) / float(self.reader.header['fps'])
        return float(self.scene.player.duration() / 1000.)

    def keyPressEvent(self, event: QEvent):
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

    @Slot()
    def play(self):
        self.running = True
        self.scene.player.play()

    @Slot()
    def stop(self):
        self.scene.player.pause()
        self.running = False
        self.bento.set_time(Timecode(30.0, start_seconds=self.scene.player.position()/1000.))

    @Slot(float)
    def setPlaybackRate(self, rate: float):
        self.scene.player.setPlaybackRate(rate)

    @Slot(Timecode)
    def updateFrame(self, t: Timecode):
        # if not self.reader:
        #     return
        # myTc = Timecode(self.reader.header['fps'], start_seconds=t.float)
        # i = min(myTc.frames, self.reader.header['numFrames']-1)
        # image, _ = self.reader.getFrame(i, decode=False)
        if self.ext=='mp4' or self.ext=='avi':
            if not self.running:
                # There is no need to do anything with native video for normal playing.
                # In fact, it messes things up with a "setPosition" infinite loop!
                # Just set the position in response to explicit repositioning.
                self.scene.player.setPosition(int(t.float * 1000.))
        # elif self.ext=='seq':
        #     self.pixmap.loadFromData(image.tobytes())
        #     self.pixmapItem.setPixmap(self.pixmap)
        else:
            raise Exception(f"video format {self.ext} not supported")

    @Slot(list)
    def updateAnnots(self, annots: list):
        self.active_annots = annots
        if isinstance(self.scene, VideoSceneAbstractBase):
            self.scene.setAnnots(self.active_annots)

    @Slot(Qt.CheckState)
    def showPoseDataChanged(self, showPoseData: Qt.CheckState):
        if self.scene:
            self.scene.setShowPoseData(bool(showPoseData))
            self.updateFrame(self.bento.current_time)   # force redraw
