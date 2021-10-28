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

    # @Slot(object)
    # def update(self, button, preSelect=True):
    #     buttonRole = self.ui.buttonBox.buttonRole(button)
    #     need_to_add = False
    #     data_changed = False
    #     camera = None
    #     with self.bento.db_sessionMaker() as db_sess:
    #         if self.camera_id:
    #             camera = db_sess.query(Camera).filter(Camera.id == self.camera_id).scalar()
    #         if buttonRole == QDialogButtonBox.ActionRole:
    #             """
    #             Delete selected camera after dispositioning any DB entries referencing it
    #             """
    #             if not camera:
    #                 print("Nothing selected, so nothing to delete")
    #             else:
    #                 result = self.dispositionOwnedItems(camera.videos, "videos", db_sess)
    #                 if result != CANCEL_OPERATION:
    #                     db_sess.delete(camera)
    #                     db_sess.commit()
    #                     self.camera_id = None
    #                     self.showSelected()
    #                 self.populateComboBox()
    #         elif (buttonRole == QDialogButtonBox.AcceptRole or
    #             buttonRole == QDialogButtonBox.ApplyRole):
    #             if not camera:
    #                 # if all fields are blank, silently do nothing
    #                 # (allow click of "Okay" to close dialog without
    #                 # creating a new blank Investigator)
    #                 if (not self.ui.nameLineEdit.text() and
    #                     not self.ui.modelLineEdit.text() and
    #                     not self.ui.lensLineEdit.text() and
    #                     not self.ui.positionLineEdit.text()
    #                     ):  # do nothing and close dialog (if Okay was clicked)
    #                     return
    #                 # Require user name, last name and first name fields
    #                 elif not (
    #                         self.ui.nameLineEdit.text() and
    #                         self.ui.positionLineEdit.text()
    #                         ):
    #                     QMessageBox.warning(self, "Requirements", "You need to provide at least a camera name and position")
    #                     return
    #                 else:
    #                     need_to_add = True
    #                     camera = Camera()
    #             if camera.name != self.ui.nameLineEdit.text():
    #                 camera.name = self.ui.nameLineEdit.text()
    #                 data_changed = True
    #             if camera.model != self.ui.modelLineEdit.text():
    #                 camera.model = self.ui.modelLineEdit.text()
    #                 data_changed = True
    #             if camera.lens != self.ui.lensLineEdit.text():
    #                 camera.lens = self.ui.lensLineEdit.text()
    #                 data_changed = True
    #             if camera.position != self.ui.positionLineEdit.text():
    #                 camera.position = self.ui.positionLineEdit.text()
    #                 data_changed = True
    #             if need_to_add:
    #                 db_sess.add(camera)
    #                 data_changed = True
    #             if data_changed:
    #                 db_sess.commit()
    #             self.populateComboBox(preSelect)
    #         elif buttonRole == QDialogButtonBox.DestructiveRole:
    #             self.reject()
    #         else:
    #             print("returning without any action")

    @Slot()
    def showSelected(self):
        if self.ui.cameraComboBox.currentIndex() == 0:
            self.camera_id = None
        else:
            with self.bento.db_sessionMaker() as db_sess:
                cameras = db_sess.query(Camera).all()
                # -1 in the next two lines due to "New Camera" first entry in combo box
                if len(cameras) >= self.ui.cameraComboBox.count()-1:
                    camera = cameras[self.ui.cameraComboBox.currentIndex()-1]
                    self.camera_id = camera.id
                    self.ui.nameLineEdit.setText(camera.name)
                    self.ui.modelLineEdit.setText(camera.model)
                    self.ui.lensLineEdit.setText(camera.lens)
                    self.ui.positionLineEdit.setText(camera.position)
                    return
        self.ui.nameLineEdit.clear()
        self.ui.modelLineEdit.clear()
        self.ui.lensLineEdit.clear()
        self.ui.positionLineEdit.clear()
