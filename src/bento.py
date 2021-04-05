# bento.py

from timecode import Timecode
from PySide2.QtCore import Signal, Slot, QObject, QPoint, QThread
from PySide2.QtWidgets import QApplication, QMessageBox
from annot.annot import Annotations, Bout
from annot.behavior import Behavior, Behaviors
from mainWindow import MainWindow
from video.videoWindow import VideoFrame
from widgets.annotationsWidget import AnnotationsScene
from widgets.neuralWidget import NeuralScene, NeuralView
from db.sessionWindow import SessionDockWidget
from db.trialWindow import TrialDockWidget
# from neural.neuralWindow import NeuralDockWidget
from neural.neuralFrame import NeuralFrame
from os.path import sep
from utils import fix_path
import sys
import time

class PlayerWorker(QThread):
    incrementTime = Signal()
    finished = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.playing = False
        self.running = False
        self.frame_sleep_time = self.default_sleep_time = 1./30.

    def run(self):
        # print("Starting player worker")
        self.running = True
        while self.running:
            if self.playing:
                self.incrementTime.emit()
            QApplication.instance().processEvents()
            time.sleep(self.frame_sleep_time)
        # print("Player worker exiting")
        self.finished.emit()

    @Slot()
    def togglePlayer(self):
        # print(f"Setting playing to {not self.playing}")
        self.playing = not self.playing

    @Slot()
    def doubleFrameRate(self):
        if self.frame_sleep_time > self.default_sleep_time / 8.:
            self.frame_sleep_time /= 2.

    @Slot()
    def halveFrameRate(self):
        if self.frame_sleep_time < self.default_sleep_time * 8.:
            self.frame_sleep_time *= 2.

    @Slot()
    def resetFrameRate(self):
        self.frame_sleep_time = self.default_sleep_time

    @Slot()
    def quit(self):
        self.running = False

