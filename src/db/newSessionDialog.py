# newSessionDialog.py

from db.schema_sqlalchemy import Session, Animal
from db.newSessionDialog_ui import Ui_NewSessionDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QAbstractItemView, QHeaderView
from widgets.tableModel import TableModel

class NewSessionDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento, investigator_id):
        super().__init__()
        self.bento = bento
        self.investigator_id = investigator_id
        self.ui = Ui_NewSessionDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.db_sess = self.bento.db_sessionMaker()
        self.populateAnimalTableView()
        self.session = Session()

    def populateAnimalTableView(self):
        results = self.db_sess.query(Animal).filter(Animal.investigator_id == self.investigator_id).all()
        header = ['ID', 'Nickname', 'Animal Services ID', 'Date of Birth', 'Sex', 'Genotype']
        data_list = [(
            elem.id,
            elem.nickname,
            str(elem.animal_services_id),
            elem.dob.isoformat(),
            elem.sex.value,
            elem.genotype
            ) for elem in results]
        oldModel = self.ui.animalTableView.selectionModel()
        model = TableModel(self, data_list, header)
        self.ui.animalTableView.setModel(model)
        self.ui.animalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.animalTableView.resizeColumnsToContents()
        self.ui.animalTableView.hideColumn(0)   # don't show the animal's ID field, but we need it for Load
        self.ui.animalTableView.setSortingEnabled(False)
        self.ui.animalTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.animalTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    @Slot()
    def accept(self):
        current_row = self.ui.animalTableView.currentIndex().row()
        if current_row >= 0:
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
        self.session.animal_id = animal_id
        self.session.investigator_id = self.investigator_id
        self.session.base_directory = self.ui.baseDirLineEdit.text()
        self.session.experiment_date = self.ui.dateEdit.date().toPython()
        self.session.session_num = int(self.ui.sessionNumLineEdit.text())
        self.db_sess.add(self.session)
        self.db_sess.commit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
