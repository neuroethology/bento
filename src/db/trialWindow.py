# trialWindow.py

from db.schema_sqlalchemy import VideoData
from db.trialWindow_ui import Ui_TrialDockWidget
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QAbstractItemView, QDockWidget, QHeaderView

from db.schema_sqlalchemy import Trial, Annotations
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
        self.quitting.connect(self.bento.quit)

        if bento.session:
            header = ['id', 'trial num', 'stimulus']
            data_list = [(
                elem.id,
                elem.trial_num,
                elem.stimulus
                ) for elem in bento.session.trials]
            model = TableModel(self, data_list, header)
            self.ui.trialTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.trialTableView.setModel(model)
            self.ui.trialTableView.resizeColumnsToContents()
            self.ui.trialTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
            self.ui.trialTableView.setSortingEnabled(True)
            self.ui.trialTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.trialTableView.setAutoScroll(False)
            self.ui.trialTableView.sortByColumn(1)

            self.ui.loadNeuralCheckBox.setCheckState(Qt.Checked)

            selectionModel = self.ui.trialTableView.selectionModel()
            selectionModel.selectionChanged.connect(self.populateVideos)
            selectionModel.selectionChanged.connect(self.populateAnnotations)

    @Slot()
    def populateVideos(self):
        current_trial_row = self.ui.trialTableView.currentIndex().row()
        if current_trial_row >= 0:
            trial_id = self.ui.trialTableView.currentIndex().siblingAtColumn(0).data()
            header = ['id', 'view', 'file path']
            db_session = self.bento.db_sessionMaker()
            trial = db_session.query(Trial).filter(Trial.id == trial_id).one()
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
            self.ui.videoTableView.sortByColumn(0)
            self.ui.videoTableView.selectRow(0)

    @Slot()
    def populateAnnotations(self):
        current_trial_row = self.ui.trialTableView.currentIndex().row()
        if current_trial_row >= 0:
            trial_id = self.ui.trialTableView.currentIndex().siblingAtColumn(0).data()
            header = ['id', 'annotator name', 'method', 'file path']
            db_session = self.bento.db_sessionMaker()
            trial = db_session.query(Trial).filter(Trial.id == trial_id).one()
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
        current_trial_row = self.ui.trialTableView.currentIndex().row()
        if current_trial_row >= 0:
            trial_id = self.ui.trialTableView.currentIndex().siblingAtColumn(0).data()
            print(f"Load trial id {trial_id}")
            db_sess = self.bento.db_sessionMaker()
            self.bento.trial = db_sess.query(Trial).filter(Trial.id == trial_id).one()
            videos = []
            for selection in self.ui.videoTableView.selectionModel().selectedRows():
                videos.append(db_sess.query(VideoData).filter(VideoData.id == selection.siblingAtColumn(0).data()).one())
            annotation = db_sess.query(Annotations).filter(
                Annotations.id == self.ui.annotationTableView.currentIndex().siblingAtColumn(0).data()
                ).one()
            loadPose = self.ui.loadPoseCheckBox.isChecked()
            loadNeural = self.ui.loadNeuralCheckBox.isChecked()
            loadAudio = self.ui.loadAudioCheckBox.isChecked()
            if self.bento.loadTrial(videos, annotation, loadPose, loadNeural, loadAudio):
                self.bento.selectTrialWindow.close()
        else:
            print("Nothing selected!")

