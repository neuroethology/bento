# trialWindow.py

from db.trialWindow_ui import Ui_TrialDockWidget
from db.editTrialDialog import EditTrialDialog
from db.editSessionDialog import EditSessionDialog
from qtpy.QtCore import Signal, Slot, QItemSelection
from qtpy.QtGui import Qt
from qtpy.QtWidgets import QAbstractItemView, QDockWidget, QHeaderView, QMessageBox

from db.schema_sqlalchemy import VideoData, Investigator, Session, Animal, Trial, AnnotationsData
from widgets.tableModel import TableModel
from datetime import date
from dateutil.relativedelta import relativedelta

class TrialDockWidget(QDockWidget):

    openReader = Signal(str)
    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_TrialDockWidget()
        self.ui.setupUi(self)
        self.ui.addOrEditSessionPushButton.clicked.connect(self.addOrEditSession)
        self.ui.addOrEditTrialPushButton.clicked.connect(self.addOrEditTrial)
        self.ui.investigatorComboBox.currentTextChanged.connect(self.populateSessions)
        self.ui.useInvestigatorCheckBox.clicked.connect(self.populateSessions)
        self.ui.useDateRangeCheckBox.clicked.connect(self.populateSessions)
        self.ui.startDateEdit.dateChanged.connect(self.populateSessions)
        self.ui.endDateEdit.dateChanged.connect(self.populateSessions)
        self.quitting.connect(self.bento.quit)

        with self.bento.db_sessionMaker() as db_session:
            query = db_session.query(Investigator).distinct()
            investigators = query.all()
            self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
            defaultInvestigator = query.filter(Investigator.id == self.bento.investigator_id).scalar()
        if defaultInvestigator:
            self.ui.investigatorComboBox.setCurrentText(defaultInvestigator.user_name)
        today = date.today()
        self.ui.startDateEdit.setDate(today + relativedelta(months=-3))
        self.ui.endDateEdit.setDate(today)
        self.bento.session_id = None

        self.populateSessions()

        self.current_trial_id = None

    @Slot()
    def populateSessions(self):
        investigator = self.ui.investigatorComboBox.currentText()
        with self.bento.db_sessionMaker() as db_sess:
            query = db_sess.query(Session, Investigator, Animal).join(Investigator, Investigator.id == Session.investigator_id)
            query = query.join(Animal, Animal.id == Session.animal_id)
            if self.ui.useInvestigatorCheckBox.isChecked() and investigator:
                query = query.filter(Investigator.user_name == investigator)
            if self.ui.useDateRangeCheckBox.isChecked():
                startDate = self.ui.startDateEdit.date().toPython()
                endDate = self.ui.endDateEdit.date().toPython()
                query = query.filter(Session.experiment_date >= startDate,
                    Session.experiment_date <= endDate)
            results = query.order_by(Session.experiment_date.desc()).all()
            header = ['id', 'investigator', 'date', 'animal', '# of trials', 'base directory']
            data_list = [(
                elem.Session.id,
                elem.Investigator.user_name,
                elem.Session.experiment_date.isoformat(),
                elem.Animal.nickname,
                len(elem.Session.trials),
                elem.Session.base_directory
                ) for elem in results]
        model = TableModel(self, data_list, header)
        self.ui.sessionTableView.setModel(model)
        self.ui.sessionTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.sessionTableView.resizeColumnsToContents()
        self.ui.sessionTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
        self.ui.sessionTableView.setSortingEnabled(True)
        self.ui.sessionTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.sessionTableView.setAutoScroll(False)

        self.bento.session_id = None

        selectionModel = self.ui.sessionTableView.selectionModel()
        if selectionModel:
            selectionModel.selectionChanged.connect(self.selectSession)

    @Slot()
    def selectSession(self):
        current_session_row = self.ui.sessionTableView.currentIndex().row()
        if current_session_row >= 0:
            self.bento.session_id = self.ui.sessionTableView.currentIndex().siblingAtColumn(0).data()
            self.populateTrials()
            selectionModel = self.ui.trialTableView.selectionModel()
            selectionModel.selectionChanged.connect(self.populateVideos)
            selectionModel.selectionChanged.connect(self.populateAnnotations)

    @Slot()
    def addOrEditSession(self):
        """
        Open the newSession Dialog
        """
        if len(self.ui.sessionTableView.selectedIndexes()) == 0:
            self.bento.session_id = None
        investigator = self.ui.investigatorComboBox.currentText()
        investigator_id = self.bento.investigator_id
        if self.ui.useInvestigatorCheckBox.isChecked() and investigator:
            with self.bento.db_sessionMaker() as db_sess:
                result = db_sess.query(Investigator).filter(Investigator.user_name == investigator).one_or_none()
                if result:
                    investigator_id = result.id
                else:
                    print("Query failed, so didn't update id")
        dialog = EditSessionDialog(self.bento, investigator_id, self.bento.session_id)
        dialog.sessionChanged.connect(self.populateSessions)
        dialog.exec()

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
    def update(self):
        self.loadTrial()
        super().update()

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
                self.bento.trialWindow.close()
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

        selectionModel = self.ui.trialTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateVideos)
        selectionModel.selectionChanged.connect(self.populateAnnotations)

    @Slot()
    def add_or_edit_trial(self, trial_id=None):
        """
        Add a new experiment trial to the database
        associated with the selected session
        """
        dialog = EditTrialDialog(self.bento, self.bento.session_id, trial_id)
        dialog.trialsChanged.connect(self.populateTrials)
        dialog.trialsChanged.connect(self.populateSessions)
        dialog.exec_()

