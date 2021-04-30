# configDialog.py

from db.schema_sqlalchemy import Camera
from db.configDialog_ui import Ui_ConfigDialog
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QDialogButtonBox

from db.schema_sqlalchemy import *

class ConfigDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.populate()

    def populate(self):
        self.ui.usernameLineEdit.setText(self.bento.config.username())
        self.ui.passwordLineEdit.setText(self.bento.config.password())
        self.ui.hostLineEdit.setText(self.bento.config.host())
        self.ui.portLineEdit.setText(self.bento.config.port())

    @Slot()
    def accept(self):
        self.bento.config.setUsername(self.ui.usernameLineEdit.text())
        self.bento.config.setPassword(self.ui.passwordLineEdit.text())
        self.bento.config.setHost(self.ui.hostLineEdit.text())
        self.bento.config.setPort(self.ui.portLineEdit.text())
        self.bento.config.write()
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
