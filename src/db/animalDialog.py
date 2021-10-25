# animalDialog.py

from db.schema_sqlalchemy import Animal, Investigator, SexEnum, Surgery
from db.animalDialog_ui import Ui_AnimalDialog
from db.surgeryDialog import SurgeryDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import (QDialog, QDialogButtonBox, QAbstractItemView, QHeaderView,
    QMessageBox)

from widgets.tableModel import TableModel
import datetime

class AnimalDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_AnimalDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)
        self.ui.asiLineEdit.setValidator(QIntValidator())

        with self.bento.db_sessionMaker() as db_sess:
            username = self.bento.config.username()
            query = db_sess.query(Investigator).distinct()
            investigators = query.all()
            self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
            self.ui.investigatorComboBox.setEditable(False)
            self.ui.investigatorComboBox.setCurrentText(username) # may not exist
        self.investigatorChanged()
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)
        self.animal_id = None
        self.ui.addSurgeryPushButton.clicked.connect(self.addSurgeryAction)
        applyButton = self.ui.buttonBox.button(QDialogButtonBox.Apply)
        applyButton.clicked.connect(self.update)

    def populateAnimalTable(self, investigator_id, db_sess):
        results = db_sess.query(Animal).filter(Animal.investigator_id == investigator_id).all()
        header = ['id', 'Animal Services ID', 'Nickname', 'Date of Birth', 'Sex', 'Genotype']
        data_list = [(
            elem.id,
            elem.animal_services_id,
            elem.nickname,
            elem.dob.isoformat(),
            elem.sex.value,
            elem.genotype
            ) for elem in results]
        data_list.insert(0, (None, None, "New Animal", "", "", ""))
        oldModel = self.ui.animalTableView.selectionModel()
        model = TableModel(self, data_list, header)
        self.ui.animalTableView.setModel(model)
        self.ui.animalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.animalTableView.resizeColumnsToContents()
        self.ui.animalTableView.hideColumn(0)   # don't show the animal's ID field, but we need it for Load
        self.ui.animalTableView.setSortingEnabled(False)
        self.ui.animalTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.animalTableView.setAutoScroll(False)
        selectionModel = self.ui.animalTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateFields)
        if oldModel:
            oldModel.deleteLater()

    @Slot()
    def investigatorChanged(self):
        username = self.ui.investigatorComboBox.currentText()
        with self.bento.db_sessionMaker() as db_sess:
            investigators = db_sess.query(Investigator).filter(Investigator.user_name == username).distinct().all()
            if investigators:
                if len(investigators) > 1:
                    QMessageBox.warning(
                        self,
                        "Duplicate Investigators",
                        "Multiple investigators have the same selected investigator username.\n"
                        "I'll use the first one I found, but you should clean that up!"
                    )
                self.investigator_id = investigators[0].id
                self.populateAnimalTable(self.investigator_id, db_sess)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Investigator",
                    "The selected investigator doesn't exist in the database."
                    )
        self.ui.animalTableView.selectRow(0)

    def clearFields(self):
        self.ui.nicknameLineEdit.clear()
        self.ui.asiLineEdit.clear()
        self.ui.dobDateEdit.setDate(datetime.date.today())
        self.ui.unknownRadioButton.click()
        self.ui.genotypeLineEdit.clear()
        oldModel = self.ui.surgeryTableView.selectionModel()
        self.ui.surgeryTableView.setModel(None)
        if oldModel:
            oldModel.deleteLater()

    def populateFields(self):
        animal_id = None
        current_animal_row = self.ui.animalTableView.currentIndex().row()
        if current_animal_row > 0:  # not "New Animal" row
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
        if animal_id:
            with self.bento.db_sessionMaker() as db_sess:
                animal = db_sess.query(Animal).filter(Animal.id == animal_id).scalar()
                if not animal:
                    print("Invalid animal ID")
                    return
                self.ui.nicknameLineEdit.setText(animal.nickname)
                self.ui.asiLineEdit.setText(str(animal.animal_services_id))
                self.ui.dobDateEdit.setDate(animal.dob)
                sex = animal.sex
                if sex == SexEnum.M:
                    self.ui.maleRadioButton.click()
                elif sex == SexEnum.F:
                    self.ui.femaleRadioButton.click()
                else:
                    self.ui.unknownRadioButton.click()
                self.ui.genotypeLineEdit.setText(animal.genotype)
                self.populateSurgeryLog(animal_id, db_sess)
            self.animal_id = animal_id
        else:
            self.animal_id = None
            self.clearFields()

    def populateSurgeryLog(self, animal_id, db_sess):
        results = db_sess.query(Surgery).filter(Surgery.animal_id == animal_id).all()
        header = ['Date', 'Implant Side', 'Injection Side', 'Procedure', 'Anesthesia', 'Follow-up Care']
        data_list = [(
            elem.date.isoformat(),
            elem.implant_side.value,
            elem.injection_side.value,
            elem.procedure,
            elem.anesthesia,
            elem.follow_up_care
            ) for elem in results]
        oldModel = self.ui.surgeryTableView.selectionModel()
        model = TableModel(self, data_list, header)
        self.ui.surgeryTableView.setModel(model)
        self.ui.surgeryTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.surgeryTableView.resizeColumnsToContents()
        self.ui.surgeryTableView.setSortingEnabled(False)
        self.ui.surgeryTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.surgeryTableView.setAutoScroll(False)
        selectionModel = self.ui.surgeryTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateFields)
        if oldModel:
            oldModel.deleteLater()

    @Slot()
    def addSurgeryAction(self):
        surgeryDialog = SurgeryDialog(self.bento, self.investigator_id, self.animal_id)
        surgeryDialog.exec()
        with self.bento.db_sessionMaker() as db_sess:
            self.populateSurgeryLog(self.animal_id, db_sess)

    @Slot()
    def update(self) -> bool:   # returns successful update
        if not self.investigator_id:
            QMessageBox.warning(self, "Warning", "No valid investigator.  Please select one.")
            return False
        with self.bento.db_sessionMaker() as db_sess:
            need_commit = False
            need_to_add = False
            if self.animal_id:
                animals = db_sess.query(Animal).filter(Animal.id == self.animal_id).all()
                if not animals:
                    QMessageBox.critical(self, "Internal Error", "No animal in database matching selection.")
                    return False
                animal = animals[0]
            elif self.ui.asiLineEdit.text():
                animal = Animal()
                need_commit = True
                need_to_add = True
            else:   # Maybe nothing selected and just exiting, or maybe incomplete new animal
                if ( not self.ui.nicknameLineEdit.text() and
                    not self.ui.genotypeLineEdit.text() and
                    not self.ui.surgeryTableView.model()
                    ):
                    return True
                else:
                    QMessageBox.warning(self, "Warning", "An Animal Services ID is required.  Please supply one.")
                    return False

            if animal.investigator_id != self.investigator_id:
                animal.investigator_id = self.investigator_id
                need_commit = True
            if animal.nickname != self.ui.nicknameLineEdit.text():
                animal.nickname = self.ui.nicknameLineEdit.text()
                need_commit = True
            if animal.animal_services_id != int(self.ui.asiLineEdit.text()):
                animal.animal_services_id = int(self.ui.asiLineEdit.text())
                need_commit = True
            if animal.dob != self.ui.dobDateEdit.date().toPython():
                animal.dob = self.ui.dobDateEdit.date().toPython()
                need_commit = True
            if not (
                animal.sex == SexEnum.M and self.ui.maleRadioButton.isChecked() or
                animal.sex == SexEnum.F and self.ui.femaleRadioButton.isChecked() or
                animal.sex == SexEnum.U and self.ui.unknownRadioButton.isChecked()
                ):
                if self.ui.maleRadioButton.isChecked():
                    animal.sex = SexEnum.M
                elif self.ui.femaleRadioButton.isChecked():
                    animal.sex = SexEnum.F
                else:
                    animal.sex = SexEnum.U
                need_commit = True
            if animal.genotype != self.ui.genotypeLineEdit.text():
                animal.genotype = self.ui.genotypeLineEdit.text()
                need_commit = True
            if need_to_add:
                db_sess.add(animal)
            if need_commit:
                db_sess.commit()
                db_sess.flush()
            self.populateAnimalTable(self.investigator_id, db_sess)
            self.animal_id = None
            self.clearFields()
            return True

    @Slot()
    def accept(self):
        if self.update():
            super().accept()

    @Slot()
    def reject(self):
        super().reject()
