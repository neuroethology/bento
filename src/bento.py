# bento.py

from timecode import Timecode
from PySide2.QtCore import Signal, Slot, QObject, QThread
from PySide2.QtWidgets import QApplication, QFileDialog, QMenuBar, QMessageBox
from annot.annot import Annotations, Bout
from annot.behavior import Behaviors
from mainWindow import MainWindow
from video.videoWindow import VideoFrame
from widgets.annotationsWidget import AnnotationsScene
from widgets.neuralWidget import NeuralScene, NeuralView
from db.sessionWindow import SessionDockWidget
from db.trialWindow import TrialDockWidget
from db.schema_sqlalchemy import Animal, Camera, Investigator, Session, Trial, new_session, create_tables
from db.investigatorDialog import InvestigatorDialog
from db.animalDialog import AnimalDialog
from db.cameraDialog import CameraDialog
from db.configDialog import ConfigDialog
from db.editSessionDialog import EditSessionDialog
from db.setInvestigatorDialog import SetInvestigatorDialog
from db.bentoConfig import BentoConfig
from db.animal_surgery_xls import import_xls_file
# from neural.neuralWindow import NeuralDockWidget
from neural.neuralFrame import NeuralFrame
from channelDialog import ChannelDialog
from os.path import expanduser, sep
from utils import fix_path, padded_rectf
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
        self.config = BentoConfig()
        goodConfig = self.config.read()
        self.time_start = Timecode('30.0', '0:0:0:1')
        self.time_end = Timecode('30.0', '23:59:59:29')
        self.current_time = self.time_start
        self.investigator_id = None
        self.active_annotations = [] # tuples ('ch_key', bout)
        self.behaviors = Behaviors()
        self.pending_bout = None
        with open('../color_profiles.txt','r') as f:
            self.behaviors.load(f)
        self.session_id = None
        self.trial_id = None
        self.player = PlayerWorker(self)
        self.annotationsScene = AnnotationsScene()
        self.video_widgets = []
        self.neural_widgets = []
        self.annotations = Annotations(self.behaviors)
        self.mainWindow = MainWindow(self)
        self.current_time.set_fractional(False)
        self.active_channels = []
        self.quitting.connect(self.player.quit)
        self.player.incrementTime.connect(self.incrementTime)
        self.player.finished.connect(self.player.deleteLater)
        self.player.finished.connect(self.player.quit)
        self.annotationsSceneUpdated.connect(self.mainWindow.ui.annotationsView.updateScene)
        self.timeChanged.connect(self.mainWindow.updateTime)
        self.annotChanged.connect(self.mainWindow.updateAnnotLabel)
        self.set_time('0:0:0:0')
        if not goodConfig:
            self.edit_config()
        try:
            self.db_sessionMaker = new_session(
                self.config.username(),
                self.config.password(),
                self.config.host(),
                self.config.port())
        except Exception as e:
            print(f"Caught Exception {e}.  Probably config data invalid")
            QMessageBox.about(self.mainWindow, "Error", f"Config data invalid.  {e}")
            exit(-1)
        if not self.config.investigator_id():
            self.set_investigator()
        self.investigator_id = self.config.investigator_id()
        self.player.start()

    def setInvestigatorId(self, investigator_id):
        self.investigator_id = investigator_id
        self.config.set_investigator_id(investigator_id)
        self.config.write()

    def load_annotations(self, fn, sample_rate = 30.):
        print(f"Loading annotations from {fn}")
        self.annotations.read(fn)
        self.active_channels = self.annotations.channel_names()
        self.annotationsScene.setSampleRate(sample_rate)
        self.annotationsScene.loadAnnotations(self.annotations, self.active_channels, sample_rate)
        self.annotationsScene.setSceneRect(padded_rectf(self.annotationsScene.sceneRect()))
        self.time_start = self.annotations.time_start()
        self.time_end = self.annotations.time_end()
        self.set_time(self.time_start)

    @Slot()
    def newChannel(self):
        dialog = ChannelDialog(self)
        dialog.exec_()

    @Slot()
    def addChannel(self, chanName):
        if chanName not in self.annotations.channel_names():
            self.annotations.addEmptyChannel(chanName)
            self.mainWindow.addChannelToCombo(chanName)

    @Slot()
    def setActiveChannel(self, chanName):
        self.active_channels = [chanName]

    @Slot()
    def save_annotations(self):
        with self.db_sessionMaker() as db_sess:
            base_directory = db_sess.query(Session).filter(Session.id == self.session_id).one().base_directory
        fileName, filter = QFileDialog.getSaveFileName(
            self.mainWindow,
            caption="Annotation File Name",
            dir=base_directory)
        with open(fileName, 'w') as file:
            with self.db_sessionMaker() as db_sess:
                trial = db_sess.query(Trial).filter(Trial.id == self.trial_id).one()
                self.annotations.write_caltech(
                    file,
                    [video_data.file_path for video_data in trial.video_data],
                    trial.stimulus
                    )
        print(f"Filter returned from file dialog was {filter}")

    # File menu actions

    @Slot()
    def set_investigator(self):
        dialog = SetInvestigatorDialog(self)
        dialog.exec_()

    @Slot()
    def import_trials(self):
        pass

    @Slot()
    def import_animals_tomomi(self):
        with self.db_sessionMaker() as db_sess:
            investigator = db_sess.query(Investigator).where(Investigator.id == self.investigator_id).scalar()
            if not investigator:
                raise RuntimeError(f"Investigator not found for id {self.investigator_id}")
            baseDir = expanduser("~")
            if not baseDir.endswith(sep):
                baseDir += sep
            file_paths, _ = QFileDialog.getOpenFileNames(
                self.mainWindow,
                "Select animal record files to import",
                baseDir,
                "Seq files (*.xls)",
                "Seq files (*.xls)")
            if len(file_paths) > 0:
                for file_path in file_paths:
                    import_xls_file(file_path, db_sess, investigator)

    # Database menu actions

    @Slot()
    def edit_config(self):
        dialog = ConfigDialog(self)
        dialog.exec_()

    @Slot()
    def edit_animal(self):
        """
        Edit or add a new animal to the database associated with the selected investigator
        """
        dialog = AnimalDialog(self)
        dialog.exec_()

    @Slot()
    def edit_camera(self):
        """
        Edit or add a new camera type to the database
        """
        dialog = CameraDialog(self)
        dialog.exec_()

    @Slot()
    def edit_investigator(self):
        """
        Edit or add a new investigator to the database
        """
        dialog = InvestigatorDialog(self)
        dialog.exec_()

    @Slot()
    def add_or_edit_session(self, session_id=None):
        """
        Add a new experiment session to the database
        associated with the selected investigator
        """
        dialog = EditSessionDialog(self, self.investigator_id, session_id)
        dialog.exec_()

    @Slot()
    def create_db(self):
        sess = self.db_sessionMaker()
        create_tables(sess)


    # State-related methods

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
        new_tc = max(self.time_start, min(self.time_end, new_tc))
        if self.current_time != new_tc:
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
        with self.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).one()
            base_directory = session.base_directory
            base_dir = base_directory + sep
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
                try:
                    self.load_annotations(annot_path, annotation.sample_rate)
                except Exception as e:
                    QMessageBox.about(self.selectTrialWindow, "Error", f"Attempt to load annotations from {annot_path} "
                        f"failed with error {str(e)}")
                    for widget in self.video_widgets:
                        widget.close()
                    self.video_widgets.clear()
                    return False
                self.annotationsSceneUpdated.emit()
            if loadPose:
                print("Load pose data if any")
                # if self.trial_id.pose_data:
                #     print(f"Load pose from {self.trial_id.pose_data[0].file_path}")
                # else:
                #     print("No pose data in trial.")
            if loadNeural:
                with self.db_sessionMaker() as db_sess:
                    trial = db_sess.query(Trial).filter(Trial.id == self.trial_id).one()
                    if trial.neural_data:
                        neuralWidget = self.newNeuralWidget(trial.neural_data[0], base_dir)
                        self.neural_widgets.append(neuralWidget)
                        if self.annotationsScene:
                            neuralWidget.overlayAnnotations(self.annotationsScene)
                        neuralWidget.show()
                    else:
                        print("No neural data in trial.")
            if loadAudio:
                print("Load audio data if any")
                # if self.trial_id.audio_data:
                #     print(f"Load audio from {self.trial_id.audio_data[0].file_path}")
                # else:
                #     print("No audio data in trial.")
        # set the time to get all the new widgets in sync
        self.set_time(self.time_start)
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

    app.aboutToQuit.connect(bento.player.quit)
    bento.screen_center = app.screens()[len(app.screens())-1].availableGeometry().center()
    # spacing = QPoint((window.width() + video.width()) / 4 + 5, 0)
    qr = bento.mainWindow.frameGeometry()
    # qr.moveCenter(bento.screen_center - spacing)
    qr.moveCenter(bento.screen_center)
    bento.mainWindow.move(qr.topLeft())
    bento.mainWindow.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
