# editTrialDialog.py

from db.schema_sqlalchemy import Camera, Trial, Session, VideoData, NeuralData, AnnotationsData, Investigator
from sqlalchemy import func, select
from db.editTrialDialog_ui import Ui_EditTrialDialog
from annot.annot import Annotations
from qtpy.QtCore import Qt, Signal, Slot
from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QDialog, QFileDialog, QHeaderView, QMessageBox
from widgets.tableModel import EditableTableModel
from widgets.deleteableTableView import DeleteableTableView
from timecode import Timecode
from os.path import expanduser, getmtime, basename
from datetime import date, datetime
from video.seqIo import seqIo_reader
from video.mp4Io import mp4Io_reader
import pymatreader as pmr
import warnings
# from caiman.utils.utils import load_dict_from_hdf5

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
        self.ui.neuralsSearchPushButton.clicked.connect(self.addNeuralFiles)
        self.ui.annotationsSearchPushButton.clicked.connect(self.addAnnotationFiles)
        self.ui.trialNumLineEdit.setValidator(QIntValidator())
        self.video_data = None

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
        self.populateNeuralsTableView(True)
        self.populateAnnotationsTableView(True)

    @Slot()
    def populateTrialNum(self):
        maxTrial = None
        with self.bento.db_sessionMaker() as db_sess:
            maxTrial = db_sess.query(func.max(Trial.trial_num)).filter(Trial.session_id == self.session_id).scalar()
        self.ui.trialNumLineEdit.setText(str(maxTrial + 1 if isinstance(maxTrial, int) else 1))

    # Video Data

    def setVideoModel(self, model):
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
            if results:
                header = results[0].header()
                data_list = [elem.toDict() for elem in results]
                model = EditableTableModel(self, data_list, header)
                self.setVideoModel(model)
                if len(data_list) > 0:
                    self.video_data = data_list[0] # needed by add_neural()

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
        ext = basename(file_path).rsplit('.', 1)[-1]
        try:
            if ext=='mp4'or ext=='avi':
                reader = mp4Io_reader(file_path)
            elif ext=='seq':
                reader = seqIo_reader(file_path, buildTable=False)
            else:
                raise Exception(f"video format {ext} not supported.")
        except Exception:
            print(f"Error trying to open video file {file_path}")
            raise

        sample_rate = float(reader.header['fps'])
        ts = reader.getTs(1)[0]
        reader.close()
        dt = datetime.fromtimestamp(ts)
        # set the video start time
        start_time = Timecode(sample_rate, dt.time().isoformat()).float

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        this_camera_position = None
        for camera_position in available_cameras:
            if file_path.lower().find(camera_position[0].lower()) >= 0:
                this_camera_position = camera_position[0]
                break
        item = {
            'id': None,
            'file_path': file_path,
            'sample_rate': sample_rate,
            'start_time': start_time,
            'camera_position': this_camera_position,
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
            print(f"addVideoFile -- header: {header}, data_list: {data_list}")
            model = EditableTableModel(self, data_list, header)
            self.setVideoModel(model)
            self.video_data = item

    @Slot()
    def addVideoFiles(self):
        #TODO: How to delete video file references from the DB?
        baseDir = None
        with self.bento.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).scalar()
            if session:
                baseDir = session.base_directory
            available_cameras = db_sess.execute(select(Camera.position)).all()
        if not baseDir:
            baseDir = expanduser("~")
        # Qt converts paths to platform-specific separators under the hood,
        # so it's correct to use forward-slash ("/") here across all platforms
        if not baseDir.endswith("/"):
            baseDir += "/"
        videoFiles, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files to add to Trial",
            baseDir,
            "Seq files (*.seq);;mp4 files (*.mp4);;Generic video files (*.avi)",
            "Seq files (*.seq)")
        if len(videoFiles) > 0:
            for file_path in videoFiles:
                self.addVideoFile(file_path, baseDir, available_cameras)

    def updateVideoData(self, trial, db_sess):
        model = self.ui.videosFileTableView.model()
        if model:
            for ix, entry in enumerate(iter(model)):
                tableIndex = model.createIndex(ix, 0)
                if self.ui.videosFileTableView.isRowHidden(ix):
                    # delete the entry from the DB
                    print(f"Delete videos row {ix} from DB")
                    if ix < len(trial.video_data) and trial.video_data[ix].id == entry['id']:
                        db_sess.delete(trial.video_data[ix])
                elif model.isDirty(tableIndex):
                    print(f"item at row {ix} is dirty")
                    if ix < len(trial.video_data) and trial.video_data[ix].id == entry['id']:
                        trial.video_data[ix].fromDict(entry, db_sess)
                    else:
                        # new item
                        item = VideoData(entry, db_sess) # update everything in the item and let the transaction figure out what changed.
                        db_sess.add(item)
                        trial.video_data.append(item)
                    model.clearDirty(tableIndex)
                else:
                    print(f"item at row {ix} wasn't dirty, so did nothing")
        else:
            print("No video files listed, so nothing to do.")

    # Neural Data

    def setNeuralModel(self, model):
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
            if results:
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
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            mat = pmr.read_mat(file_path)
        try:
            data = mat['results']['C_raw']
        except Exception as e:
            QMessageBox.about(self, "File Read Error", f"Error reading neural data file {file_path}: {e}")
            return
        # Get various data from neural file
        # if the file is a h5 file, we can read it using caiman.utils, as below
        # neural_dict = load_dict_from_hdf5(file_path)
        # Otherwise, we can only guess from the video file info.
        if isinstance(self.video_data, dict):
            sample_rate = self.video_data['sample_rate']
            start_time = self.video_data['start_time']
        else:
            sample_rate = 30.0
            # get start time (seconds from midnight) from file create time
            create_time = datetime.fromtimestamp(getmtime(file_path))
            create_day_midnight = datetime.fromordinal(create_time.toordinal())
            start_time = create_time.timestamp() - create_day_midnight.timestamp()
        start_frame = 1
        stop_frame = data.shape[1]

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        item = {
            'id': None,
            'file_path': file_path,
            'sample_rate': sample_rate,
            'format': 'CNMFE', # by default
            'start_time': start_time,
            'start_frame': start_frame,
            'stop_frame': stop_frame,
            'trial_id': self.trial_id,
            'dirty': True
        }
        model = self.ui.neuralsTableView.model()
        if model:
            print(f"addNeuralFile: found existing model to append item {item} to")
            model.appendData(item)
        else:
            print(f"addNeuralFile: didn't find existing model; making a new one with {item}")
            header = NeuralData().header()
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
        # Qt converts paths to platform-specific separators under the hood,
        # so it's correct to use forward-slash ("/") here across all platforms
        if not baseDir.endswith("/"):
            baseDir += "/"
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
        if model:
            for ix, entry in enumerate(iter(model)):
                print(f"updateNeural ix = {ix}, entry = {entry}")
                tableIndex = model.createIndex(ix, 0)
                if self.ui.neuralsTableView.isRowHidden(ix):
                    # delete the entry from the DB
                    print(f"Delete neural data row {ix} from DB")
                    if ix < len(trial.neural_data) and trial.neural_data[ix].id == entry['id']:
                        db_sess.delete(trial.neural_data[ix])
                elif model.isDirty(tableIndex):
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
        else:
            print("No neural data listed, so nothing to do")

    # Annotations

    def setAnnotationsModel(self, model):
        oldModel = self.ui.annotationsTableView.selectionModel()
        self.ui.annotationsTableView.setModel(model)
        self.ui.annotationsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.annotationsTableView.resizeColumnsToContents()
        self.ui.annotationsTableView.hideColumn(0)   # don't show the ID field, but we need it for reference
        self.ui.annotationsTableView.setSortingEnabled(False)
        self.ui.annotationsTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def populateAnnotationsTableView(self, updateTrialNum):
        with self.bento.db_sessionMaker() as db_sess:
            results = db_sess.query(AnnotationsData).filter(AnnotationsData.trial == self.trial_id).all()
            if results:
                header = results[0].header()
                data_list = [elem.toDict() for elem in results]
                model = EditableTableModel(self, data_list, header)
                self.setAnnotationsModel(model)

                selectionModel = self.ui.annotationsTableView.selectionModel()
                if updateTrialNum:
                    selectionModel.selectionChanged.connect(self.populateTrialNum)
                else:
                    try:
                        selectionModel.selectionChanged.disconnect(self.populateTrialNum)
                    except RuntimeError:
                        # The above call raises RuntimeError if the signal is not connected,
                        # which we can safely ignore.
                        pass

    def addAnnotationFile(self, file_path, baseDir):
        """
        """
        print(f"Add annotation file {file_path}")
        annotations = Annotations(self.bento.behaviors)
        try:
            annotations.read(file_path)
        except Exception as e:
            QMessageBox.about(self, "File Read Error", f"Error reading annotations file {file_path}: {e}")
            return
        # Get various data from the annotations file
        # if the file is a h5 file, we can read it using caiman.utils, as below
        # neural_dict = load_dict_from_hdf5(file_path)
        # Otherwise, we can only guess from the video file info.
        if isinstance(annotations, Annotations):
            sample_rate = annotations.sample_rate()
        else:
            sample_rate = 30.0

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        annotator_name = ""
        if self.bento.investigator_id:
            with self.bento.db_sessionMaker() as db_sess:
                investigator = db_sess.query(Investigator).filter(Investigator.id == self.bento.investigator_id).scalar()
                if investigator:
                    annotator_name = investigator.user_name

        item = {
            'id': None,
            'file_path': file_path,
            'sample_rate': sample_rate,
            'format': annotations.format(),
            'start_time': annotations.time_start().float,
            'start_frame': annotations.time_start().frame_number,
            'stop_frame': annotations.time_end().frame_number,
            'annotator_name': annotator_name,
            'method': "manual",
            'trial_id': self.trial_id,
            'dirty': True
        }
        model = self.ui.annotationsTableView.model()
        if model:
            print(f"addAnnotationFile: found existing model to append item {item} to")
            model.appendData(item)
        else:
            print(f"addNAnnotationFile: didn't find existing model; making a new one with {item}")
            header = AnnotationsData().header()
            data_list = [item]
            model = EditableTableModel(self, data_list, header)
            self.setAnnotationsModel(model)

    def updateAnnotationsData(self, trial, db_sess):
        model = self.ui.annotationsTableView.model()
        if model:
            for ix, entry in enumerate(iter(model)):
                print(f"updateAnnotations ix = {ix}, entry = {entry}")
                tableIndex = model.createIndex(ix, 0)
                if self.ui.annotationsTableView.isRowHidden(ix):
                    # delete the entry from the DB
                    print(f"Delete annotation row {ix} from DB")
                    if ix < len(trial.annotations) and trial.annotations[ix].id == entry['id']:
                        db_sess.delete(trial.annotations[ix])
                elif model.isDirty(tableIndex):
                    print(f"item at row {ix} is dirty")
                    if ix < len(trial.annotations) and trial.annotations[ix].id == entry['id']:
                        print(f"Existing db entry for id {entry['id']} at index {ix}; updating in place")
                        trial.annotations[ix].fromDict(entry, db_sess)
                    else:
                        # new item
                        print(f"No existing db entry for index {ix}; create a new item")
                        item = AnnotationsData(entry, db_sess) # update everything in the item and let the transaction figure out what changed.
                        db_sess.add(item)
                        trial.annotations.append(item)
                    model.clearDirty(tableIndex)
                else:
                    print(f"item at row {ix} wasn't dirty, so did nothing")
        else:
            print("No annotations listed, so nothing to do.")

    @Slot()
    def addAnnotationFiles(self):
        #TODO: How to delete annotation file references from the DB?
        baseDir = None
        with self.bento.db_sessionMaker() as db_sess:
            session = db_sess.query(Session).filter(Session.id == self.session_id).scalar()
            if session:
                baseDir = session.base_directory
        if not baseDir:
            baseDir = expanduser("~")
        # Qt converts paths to platform-specific separators under the hood,
        # so it's correct to use forward-slash ("/") here across all platforms
        if not baseDir.endswith("/"):
            baseDir += "/"
        annotationFiles, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Annotation Files to add to Trial",
            baseDir,
            "Caltech Annotation files (*.annot)",
            "Caltech Annotation files (*.annot)")
        if len(annotationFiles) > 0:
            for file_path in annotationFiles:
                self.addAnnotationFile(file_path, baseDir)

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
            self.updateAnnotationsData(trial, db_sess)
            db_sess.commit()
            self.trialsChanged.emit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
