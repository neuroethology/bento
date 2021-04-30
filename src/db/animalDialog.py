# animalDialog.py

from db.schema_sqlalchemy import Animal
from db.animalDialog_ui import Ui_AnimalDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox

class AnimalDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_AnimalDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.db_sess = self.bento.db_sessionMaker()
        self.populateComboBox(False)
        self.ui.animalComboBox.currentIndexChanged.connect(self.showSelected)
        self.animal = Animal()

    def populateComboBox(self, preSelect):
        if preSelect:
            selection = self.ui.animalComboBox.currentText()
        self.ui.animalComboBox.clear()
        self.ui.animalComboBox.addItem("new Animal")
        animals = self.db_sess.query(Animal).distinct().all()
        self.ui.animalComboBox.addItems([elem.nickname for elem in animals])
        self.ui.animalComboBox.setEditable(False)
        if preSelect:
            self.ui.animalComboBox.setCurrentText(selection)

    @Slot(object)
    def update(self, button, preSelect=True):
        print(f"update called with button {button}, preSelect {preSelect}")
        if (not button or self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Apply):
            print("processing update")
            #TODO: Need investigator
            self.animal.animal_services_id = self.ui.asiLineEdit.text()
            self.animal.dob = self.ui.lastNameLineEdit.text()
            self.animal.sex = self.ui.firstNameLineEdit.text()
            self.animal.genotype = self.ui.institutionLineEdit.text()
            self.animal.nickname = self.ui.eMailLineEdit.text()
            self.db_sess.add(self.animal)
            self.db_sess.commit()
            self.populateComboBox(preSelect)
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