class Bento(QObject):
    """
    Bento - class representing core machinery (no UI)
    """

    def __init__(self):
        super().__init__()
        self.time_start = Timecode('30.0', '0:0:0:1')
        self.time_end = Timecode('30.0', '23:59:59:29')
        self.current_time = self.time_start
        self.active_annotations = [] # tuples ('ch_key', bout)
        self.behaviors = Behaviors()
        self.pending_bout = None
        f = open('../color_profiles.txt','r')
        self.behaviors.load(f)
        f.close()
        self.session = None
        self.mainWindow = None
        self.video_widgets = []
        self.neural_widgets = []
        self.annotations = Annotations(self.behaviors)
        self.annotationsScene = AnnotationsScene()
        self.current_time.set_fractional(False)
        self.active_channels = []
        self.player = PlayerWorker(self)
        self.quitting.connect(self.player.quit)
        self.player.incrementTime.connect(self.incrementTime)
        self.player.finished.connect(self.player.deleteLater)
        self.player.finished.connect(self.player.quit)
        self.player.start()

    def load_annotations(self, fn, sample_rate = 30.):
        print(f"Loading annotations from {fn}")
        self.annotations.read(fn)
        self.active_channels = self.annotations.channel_names()
        self.annotationsScene.setSampleRate(sample_rate)
        self.annotationsScene.loadAnnotations(self.annotations, self.active_channels, sample_rate)
        rect = self.annotationsScene.sceneRect()
        self.annotationsScene.setSceneRect(rect.x() - 30., rect.y(), rect.width() + 2. * 30., rect.height())
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
        for (ch, bout) in self.active_annotations:
            next_event = min(next_event, bout.end() + 1)
        for ch in self.active_channels:
            next_bout = self.annotations.channel(ch).get_next_start(self.current_time)
            next_event = min(next_event, next_bout.start())
        self.set_time(next_event)
    
    @Slot()
    def toPrevEvent(self):
        prev_event = self.time_start
        for (ch, bout) in self.active_annotations:
            prev_event = max(prev_event, bout.start() - 1)
        for ch in self.active_channels:
            prev_bout = self.annotations.channel(ch).get_prev_end(self.current_time - 1)
            prev_event = max(prev_event, prev_bout.end())
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
                # for chan in self.active_channels:
                chan = self.active_channels[0]
                print(f"processHotKey: adding new bout to chan {chan}")
                self.annotations.add_bout(self.pending_bout, chan)
                self.annotationsScene.addBout(self.pending_bout, chan)
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

    def newVideoWidget(self, video_path):
        video = VideoFrame(self)
        video.load_video(video_path)
        self.timeChanged.connect(video.updateFrame)
        self.annotChanged.connect(video.updateAnnots)
        return video

    def newNeuralWidget(self, neuralData, base_dir):
        # neuralWidget = NeuralDockWidget(self)
        neuralWidget = NeuralFrame(self)
        neuralWidget.load(neuralData, base_dir)
        self.timeChanged.connect(neuralWidget.updateTime)
        return neuralWidget

    @Slot()
    def selectTrial(self):
        self.selectTrialWindow = TrialDockWidget(self)
        self.selectTrialWindow.show()

    @Slot()
    def loadTrial(self, videos, annotation, loadPose, loadNeural, loadAudio):
        self.video_widgets.clear()
        base_dir = self.session.base_directory + sep
        for video_data in videos:
            widget = self.newVideoWidget(fix_path(base_dir + video_data.file_path))
            self.video_widgets.append(widget)
            qr = widget.frameGeometry()
            # qr.moveCenter(self.screen_center + spacing)
            qr.moveCenter(self.screen_center)
            widget.move(qr.topLeft())    #TODO: need to space multiple videos out
            widget.show()
        if annotation:
            annot_path = fix_path(base_dir + annotation.file_path)
            # try:
            self.load_annotations(annot_path, annotation.sample_rate)
            # except Exception as e:
            #     QMessageBox.about(self.selectTrialWindow, "Error", f"Problem loading annotations from {annot_path}\n"
            #         f"Error reported was {str(e)}")
            #     for widget in self.video_widgets:
            #         widget.close() 
            #     self.video_widgets.clear()
            #     return False
            self.annotationsSceneUpdated.emit()
        if loadPose:
            if self.trial.pose_data:
                print(f"Load pose from {self.trial.pose_data[0].file_path}")
            else:
                print("No pose data in trial.")
        if loadNeural:
            if self.trial.neural_data:
                neuralWidget = self.newNeuralWidget(self.trial.neural_data[0], base_dir)
                self.neural_widgets.append(neuralWidget)
                if self.annotationsScene:
                    neuralWidget.overlayAnnotations(self.annotationsScene)
                neuralWidget.show()
            else:
                print("No neural data in trial.")
        if loadAudio:
            if self.trial.audio_data:
                print(f"Load audio from {self.trial.audio_data[0].file_path}")
            else:
                print("No audio data in trial.")
        return True

   # Signals
    quitting = Signal()
    timeChanged = Signal(Timecode)
    annotChanged = Signal(list)
    annotationsSceneUpdated = Signal()
    
if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    bento = Bento()

    bento.mainWindow = MainWindow(bento)
    app.aboutToQuit.connect(bento.player.quit)
    bento.annotationsSceneUpdated.connect(bento.mainWindow.ui.annotationsView.updateScene)
    bento.timeChanged.connect(bento.mainWindow.updateTime)
    bento.annotChanged.connect(bento.mainWindow.updateAnnotLabel)
    bento.set_time('0:0:0:0')
    bento.mainWindow.selectSession()
    bento.screen_center = app.screens()[1].availableGeometry().center()
    # spacing = QPoint((window.width() + video.width()) / 4 + 5, 0)
    qr = bento.mainWindow.frameGeometry()
    # qr.moveCenter(bento.screen_center - spacing)
    qr.moveCenter(bento.screen_center)
    bento.mainWindow.move(qr.topLeft())
    bento.mainWindow.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
