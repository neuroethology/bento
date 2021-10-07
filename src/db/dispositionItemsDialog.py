# dispositionItemsDialog.py

from db.dispositionItemsDialog_ui import Ui_DispositionItemsDialog

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox

CANCEL_OPERATION = -1
DISCARD_RESULT = -2

class DispositionItemsDialog(QDialog):
    """
    Dialog to ask the user how to handle items owned by an item that is
    about to be deleted from the database.  Options are:

    Delete the items along with the owner
    Reassign the items to a new owner before delete the owner
    Cancel deleting the owner
    """

    def __init__(self, db_sess, ownerCategoryStr, ownerDbType, itemCategoryStr, current_id):
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
        self.populateComboBox(db_sess, ownerDbType, current_id)
        self.ui.assignToComboBox.currentIndexChanged.connect(self.setNewOwner)
        self.new_owner_id = -1
        self.ui.reassignButton.clicked.connect(self.reassign)
        self.ui.deleteButton.clicked.connect(self.discard)

    def populateComboBox(self, db_sess, dbType, current_id):
        try:
            possibilities = db_sess.query(dbType).distinct().all()
            for elem in possibilities:
                if elem.id == current_id:
                    continue
                self.ui.assignToComboBox.addItem(elem.user_name, userData=elem.id)
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
    def discard(self):
        self.done(DISCARD_RESULT)

    @Slot()
    def reject(self):
        self.done(CANCEL_OPERATION)   # not okay to continue the delete of the owner

    @Slot()
    def accept(self):
        raise Exception("Shouldn't be possible to get here")

