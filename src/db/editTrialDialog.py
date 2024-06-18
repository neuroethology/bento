# editTrialDialog.py

from db.schema_sqlalchemy import (Camera, Trial, Session, VideoData, NeuralData,
    AnnotationsData, PoseData, Investigator)
from sqlalchemy import func, select
from db.editTrialDialog_ui import Ui_EditTrialDialog
from annot.annot import Annotations
from qtpy.QtCore import QModelIndex, Qt, Signal, Slot
from qtpy.QtGui import QBrush, QIntValidator, QStandardItemModel
from qtpy.QtWidgets import (QDialog, QFileDialog, QHeaderView, QMessageBox,
    QTreeWidgetItem, QTreeWidgetItemIterator, QLineEdit)
from models.tableModel import EditableTableModel
from widgets.deleteableViews import (DeleteableTreeWidget, 
                                     OffsetTimeItemDelegate, CustomComboBoxDelegate)
# from models.videoTreeModel import VideoTreeModel
from timecode import Timecode
from os.path import expanduser, getmtime, basename
from datetime import date, datetime
from video.seqIo import seqIo_reader
from video.mp4Io import mp4Io_reader
import pymatreader as pmr
import warnings
# from caiman.utils.utils import load_dict_from_hdf5

def addPoseHeaderIfNeeded(parent):
    if parent.childCount() == 0:
        header = PoseData().header()
        poseHeaderItem = QTreeWidgetItem(parent, header, type=DeleteableTreeWidget.PoseHeaderType)
        flags = poseHeaderItem.flags()
        flags &= ~Qt.ItemIsEditable
        flags &= ~Qt.ItemIsSelectable
        poseHeaderItem.setFlags(flags)
        poseHeaderItem.setToolTip(header.index('Offset Time'), 'ss.ms')
        font = poseHeaderItem.font(0)
        font.setBold(True)
        for column in range(poseHeaderItem.columnCount()):
            poseHeaderItem.setFont(column, font)
            poseHeaderItem.setTextAlignment(column, Qt.AlignCenter)
        parent.addChild(poseHeaderItem)
    elif parent.child(0).type() == DeleteableTreeWidget.PoseHeaderType and parent.child(0).isHidden():
        # there is already a header that was hidden previously and not yet deleted, so unhide it
        parent.child(0).setHidden(False)
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
        self.ui.addPosePushButton.clicked.connect(self.addPoseFileToVideo)
        self.ui.trialNumLineEdit.setValidator(QIntValidator())
        self.ui.trialDateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        self.ui.trialDateTimeEdit.setDateTime(datetime.strptime(
                                              str(datetime.now().isoformat(sep=" ", timespec="milliseconds")),
                                              "%Y-%m-%d %H:%M:%S.%f"
                                            ))
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
                trial_start_time = str(datetime.fromtimestamp(trial.trial_start_time).isoformat(sep=' ', timespec='milliseconds'))
                self.ui.trialDateTimeEdit.setDateTime(datetime.strptime(trial_start_time, "%Y-%m-%d %H:%M:%S.%f"))
        self.populateVideosTreeWidget(True)
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
        oldModel = self.ui.videosTreeView.selectionModel()
        self.ui.videosTreeView.setModel(model)
        # Unlike for the table views, header font and resizing takes place for Video data
        # during populateViewsTreeWidget, when the header is set.  See below.
        self.ui.videosTreeView.setSortingEnabled(False)
        self.ui.videosTreeView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def populateVideosTreeWidget(self, updateTrialNum):
        headerSet = False
        with self.bento.db_sessionMaker() as db_sess:
            results = db_sess.query(VideoData).filter(VideoData.trial == self.trial_id).all()
            if results:
                for elem in results:
                    videoTreeItem = QTreeWidgetItem(self.ui.videosTreeWidget)
                    videoTreeItem.setFlags(videoTreeItem.flags() | Qt.ItemIsEditable)
                    videoDict = elem.toDict()
                    header = elem.header()
                    if not headerSet:
                        self.ui.videosTreeWidget.setColumnCount(len(header))
                        self.ui.videosTreeWidget.setHeaderLabels(header)
                        self.ui.videosTreeWidget.hideColumn(header.index('id'))
                        self.ui.videosTreeWidget.hideColumn(header.index('trial_id'))
                        self.ui.videosTreeWidget.setItemDelegate(OffsetTimeItemDelegate())
                        headerItem = self.ui.videosTreeWidget.headerItem()
                        headerItem.setToolTip(header.index('Offset Time'), 'ss.ms')
                        font = headerItem.font(0)
                        font.setBold(True)
                        for column in range(headerItem.columnCount()):
                            headerItem.setFont(column, font)
                            headerItem.setTextAlignment(column, Qt.AlignCenter)
                        headerSet = True
                    videoTreeItem.setToolTip(header.index('Offset Time'), 'ss.ms')
                    for ix, key in enumerate(header):
                        videoTreeItem.setData(ix, Qt.EditRole, videoDict[key])
                    if len(elem.pose_data) > 0:
                        addPoseHeaderIfNeeded(videoTreeItem)
                        for poseItem in elem.pose_data:
                            poseTreeItem = QTreeWidgetItem(videoTreeItem)
                            poseTreeItem.setFlags(poseTreeItem.flags() | Qt.ItemIsEditable)
                            poseTreeItem.setToolTip(poseItem.header().index('Offset Time'), 'ss.ms')
                            poseDict = poseItem.toDict()
                            for iy, poseKey in enumerate(poseItem.header()):
                                poseTreeItem.setData(iy, Qt.EditRole, poseDict[poseKey])
                            videoTreeItem.addChild(poseTreeItem)
                    self.ui.videosTreeWidget.addTopLevelItem(videoTreeItem)

                for column in range(self.ui.videosTreeWidget.columnCount()):
                    self.ui.videosTreeWidget.resizeColumnToContents(column)

                # if updateTrialNum:
                #     self.ui.videosTreeWidget.itemSelectionChanged.connect(self.populateTrialNum)
                # else:
                #     try:
                #         self.ui.videosTreeWidget.itemSelectionChanged.disconnect(self.populateTrialNum)
                #     except RuntimeError:
                #         # The above call raises RuntimeError if the signal is not connected,
                #         # which we can safely ignore.
                #         pass

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
                #create_time = getmtime(file_path)
            elif ext=='seq':
                reader = seqIo_reader(file_path, buildTable=False)
                #create_time = 0.
            else:
                raise Exception(f"video format {ext} not supported.")
        except Exception:
            print(f"Error trying to open video file {file_path}")
            raise

        sample_rate = float(reader.header['fps'])
        ts = reader.getTs(1)[0]
        reader.close()
        # set the video offset time
        offset_time = float(0.000)

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        this_camera_position = None
        for camera_position in available_cameras:
            if file_path.lower().find(camera_position[0].lower()) >= 0:
                this_camera_position = camera_position[0]
                break
        item = {
            'id': None,
            'Video File Path': file_path,
            'Sample Rate': sample_rate,
            'Offset Time': offset_time,
            'Camera Position': this_camera_position,
            'trial_id': self.trial_id,
            'pose_data': [],
            'dirty': True
        }
        # Okay, load it into the tree
        videoKeys = VideoData().header()
        # If there's nothing in the tree yet, we need to do some initialization
        if self.ui.videosTreeWidget.topLevelItemCount() == 0:
            self.ui.videosTreeWidget.setColumnCount(len(videoKeys))
            self.ui.videosTreeWidget.setHeaderLabels(videoKeys)
            self.ui.videosTreeWidget.hideColumn(videoKeys.index('id'))
            self.ui.videosTreeWidget.setItemDelegate(OffsetTimeItemDelegate())
        # Attach the video file to treeWidget as a top-level item
        videoItem = QTreeWidgetItem(self.ui.videosTreeWidget)
        videoItem.setFlags(videoItem.flags() | Qt.ItemIsEditable)
        videoItem.setToolTip(videoKeys.index('Offset Time'), 'ss.ms')
        # insert the data into item
        for key in videoKeys:
            videoItem.setData(videoKeys.index(key), Qt.EditRole, item[key])
        self.ui.videosTreeWidget.addTopLevelItem(videoItem)

    def addPoseFileToVideo(self):
        """
        Add the specified pose file to the selected video, displayed as a child node
        """
        # get selected video, or warn if none or invalid
        selectedItems = self.ui.videosTreeWidget.selectedItems()
        if len(selectedItems) < 1:
            warningMsg = "No video seleted"
            QMessageBox.information(self, "Add Pose...", warningMsg)
        videoItem = selectedItems[0] # the Tree Widget is configured to only allow one selection
        if bool(videoItem.parent()): # not a top level item
            QMessageBox.information(self, "Add Pose...", "Please select a video file, not a pose")
            return
        # open the file dialog and get a pose file to attach to the video data
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
        poseFilePath, format = self.bento.pose_registry.getPoseFilePath(self, baseDir)
        if not poseFilePath:
            return
        # make path relative to baseDir if possible
        if poseFilePath.startswith(baseDir):
            poseFilePath = poseFilePath[len(baseDir):]
        # Attach the pose file to the video data in the treeWidget as a child node
        addPoseHeaderIfNeeded(videoItem)
        poseItem = QTreeWidgetItem(videoItem)
        poseItem.setFlags(poseItem.flags() | Qt.ItemIsEditable)
        videosHeaderItem = self.ui.videosTreeWidget.headerItem()
        videosHeader = [videosHeaderItem.data(ix, Qt.DisplayRole) for ix in range(videosHeaderItem.columnCount())]
        # insert the data into the pose child item
        poseKeys = PoseData().keys
        poseItem.setToolTip(poseKeys.index('Offset Time'), 'ss.ms')
        poseItem.setData(poseKeys.index('Pose File Path'), Qt.EditRole, poseFilePath)
        poseItem.setData(poseKeys.index('Sample Rate'), Qt.EditRole, videoItem.data(videosHeader.index('Sample Rate'), Qt.DisplayRole))
        poseItem.setData(poseKeys.index('Offset Time'), Qt.EditRole, videoItem.data(videosHeader.index('Offset Time'), Qt.DisplayRole))
        poseItem.setData(poseKeys.index('Format'), Qt.EditRole, format)
        poseItem.setData(poseKeys.index('video_id'), Qt.EditRole, videoItem.data(videosHeader.index('id'), Qt.DisplayRole))
        poseItem.setData(poseKeys.index('trial_id'), Qt.EditRole, videoItem.data(videosHeader.index('trial_id'), Qt.DisplayRole))
        # poseItem.setData(poseKeys.index('id'), Qt.EditRole, "1")
        videoItem.addChild(poseItem)

    @Slot()
    def addVideoFiles(self):
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
            "Seq files (*.seq);;mp4 files (*.mp4);;Generic video files (*.avi);; Supported videos (*.seq *.mp4 *.avi)",
            "Supported videos (*.seq *.mp4 *.avi)")
        if len(videoFiles) > 0:
            for file_path in videoFiles:
                self.addVideoFile(file_path, baseDir, available_cameras)

    def updateVideoData(self, trial, db_sess):
        videoHeader = VideoData().header()
        poseHeader = PoseData().header()
        treeIterator = QTreeWidgetItemIterator(self.ui.videosTreeWidget)
        deferredActionList = []
        for treeItemIter in iter(treeIterator):
            treeItem = treeItemIter.value()
            if treeItem.parent():
                # this is a pose item; save it to do after videos
                if treeItem.type() != DeleteableTreeWidget.PoseHeaderType:
                    # skip the pose header
                    deferredActionList.append(treeItem)
                continue

            # top-level item: video data
            thisVideo_data = None
            thisVideo_data_index = -1
            for ix, video_dataItem in enumerate(trial.video_data):
                if video_dataItem.id == treeItem.data(videoHeader.index('id'), Qt.DisplayRole):
                    thisVideo_data = video_dataItem
                    thisVideo_data_index = ix
                    break
            if bool(thisVideo_data) and treeItem.isHidden():
                # delete the entry from the DB
                db_sess.delete(thisVideo_data)
                continue
            # create a dict from the treeItem for either updating or a new DB entry
            videoItemDict = {}
            for key in videoHeader:
                videoItemDict[key] = treeItem.data(videoHeader.index(key), Qt.DisplayRole)
            if bool(thisVideo_data):
                # update any items that have changed in the existing entry
                trial.video_data[thisVideo_data_index].fromDict(videoItemDict, db_sess)
            else:
                # new item
                dbItem = VideoData(videoItemDict, db_sess)
                db_sess.add(dbItem)
                trial.video_data.append(dbItem)
                # db_sess.commit()

        # deal with pose data, now that trial.video_data is updated
        for treeItem in deferredActionList:
                # pose data associated with video referenced by parent
            videoTreeItem = treeItem.parent()
            assert bool(videoTreeItem)
            thisVideo_data = None
            thisVideo_data_index = -1
            for ix, video_dataItem in enumerate(trial.video_data):
                if video_dataItem.id == videoTreeItem.data(videoHeader.index('id'), Qt.DisplayRole):
                    thisVideo_data = video_dataItem
                    thisVideo_data_index = ix
                    break
            if not thisVideo_data:
                continue
            thisPose_data = None
            thisPose_data_index = -1
            for iy, pose_dataItem in enumerate(thisVideo_data.pose_data):
                if pose_dataItem.pose_id == treeItem.data(poseHeader.index('id'), Qt.DisplayRole):
                    thisPose_data = pose_dataItem
                    thisPose_data_index = iy
                    break
            if bool(thisPose_data) and treeItem.isHidden():
                # delete the pose entry from the DB
                db_sess.delete(thisPose_data)
                continue
            # create a dict from the treeItem for either updating or a new pose DB entry
            poseItemDict = {}
            for key in poseHeader:
                poseItemDict[key] = treeItem.data(poseHeader.index(key), Qt.DisplayRole)
            if bool(thisPose_data):
                # update any changed fields in the existing entry
                thisVideo_data.pose_data[thisPose_data_index].fromDict(poseItemDict, db_sess)
            else:
                # new Pose item
                dbPoseItem = PoseData(poseItemDict, db_sess)
                db_sess.add(dbPoseItem)
                thisVideo_data.pose_data.append(dbPoseItem)

    # Neural Data

    def setNeuralModel(self, model):
        oldModel = self.ui.neuralsTableView.selectionModel()
        self.ui.neuralsTableView.setModel(model)
        font = self.ui.neuralsTableView.horizontalHeader().font()
        font.setBold(True)
        self.ui.neuralsTableView.horizontalHeader().setFont(font)
        self.ui.neuralsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.neuralsTableView.resizeColumnsToContents()
        keys = NeuralData().keys
        self.ui.neuralsTableView.hideColumn(keys.index('id'))   # don't show the ID field, but we need it for reference
        self.ui.neuralsTableView.hideColumn(keys.index('trial_id')) # also don't show the trial_id field
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
                # if updateTrialNum:
                #     selectionModel.selectionChanged.connect(self.populateTrialNum)
                # else:
                #     try:
                #         selectionModel.selectionChanged.disconnect(self.populateTrialNum)
                #     except RuntimeError:
                #         # The above call raises RuntimeError if the signal is not connected,
                #         # which we can safely ignore.
                #         pass

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
            offset_time = float(0.)
        else:
            sample_rate = 30.0
            offset_time = float(0.)
        start_frame = 1
        stop_frame = data.shape[1]

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        item = {
            'id': None,
            'Neural File Path': file_path,
            'Sample Rate': sample_rate,
            'Format': 'CNMFE', # by default
            'Offset Time': offset_time,
            'Start Frame': start_frame,
            'Stop Frame': stop_frame,
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
        font = self.ui.annotationsTableView.horizontalHeader().font()
        font.setBold(True)
        self.ui.annotationsTableView.horizontalHeader().setFont(font)
        self.ui.annotationsTableView.setItemDelegate(CustomComboBoxDelegate(self.bento.annotations_format))

        #self.ui.annotationsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.annotationsTableView.resizeColumnsToContents()
        keys = AnnotationsData().keys
        self.ui.annotationsTableView.hideColumn(keys.index('id'))   # don't show the ID field, but we need it for reference
        self.ui.annotationsTableView.hideColumn(keys.index('trial_id')) # also don't show the internal trial_id field

        
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
                # if updateTrialNum:
                #     selectionModel.selectionChanged.connect(self.populateTrialNum)
                # else:
                #     try:
                #         selectionModel.selectionChanged.disconnect(self.populateTrialNum)
                #     except RuntimeError:
                #         # The above call raises RuntimeError if the signal is not connected,
                #         # which we can safely ignore.
                #         pass

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
        if isinstance(annotations, Annotations) and annotations.sample_rate():
            sample_rate = annotations.sample_rate()
        else:
            sample_rate = None

        if file_path.startswith(baseDir):
            file_path = file_path[len(baseDir):]

        annotator_name = ""
        if self.bento.investigator_id:
            with self.bento.db_sessionMaker() as db_sess:
                investigator = db_sess.query(Investigator).filter(Investigator.id == self.bento.investigator_id).scalar()
                if investigator:
                    annotator_name = investigator.user_name

        if annotations.start_date_time():
            trial_start_time = datetime.timestamp(datetime.fromisoformat(
                                                 self.ui.trialDateTimeEdit.textFromDateTime(self.ui.trialDateTimeEdit.dateTime())))
            offset_time = datetime.timestamp(datetime.fromisoformat(str(annotations.start_date_time()))) -  trial_start_time
        else:
            offset_time = float(0.)

        item = {
            'id': None,
            'Annotations File Path': file_path,
            'Sample Rate': sample_rate,
            'Format': annotations.format(),
            'Offset Time': offset_time,
            'Start Frame': annotations.start_frame(),
            'Stop Frame': annotations.end_frame(),
            'Annotator Name': annotator_name,
            'Method': "manual",
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
            "Bento Annotation files (*.annot);;Boris Annotation files (*.csv);;\
            Simba Annotation files (*.csv);;Caltech Annotation files (*.txt)",
            "Bento Annotation files (*.annot)")
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
            trial.trial_start_time = datetime.timestamp(datetime.fromisoformat(
                                                        self.ui.trialDateTimeEdit.textFromDateTime(self.ui.trialDateTimeEdit.dateTime())))

            self.updateVideoData(trial, db_sess)
            self.updateNeuralData(trial, db_sess)
            self.updateAnnotationsData(trial, db_sess)
            db_sess.commit()
            self.trialsChanged.emit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
