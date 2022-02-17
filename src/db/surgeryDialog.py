# surgeryDialog.py

from db.schema_sqlalchemy import Investigator
from db.surgeryDialog_ui import Ui_SurgeryDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QDialog, QDialogButtonBox

from db.schema_sqlalchemy import Surgery, LateralityEnum
from datetime import date

class SurgeryDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento, investigator_id, animal_id):
        super().__init__()
        self.bento = bento
        self.ui = Ui_SurgeryDialog()
        self.ui.setupUi(self)
        self.ui.dateEdit.setDate(date.today())
        self.quitting.connect(self.bento.quit)

        self.investigator_id = investigator_id
        self.animal_id = animal_id

    @Slot()
    def accept(self):
        with self.bento.db_sessionMaker() as db_sess:
            surgery = Surgery()
            surgery.animal_id = self.animal_id
            surgery.investigator_id = self.investigator_id
            surgery.date = self.ui.dateEdit.date().toPython()
            if self.ui.leftImplantRadioButton.isChecked():
                implant_side = LateralityEnum.Left
            elif self.ui.rightImplantRadioButton.isChecked():
                implant_side = LateralityEnum.Right
            elif self.ui.bilatImplantRadioButton.isChecked():
                implant_side = LateralityEnum.Bilateral
            else:
                implant_side = LateralityEnum.Nothing
            surgery.implant_side = implant_side
            if self.ui.leftInjectionRadioButton.isChecked():
                injection_side = LateralityEnum.Left
            elif self.ui.rightInjectionRadioButton.isChecked():
                injection_side = LateralityEnum.Right
            elif self.ui.bilatInjectionRadioButton.isChecked():
                injection_side = LateralityEnum.Bilateral
            else:
                injection_side = LateralityEnum.Nothing
            surgery.injection_side = injection_side
            surgery.procedure = self.ui.procedureLineEdit.text()
            surgery.anesthesia = self.ui.anesthesiaLineEdit.text()
            surgery.follow_up_care = self.ui.followUpLineEdit.text()
            db_sess.add(surgery)
            db_sess.commit()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
