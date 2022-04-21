# videoScene.py
"""
Implement base class and derived classes for showing videos with pose and annotation overlays
"""
from pose.pose import PoseBase
import video.seqIo as seqIo
from qtpy.QtCore import QEvent, QMargins, QObject, QPointF, QRectF, Qt, QUrl, Signal, Slot
from qtpy.QtGui import QBrush, QColor, QFontMetrics, QPen, QPainter, QPixmap, QImage, QPolygonF
from qtpy.QtWidgets import QFrame, QGraphicsScene, QGraphicsItem
from qtpy.QtMultimedia import QMediaPlayer, QVideoSurfaceFormat
from qtpy.QtMultimediaWidgets import QGraphicsVideoItem
from timecode import Timecode
import numpy as np
import os
import time

class VideoSceneAbstractBase(QGraphicsScene):
    """
    An abstract scene that knows how to draw annotations text and pose data
    into its foreground
    """

    def __init__(self, bento: QObject, parent: QObject=None):
        super().__init__(parent)
        self.annots = None
        self.pose_class = None
        self.showPoseData = False

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
        frame_ix = round(self.player.position() * self.frameRate / 1000.)   # position() is in msec
        painter.save()
        videoBounds = self.playerItem.boundingRect()
        videoNativeSize = self.playerItem.nativeSize()
        sx = videoBounds.width() / videoNativeSize.width()
        sy = videoBounds.height() / videoNativeSize.height()
        painter.scale(sx, sy)
        self.drawPoses(painter, frame_ix)
        painter.restore()
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

class VideoSceneNative(VideoSceneAbstractBase):
    """
    A scene that knows how to play video in various standard formats
    """

    # update current time every 1/10 second
    time_update_msec: int = round(1000 / 10)

    def __init__(self, bento: QObject, parent: QObject=None):
        super().__init__(parent)
        self.player = QMediaPlayer()
        self.playerItem = QGraphicsVideoItem()
        self.player.setVideoOutput(self.playerItem)
        self.addItem(self.playerItem)
        self.player.durationChanged.connect(bento.noteVideoDurationChanged)
        self.player.positionChanged.connect(bento.set_time_msec)
        self.player.setNotifyInterval(self.time_update_msec)
        self.frameRate = 30.0

    @Slot(QVideoSurfaceFormat)
    def noteSurfaceFormatChanged(self, surfaceFormat: QVideoSurfaceFormat):
        frameRate = surfaceFormat.frameRate()
        if frameRate > 0.:
            print(f"Setting frameRate to {frameRate}")
            self.frameRate = frameRate

    def setVideoPath(self, videoPath: str):
        self.player.setMedia(QUrl.fromLocalFile(videoPath))
        # force the player to load the media
        self.player.play()
        self.player.pause()
        # reset to beginning
        self.player.setPosition(0)
        frameRate = self.playerItem.videoSurface().surfaceFormat().frameRate()
        if frameRate > 0:
            self.frameRate = frameRate
        self.playerItem.videoSurface().surfaceFormatChanged.connect(self.noteSurfaceFormatChanged)

class VideoSceneSeq(VideoSceneAbstractBase):
    """
    A scene that knows how to play videos in Caltech Anderson Lab .seq format
    """

    def __init__(self, bento: QObject, parent: QObject=None):
        super().__init__(parent)
