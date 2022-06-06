# videoScene.py
"""
Implement base class and derived classes for showing videos with pose and annotation overlays
"""
from pose.pose import PoseBase
import video.seqIo as seqIo
import video.mp4Io as mp4Io
from qtpy.QtCore import QMargins, QObject, QRectF, Qt, QUrl, Slot
from qtpy.QtGui import QBrush, QFontMetrics, QPainter, QPixmap
from qtpy.QtWidgets import QGraphicsScene, QGraphicsItem
from qtpy.QtMultimedia import QMediaContent, QMediaPlayer, QVideoSurfaceFormat
from qtpy.QtMultimediaWidgets import QGraphicsVideoItem
from timecode import Timecode
import os
from typing import List

class VideoSceneAbstractBase(QGraphicsScene):
    """
    An abstract scene that knows how to draw annotations text and pose data
    into its foreground
    """

    @staticmethod
    def supportedFormats() -> List:
        raise NotImplementedError("Derived class needs to override this method")

    def __init__(self, bento: QObject, start_time: Timecode, parent: QObject=None):
        super().__init__(parent)
        self.bento = bento
        self.annots = None
        self.pose_class = None
        self.showPoseData = False
        self.frame_ix = 0
        self.start_time = start_time
        self._frameWidth = 0.
        self._frameHeight = 0.
        self._aspectRatio = 0.

    def setAnnots(self, annots: list):
        self.annots = annots

    def setPoseClass(self, pose_class: PoseBase):
        self.pose_class = pose_class

    def setShowPoseData(self, showPoseData: bool):
        self.showPoseData = showPoseData

    def drawPoses(self, painter: QPainter, frame_ix: int):
        if self.showPoseData and self.pose_class:
            self.pose_class.drawPoses(painter, frame_ix)

    def drawForeground(self, painter: QPainter, rect: QRectF):
        # add poses
        self.drawPoses(painter, self.frame_ix)
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

    def frameWidth(self) -> float:
        return self._frameWidth

    def frameHeight(self) -> float:
        return self._frameHeight

    def aspectRatio(self) -> float:
        return self._aspectRatio

    def videoItem(self) -> QGraphicsItem:
        raise NotImplementedError("Derived class needs to override this method")

    def running_time(self) -> float:
        raise NotImplementedError("Derived class needs to override this method")

    def sample_rate(self) -> float:
        raise NotImplementedError("Derived class needs to override this method")

    @Slot(Timecode)
    def updateFrame(self, t: Timecode):
        raise NotImplementedError("Derived class needs to override this method")

    def getPlayer(self) -> QMediaPlayer:
        return None

    def reset(self):
        pass

