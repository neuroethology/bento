# sessionWindow.py

from db.sessionWindow_ui import Ui_SessionDockWidget
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QAbstractItemView, QDockWidget, QHeaderView
from db.schema_sqlalchemy import Investigator, Animal, Session
from widgets.tableModel import TableModel
from datetime import date
from dateutil.relativedelta import relativedelta

class SessionDockWidget(QDockWidget):

    openReader = Signal(str)
    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_SessionDockWidget()
        self.ui.setupUi(self)
        self.ui.searchPushButton.clicked.connect(self.search)
        self.ui.loadPushButton.clicked.connect(self.loadSession)
        self.ui.addOrEditSessionPushButton.clicked.connect(self.addOrEditSession)
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
        self.current_session_id = None

        self.search()


    @Slot()
    def search(self):
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
        self.ui.sessionsTableView.setModel(model)
        self.ui.sessionsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.sessionsTableView.resizeColumnsToContents()
        self.ui.sessionsTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
        self.ui.sessionsTableView.setSortingEnabled(True)
        self.ui.sessionsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.sessionsTableView.setAutoScroll(False)

        self.current_session_id = None

        selectionModel = self.ui.sessionsTableView.selectionModel()
        if selectionModel:
            selectionModel.selectionChanged.connect(self.selectSession)

    @Slot()
    def selectSession(self):
        current_session_row = self.ui.sessionsTableView.currentIndex().row()
        if current_session_row >= 0:
            self.current_session_id = self.ui.sessionsTableView.currentIndex().siblingAtColumn(0).data()


    @Slot()
    def loadSession(self):
        if self.current_session_id:
            print(f"Load session id {self.current_session_id}")
            self.bento.session_id = self.current_session_id
            self.bento.selectTrial()
            self.close()
        else:
            print("Nothing selected!")

    @Slot()
    def addOrEditSession(self):
        """
        Open the newSession Dialog
        """
        if len(self.ui.sessionsTableView.selectedIndexes()) == 0:
            self.current_session_id = None
        self.bento.add_or_edit_session(self.current_session_id)
