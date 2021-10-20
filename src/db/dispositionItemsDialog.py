# dispositionItemsDialog.py

from db.dispositionItemsDialog_ui import Ui_DispositionItemsDialog

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

CANCEL_OPERATION = -1
DELETE_ITEMS = -2
NOTHING_TO_DO = -3

class DispositionItemsDialog(QDialog):
    """
    Dialog to ask the user how to handle items owned by an item that is
    about to be deleted from the database.  Options are:

    Delete the items along with the owner
    Reassign the items to a new owner before delete the owner
    Cancel deleting the owner
    """

    def __init__(self, db_sess, ownerCategoryStr, ownerDbType, displayField, itemCategoryStr, current_id):
        super().__init__()
        self.ui = Ui_DispositionItemsDialog()
        self.ui.setupUi(self)
        self.ui.reassignButton = self.ui.buttonBox.addButton("Reassign Items", QDialogButtonBox.ActionRole)
        self.ui.deleteButton = self.ui.buttonBox.addButton("Delete Items", QDialogButtonBox.NoRole)
        self.db_sess = db_sess
        label_text = (f"The {ownerCategoryStr} being deleted owns one or more {itemCategoryStr} "
            f"that need to be dispositioned.  You can delete them along with the {ownerCategoryStr}, "
            f"reassign them to another {ownerCategoryStr} (selected below), or cancel the whole operation.")
        self.ui.dispositionLabel.setText(label_text)
        self.populateComboBox(db_sess, ownerDbType, displayField, current_id)
        self.ui.assignToComboBox.currentIndexChanged.connect(self.setNewOwner)
        self.new_owner_id = self.ui.assignToComboBox.currentData()
        self.ui.reassignButton.clicked.connect(self.reassign)
        self.ui.deleteButton.clicked.connect(self.deleteItems)

    def populateComboBox(self, db_sess, dbType, displayField, current_id):
        try:
            possibilities = db_sess.query(dbType).distinct().all()
            for elem in possibilities:
                if elem.id == current_id:
                    continue
                attr = getattr(elem, displayField)
                self.ui.assignToComboBox.addItem(attr, userData=elem.id)
        except Exception as e:
            print(f"Exception in populateComboBox: {e}")
            pass # no database yet?

    @Slot()
    def setNewOwner(self):
        self.new_owner_id = self.ui.assignToComboBox.currentData()

    @Slot()
    def reassign(self):
        self.done(self.new_owner_id)

    @Slot()
    def deleteItems(self):
        answer = QMessageBox.question(self, "Delete Confirmation", "You're about to delete items from the database!  Are you sure?")
        if answer == QMessageBox.StandardButton.Yes:
            self.done(DELETE_ITEMS)
        elif answer == QMessageBox.StandardButton.No:
            return
        else:
            raise Exception("Unexpected button response--shouldn't be possible.")


    @Slot()
    def reject(self):
        self.done(CANCEL_OPERATION)   # not okay to continue the delete of the owner

    @Slot()
    def accept(self):
        raise Exception("Shouldn't be possible to get here")

