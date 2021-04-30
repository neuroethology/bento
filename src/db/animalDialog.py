# animalDialog.py

from db.schema_sqlalchemy import Animal, Investigator, SexEnum, Surgery
from db.animalDialog_ui import Ui_AnimalDialog
from PySide2.QtCore import Qt, QDate, Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QAbstractItemView, QHeaderView

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

        self.db_sess = self.bento.db_sessionMaker()
        username = self.bento.config.username()
        query = self.db_sess.query(Investigator).distinct()
        investigators = query.all()
        self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
        self.ui.investigatorComboBox.setEditable(False)
        self.ui.investigatorComboBox.setCurrentText(username) # may not exist
        investigator_name = self.ui.investigatorComboBox.currentText()
        investigator = query.filter(Investigator.user_name == investigator_name).scalar()
        if investigator:
            self.investigator_id = investigator.id
            self.populateAnimalTable(investigator.id)
        else:
            self.investigator_id = None
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)
        self.animal = Animal()

    def populateAnimalTable(self, investigator_id):
        results = self.db_sess.query(Animal).filter(Animal.investigator_id == investigator_id).all()
        header = ['id', 'Nickname', 'Animal Services ID', 'Date of Birth', 'Sex', 'Genotype']
        data_list = [(
            elem.id,
            elem.nickname,
            elem.animal_services_id,
            elem.dob.isoformat(),
            elem.sex.value,
            elem.genotype
            ) for elem in results]
        data_list.insert(0, (0, "New Animal", None, "", "", ""))
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
        investigator= self.db_sess.query(Investigator).filter(Investigator.user_name == username).distinct().one()
        self.investigator_id = investigator.id
        self.populateAnimalTable(self.investigator_id)

    def clearFields(self):
        self.ui.nicknameLineEdit.clear()
        self.ui.asiLineEdit.clear()
        self.ui.dobDateEdit.clearMinimumDate()
        self.ui.unknownRadioButton.click()
        self.ui.genotypeLineEdit.clear()
        oldModel = self.ui.surgeryTableView.selectionModel()
        self.ui.surgeryTableView.setModel(None)
        if oldModel:
            oldModel.deleteLater()
        
    def populateFields(self):
        animal_id = None
        current_animal_row = self.ui.animalTableView.currentIndex().row()
        if current_animal_row >= 0:
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
        if animal_id:
            self.animal = self.db_sess.query(Animal).filter(Animal.id == animal_id).scalar()
            if not self.animal:
                print("Invalid animal ID")
                return
            self.ui.nicknameLineEdit.setText(self.animal.nickname)
            self.ui.asiLineEdit.setText(str(self.animal.animal_services_id))
            self.ui.dobDateEdit.setDate(self.animal.dob)
            sex = self.animal.sex
            if sex == SexEnum.M:
                self.ui.maleRadioButton.click()
            elif sex == SexEnum.F:
                self.ui.femaleRadioButton.click()
            else:
                self.ui.unknownRadioButton.click()
            self.ui.genotypeLineEdit.setText(self.animal.genotype)
            self.populateSurgeryLog()
        else:
            self.animal = Animal()
            self.clearFields()

    def populateSurgeryLog(self):
        if self.animal:
            results = self.db_sess.query(Surgery).filter(Surgery.animal_id == self.animal.id).all()
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


    @Slot(object)
    def update(self, button):
        print(f"update called with button {button}")
        if (not button or self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Apply):
            print("processing update")
            if not self.investigator_id:
                print("No valid investigator.  Doing nothing.")
                return
            self.animal.investigator_id = self.investigator_id
            self.animal.animal_services_id = int(self.ui.asiLineEdit.text())
            self.animal.dob = self.ui.dobDateEdit.date().toPython()
            if self.ui.maleRadioButton.isChecked():
                self.animal.sex = SexEnum.M
            elif self.ui.femaleRadioButton.isChecked():
                self.animal.sex = SexEnum.F
            else:
                self.animal.sex = SexEnum.U
            self.animal.genotype = self.ui.genotypeLineEdit.text()
            self.animal.nickname = self.ui.eMailLineEdit.text()
            self.db_sess.add(self.animal)
            self.db_sess.commit()
            self.populateAnimalTable(self.investigator_id)

        elif self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Discard:
            self.reject()
        else:
            print("returning without any action")

    @Slot()
    def accept(self):
        self.update(None, False)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()

    @Slot()
    def showSelected(self):
        if self.ui.investigatorComboBox.currentIndex() == 0:
            self.investigator = Investigator()
        else:
            investigator_username = self.ui.investigatorComboBox.currentText()
            query = self.db_sess.query(Investigator)
            result = query.filter(Investigator.user_name == investigator_username).all()
            if len(result) > 0:
                self.investigator = result[0]
                self.ui.usernameLineEdit.setText(self.investigator.user_name)
                self.ui.lastNameLineEdit.setText(self.investigator.last_name)
                self.ui.firstNameLineEdit.setText(self.investigator.first_name)
                self.ui.institutionLineEdit.setText(self.investigator.institution)
                self.ui.eMailLineEdit.setText(self.investigator.e_mail)
                return
        self.ui.usernameLineEdit.clear()
        self.ui.lastNameLineEdit.clear()
        self.ui.firstNameLineEdit.clear()
        self.ui.institutionLineEdit.clear()
        self.ui.eMailLineEdit.clear()
