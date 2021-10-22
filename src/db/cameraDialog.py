# cameraDialog.py

from db.schema_sqlalchemy import Camera
from db.cameraDialog_ui import Ui_CameraDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QDialog, QDialogButtonBox

from db.schema_sqlalchemy import *

class CameraDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_CameraDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.db_sess = self.bento.db_sessionMaker()
        self.populateComboBox(False)
        self.ui.cameraComboBox.currentIndexChanged.connect(self.showSelected)
        self.camera = Camera()

    def populateComboBox(self, preSelect):
        if preSelect:
            selection = self.ui.cameraComboBox.currentText()
        self.ui.cameraComboBox.clear()
        self.ui.cameraComboBox.addItem("new Camera")
        cameras = self.db_sess.query(Camera).distinct().all()
        self.ui.cameraComboBox.addItems([elem.name for elem in cameras])
        self.ui.cameraComboBox.setEditable(False)
        if preSelect:
            self.ui.cameraComboBox.setCurrentText(selection)

    @Slot(object)
    def update(self, button, preSelect=True):
        buttonRole = self.ui.buttonBox.buttonRole(button)
        if (buttonRole == QDialogButtonBox.AcceptRole or
            buttonRole == QDialogButtonBox.ApplyRole):
            self.camera.name = self.ui.nameLineEdit.text()
            self.camera.model = self.ui.modelLineEdit.text()
            self.camera.lens = self.ui.lensLineEdit.text()
            self.camera.position = self.ui.positionLineEdit.text()
            self.db_sess.add(self.camera)
            self.db_sess.commit()
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
        if self.ui.cameraComboBox.currentIndex() == 0:
            self.camera = Camera()
        else:
            camera_name = self.ui.cameraComboBox.currentText()
            query = self.db_sess.query(Camera)
            result = query.filter(Camera.name == camera_name).all()
            if len(result) > 0:
                self.camera = result[0]
                self.ui.nameLineEdit.setText(self.camera.name)
                self.ui.modelLineEdit.setText(self.camera.model)
                self.ui.lensLineEdit.setText(self.camera.lens)
                self.ui.positionLineEdit.setText(self.camera.position)
                return
        self.ui.nameLineEdit.clear()
        self.ui.modelLineEdit.clear()
        self.ui.lensLineEdit.clear()
        self.ui.positionLineEdit.clear()
