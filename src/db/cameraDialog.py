# cameraDialog.py

from db.schema_sqlalchemy import Camera
from db.cameraDialog_ui import Ui_CameraDialog
from db.dispositionItemsDialog import DispositionItemsDialog, CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

from db.schema_sqlalchemy import *

class CameraDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_CameraDialog()
        self.ui.setupUi(self)
        self.ui.deleteButton = self.ui.buttonBox.addButton("Delete...", QDialogButtonBox.ActionRole)
        self.quitting.connect(self.bento.quit)

        self.camera_id = None
        self.ui.cameraComboBox.setEditable(False)
        self.ui.cameraComboBox.currentIndexChanged.connect(self.showSelected)
        self.populateComboBox(False)

    def populateComboBox(self, preSelect: bool = False):
        # prevent unwanted side effects while we're populating the combo box
        self.ui.cameraComboBox.blockSignals(True)
        if preSelect:
            selection = self.ui.cameraComboBox.currentText()
            selection_name = None
        self.ui.cameraComboBox.clear()
        self.ui.cameraComboBox.addItem("New Camera")
        with self.bento.db_sessionMaker() as db_sess:
            try:
                cameras = db_sess.query(Camera).distinct().all()
                for camera in cameras:
                    self.ui.cameraComboBox.addItem(camera.name)
                    if preSelect and self.camera_id == camera.id:
                        selection_name = camera.name
            except Exception as e:
                pass # no database yet?

        if preSelect:
            if selection_name:
                self.ui.cameraComboBox.setCurrentText(selection_name)
            else:
                self.ui.cameraComboBox.setCurrentText("New Camera")
            self.showSelected()
        # reenable signals so that showSelected will be invoked when the combo box selection changes
        self.ui.cameraComboBox.blockSignals(False)

    def dispositionOwnedItems(self, items: list, category_str: str, db_sess, default_action=None) -> int:
        """
        Delete or reassign sessions where this camera is used

        Which to do depends on what the user selects in the disposition box
        """
        if items:
            if default_action:
                result = default_action
            else:
                dispositionItemsDialog = DispositionItemsDialog(
                    db_sess,
                    "Camera",
                    Camera,
                    "position",
                    category_str,
                    self.camera_id
                    )
                dispositionItemsDialog.exec_()
                result = dispositionItemsDialog.result()
            if result == CANCEL_OPERATION:
                pass
            elif result == DELETE_ITEMS:
                for item in items:
                    db_sess.delete(item)
                db_sess.commit()
            elif result >= 0:
                new_owner = db_sess.query(Camera).filter(Camera.id == result).scalar()
                if not new_owner:
                    print(f"Internal Error: New owner with ID {result} not in database.")
                    raise Exception(f"InternalError: New owner with ID {result} not in database.")
                for item in items:
                    if hasattr(item, "camera_id"):
                        item.camera_id = result
                db_sess.commit()
            else:
                raise Exception("shouldn't get here")
        else:
            result = NOTHING_TO_DO
        return result

    @Slot(object)
    def update(self, button, preSelect=True):
        buttonRole = self.ui.buttonBox.buttonRole(button)
        need_to_add = False
        data_changed = False
        camera = None
        with self.bento.db_sessionMaker() as db_sess:
            if self.camera_id:
                camera = db_sess.query(Camera).filter(Camera.id == self.camera_id).scalar()
            if buttonRole == QDialogButtonBox.ActionRole:
                """
                Delete selected camera after dispositioning any DB entries referencing it
                """
                if not camera:
                    print("Nothing selected, so nothing to delete")
                else:
                    result = self.dispositionOwnedItems(camera.videos, "videos", db_sess)
                    if result != CANCEL_OPERATION:
                        db_sess.delete(camera)
                        db_sess.commit()
                        self.camera_id = None
                        self.showSelected()
                    self.populateComboBox()
            elif (buttonRole == QDialogButtonBox.AcceptRole or
                buttonRole == QDialogButtonBox.ApplyRole):
                if not camera:
                    # if all fields are blank, silently do nothing
                    # (allow click of "Okay" to close dialog without
                    # creating a new blank Investigator)
                    if (not self.ui.nameLineEdit.text() and
                        not self.ui.modelLineEdit.text() and
                        not self.ui.lensLineEdit.text() and
                        not self.ui.positionLineEdit.text()
                        ):  # do nothing and close dialog (if Okay was clicked)
                        return
                    # Require user name, last name and first name fields
                    elif not (
                            self.ui.nameLineEdit.text() and
                            self.ui.positionLineEdit.text()
                            ):
                        QMessageBox.warning(self, "Requirements", "You need to provide at least a camera name and position")
                        return
                    else:
                        need_to_add = True
                        camera = Camera()
                if camera.name != self.ui.nameLineEdit.text():
                    camera.name = self.ui.nameLineEdit.text()
                    data_changed = True
                if camera.model != self.ui.modelLineEdit.text():
                    camera.model = self.ui.modelLineEdit.text()
                    data_changed = True
                if camera.lens != self.ui.lensLineEdit.text():
                    camera.lens = self.ui.lensLineEdit.text()
                    data_changed = True
                if camera.position != self.ui.positionLineEdit.text():
                    camera.position = self.ui.positionLineEdit.text()
                    data_changed = True
                if need_to_add:
                    db_sess.add(camera)
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
        # implicitly calls self.update()
        # self.update(self.ui.buttonBox.button(QDialogButtonBox.Ok), False)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()

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
