# bento.py

from timecode import Timecode
from PySide2.QtCore import Signal, Slot, QObject, QPoint, QThread
from PySide2.QtWidgets import QApplication
from annot.annot import Annotations, Bout
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
        self.active_annotations = [] # tuples ('ch_key', bout)
        self.behaviors = Behaviors()
        self.pending_bout = None
        f = open('../color_profiles.txt','r')
        self.behaviors.load(f)
        f.close()
        self.annotations = Annotations(self.behaviors)
        self.scene = AnnotationsScene()
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
        self.active_channels = self.annotations.channel_names()
        self.scene.loadBouts(self.annotations.channel(self.active_channels[0]))
        rect = self.scene.sceneRect()
        self.scene.setSceneRect(rect.x() - 30., rect.y(), rect.width() + 2. * 30., rect.height())
        self.time_start = self.annotations.time_start()
        self.time_end = self.annotations.time_end()
        self.set_time(self.time_start)

    def update_active_annotations(self):
        self.active_annotations.clear()
        for ch in self.active_channels:
            bouts = self.annotations.channel(ch).get_at(self.current_time)
            for bout in bouts:
                self.active_annotations.append((ch, bout))
        self.annotChanged.emit([(
            c, 
            bout.name(),
            bout.color())
            for (c, bout) in self.active_annotations])

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
        print(f"toNextEvent: current_time is {self.current_time.frames}, next_event is {next_event.frames}")
        for (ch, bout) in self.active_annotations:
            next_event = min(next_event, bout.end() + 1)
            print(f"  in loop 1: value is {next_event.frames}")
            print(f"  after active bout {bout.name()}: {bout.start().frames} - {bout.end().frames}")
        for ch in self.active_channels:
            print(f"Channel {ch}")
            next_bout = self.annotations.channel(ch).get_next_start(self.current_time)
            next_event = min(next_event, next_bout.start())
            print(f"  in loop 2: next_event is {next_event.frames}")
            print(f"  next bout {next_bout.name()}: {next_bout.start().frames} - {next_bout.end().frames}")
        print(f"  finally, value is {next_event.frames}")
        self.set_time(next_event)
    
    @Slot()
    def toPrevEvent(self):
        prev_event = self.time_start
        print(f"toPrevEvent: current_time is {self.current_time.frames}, prev_event is {prev_event.frames}")
        for (ch, bout) in self.active_annotations:
            prev_event = max(prev_event, bout.start() - 1)
            print(f"  in loop 1: prev_event is {prev_event.frames}")
            print(f"  before active bout {bout.name()}: {bout.start().frames} - {bout.end().frames}")
        for ch in self.active_channels:
            print(f"Channel {ch}")
            prev_bout = self.annotations.channel(ch).get_prev_end(self.current_time - 1)
            prev_event = max(prev_event, prev_bout.end())
            print(f"  in loop 2: prev_event is {prev_event.frames}")
            print(f"  prev_bout is {prev_bout.name()}: {prev_bout.start().frames} - {prev_bout.end().frames}")
        print(f"  finally, prev_event is {prev_event.frames}")
        self.set_time(prev_event)

    @Slot(int)
    def processHotKey(self, key: int):
        """
        processHotKey - start or finish a bout referenced by a hot key
        """
        # Which behavior does the key correspond to?
        print(f"processHotKey: key = {chr(key).lower()}")
        beh = self.behaviors.from_hot_key(chr(key).lower())
        if not beh:
            # that hot key is not defined; do nothing
            print(f"processHotKey: didn't match a behavior, so doing nothing")
            return
        # Is there a pending bout?
        if self.pending_bout:
            # if it's the same as the current hot key, end it here
            if self.pending_bout.name() == beh.get_name():
                if self.pending_bout.start() > self.current_time:
                    # swap start and end before completing
                    self.pending_bout.set_end(self.pending_bout.start())
                    self.pending_bout.set_start(self.current_time)
                    print("processHotKey: swapping start and end")
                else:
                    # typical case
                    self.pending_bout.set_end(self.current_time)
                # insert the pending bout in the active channel
                #TODO: need a way to specify the active channel, as distinct from visible channels
                for chan in self.active_channels:
                    print(f"processHotKey: adding new bout to chan {chan}")
                    self.annotations.add_bout(self.pending_bout, chan)
                self.scene.addBout(self.pending_bout)
                self.pending_bout = None
                return
            else:
                self.pending_bout = None
        # Is that annotation active here?
        for (c, bout) in self.active_annotations:
            if bout.name() == beh.get_name():
                # what to do to "toggle" it?
                print(f"processHotKey: behavior {beh.get_name()} is already active")
                pass
        self.pending_bout = Bout(self.current_time, self.current_time, beh)
        print(f"processHotKey: pending_bout is now {self.pending_bout}")            

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
