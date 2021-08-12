# trialWindow.py

from db.schema_sqlalchemy import VideoData, Session
from db.trialWindow_ui import Ui_TrialDockWidget
from db.editTrialDialog import EditTrialDialog
from PySide6.QtCore import Signal, Slot, QItemSelection
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QDockWidget, QHeaderView, QMessageBox

from db.schema_sqlalchemy import Trial, AnnotationsData
from widgets.tableModel import TableModel

class TrialDockWidget(QDockWidget):

    openReader = Signal(str)
    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_TrialDockWidget()
        self.ui.setupUi(self)
        self.ui.loadTrialPushButton.clicked.connect(self.loadTrial)
        self.ui.newTrialPushButton.clicked.connect(self.addOrEditTrial)
        self.quitting.connect(self.bento.quit)

        self.current_trial_id = None
        self.populateTrials()
        selectionModel = self.ui.trialTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateVideos)
        selectionModel.selectionChanged.connect(self.populateAnnotations)

    @Slot()
    def populateTrials(self):
        if self.bento.session_id:
            with self.bento.db_sessionMaker() as db_sess:
                session = db_sess.query(Session).where(Session.id == self.bento.session_id).one()
                header = ['id', 'trial num', 'stimulus']
                data_list = [(
                    elem.id,
                    elem.trial_num,
                    elem.stimulus
                    ) for elem in session.trials]
            model = TableModel(self, data_list, header)
            self.ui.trialTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.trialTableView.setModel(model)
            self.ui.trialTableView.resizeColumnsToContents()
            self.ui.trialTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
            self.ui.trialTableView.setSortingEnabled(True)
            self.ui.trialTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.trialTableView.setAutoScroll(False)
            self.ui.trialTableView.sortByColumn(1, Qt.AscendingOrder)

            self.ui.loadNeuralCheckBox.setCheckState(Qt.Checked)

    @Slot(QItemSelection, QItemSelection)
    def populateVideos(self, selected, deselected):
        header = ['id', 'view', 'file path']
        if selected.empty():
            # clear table
            model = TableModel(self, [], header)
        else:
            # populate with videos from the (first) selected trial
            indexes = selected.first().indexes()
            if len(indexes) > 0:
                trial_id = indexes[0].siblingAtColumn(0).data()
                with self.bento.db_sessionMaker() as db_session:
                    trial = db_session.query(Trial).where(Trial.id == trial_id).one()
                    data_list = [(
                        elem.id,
                        elem.camera.position,
                        elem.file_path
                        ) for elem in trial.video_data]
            model = TableModel(self, data_list, header)
        self.ui.videoTableView.setModel(model)
        self.ui.videoTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.videoTableView.resizeColumnsToContents()
        self.ui.videoTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
        self.ui.videoTableView.setSortingEnabled(True)
        self.ui.videoTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.videoTableView.setAutoScroll(False)
        self.ui.videoTableView.sortByColumn(0, Qt.AscendingOrder)
        self.ui.videoTableView.selectRow(0)

    @Slot(QItemSelection, QItemSelection)
    def populateAnnotations(self, selected, deselected):
        header = ['id', 'annotator name', 'method', 'file path']
        if selected.empty():
            # clear table
            model = TableModel(self, [], header)
        else:
            # populate with annotations from the (first) selected trial
            indexes = selected.first().indexes()
            if len(indexes) > 0:
                trial_id = indexes[0].siblingAtColumn(0).data()
                with self.bento.db_sessionMaker() as db_session:
                    trial = db_session.query(Trial).where(Trial.id == trial_id).one()
                    data_list = [(
                        elem.id,
                        elem.annotator_name,
                        elem.method,
                        elem.file_path
                        ) for elem in trial.annotations]
            model = TableModel(self, data_list, header)
        self.ui.annotationTableView.setModel(model)
        self.ui.annotationTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.annotationTableView.resizeColumnsToContents()
        self.ui.annotationTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
        self.ui.annotationTableView.setSortingEnabled(True)
        self.ui.annotationTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.annotationTableView.setAutoScroll(False)
        self.ui.annotationTableView.selectRow(0)

    @Slot()
    def loadTrial(self):
        trialSelectionModel = self.ui.trialTableView.selectionModel()
        if trialSelectionModel and trialSelectionModel.hasSelection():
            if len(trialSelectionModel.selectedRows()) > 1:
                QMessageBox.about(self, "Error", "More than one Trial is selected!")
                return
            trial_id = trialSelectionModel.selectedRows()[0].siblingAtColumn(0).data()
            print(f"Load trial id {trial_id}")
            videos = []
            videoSelectionModel = self.ui.videoTableView.selectionModel()
            annotation = None
            if videoSelectionModel and videoSelectionModel.hasSelection():
                with self.bento.db_sessionMaker() as db_session:
                    self.bento.trial_id = db_session.query(Trial).where(Trial.id == trial_id).one().id
                    for selection in self.ui.videoTableView.selectionModel().selectedRows():
                        videos.append(db_session.query(VideoData).where(VideoData.id == selection.siblingAtColumn(0).data()).one())
                    annotation = db_session.query(AnnotationsData).where(
                        AnnotationsData.id == self.ui.annotationTableView.currentIndex().siblingAtColumn(0).data()
                        ).scalar()
            loadPose = self.ui.loadPoseCheckBox.isChecked()
            loadNeural = self.ui.loadNeuralCheckBox.isChecked()
            loadAudio = self.ui.loadAudioCheckBox.isChecked()
            if self.bento.loadTrial(videos, annotation, loadPose, loadNeural, loadAudio):
                self.bento.selectTrialWindow.close()
        else:
            print("No trial selected!")

    @Slot()
    def addOrEditTrial(self):
        """
        Open the editTrial Dialog
        """
        selectionModel = self.ui.trialTableView.selectionModel()
        if selectionModel.hasSelection():
            if len(selectionModel.selectedRows()) > 1:
                QMessageBox.about(self, "Error", "More than one Trial is selected!")
                return
            self.current_trial_id = selectionModel.selectedRows()[0].siblingAtColumn(0).data()
        else:
            self.current_trial_id = None

        self.add_or_edit_trial(self.current_trial_id)

    @Slot()
    def add_or_edit_trial(self, trial_id=None):
        """
        Add a new experiment trial to the database
        associated with the selected session
        """
        dialog = EditTrialDialog(self.bento, self.bento.session_id, trial_id)
        dialog.trialsChanged.connect(self.populateTrials)
        dialog.exec_()

