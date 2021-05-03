# surgeryDialog.py

from db.schema_sqlalchemy import Investigator
from db.surgeryDialog_ui import Ui_SurgeryDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox

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

        self.db_sess = self.bento.db_sessionMaker()
        self.investigator_id = investigator_id
        self.animal_id = animal_id
        self.surgery = Surgery()

    @Slot()
    def accept(self):
        self.surgery.animal_id = self.animal_id
        self.surgery.investigator_id = self.investigator_id
        self.surgery.date = self.ui.dateEdit.date().toPython()
        if self.ui.leftImplantRadioButton.isChecked():
            implant_side = LateralityEnum.Left
        elif self.ui.rightImplantRadioButton.isChecked():
            implant_side = LateralityEnum.Right
        elif self.ui.bilatImplantRadioButton.isChecked():
            implant_side = LateralityEnum.Bilateral
        else:
            implant_side = LateralityEnum.Nothing
        self.surgery.implant_side = implant_side
        if self.ui.leftInjectionRadioButton.isChecked():
            injection_side = LateralityEnum.Left
        elif self.ui.rightInjectionRadioButton.isChecked():
            injection_side = LateralityEnum.Right
        elif self.ui.bilatInjectionRadioButton.isChecked():
            injection_side = LateralityEnum.Bilateral
        else:
            injection_side = LateralityEnum.Nothing
        self.surgery.injection_side = injection_side
        self.surgery.procedure = self.ui.procedureLineEdit.text()
        self.surgery.anesthesia = self.ui.anesthesiaLineEdit.text()
        self.surgery.follow_up_care = self.ui.followUpLineEdit.text()
        self.db_sess.add(self.surgery)
        self.db_sess.commit()
        self.db_sess.flush()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
