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
        self.scene = None
        self.aspect_ratio = 1.

        self.active_annots = []

    def resizeEvent(self, event):
        # self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)
        self.ui.videoView.fitInView(self.scene.videoItem(), aspectRadioMode=Qt.KeepAspectRatio)

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
        self.ext = self.ext.lower()
        if self.ext in ['mp4', 'avi']:
            self.scene = VideoSceneNative(self.bento)
        elif self.ext == 'seq':
            self.scene = VideoSceneSeq(self.bento)
        else:
            raise Exception(f"video format {self.ext} not supported.")
        self.scene.setVideoPath(fn)
        self.ui.videoView.setScene(self.scene)
        self.ui.showPoseCheckBox.stateChanged.connect(self.showPoseDataChanged)
        self.ui.videoView.show()
        self.aspect_ratio = self.scene.aspectRatio()
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.scene.updateFrame(self.bento.current_time())
        self.ui.videoView.fitInView(self.scene.videoItem(), aspectRadioMode=Qt.KeepAspectRatio)

    def set_pose_class(self, pose_class):
        self.scene.setPoseClass(pose_class)
        self.ui.showPoseCheckBox.setEnabled(bool(pose_class))
        self.scene.setShowPoseData(bool(pose_class) and self.ui.showPoseCheckBox.isChecked())

    def sample_rate(self) -> float:
        return self.scene.sample_rate()

    def running_time(self) -> float:
        return self.scene.running_time()

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

    @Slot(list)
    def updateAnnots(self, annots: list):
        self.active_annots = annots
        if isinstance(self.scene, VideoSceneAbstractBase):
            self.scene.setAnnots(self.active_annots)

    @Slot(Qt.CheckState)
    def showPoseDataChanged(self, showPoseData: Qt.CheckState):
        if self.scene:
            self.scene.setShowPoseData(bool(showPoseData))
            self.scene.updateFrame(self.bento.current_time())   # force redraw

    def getPlayer(self) -> QMediaPlayer:
        if not self.scene:
            return None
        return self.scene.getPlayer()