# investigatorDialog.py

from db.investigatorDialog_ui import Ui_InvestigatorDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox

from db.schema_sqlalchemy import Investigator

class InvestigatorDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_InvestigatorDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.investigator_id = None
        self.populateComboBox(False)
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.showSelected)

    def populateComboBox(self, preSelect):
        if preSelect:
            selection = self.ui.investigatorComboBox.currentText()
        self.ui.investigatorComboBox.clear()
        self.ui.investigatorComboBox.addItem("new Investigator")
        with self.bento.db_sessionMaker() as db_sess:
            try:
                investigators = db_sess.query(Investigator).distinct().all()
                self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
            except Exception as e:
                pass # no database yet?

        self.ui.investigatorComboBox.setEditable(False)
        if preSelect:
            self.ui.investigatorComboBox.setCurrentText(selection)

    @Slot(object)
    def update(self, button, preSelect=True):
        buttonRole = self.ui.buttonBox.buttonRole(button)
        if (buttonRole == QDialogButtonBox.AcceptRole or
            buttonRole == QDialogButtonBox.ApplyRole):
            with self.bento.db_sessionMaker() as db_sess:
                investigator = Investigator()
                investigator.user_name = self.ui.usernameLineEdit.text()
                investigator.last_name = self.ui.lastNameLineEdit.text()
                investigator.first_name = self.ui.firstNameLineEdit.text()
                investigator.institution = self.ui.institutionLineEdit.text()
                investigator.e_mail = self.ui.eMailLineEdit.text()
                db_sess.add(investigator)
                db_sess.commit()
            self.populateComboBox(preSelect)
        elif buttonRole == QDialogButtonBox.DestructiveRole:
            self.reject()
        else:
            print("returning without any action")

    @Slot()
    def accept(self):
        self.update(self.ui.buttonBox.button(QDialogButtonBox.Ok), False)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()

    @Slot()
    def showSelected(self):
        if self.ui.investigatorComboBox.currentIndex() == 0:
            self.investigator_id = None
        else:
            investigator_username = self.ui.investigatorComboBox.currentText()
            with self.bento.db_sessionMaker() as db_sess:
                query = db_sess.query(Investigator)
                result = query.filter(Investigator.user_name == investigator_username).all()
                if len(result) > 0:
                    investigator = result[0]
                    self.investigator_id = investigator.id
                    self.ui.usernameLineEdit.setText(investigator.user_name)
                    self.ui.lastNameLineEdit.setText(investigator.last_name)
                    self.ui.firstNameLineEdit.setText(investigator.first_name)
                    self.ui.institutionLineEdit.setText(investigator.institution)
                    self.ui.eMailLineEdit.setText(investigator.e_mail)
                    return
        self.ui.usernameLineEdit.clear()
        self.ui.lastNameLineEdit.clear()
        self.ui.firstNameLineEdit.clear()
        self.ui.institutionLineEdit.clear()
        self.ui.eMailLineEdit.clear()
