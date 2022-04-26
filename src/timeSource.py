# timeSource.py

from qtpy.QtCore import QObject, QSignalBlocker, QTimer, Signal, Slot
from qtpy.QtMultimedia import QMediaPlayer
from timecode import Timecode

class TimeSourceAbstractBase(QObject):
    """
    Abstract base class for sources of timing ticks,
    whether internal or external
    """

    timeChanged: Signal = Signal(Timecode)
    tickRateChanged: Signal = Signal(float)

    def __init__(self, notifyTimeChanged: Slot):
        super().__init__()
        self._currentTime = Timecode(30., "00:00:00:01")
        self._maxFrameRate: float = 1.
        self._minFrameRate: float = 1.
        self._frameRate: float = 1.
        self.timeChanged.connect(notifyTimeChanged)

    def start(self):
        raise NotImplementedError("The derived class needs to implement this method")

    def stop(self):
        raise NotImplementedError("The derived class needs to implement this method")

    @Slot()
    def doubleFrameRate(self):
        raise NotImplementedError("The derived class needs to implement this method")

    @Slot()
    def halveFrameRate(self):
        raise NotImplementedError("The derived class needs to implement this method")

    @Slot()
    def resetFrameRate(self):
        raise NotImplementedError("The derived class needs to implement this method")

    def setMaxFrameRate(self, maxRate: float):
        self._maxFrameRate = maxRate

    def setMinFrameRate(self, minRate: float):
        self._minFrameRate = minRate

    def setCurrentTime(self, currentTime: Timecode):
        if self._currentTime != currentTime:
            self._currentTime = currentTime
            self.timeChanged.emit(self._currentTime)

    def currentTime(self) -> Timecode:
        return self._currentTime

    @Slot()
    def quit(self):
        raise NotImplementedError("The derived class needs to implement this method")


class TimeSourceQTimer(TimeSourceAbstractBase):
    """
    Tick source coming from a QTimer
    """

    def __init__(self, notifyTimeChanged: Slot):
        super().__init__(notifyTimeChanged)
        self.default_frame_interval: float = 1000./30.
        self.timer: QTimer = QTimer()
        self.timer.setInterval(round(self.default_frame_interval))
        self.timer.timeout.connect(self.doTick)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    Slot()
    def doubleFrameRate(self):
        if self._frameRate * 2. <= self._maxFrameRate:
            self._frameRate *= 2.
            self.timer.setInterval(round(self.default_frame_interval / self._frameRate))
            self.tickRateChanged.emit(self._frameRate)

    @Slot()
    def halveFrameRate(self):
        if self._frameRate / 2. >= self._minFrameRate:
            self._frameRate /= 2.
            self.timer.setInterval(round(self.default_frame_interval / self._frameRate))
            self.tickRateChanged.emit(self._frameRate)

    @Slot()
    def resetFrameRate(self):
        if self._frameRate != 1.:
            self._frameRate = 1.
            self.timer.setInterval(round(self.default_frame_interval / self._frameRate))
            self.tickRateChanged.emit(self._frameRate)

    @Slot()
    def doTick(self):
        currentTime = self._currentTime + 1
        self._currentTime = currentTime
        self.timeChanged.emit(self._currentTime)

    @Slot()
    def quit(self):
        if self.timer.isActive():
            self.timer.stop()

class TimeSourceQMediaPlayer(TimeSourceAbstractBase):
    """
    Tick source coming from a video player
    """

    #Signals
    startCalled = Signal()
    stopCalled = Signal()
    quitCalled = Signal()

    def __init__(self, notifyTimeChanged: Slot, player: QMediaPlayer):
        super().__init__(notifyTimeChanged)
        self.player = player
        self.player.positionChanged.connect(self.doTick)
        self.startCalled.connect(player.play)
        self.stopCalled.connect(player.pause)
        self.tickRateChanged.connect(player.setPlaybackRate)
        self.quitCalled.connect(player.stop)
        self.playing = False

    @Slot(int)
    def doTick(self, msec: int):
        # We need to avoid a recursive "set time" loop with the media player,
        # so temporarily disconnect the signal from the slot to break the loop
        blocker = QSignalBlocker(self.player)
        self._currentTime = Timecode(self._currentTime.framerate, start_seconds=msec / 1000.)
        self.timeChanged.emit(self._currentTime)

    def start(self):
        self.playing = True
        self.startCalled.emit()

    def stop(self):
        self.playing = False
        self.stopCalled.emit()

    @Slot()
    def doubleFrameRate(self):
        if self._frameRate * 2. <= self._maxFrameRate:
            self._frameRate *= 2.
            self.tickRateChanged.emit(self._frameRate)

    @Slot()
    def halveFrameRate(self):
        if self._frameRate / 2. >= self._minFrameRate:
            self._frameRate /= 2.
            self.tickRateChanged.emit(self._frameRate)

    @Slot()
    def resetFrameRate(self):
        if self._frameRate != 1.:
            self._frameRate = 1.
            self.tickRateChanged.emit(self._frameRate)

    def quit(self):
        self.quitCalled.emit()

    def setCurrentTime(self, currentTime: Timecode):
        # We need to avoid a recursive "set time" loop with the media player,
        # so disconnect the signal from the slot to break the loop
        blocker = QSignalBlocker(self.player)
        super().setCurrentTime(currentTime)
