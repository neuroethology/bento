# bento.py
# import faulthandler
# faulthandler.enable()
from timecode import Timecode
from qtpy.QtCore import QMarginsF, QObject, QRectF, QTimer, Qt, Signal, Slot
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication, QFileDialog, QMessageBox, QProgressDialog
from annot.annot import Annotations, Bout
from annot.behavior import Behaviors
from pose.pose import load_poses
from mainWindow import MainWindow
from video.videoWindow import VideoFrame
from widgets.annotationsWidget import AnnotationsScene
from db.schema_sqlalchemy import (AnnotationsData, Investigator, Session, Trial,
    VideoData, new_session, create_tables)
from db.investigatorDialog import InvestigatorDialog
from db.animalDialog import AnimalDialog
from db.cameraDialog import CameraDialog
from db.configDialog import ConfigDialog
from db.setInvestigatorDialog import SetInvestigatorDialog
from db.bentoConfig import BentoConfig
from db.animal_surgery_xls import import_animal_xls_file
from db.behaviorsDialog import BehaviorsDialog
from db.bento_xls import import_bento_xls_file
from neural.neuralFrame import NeuralFrame
from channelDialog import ChannelDialog
from os.path import expanduser, isabs, sep, relpath, splitext
from utils import fix_path, padded_rectf
import sys, traceback, time

