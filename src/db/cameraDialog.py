# cameraDialog.py

from db.schema_sqlalchemy import Camera
from db.cameraDialog_ui import Ui_CameraDialog
from db.dispositionItemsDialog import CANCEL_OPERATION
from db.dbDialog import DBDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QDialogButtonBox, QMessageBox

from db.schema_sqlalchemy import *

class CameraDialog(DBDialog):

    quitting = Signal()

    def __init__(self, bento):
        dialogConfig = {
            'newItemName': "New Camera",
            'dbClass': "Camera",
            'comboBoxName': "cameraComboBox",
            'selectionKey': "position",
            'newOwnerAttr': 'camera_id',
            'allFieldsBlankLambda': lambda ui : (
                not ui.nameLineEdit.text() and
                not ui.modelLineEdit.text() and
                not ui.lensLineEdit.text() and
                not ui.positionLineEdit.text()
            ),
            'requiredFieldsLambda': lambda ui : (
                ui.nameLineEdit.text() and
                ui.positionLineEdit.text()
            ),
            'requiredFieldsWarning': "You need to provide at least a camera name and position",
            'toDisposition': [
                {
                    'field': 'videos',
                    'description': "videos"
                }
            ],
            'fields': [
                ('name', 'nameLineEdit'),
                ('model', 'modelLineEdit'),
                ('lens', 'lensLineEdit'),
                ('position', 'positionLineEdit')
            ]
        }
        super().__init__(bento, dialogConfig, Ui_CameraDialog())