class VideoSceneNative(VideoSceneAbstractBase):
    """
    A scene that knows how to play video in various standard formats
    Avoiding endless update loops is tricky.  The player's position is only set
    explicitly when the player is *not* playing.
    """

    @staticmethod
    def supportedFormats() -> List:
        return ['mp4', 'avi']

    # update current time every 1/10 second
    time_update_msec: int = round(1000 / 10)

    def __init__(self, bento: QObject, start_time: Timecode, parent: QObject=None):
        super().__init__(bento, start_time, parent)
        self.player = QMediaPlayer()
        self.playerItem = QGraphicsVideoItem()
        self.player.setVideoOutput(self.playerItem)
        self.addItem(self.playerItem)
        self.player.durationChanged.connect(bento.noteVideoDurationChanged)
        self.player.setNotifyInterval(self.time_update_msec)
        self.frameRate = 30.0
        self.duration = 0.0
        self._isTimeSource = False
        self._running = False

    def drawPoses(self, painter: QPainter, frame_ix: int):
        super().drawPoses(painter, frame_ix)

    def drawForeground(self, painter: QPainter, rect: QRectF):
        self.frame_ix = round(self.player.position() * self.frameRate / 1000.)   # position() is in msec
        if self.playerItem:
            videoBounds = self.playerItem.boundingRect()
            videoNativeSize = self.playerItem.nativeSize()
            if not videoNativeSize.isEmpty() and not videoBounds.isEmpty():
                # prevent divide by zero or pointless work
                painter.save()
                sx = videoBounds.width() / videoNativeSize.width()
                sy = videoBounds.height() / videoNativeSize.height()
                painter.scale(sx, sy)
                super().drawForeground(painter, rect)
                painter.restore()

    @Slot(QVideoSurfaceFormat)
    def noteSurfaceFormatChanged(self, surfaceFormat: QVideoSurfaceFormat):
        frameRate = surfaceFormat.frameRate()
        self._frameWidth = surfaceFormat.frameWidth()
        self._frameHeight = surfaceFormat.frameHeight()
        self._aspectRatio = surfaceFormat.pixelAspectRatio()
        if frameRate > 0.:
            print(f"Setting frameRate to {frameRate}")
            self.frameRate = frameRate

    def setVideoPath(self, videoPath: str):
        _, ext = os.path.splitext(videoPath)
        ext = ext.lower()
        if self.duration == 0.0 and ext in ['.avi', '.mp4']:
            self.reader = mp4Io.mp4Io_reader(videoPath)
            self.duration = float(self.reader.header['numFrames']) / float(self.reader.header['fps'])
        self.player.setMedia(QUrl.fromLocalFile(videoPath))
        self.playerItem.videoSurface().surfaceFormatChanged.connect(self.noteSurfaceFormatChanged)
        # force the player to load the media
        self.player.play()
        self.player.pause()
        # reset to beginning
        self.player.setPosition(0)
        # do some other setup
        frameRate = self.playerItem.videoSurface().surfaceFormat().frameRate()
        if frameRate > 0:
            self.frameRate = frameRate
        self.bento.timeChanged.connect(self.updateFrame)

    @Slot(Timecode)
    def updateFrame(self, t: Timecode):
        """
        Only act on external time updates if we're not currently playing.
        This is to avoid an endless time update loop when this player is
        acting as the timeSource for bento.
        Note that the check for self._running is needed to avoid a problem when
        playing has just stopped and we set bento's current time (below).
        """
        if self.player.state() != QMediaPlayer.PlayingState and not self._running:
            self.player.setPosition(round(t.float * 1000.))

    @Slot()
    def play(self):
        self._running = True
        self.player.play()

    @Slot()
    def stop(self):
        self.player.pause()
        if self._isTimeSource:
            self.bento.set_time(Timecode(30.0, start_seconds=self.player.position()/1000.))
        self._running = False

    @Slot(float)
    def setPlaybackRate(self, rate: float):
        self.player.setPlaybackRate(rate)

    def videoItem(self) -> QGraphicsItem:
        return self.playerItem

    def running_time(self) -> float:
        return float(self.duration)

    def sample_rate(self) -> float:
        if self.frameRate == 0.:
            return 30.0
        else:
            return self.frameRate

    def setIsTimeSource(self, isTimeSource: bool):
        self._isTimeSource = isTimeSource

    def getPlayer(self) -> QMediaPlayer:
        return self.player

    def reset(self):
        if self.player:
            self.player.setMedia(QMediaContent(None))

class VideoScenePixmap(VideoSceneAbstractBase):
    """
    A scene that knows how to play videos in Caltech Anderson Lab .seq format
    """

    @staticmethod
    def supportedFormats() -> List:
        return ['seq', 'mp4', 'avi']

    def __init__(self, bento: QObject, start_time: Timecode, parent: QObject=None):
        super().__init__(bento, start_time, parent)
        self.reader = None
        self.frame_ix: int = 0
        self.pixmap = QPixmap()
        self.pixmapItem = self.addPixmap(self.pixmap)
        # self.region = None

    def setVideoPath(self, videoPath: str):
        _, ext = os.path.splitext(videoPath)
        ext = ext.lower()
        if ext == '.seq':
            self.reader = seqIo.seqIo_reader(videoPath)
        elif ext in ['.avi', '.mp4']:
            self.reader = mp4Io.mp4Io_reader(videoPath)
        else:
            raise ValueError("Expected .seq file")
        self._frameWidth = self.reader.header['width']
        self._frameHeight = self.reader.header['height']
        self._aspectRatio = self._frameHeight / self._frameWidth
        self.bento.timeChanged.connect(self.updateFrame)

    @Slot(Timecode)
    def updateFrame(self, t: Timecode):
        if not self.reader or t < self.start_time:
            return
        myTc = Timecode(self.reader.header['fps'], start_seconds = t.float)
        self.frame_ix = min(myTc.frames, self.reader.header['numFrames']-1)
        self.pixmap = self.reader.getFrameAsQPixmap(self.frame_ix, decode=False)
        self.pixmapItem.setPixmap(self.pixmap)

    def videoItem(self) -> QGraphicsItem:
        return self.pixmapItem

    def running_time(self) -> float:
        if not self.reader:
            return 0.
        return float(self.reader.header['numFrames']) / float(self.reader.header['fps'])

    def sample_rate(self) -> float:
        if not self.reader:
            return 30.0
        else:
            return self.reader.header['fps']
