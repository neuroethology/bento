# bento.py

from timecode import Timecode
from PySide2.QtCore import Signal, Slot, QObject, QPoint, QThread
from PySide2.QtWidgets import QApplication
from annot.annot import Annotations
from annot.behavior import Behavior, Behaviors
from mainWindow import MainWindow
from video.videoWindow import VideoDockWidget
from widgets.annotationsWidget import AnnotationsScene
import sys
import time

class PlayerWorker(QThread):
    incrementTime = Signal()
    finished = Signal()

    def __init__(self, bento):
        super(PlayerWorker, self).__init__()
        self.bento = bento
        self.playing = False
        self.running = False
        self.frame_sleep_time = 1./30.

    def run(self):
        print("Starting player worker")
        self.running = True
        while self.running:
            if self.playing:
                self.incrementTime.emit()
            QApplication.instance().processEvents()
            time.sleep(self.frame_sleep_time)
        print("Player worker exiting")
        self.finished.emit()

    @Slot()
    def togglePlayer(self):
        print(f"Setting playing to {not self.playing}")
        self.playing = not self.playing

    @Slot()
    def doubleFrameRate(self):
        self.frame_sleep_time /= 2.

    @Slot()
    def halveFrameRate(self):
        self.frame_sleep_time *= 2.

    @Slot()
    def quit(self):
        self.running = False

class Bento(QObject):
    """
    Bento - class representing core machinery (no UI)
    """

    quitting = Signal()

    def __init__(self):
        super(Bento, self).__init__()
        self.time_start = Timecode('30.0', '0:0:0:1')
        self.time_end = Timecode('30.0', '23:59:59:29')
        self.current_time = self.time_start
        self.active_annotations = [] # tuples ('ch_key', idx)
        self.behaviors = Behaviors()
        f = open('../color_profiles.txt','r')
        self.behaviors.load(f)
        f.close()
        self.annotations = Annotations(self.behaviors)
        self.scene = AnnotationsScene()
        self.bouts_by_end = {}
        self.current_time.set_fractional(False)
        self.active_channels = []
        self.player = PlayerWorker(self)
        self.quitting.connect(self.player.quit)
        self.player.incrementTime.connect(self.incrementTime)
        self.player.finished.connect(self.player.deleteLater)
        self.player.finished.connect(self.player.quit)
        self.player.start()

    def load_annotations(self, fn):
        self.annotations.read(fn)
        self.annotations.sort_channels()
        self.build_and_sort_end_bouts()
        self.active_channels = self.annotations.channel_names()
        self.scene.load(self.annotations.bouts(self.active_channels[0]))
        rect = self.scene.sceneRect()
        self.scene.setSceneRect(rect.x() - 30., rect.y(), rect.width() + 2. * 30., rect.height())
        self.time_start = self.annotations.time_start()
        self.time_end = self.annotations.time_end()
        self.set_time(self.time_start)

    def build_and_sort_end_bouts(self):
        for ch in self.annotations.channel_names():
            bouts = self.annotations.bouts(ch)
            self.bouts_by_end[ch] = list(range(len(bouts)))
            self.bouts_by_end[ch] = sorted(
                self.bouts_by_end[ch],
                key=lambda i : bouts[self.bouts_by_end[ch][i]].end())
    
    def update_active_annotations(self):
        self.active_annotations.clear()
        for ch in self.active_channels:
            bouts = self.annotations.bouts(ch)
            for ix in range(len(bouts)):
                if bouts[ix]._end < self.current_time:
                    continue
                if bouts[ix]._start > self.current_time:
                    break
                self.active_annotations.append((ch, ix))
        self.annotChanged.emit([(
            c, 
            self.annotations.bouts(c)[i].name(),
            self.annotations.bouts(c)[i].color())
            for (c, i) in self.active_annotations])

    def set_time(self, new_tc: Timecode):
        if not isinstance(new_tc, Timecode):
            new_tc = Timecode('30.0', new_tc)
        self.current_time = new_tc
        self.update_active_annotations()
        self.timeChanged.emit(self.current_time)
    
    def change_time(self, increment: Timecode):
        self.set_time(self.current_time + increment)

    def get_time(self):
        return self.current_time

    @Slot()
    def incrementTime(self):
        self.change_time(1)
    
    @Slot()
    def decrementTime(self):
        self.change_time(-1)

    @Slot()
    def skipForward(self):
        self.change_time(30)

    @Slot()
    def skipBackward(self):
        self.change_time(-30)

    @Slot()
    def toStart(self):
        self.set_time(self.time_start)

    @Slot()
    def toEnd(self):
        self.set_time(self.time_end)
    
    @Slot()
    def toNextEvent(self):
        next_event = self.time_end
        for (ch, ix) in self.active_annotations:
            next_event = min(next_event, self.annotations.bouts(ch)[ix].end() + 1)
        for ch in self.active_channels:
            bouts = self.annotations.bouts(ch)
            for ix in range(len(bouts)):
                if bouts[ix].end() < self.current_time:
                    continue
                if bouts[ix].start() > self.current_time:
                    next_event = min(next_event, bouts[ix].start())
                    break   # can break here because annotations are sorted in start order
        self.set_time(next_event)
    
    @Slot()
    def toPrevEvent(self):
        prev_event = self.time_start
        for (ch, ix) in self.active_annotations:
            prev_event = max(prev_event, self.annotations.bouts(ch)[ix].start() - 1)
        for ch in self.active_channels:
            bouts = self.annotations.bouts(ch)
            bouts_by_end = self.bouts_by_end[ch]
            for ix in range(len(bouts))[::-1]:
                if bouts[bouts_by_end[ix]].start() > self.current_time:
                    continue
                if bouts[bouts_by_end[ix]].end() < self.current_time:
                    prev_event = max(prev_event, bouts[bouts_by_end[ix]].end())
                    break
        self.set_time(prev_event)

    @Slot(int)
    def toggleAnnotation(self, key: int):
        # map key to annotation name
        """
        name = self.annot_key_map[key]
        """
        # Is that annotation active here?
        for bout in self.active_annotations:
            if bout.name() == name:
                # what to do to "toggle" it?
                pass            

    @Slot()
    def quit(self):
        self.quitting.emit()
        QApplication.instance().processEvents()
        time.sleep(3./30.)  # wait for threads to shut down
        QApplication.instance().quit()
    
   # Signals
    timeChanged = Signal(Timecode)
    annotChanged = Signal(list)
    
if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    bento = Bento()

    window = MainWindow(bento)
    app.aboutToQuit.connect(bento.player.quit)
    bento.timeChanged.connect(window.updateTime)
    bento.annotChanged.connect(window.updateAnnotLabel)
    video = VideoDockWidget(bento)
    bento.timeChanged.connect(video.updateFrame)
    bento.annotChanged.connect(video.updateAnnots)
    video2 = VideoDockWidget(bento)
    bento.timeChanged.connect(video2.updateFrame)
    bento.annotChanged.connect(video2.updateAnnots)
    bento.set_time('0:0:0:0')
    center = app.screens()[1].availableGeometry().center()
    spacing = QPoint((window.width() + video.width()) / 4 + 5, 0)
    qr = window.frameGeometry()
    qr.moveCenter(center - spacing)
    window.move(qr.topLeft())
    qr = video.frameGeometry()
    qr.moveCenter(center + spacing)
    video.move(qr.topLeft())
    video.show()
    video2.show()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
