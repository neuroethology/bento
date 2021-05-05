# setInvestigatorDialog.py

from db.schema_sqlalchemy import Investigator
from db.setInvestigatorDialog_ui import Ui_SetInvestigatorDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog

class SetInvestigatorDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_SetInvestigatorDialog()
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
        else:
            self.investigator_id = None
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)

    @Slot()
    def investigatorChanged(self):
        username = self.ui.investigatorComboBox.currentText()
        investigator= self.db_sess.query(Investigator).filter(Investigator.user_name == username).distinct().one()
        self.investigator_id = investigator.id

    @Slot()
    def accept(self):
        self.bento.setInvestigatorId(self.investigator_id)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