class Player(QObject):

    def __init__(self, bento):
        super().__init__()
        self.playing = False
        self.timer = QTimer()
        self.frame_interval = self.default_frame_interval = 1000./30.
        self.timer.setInterval(round(self.frame_interval))
        self.timer.timeout.connect(bento.incrementTime)

    @Slot()
    def togglePlayer(self):
        # print(f"Setting playing to {not self.playing}")
        self.playing = not self.playing
        if self.playing:
            self.timer.start()
        else:
            self.timer.stop()

    @Slot()
    def doubleFrameRate(self):
        if self.frame_interval > self.default_frame_interval / 8.:
            self.frame_interval /= 2.
            print(f"setting frame interval to {round(self.frame_interval)}")
            self.timer.setInterval(round(self.frame_interval))

    @Slot()
    def halveFrameRate(self):
        if self.frame_interval < self.default_frame_interval * 8.:
            self.frame_interval *= 2.
            print(f"setting frame interval to {round(self.frame_interval)}")
            self.timer.setInterval(round(self.frame_interval))

    @Slot()
    def resetFrameRate(self):
        self.frame_interval = self.default_frame_interval
        print(f"resetting frame interval to {round(self.frame_interval)}")
        self.timer.setInterval(round(self.frame_interval))

    @Slot()
    def quit(self):
        if self.timer.isActive():
            self.timer.stop()

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
        self.current_annotations = [] # tuples ('ch_key', bout)
        self.behaviors = Behaviors()
        self.pending_bout = None
        self.bento_dir = expanduser("~") + sep + ".bento" + sep
        self.loadBehaviors()
        self.behaviorsDialog = BehaviorsDialog(self)
        self.behaviorsDialog.show()

        self.session_id = None
        self.trial_id = None
        self.player = Player(self)
        self.annotationsScene = AnnotationsScene()
        self.newAnnotations = False
        self.video_widgets = []
        self.neural_widgets = []
        self.annotations = Annotations(self.behaviors)
        self.annotations.annotations_changed.connect(self.noteAnnotationsChanged)
        self.mainWindow = MainWindow(self)
        self.current_time.set_fractional(False)
        self.active_channels = []
        self.quitting.connect(self.player.quit)
        self.timeChanged.connect(self.mainWindow.updateTime)
        self.currentAnnotsChanged.connect(self.mainWindow.updateAnnotLabel)
        self.active_channel_changed.connect(self.mainWindow.selectChannelByName)
        self.set_time('0:0:0:0')
        if not goodConfig:
            self.edit_config()
        try:
            self.db_sessionMaker = new_session(
                self.config.username(),
                self.config.password(),
                self.config.host(),
                self.config.port(),
                self.config.usePrivateDB())
        except Exception as e:
            print(f"Caught Exception {e}.  Probably config data invalid")
            QMessageBox.about(self.mainWindow, "Error", f"Config data invalid.  {e}")
            exit(-1)
        if not self.config.investigator_id():
            self.set_investigator()
        self.investigator_id = self.config.investigator_id()
        self.mainWindow.show()

    def setInvestigatorId(self, investigator_id):
        self.investigator_id = investigator_id
        self.config.set_investigator_id(investigator_id)
        self.config.write()

    def load_or_init_annotations(self, fn, sample_rate = 30., running_time = None):
        self.annotationsScene.setSampleRate(sample_rate)
        self.annotations.clear_channels()
        self.active_channels.clear()
        self.mainWindow.clearChannelsCombo()
        loaded = False
        if isinstance(fn, str) and len(fn) > 0:
            print(f"Try loading annotations from {fn}")
            try:
                self.annotationsScene.clear()
                self.annotations.read(fn)
                if self.annotations.channel_names():
                    self.mainWindow.addChannelToCombo(self.annotations.channel_names())
                    print(f"channel_names: {self.annotations.channel_names()}")
                    self.setActiveChannel(self.annotations.channel_names()[0])
                self.annotationsScene.loadAnnotations(self.annotations, self.annotations.channel_names(), sample_rate)
                height = len(self.annotations.channel_names()) - self.annotationsScene.sceneRect().height()
                self.annotationsScene.setSceneRect(padded_rectf(self.annotationsScene.sceneRect()) + QMarginsF(0., 0., 0., float(height)))
                self.annotationsSceneHeightChanged.emit(float(self.annotationsScene.sceneRect().height()))
                self.time_start = self.annotations.start_time()
                self.time_end = self.annotations.end_time()
                loaded = True
            except Exception as e:
                pass
                print(f"Attempt to load annotations from file {fn} failed with exception {e}")
                traceback.print_exc()
        if not loaded:
            print("Initializing new annotations")
            self.active_channels.clear()
            self.annotationsScene.clear()
            self.annotationsScene.setSceneRect(padded_rectf(QRectF(0., 0., running_time, 1.)))
            self.time_end = Timecode(self.time_start.framerate, start_seconds=self.time_start.float + running_time)
            self.annotations.set_sample_rate(sample_rate)
            self.annotations.set_start_frame(self.time_start)
            self.annotations.set_end_frame(self.time_end)
            self.newAnnotations = True
            self.annotationsScene.loaded = True
        self.annotations.active_annotations_changed.connect(self.noteAnnotationsChanged)
        self.set_time(self.time_start)

    @Slot()
    def newChannel(self):
        dialog = ChannelDialog(self)
        dialog.exec()

    @Slot()
    def addChannel(self, chanName):
        if chanName not in self.annotations.channel_names():
            self.annotations.addEmptyChannel(chanName)
            self.mainWindow.addChannelToCombo(chanName)
            self.annotationsScene.addItem(self.annotations.channel(chanName))
            self.annotations.channel(chanName).set_top(float(len(self.annotations.channel_names())-1.))
            height = len(self.annotations.channel_names()) - self.annotationsScene.sceneRect().height()
            self.annotationsScene.setSceneRect(self.annotationsScene.sceneRect() + QMarginsF(0., 0., 0., float(height)))
            self.annotationsScene.height = self.annotationsScene.sceneRect().height()
            self.annotationsSceneHeightChanged.emit(float(self.annotationsScene.sceneRect().height()))
            self.setActiveChannel(chanName)

    @Slot()
    def setActiveChannel(self, chanName):
        self.active_channels = [chanName]
        self.active_channel_changed.emit(self.active_channels[0])

    def loadBehaviors(self):
        profile_paths = [self.bento_dir, ""]
        for path in profile_paths:
            try:
                fn = path + 'color_profiles.txt'
                print(f"Trying to load behavior definitions from {fn}...")
                with open(fn,'r') as f:
                    self.behaviors.load(f)
                print("  Success!")
                break   # no exception, so success
            except Exception as e:
                print(f"Exception caught: {e}")
                continue

    def saveBehaviors(self):
        fn = self.bento_dir + "color_profiles.txt"
        try:
            with open(fn, 'w') as f:
                self.behaviors.save(f)
        except Exception as e:
            print(f"Caught Exception {e}")
            QMessageBox.about(self.mainWindow, "Error", f"Saving behaviors to {fn} failed.  {e}")

    @Slot()
    def save_annotations(self):
        msgBox = QMessageBox(
            QMessageBox.Question,
            "Save Annotations",
            "This will delete inactive behaviors.  Okay?",
            buttons=QMessageBox.Save | QMessageBox.Cancel)
        result = msgBox.exec()
        if result == QMessageBox.Save:
            self.annotations.ensure_active_behaviors()
            self.annotations.delete_inactive_bouts()
            with self.db_sessionMaker() as db_sess:
                base_directory = db_sess.query(Session).filter(Session.id == self.session_id).one().base_directory
            fileName, _ = QFileDialog.getSaveFileName(
                self.mainWindow,
                caption="Annotation File Name",
                dir=base_directory)
            if fileName:
                # ensure a ".annot" extension
                _, ext = splitext(fileName)
                if ext != ".annot":
                    fileName += ".annot"
                with self.db_sessionMaker() as db_sess:
                    trial = db_sess.query(Trial).filter(Trial.id == self.trial_id).one()
                    self.annotations.set_sample_rate(
                        trial.video_data[0].sample_rate if len(trial.video_data) > 0 else 30.0)
                    # The following will need to change when video and annotation frame rates can be different
                    self.annotations.set_start_frame(self.time_start)
                    self.annotations.set_end_frame(self.time_end)
                    self.annotations.set_format("Caltech")
                    with open(fileName, 'w') as file:
                        self.annotations.write_caltech(
                            file,
                            [video_data.file_path for video_data in trial.video_data],
                            trial.stimulus
                            )
                    # Is the annotation filename a new one, or does it exist already?
                    existingAnnot = None
                    for annot in trial.annotations:
                        if annot.file_path == fileName:
                            existingAnnot = annot
                            break
                    if self.newAnnotations or not existingAnnot:
                        investigator = db_sess.query(Investigator).filter(Investigator.id == self.investigator_id).one()
                        # For unknown reasons, using self.annotations.time_start() behaves differently than self.time_start
                        newAnnot = AnnotationsData()
                        newAnnot.file_path = relpath(fileName, base_directory)
                        newAnnot.sample_rate = self.annotations.sample_rate()
                        newAnnot.format = self.annotations.format()
                        newAnnot.start_time = self.time_start.float
                        newAnnot.start_frame = self.time_start.frame_number
                        newAnnot.stop_frame = self.time_end.frame_number
                        newAnnot.annotator_name = investigator.user_name
                        newAnnot.method = "manual"
                        newAnnot.trial_id = self.trial_id
                        db_sess.add(newAnnot)
                        db_sess.commit()
                        trial.annotations.append(newAnnot)
                        db_sess.commit()
                        self.newAnnotations = False

    # File menu actions

    @Slot()
    def set_investigator(self):
        dialog = SetInvestigatorDialog(self)
        dialog.exec()

    @Slot()
    def import_trials(self):
        with self.db_sessionMaker() as db_sess:
            investigator = db_sess.query(Investigator).where(Investigator.id == self.investigator_id).scalar()
            if not investigator:
                raise RuntimeError(f"Investigator not found for id {self.investigator_id}")
            baseDir = expanduser("~")
            # Qt converts paths to platform-specific separators under the hood,
            # so it's correct to use forward-slash ("/") here across all platforms
            if not baseDir.endswith("/"):
                baseDir += "/"
            file_paths, _ = QFileDialog.getOpenFileNames(
                self.mainWindow,
                "Select MatLab bento session file(s) to import",
                baseDir,
                "Seq files (*.xls)",
                "Seq files (*.xls)")
            if len(file_paths) > 0:
                for file_path in file_paths:
                    import_bento_xls_file(file_path, db_sess, self.investigator_id)

    @Slot()
    def import_animals_tomomi(self):
        with self.db_sessionMaker() as db_sess:
            investigator = db_sess.query(Investigator).where(Investigator.id == self.investigator_id).scalar()
            if not investigator:
                raise RuntimeError(f"Investigator not found for id {self.investigator_id}")
            baseDir = expanduser("~")
            # Qt converts paths to platform-specific separators under the hood,
            # so it's correct to use forward-slash ("/") here across all platforms
            if not baseDir.endswith("/"):
                baseDir += "/"
            file_paths, _ = QFileDialog.getOpenFileNames(
                self.mainWindow,
                "Select animal record files to import",
                baseDir,
                "Seq files (*.xls)",
                "Seq files (*.xls)")
            if len(file_paths) > 0:
                for file_path in file_paths:
                    import_animal_xls_file(file_path, db_sess, investigator)

    # Database menu actions

    @Slot()
    def edit_config(self):
        dialog = ConfigDialog(self)
        dialog.exec()

    @Slot()
    def edit_animal(self):
        """
        Edit or add a new animal to the database associated with the selected investigator
        """
        dialog = AnimalDialog(self)
        dialog.exec()

    @Slot()
    def edit_camera(self):
        """
        Edit or add a new camera type to the database
        """
        dialog = CameraDialog(self)
        dialog.exec()

    @Slot()
    def edit_investigator(self):
        """
        Edit or add a new investigator to the database
        """
        dialog = InvestigatorDialog(self)
        dialog.exec()

    @Slot()
    def create_db(self):
        sess = self.db_sessionMaker()
        create_tables(sess)


    # State-related methods

    def update_current_annotations(self):
        self.current_annotations.clear()
        for ch in self.active_channels:
            bouts = self.annotations.channel(ch).get_at(self.current_time)
            for bout in bouts:
                if bout.is_visible():
                    self.current_annotations.append((ch, bout))
        self.currentAnnotsChanged.emit([(
            c,
            bout.name(),
            bout.color())
            for (c, bout) in self.current_annotations])

    def set_time(self, new_tc: Timecode):
        if not isinstance(new_tc, Timecode):
            new_tc = Timecode('30.0', new_tc)
        new_tc = max(self.time_start, min(self.time_end, new_tc))
        if self.current_time != new_tc:
            self.current_time = new_tc
            self.update_current_annotations()
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
        for (ch, bout) in self.current_annotations:
            next_event = min(next_event, bout.end() + 1)
        for ch in self.active_channels:
            next_bout = self.annotations.channel(ch).get_next_start(self.current_time)
            next_event = min(next_event, next_bout.start())
        self.set_time(next_event)

    @Slot()
    def toPrevEvent(self):
        prev_event = self.time_start
        for (ch, bout) in self.current_annotations:
            prev_event = max(prev_event, bout.start() - 1)
        for ch in self.active_channels:
            prev_bout = self.annotations.channel(ch).get_prev_end(self.current_time - 1)
            prev_event = max(prev_event, prev_bout.end())
        self.set_time(prev_event)

    # @Slot(QObject.event)
    def processHotKey(self, event: QObject.event):
        """
        processHotKey - start or finish a bout referenced by a hot key
        """
        if event.key() == Qt.Key_Escape:
            self.pending_bout = None
            return
        shift = bool(event.modifiers() & Qt.ShiftModifier)
        do_delete = (event.key() == Qt.Key_Backspace)

        # Which behavior does the key correspond to?
        if do_delete:
            beh = self.behaviors.getDeleteBehavior()
        else:
            key = chr(event.key())
            key = key.upper() if shift else key.lower()
            behs = [beh for beh in self.behaviors.from_hot_key(key) if beh.is_active()]
            if not behs:
                # that hot key is not defined; do nothing
                print(f"processHotKey: didn't match an active behavior, so doing nothing")
                return
            beh = behs[0]

        # Is there a pending bout?  If so, complete the annotation activity
        if self.pending_bout:
            chan = self.active_channels[0]
            if self.pending_bout.start() > self.current_time:
                # swap start and end before completing
                self.pending_bout.set_end(self.pending_bout.start())
                self.pending_bout.set_start(self.current_time)
            else:
                self.pending_bout.set_end(self.current_time)

            if do_delete:
                # truncate or remove any bouts of the same behavior as pending_bout
                self.annotations.truncate_or_remove_bouts(
                    self.pending_bout.behavior(),
                    self.pending_bout.start(),
                    self.pending_bout.end(),
                    chan)

            elif self.pending_bout.name() == beh.get_name():
                # insert the pending bout into the active channel (typical case)
                self.annotations.add_bout(self.pending_bout, chan)
                self.annotations.coalesce_bouts(
                    self.pending_bout.start(),
                    self.pending_bout.end(),
                    chan)
            start = self.pending_bout.start()
            end = self.pending_bout.end()
            self.pending_bout = None
            self.noteAnnotationsChanged(start, end)
        else:
            # Start a new annotation activity by saving a pending_bout
            self.pending_bout = Bout(self.current_time, self.current_time, beh)

    @Slot()
    def quit(self, event):
        if event:
            print(f"User has clicked close (x) button on the MainWindow")
            self.quitting.emit()
            QApplication.instance().processEvents()
            time.sleep(3./30.)  # wait for threads to shut down
            QApplication.instance().quit()
        else:
            #print("bento.quit() called")
            print(f"User has clicked on quit button on the MainWindow")
            self.mainWindow.flag = "quit"
            self.quitting.emit()
            QApplication.instance().processEvents()
            time.sleep(3./30.)  # wait for threads to shut down
            QApplication.instance().quit()

    def newVideoWidget(self, video_path: str) -> VideoFrame:
        video = VideoFrame(self)
        video.load_video(video_path)
        self.timeChanged.connect(video.updateFrame)
        self.currentAnnotsChanged.connect(video.updateAnnots)
        return video

    def newNeuralWidget(self, neuralData, base_dir: str) -> NeuralFrame:
        neuralWidget = NeuralFrame(self)
        neuralWidget.load(neuralData, base_dir)
        self.timeChanged.connect(neuralWidget.updateTime)
        self.active_channel_changed.connect(neuralWidget.setActiveChannel)
        return neuralWidget

    def load_poses(self, pose_path: str) -> object:
        return None

    @Slot()
    def loadTrial(self, videos, annotation, loadPose, loadNeural, loadAudio):
        self.video_widgets.clear()
        progressTotal = (
            len(videos) +
            (1 if annotation else 0) +
            (len(videos) if loadPose else 0) +  # potentially one pose per video
            (1 if loadNeural else 0) +
            (1 if loadAudio else 0))
        progressCompleted = 0
        progress = QProgressDialog("Loading Trial ...", "Cancel", 0, progressTotal, None)
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        with self.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).one()
            base_directory = session.base_directory
            # Qt converts paths to platform-specific separators under the hood,
            # so it's correct to use forward-slash ("/") here across all platforms
            base_dir = base_directory + "/"
            runningTime = 0.
            sample_rate = 30.0
            sample_rate_set = False
            for ix, video_data in enumerate(videos):
                progress.setLabelText(f"Loading video #{ix}...")
                progress.setValue(progressCompleted)
                if not isabs(video_data.file_path):
                    path = base_dir + video_data.file_path
                else:
                    path = video_data.file_path
                widget = self.newVideoWidget(fix_path(path))
                self.video_widgets.append(widget)
                if loadPose:
                    video = db_sess.query(VideoData).filter(VideoData.id == video_data.id).one()
                    if len(video.pose_data) > 0:
                        progress.setLabelText(f"Loading pose data for video #{ix}...")
                        progress.setValue(progressCompleted)
                        # for now, the UI only supports displaying the first pose file
                        pose_path = video.pose_data[0].file_path
                        if not isabs(pose_path):
                            pose_path = base_dir + pose_path
                        pose_polys = load_poses(self.mainWindow, pose_path)
                        widget.set_pose_data(pose_polys)
                    else:
                        print("No pose data in trial to load.")
                    progressCompleted += 1

                qr = widget.frameGeometry()
                # qr.moveCenter(self.screen_center + spacing)
                qr.moveCenter(self.screen_center)
                widget.move(qr.topLeft())    #TODO: need to space multiple videos out
                widget.show()
                runningTime = max(runningTime, widget.running_time())
                if not sample_rate_set:
                    sample_rate = widget.sample_rate()
                    sample_rate_set = True
                progressCompleted += 1
            if annotation:
                if not isabs(annotation.file_path):
                    annot_path = base_dir + annotation.file_path
                else:
                    annot_path = annotation.file_path
                annot_path = fix_path(annot_path)
                sample_rate = annotation.sample_rate
            else:
                annot_path = None
            progress.setLabelText("Loading annotations...")
            progress.setValue(progressCompleted)
            self.load_or_init_annotations(annot_path, sample_rate, runningTime)
            # try:
            #     self.load_or_init_annotations(annot_path, sample_rate, runningTime)
            # except Exception as e:
            #     QMessageBox.about(self.selectTrialWindow, "Error", f"Attempt to load annotations from {annot_path} "
            #         f"failed with error {str(e)}")
            #     for widget in self.video_widgets:
            #         widget.close()
            #     self.video_widgets.clear()
            #     return False
            progressCompleted += 1
            self.noteAnnotationsChanged(self.time_start, self.time_end)

            # load neural data
            if loadNeural:
                with self.db_sessionMaker() as db_sess:
                    trial = db_sess.query(Trial).filter(Trial.id == self.trial_id).one()
                    if trial.neural_data:
                        progress.setLabelText("Loading neural data...")
                        progress.setValue(progressCompleted)
                        neuralWidget = self.newNeuralWidget(trial.neural_data[0], base_dir)
                        self.neural_widgets.append(neuralWidget)
                        if self.annotationsScene:
                            neuralWidget.overlayAnnotations(self.annotationsScene)
                        if runningTime==0 and self.newAnnotations and len(videos)==0:
                            running_time = trial.neural_data[0].sample_rate * (trial.neural_data[0].stop_frame-trial.neural_data[0].start_frame)
                            self.time_end = Timecode(self.time_start.framerate, start_seconds=self.time_start.float + running_time)
                        neuralWidget.show()
                        progressCompleted += 1
                    else:
                        print("No neural data in trial.")
            if loadAudio:
                print("Load audio data if any")
                progress.setLabelText("Loading audio data...")
                progress.setValue(progressCompleted)
                # if self.trial_id.audio_data:
                #     print(f"Load audio from {self.trial_id.audio_data[0].file_path}")
                # else:
                #     print("No audio data in trial.")
                progressCompleted += 1
        # set the time to get all the new widgets in sync
        progress.setLabelText("Done")
        progress.setValue(progressCompleted)
        self.set_time(self.time_start)
        return True

    @Slot()
    def toggleBehaviorVisibility(self):
        self.behaviorsDialog.toggleVisibility()

    @Slot(float, float)
    def noteAnnotationsChanged(self, start=None, end=None):
        if start == None:
            start = self.time_start.float
        elif isinstance(start, Timecode):
            start = start.float
        if end == None:
            end = self.time_end.float
        elif isinstance(end, Timecode):
            end = end.float
        self.newAnnotations = True
        self.annotationsScene.sceneChanged(start, end)

    def deleteAnnotationsByName(self, behaviorName):
        beh = self.behaviors.get(behaviorName)
        for chan in self.annotations.channel_names():
            self.annotations.truncate_or_remove_bouts(beh, self.time_start, self.time_end, chan)

   # Signals
    quitting = Signal()
    timeChanged = Signal(Timecode)
    currentAnnotsChanged = Signal(list)
    active_channel_changed = Signal(str)
    annotationsSceneHeightChanged = Signal(float)

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
