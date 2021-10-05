# dispositionItemsDialog.py

from db.dispositionItemsDialog_ui import Ui_DispositionItemsDialog

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox

REASSIGN_TO_RESULT = 1000
DISCARD_RESULT = 2000

class DispositionItemsDialog(QDialog):
    """
    Dialog to ask the user how to handle items owned by an item that is
    about to be deleted from the database.  Options are:

    Delete the items along with the owner
    Reassign the items to a new owner before delete the owner
    Cancel deleting the owner
    """

    def __init__(self, db_sess, ownerCategoryStr, itemCategoryStr, dbType, current_id):
        super().__init__()
        self.ui = Ui_DispositionItemsDialog()
        self.ui.reassignButton = self.ui.buttonBox.addButton("Reassign Items", QDialogButtonBox.ActionRole)
        self.ui.deleteButton = self.ui.buttonBox.addButton("Delete Items", QDialogButtonBox.NoRole)
        self.db_sess = db_sess
        label_text = f"The {ownerCategoryStr} being deleted owns one or more {itemCategoryStr} items \
            that need to be dispositioned.  You can delete them along with the {ownerCategoryStr}, \
            reassign them to another {ownerCategoryStr} (selected below), or cancel the whole operation."
        self.ui.dispositionLabel.setText(label_text)
        self.populateComboBox(db_sess, dbType, current_id)

    def populateComboBox(self, db_sess, dbType, current_id):
        try:
            possibilities = db_sess.query(dbType).distinct().all()
            self.ui.assignToComboBox.addItems([elem for elem in possibilities if elem.id != current_id])
        except Exception as e:
            print(f"Exception in populateComboBox: {e}")
            pass # no database yet?

    @Slot()
    def reject(self):
        return False    # not okay to continue the delete of the owner

    @Slot()
    def accept(self):
        raise Exception("Shouldn't be possible to get here")

