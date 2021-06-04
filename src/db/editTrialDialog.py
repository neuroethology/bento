# editTrialDialog.py

from db.schema_sqlalchemy import Camera, Trial, Session, VideoData, NeuralData
from sqlalchemy import func, select
from db.editTrialDialog_ui import Ui_EditTrialDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import QDialog, QFileDialog, QComboBox, QHeaderView
from widgets.tableModel import EditableTableModel
from timecode import Timecode
from os.path import expanduser, abspath, dirname, isdir, sep
from datetime import date, datetime
from video.seqIo import seqIo_reader

class EditTrialDialog(QDialog):

    quitting = Signal()
    trialsChanged = Signal()

    def __init__(self, bento, session_id, trial_id=None):
        super().__init__()
        self.bento = bento
        self.session_id = session_id
        self.ui = Ui_EditTrialDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)
        self.ui.videosSearchPushButton.clicked.connect(self.addVideoFiles)
        self.ui.trialNumLineEdit.setValidator(QIntValidator())

        self.trial_id = trial_id
        if trial_id:
            self.updateUIFromCurrentTrial()
        else:
            self.populateTrialNum()

    def updateUIFromCurrentTrial(self):
        with self.bento.db_sessionMaker() as db_sess:
            trial = db_sess.query(Trial).where(Trial.id == self.trial_id).scalar()
            if trial:
                self.ui.trialNumLineEdit.setText(str(trial.trial_num))
                self.ui.stimulusLineEdit.setText(trial.stimulus)
        self.populateVideosTableView(True)

    @Slot()
    def populateTrialNum(self):
        maxTrial = None
        with self.bento.db_sessionMaker() as db_sess:
            maxTrial = db_sess.query(func.max(Trial.trial_num)).filter(Trial.session_id == self.session_id).scalar()
        self.ui.trialNumLineEdit.setText(str(maxTrial + 1 if isinstance(maxTrial, int) else 1))
        print(f'trialNumLineEdit text is "{self.ui.trialNumLineEdit.text()}"')


    # Video Data

    def setVideoModel(self, model):
        print("in setVideoModel")
        oldModel = self.ui.videosFileTableView.selectionModel()
        self.ui.videosFileTableView.setModel(model)
        self.ui.videosFileTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.videosFileTableView.resizeColumnsToContents()
        self.ui.videosFileTableView.hideColumn(0)   # don't show the ID field, but we need it for reference
        self.ui.videosFileTableView.setSortingEnabled(False)
        self.ui.videosFileTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def populateVideosTableView(self, updateTrialNum):
        with self.bento.db_sessionMaker() as db_sess:
            results = db_sess.query(VideoData).filter(VideoData.trial == self.trial_id).all()
            header = results[0].header()
            data_list = [elem.toDict() for elem in results]
        model = EditableTableModel(self, data_list, header)
        self.setVideoModel(model)

        selectionModel = self.ui.videosFileTableView.selectionModel()
        if updateTrialNum:
            selectionModel.selectionChanged.connect(self.populateTrialNum)
        else:
            try:
                selectionModel.selectionChanged.disconnect(self.populateTrialNum)
            except RuntimeError:
                # The above call raises RuntimeError if the signal is not connected,
                # which we can safely ignore.
                pass
    
    def addVideoFile(self, file_path, baseDir, available_cameras):
        """
        available_cameras is a tuple (id, position)
        """
        print(f"Add video file {file_path}")
        # Get various data from video file
        try:
            reader = seqIo_reader(file_path)
        except Exception:
            print(f"Error trying to open video file {file_path}")
            raise

        sample_rate = reader.header['fps']
        ts = reader.getTs(1)[0]
        reader.close()
        dt = datetime.fromtimestamp(ts)
        # set the video start time
        start_time = Timecode(sample_rate, dt.time().isoformat()).float

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        camera_position = None
        for camera in available_cameras:
            if file_path.lower().find(camera[1].lower()) >= 0:
                camera_position = camera[1]
                camera_id = camera[0]
                break
        item = {
            'id': None,
            'file_path': file_path,
            'sample_rate': sample_rate,
            'start_time': start_time,
            'camera': camera_position,
            'camera_id': camera_id,
            'trial_id': self.trial_id,
            #TODO: pose_data?
            'dirty': True
        }
        model = self.ui.videosFileTableView.model()
        if model:
            print(f"addVideoFile: found existing model to append item {item} to")
            model.appendData(item)
        else:
            print(f"addVideoFile: didn't find existing model; making a new one with {item}")
            header = VideoData().header()
            data_list = [item]
            model = EditableTableModel(self, data_list, header)
            self.setVideoModel(model)

    @Slot()
    def addVideoFiles(self):
        #TODO: How to delete video file references from the DB?
        baseDir = None
        with self.bento.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).scalar()
            if session:
                baseDir = session.base_directory
            available_cameras = db_sess.execute(select([Camera.id, Camera.position])).all()
        if not baseDir:
            baseDir = expanduser("~")
        if not baseDir.endswith(sep):
            baseDir += sep
        videoFiles, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files to add to Trial",
            baseDir,
            "Seq files (*.seq);;Generic video files (*.avi)",
            "Seq files (*.seq)")
        if len(videoFiles) > 0:
            for file_path in videoFiles:
                self.addVideoFile(file_path, baseDir, available_cameras)

    def updateVideoData(self, trial, db_sess):
        model = self.ui.videosFileTableView.model()
        for ix, entry in enumerate(model.getIterator()):
            print(f"updateVideos: ix = {ix}, entry = {entry}")
            tableIndex = model.createIndex(ix, 0)
            if model.isDirty(tableIndex):
                print(f"item at row {ix} is dirty")
                if ix < len(trial.video_data) and trial.video_data[ix].id == entry['id']:
                    print(f"Existing db entry for id {entry['id']} at index {ix}; updating in place")
                    trial.video_data[ix].fromDict(entry, db_sess)
                else:
                    # new item
                    print(f"No existing db entry for index {ix}; create a new item")
                    item = VideoData(entry, db_sess) # update everything in the item and let the transaction figure out what changed.
                    db_sess.add(item)
                    trial.video_data.append(item)
                model.clearDirty(tableIndex)
            else:
                print(f"item at row {ix} wasn't dirty, so did nothing")

    # Neural Data

    def setNeuralModel(self, model):
        print("in setVideoModel")
        oldModel = self.ui.neuralsTableView.selectionModel()
        self.ui.neuralsTableView.setModel(model)
        self.ui.neuralsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.neuralsTableView.resizeColumnsToContents()
        self.ui.neuralsTableView.hideColumn(0)   # don't show the ID field, but we need it for reference
        self.ui.neuralsTableView.setSortingEnabled(False)
        self.ui.neuralsTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def populateNeuralsTableView(self, updateTrialNum):
        with self.bento.db_sessionMaker() as db_sess:
            results = db_sess.query(NeuralData).filter(NeuralData.trial == self.trial_id).all()
            header = results[0].header()
            data_list = [elem.toDict() for elem in results]
        model = EditableTableModel(self, data_list, header)
        self.setNeuralModel(model)

        selectionModel = self.ui.neuralsTableView.selectionModel()
        if updateTrialNum:
            selectionModel.selectionChanged.connect(self.populateTrialNum)
        else:
            try:
                selectionModel.selectionChanged.disconnect(self.populateTrialNum)
            except RuntimeError:
                # The above call raises RuntimeError if the signal is not connected,
                # which we can safely ignore.
                pass

    def addNeuralFile(self, file_path, baseDir):
        """
        """
        print(f"Add neural file {file_path}")
        # Get various data from neural file
        dt = datetime.fromtimestamp(ts)
        # set the video start time
        start_time = Timecode(sample_rate, dt.time().isoformat()).float

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        item = {
            'id': None,
            'file_path': file_path,
            'sample_rate': sample_rate,
            'format': 'CNMFE', # by default
            'start_time': start_time,
            'start_frame': 1,
            'stop_frame': stop_frame,
            'trial_id': self.trial_id,
            'dirty': True
        }
        model = self.ui.videosFileTableView.model()
        if model:
            print(f"addVideoFile: found existing model to append item {item} to")
            model.appendData(item)
        else:
            print(f"addVideoFile: didn't find existing model; making a new one with {item}")
            header = VideoData().header()
            data_list = [item]
            model = EditableTableModel(self, data_list, header)
            self.setNeuralModel(model)

    @Slot()
    def addNeuralFiles(self):
        #TODO: How to delete neural file references from the DB?
        baseDir = None
        with self.bento.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).scalar()
            if session:
                baseDir = session.base_directory
        if not baseDir:
            baseDir = expanduser("~")
        if not baseDir.endswith(sep):
            baseDir += sep
        neuralFiles, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Neural Files to add to Trial",
            baseDir,
            "MatLab format files (*.mat)",
            "MatLab format files (*.mat)")
        if len(neuralFiles) > 0:
            for file_path in neuralFiles:
                self.addNeuralFile(file_path, baseDir)

    def updateNeuralData(self, trial, db_sess):
        model = self.ui.neuralsTableView.model()
        for ix, entry in enumerate(model.getIterator()):
            print(f"updateNeural ix = {ix}, entry = {entry}")
            tableIndex = model.createIndex(ix, 0)
            if model.isDirty(tableIndex):
                print(f"item at row {ix} is dirty")
                if ix < len(trial.neural_data) and trial.neural_data[ix].id == entry['id']:
                    print(f"Existing db entry for id {entry['id']} at index {ix}; updating in place")
                    trial.neural_data[ix].fromDict(entry, db_sess)
                else:
                    # new item
                    print(f"No existing db entry for index {ix}; create a new item")
                    item = NeuralData(entry, db_sess) # update everything in the item and let the transaction figure out what changed.
                    db_sess.add(item)
                    trial.neural_data.append(item)
                model.clearDirty(tableIndex)
            else:
                print(f"item at row {ix} wasn't dirty, so did nothing")

    @Slot()
    def accept(self):
        with self.bento.db_sessionMaker() as db_sess:
            if self.trial_id:
                trial = db_sess.query(Trial).filter(Trial.id == self.trial_id).scalar()
                if not trial:
                    raise RuntimeWarning(f"Trial id {self.trial_id} not found!")
            else:
                trial = Trial()
                db_sess.add(trial)
                trial.session_id = self.session_id
            trial.trial_num = self.ui.trialNumLineEdit.text()
            trial.stimulus = self.ui.stimulusLineEdit.text()

            self.updateVideoData(trial, db_sess)
            self.updateNeuralData(trial, db_sess)
            db_sess.commit()
            self.trialsChanged.emit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
