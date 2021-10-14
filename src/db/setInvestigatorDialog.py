# setInvestigatorDialog.py

from db.schema_sqlalchemy import Investigator
from db.setInvestigatorDialog_ui import Ui_SetInvestigatorDialog
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QDialog

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
        try:
            with self.bento.db_sessionMaker() as db_sess:
                query = db_sess.query(Investigator).distinct()
                investigators = query.all()
                investigator_candidates = query.filter(Investigator.user_name == username).all()
                self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
                self.ui.investigatorComboBox.setEditable(False)
                if len(investigator_candidates) > 0:
                    investigator = investigator_candidates[0]
                    if len(investigator_candidates) > 1:
                        #TODO: put up alert box here to warn that there are duplicate investigators
                        pass
                elif len(investigators) > 0:
                    investigator = investigators[0]
            print(f"setting investigator_id to {investigator.id}")
            self.investigator_id = investigator.id
            self.ui.investigatorComboBox.setCurrentText(investigator.user_name)
            self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)
        except Exception as e:
            print(f"Caught exception: {e}")
            pass # no database yet?

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
