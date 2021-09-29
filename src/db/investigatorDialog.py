# investigatorDialog.py

from db.investigatorDialog_ui import Ui_InvestigatorDialog
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox

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
            selection_username = None
        self.ui.investigatorComboBox.clear()
        # For some unknown reason, addItem resets self.investigator_id to None!
        # So we need to preserve and restore it
        investigator_id = self.investigator_id
        self.ui.investigatorComboBox.addItem("New Investigator")
        self.investigator_id = investigator_id
        with self.bento.db_sessionMaker() as db_sess:
            try:
                investigators = db_sess.query(Investigator).distinct().all()
                self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
                if preSelect and self.investigator_id:
                    selection_username = investigators[self.investigator_id-1].user_name
            except Exception as e:
                pass # no database yet?

        self.ui.investigatorComboBox.setEditable(False)
        if preSelect:
            if self.investigator_id and self.investigator_id > 0 and selection_username == selection:
                self.ui.investigatorComboBox.setCurrentIndex(self.investigator_id)
            else:
                self.ui.investigatorComboBox.setCurrentText(selection)

    @Slot(object)
    def update(self, button, preSelect=True):
        buttonRole = self.ui.buttonBox.buttonRole(button)
        if (buttonRole == QDialogButtonBox.AcceptRole or
            buttonRole == QDialogButtonBox.ApplyRole):
            with self.bento.db_sessionMaker() as db_sess:
                need_to_add = False
                data_changed = False
                investigator = None
                if self.investigator_id:
                    investigator = db_sess.query(Investigator).filter(Investigator.id == self.investigator_id).scalar()
                if not investigator:
                    need_to_add = True
                    investigator = Investigator()
                if investigator.user_name != self.ui.usernameLineEdit.text():
                    investigator.user_name = self.ui.usernameLineEdit.text()
                    data_changed = True
                if investigator.last_name != self.ui.lastNameLineEdit.text():
                    investigator.last_name = self.ui.lastNameLineEdit.text()
                    data_changed = True
                if investigator.first_name != self.ui.firstNameLineEdit.text():
                    investigator.first_name = self.ui.firstNameLineEdit.text()
                    data_changed = True
                if investigator.institution != self.ui.institutionLineEdit.text():
                    investigator.institution = self.ui.institutionLineEdit.text()
                    data_changed = True
                if investigator.e_mail != self.ui.eMailLineEdit.text():
                    investigator.e_mail = self.ui.eMailLineEdit.text()
                    data_changed = True
                if need_to_add:
                    db_sess.add(investigator)
                    data_changed = True
                if data_changed:
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
            with self.bento.db_sessionMaker() as db_sess:
                investigators = db_sess.query(Investigator).all()
                # -1 in the next two lines due to "New Investigator" first entry in combo box
                if len(investigators) >= self.ui.investigatorComboBox.count()-1:
                    investigator = investigators[self.ui.investigatorComboBox.currentIndex()-1]
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
