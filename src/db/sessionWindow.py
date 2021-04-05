# sessionWindow.py

from db.sessionWindow_ui import Ui_SessionDockWidget
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QAbstractItemView, QDockWidget
from db.schema_sqlalchemy import *
from widgets.tableModel import TableModel

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
        self.quitting.connect(self.bento.quit)

        self.DB_Session = new_session()
        db_session = self.DB_Session()
        investigators = db_session.query(Investigator).distinct().all()
        self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])

    @Slot()
    def search(self):
        db_sess = self.DB_Session()
        query = db_sess.query(Session, Investigator, Animal).join(Investigator, Investigator.id == Session.investigator_id)
        query = query.join(Animal, Animal.id == Session.animal_id)
        investigator = self.ui.investigatorComboBox.currentText()
        if self.ui.useInvestigatorCheckBox.isChecked() and investigator:
            query = query.filter(Investigator.user_name == investigator)
        if self.ui.useDateRangeCheckBox.isChecked():
            startDate = self.ui.startCalendarWidget.selectedDate().toPython()
            endDate = self.ui.endCalendarWidget.selectedDate().toPython()
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
        self.ui.sessionsTableView.resizeColumnsToContents()
        self.ui.sessionsTableView.hideColumn(0)   # don't show the trial's ID field, but we need it for Load
        self.ui.sessionsTableView.setSortingEnabled(True)
        self.ui.sessionsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.sessionsTableView.setAutoScroll(False)

    @Slot()
    def loadSession(self):
        current_row = self.ui.sessionsTableView.currentIndex().row()
        if current_row >= 0:
            session_id = self.ui.sessionsTableView.currentIndex().siblingAtColumn(0).data()
            print(f"Load session id {session_id}")
            db_sess = self.DB_Session()
            self.bento.session = db_sess.query(Session).filter(Session.id == session_id).one()
            self.bento.selectTrial()
            self.close()
        else:
            print("Nothing selected!")

