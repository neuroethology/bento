# videoWindow.py

from video.videoWindow_ui import Ui_videoFrame
import video.seqIo as seqIo
import video.mp4Io as mp4Io
from qtpy.QtCore import Signal, Slot, QMargins, QPointF, QRectF, Qt, QUrl
from qtpy.QtGui import QBrush, QFontMetrics, QPen, QPixmap, QImage, QPolygonF
from qtpy.QtWidgets import QFrame, QGraphicsScene, QGraphicsItem
from qtpy.QtMultimedia import QMediaPlayer
from qtpy.QtMultimediaWidgets import QGraphicsVideoItem
from timecode import Timecode
import numpy as np
import os
import time

class VideoScene(QGraphicsScene):
    """
    A scene that knows how to draw annotations text into its foreground
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.annots = None
        self.pose_class = None
        self.pose_frame_ix = 0
        self.showPoseData = False

    def setAnnots(self, annots):
        self.annots = annots

    def setPoseClass(self, pose_class):
        self.pose_class = pose_class

    def setShowPoseData(self, showPoseData):
        self.showPoseData = showPoseData

    def setPoseFrameIx(self, ix):
        self.pose_frame_ix = ix

    def drawPoses(self, painter):
        if self.showPoseData and self.pose_class:
            self.pose_class.drawPoses(painter, self.pose_frame_ix)

    def drawForeground(self, painter, rect):
        # add poses
        self.drawPoses(painter)
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
        if self.annots:
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

        # data related to video
        self.reader = None
        self.scene = VideoScene()
        self.ui.videoView.setScene(self.scene)
        self.ui.showPoseCheckBox.stateChanged.connect(self.showPoseDataChanged)
        self.player = QMediaPlayer()
        self.playerItem = QGraphicsVideoItem()
        self.player.setVideoOutput(self.playerItem)
        self.scene.addItem(self.playerItem)
        self.playerItem.setFlag(QGraphicsItem.ItemStacksBehindParent)
        self.playerItem.setZValue(2.0)
        bounds = self.playerItem.boundingRect()
        leftHalf = QRectF(bounds)
        leftHalf.setWidth(bounds.width() / 2.)
        self.rectItem = self.scene.addRect(leftHalf, brush=QBrush(Qt.red))
        self.rectItem.setZValue(1.0)
        self.player.durationChanged.connect(self.bento.noteVideoDurationChanged)

        # self.pixmap = QPixmap()
        # self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.active_annots = []
        self.aspect_ratio = 1.

    def resizeEvent(self, event):
        # self.ui.videoView.fitInView(self.pixmapItem, aspectRadioMode=Qt.KeepAspectRatio)
        self.ui.videoView.fitInView(self.playerItem, aspectRadioMode=Qt.KeepAspectRatio)

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
            self.player.setMedia(QUrl(f"file:///{fn}"))
            self.ui.videoView.show()
            # force the player to load the media
            self.player.play()
            self.player.pause()
            # reset to beginning
            self.player.setPosition(0)
            # self.reader = mp4Io.mp4Io_reader(fn)
        # elif self.ext=='seq':
        #     self.reader = seqIo.seqIo_reader(fn)
        else:
            raise Exception(f"video format {self.ext} not supported.")
        frame_size = self.playerItem.nativeSize()
        self.aspect_ratio = frame_size.height() / frame_size.width()
        # frame_width = self.reader.header['width']
        # frame_height = self.reader.header['height']
        # self.aspect_ratio = float(frame_height) / float(frame_width)
        print(f"aspect_ratio set to {self.aspect_ratio}")
        self.updateFrame(self.bento.current_time)
        self.ui.videoView.fitInView(self.playerItem, aspectRadioMode=Qt.KeepAspectRatio)
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
        return float(self.player.duration() / 1000.)

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

    @Slot()
    def play(self):
        self.player.play()

    @Slot()
    def stop(self):
        self.player.pause()
        self.bento.set_time(Timecode(30.0, start_seconds=self.player.position()/1000.))

    @Slot(float)
    def setPlaybackRate(self, rate):
        self.player.setPlaybackRate(rate)

    @Slot(Timecode)
    def updateFrame(self, t):
        # if not self.reader:
        #     return
        # myTc = Timecode(self.reader.header['fps'], start_seconds=t.float)
        # i = min(myTc.frames, self.reader.header['numFrames']-1)
        # image, _ = self.reader.getFrame(i, decode=False)
        if self.ext=='mp4' or self.ext=='avi':
            # no need to do anything with native video for normal playing
            # just set the position in response to explicit repositioning
            self.player.setPosition(int(t.float * 1000.))
            # h, w, ch = image.shape
            # bytes_per_line = ch * w
            # convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
            # convert_to_Qt_format = QPixmap.fromImage(convert_to_Qt_format)
            # self.pixmapItem.setPixmap(convert_to_Qt_format)
        # elif self.ext=='seq':
        #     self.pixmap.loadFromData(image.tobytes())
        #     self.pixmapItem.setPixmap(self.pixmap)
        else:
            raise Exception(f"video format {self.ext} not supported")

        # get the frame number for this frame and set it into the scene,
        # whether we have and are showing pose data or not
        # self.scene.setPoseFrameIx(myTc.frames)
        self.scene.setPoseFrameIx(t.frames)
        self.ui.videoView.update()

        if isinstance(self.scene, VideoScene):
            self.scene.setAnnots(self.active_annots)
        self.show()

    @Slot(list)
    def updateAnnots(self, annots):
        self.active_annots = annots

    @Slot(Qt.CheckState)
    def showPoseDataChanged(self, showPoseData):
        if self.scene:
            self.scene.setShowPoseData(bool(showPoseData))
            self.updateFrame(self.bento.current_time)   # force redraw
