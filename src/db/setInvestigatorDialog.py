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
        print("setting investigator_id to None")
        self.investigator_id = None

        username = self.bento.config.username()
        with self.bento.db_sessionMaker() as db_sess:
            try:
                query = db_sess.query(Investigator).distinct()
                investigators = query.all()
                investigator = query.filter(Investigator.user_name == username).scalar()
                self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
                self.ui.investigatorComboBox.setEditable(False)
                if investigator:
                    print(f"setting investigator_id to {investigator.id}")
                    self.investigator_id = investigator.id
                    self.ui.investigatorComboBox.setCurrentText(investigator.user_name)
                elif len(investigators) > 0:
                    self.investigator_id = investigators[0].id
                    self.ui.investigatorComboBox.setCurrentText(investigators[0].user_name)
            except Exception as e:
                print(f"Caught exception {e}")
                pass # no database yet?
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)

    @Slot()
    def investigatorChanged(self):
        username = self.ui.investigatorComboBox.currentText()
        with self.bento.db_sessionMaker() as db_sess:
            investigator= db_sess.query(Investigator).filter(Investigator.user_name == username).distinct().one()
            self.investigator_id = investigator.id

    @Slot()
    def accept(self):
        self.bento.setInvestigatorId(self.investigator_id)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
