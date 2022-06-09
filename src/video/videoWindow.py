# videoWindow.py

from video.videoWindow_ui import Ui_videoFrame
from video.videoScene import VideoSceneAbstractBase, VideoSceneNative, VideoScenePixmap
from qtpy.QtCore import QEvent, Qt, Signal, Slot
from qtpy.QtWidgets import QFrame
from qtpy.QtMultimedia import QMediaPlayer
import os
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
        bento.quitting.connect(self.close)

        # data related to video
        self.scene = None
        self.aspect_ratio = 1.

        self.active_annots = []

    def resizeFrame(self):
        self.ui.videoView.fitInView(self.scene.videoItem(), aspectRadioMode=Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.resizeFrame()

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

    def supported_by_native_player(self, fn: str) -> bool:
        ext = os.path.basename(fn).rsplit('.',1)[-1].lower()
        if ext in VideoSceneNative(self.bento, self.bento.current_time()).supportedFormats():
            return True
        if not ext in VideoScenePixmap(self.bento, self.bento.current_time()).supportedFormats():
            raise Exception(f"video format {ext} not supported.")
        return False

    def load_video(self, fn: str, start_time: Timecode, forcePixmapMode: bool):
        if not forcePixmapMode and self.supported_by_native_player(fn):
            self.scene = VideoSceneNative(self.bento, start_time)
        else:
            self.scene = VideoScenePixmap(self.bento, start_time)
        self.scene.setVideoPath(fn)
        self.ui.videoView.setScene(self.scene)
        self.ui.showPoseCheckBox.stateChanged.connect(self.showPoseDataChanged)
        self.ui.videoView.show()
        self.aspect_ratio = self.scene.aspectRatio()
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.resizeFrame()
        self.scene.updateFrame(self.bento.current_time())

    def set_pose_class(self, pose_class):
        self.scene.setPoseClass(pose_class)
        self.ui.showPoseCheckBox.setEnabled(bool(pose_class))
        self.scene.setShowPoseData(bool(pose_class) and self.ui.showPoseCheckBox.isChecked())

    def set_start_time(self, t):
        self.scene.setStartTime(t)

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

    def reset(self):
        if isinstance(self.scene, VideoSceneAbstractBase):
            self.scene.reset()

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