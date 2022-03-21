# editSessionDialog.py

from db.schema_sqlalchemy import Session, Animal
from sqlalchemy import func
from db.editSessionDialog_ui import Ui_EditSessionDialog
from qtpy.QtCore import Signal, Slot, QItemSelectionModel
from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import QDialog, QFileDialog, QAbstractItemView, QHeaderView
from models.tableModel import TableModel
from os.path import expanduser
from datetime import date

class EditSessionDialog(QDialog):

    quitting = Signal()
    sessionChanged = Signal()

    def __init__(self, bento, investigator_id, session_id=None):
        super().__init__()
        self.bento = bento
        self.session_id = session_id
        self.investigator_id = investigator_id
        selectedAnimal = None
        if session_id:
            with self.bento.db_sessionMaker() as db_sess:
                session = db_sess.query(Session).filter(Session.id == session_id).scalar()
                if session:
                    self.investigator_id = session.investigator_id
                    selectedAnimal = session.animal_id
        self.ui = Ui_EditSessionDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)
        self.ui.selectBaseDirPushButton.clicked.connect(self.selectBaseDir)
        self.ui.sessionNumLineEdit.setValidator(QIntValidator())

        self.populateAnimalTableView(not bool(session_id), selectedAnimal)
        if session_id:
            with self.bento.db_sessionMaker() as db_sess:
                session = db_sess.query(Session).filter(Session.id == session_id).scalar()
                if session:
                    self.updateUIFromCurrentSession(session)
                    return
        self.ui.dateEdit.setDate(date.today())

    def populateAnimalTableView(self, updateSessionNum, selectedAnimal=None):
        header = ['ID', 'Nickname', 'Animal Services ID', 'Date of Birth', 'Sex', 'Genotype']
        selectedRow = None
        with self.bento.db_sessionMaker() as db_sess:
            results = db_sess.query(Animal).filter(Animal.investigator_id == self.investigator_id).all()
            data_list = []
            for ix, elem in enumerate(results):
                data_list.append((
                    elem.id,
                    elem.nickname,
                    str(elem.animal_services_id),
                    elem.dob.isoformat(),
                    elem.sex.value,
                    elem.genotype
                    ))
                if selectedAnimal == elem.id:
                    selectedRow = ix
        oldModel = self.ui.animalTableView.selectionModel()
        model = TableModel(self, data_list, header)
        self.ui.animalTableView.setModel(model)
        self.ui.animalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.animalTableView.resizeColumnsToContents()
        self.ui.animalTableView.hideColumn(0)   # don't show the animal's ID field, but we need it for Load
        self.ui.animalTableView.setSortingEnabled(False)
        self.ui.animalTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.animalTableView.setAutoScroll(False)
        if selectedRow != None:
            self.ui.animalTableView.setCurrentIndex(model.index(selectedRow, 0))
        if oldModel:
            oldModel.deleteLater()

        selectionModel = self.ui.animalTableView.selectionModel()
        if updateSessionNum:
            selectionModel.selectionChanged.connect(self.populateSessionNum)
        else:
            try:
                selectionModel.selectionChanged.disconnect(self.populateSessionNum)
            except RuntimeError:
                # The above call raises RuntimeError if the signal is not connected,
                # which we can safely ignore.
                pass

    def updateUIFromCurrentSession(self, session):
        model = self.ui.animalTableView.model()
        animal_id = session.animal_id
        for row in range(model.rowCount(self.ui.animalTableView.rootIndex())):
            index = model.index(row, 0, self.ui.animalTableView.rootIndex())
            if index.data() == animal_id:
                self.ui.animalTableView.setCurrentIndex(index)
                break
        self.ui.dateEdit.setDate(session.experiment_date)
        self.ui.baseDirLineEdit.setText(session.base_directory)
        self.ui.sessionNumLineEdit.setText(str(session.session_num))

    @Slot()
    def populateSessionNum(self):
        current_animal_row = self.ui.animalTableView.currentIndex().row()
        maxSession = None
        if current_animal_row >= 0:
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
            with self.bento.db_sessionMaker() as db_sess:
                maxSession = db_sess.query(func.max(Session.session_num)).filter(Session.animal_id == animal_id).scalar()
        self.ui.sessionNumLineEdit.setText(str(maxSession + 1 if isinstance(maxSession, int) else 1))

    @Slot()
    def selectBaseDir(self):
        startingDir = self.ui.baseDirLineEdit.text()
        if not startingDir:
            startingDir = expanduser("~")
        baseDir = QFileDialog.getExistingDirectory(self, caption="Select Session Base Directory", dir=startingDir)
        if baseDir:
            self.ui.baseDirLineEdit.setText(baseDir)

    @Slot()
    def accept(self):
        current_row = self.ui.animalTableView.currentIndex().row()
        if current_row >= 0:
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
        with self.bento.db_sessionMaker().begin() as transaction:
            if self.session_id:
                session = transaction.session.query(Session).filter(Session.id == self.session_id).scalar()
                if not session:
                    raise RuntimeWarning(f"Session id {self.session_id} not found!")
            else:
                session = Session()
                transaction.session.add(session)
            session.animal_id = animal_id
            session.investigator_id = self.investigator_id
            session.base_directory = self.ui.baseDirLineEdit.text()
            session.experiment_date = self.ui.dateEdit.date().toPython()
            session.session_num = int(self.ui.sessionNumLineEdit.text())
        self.sessionChanged.emit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
