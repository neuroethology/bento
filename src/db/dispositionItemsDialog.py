# dispositionItemsDialog.py

from db.dispositionItemsDialog_ui import Ui_DispositionItemsDialog

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

CANCEL_OPERATION = -1
DELETE_ITEMS = -2
NOTHING_TO_DO = -3

class DispositionItemsDialog(QDialog):
    """
    This class implements a dialog widget to ask the user how to handle items owned
    by an item that is about to be deleted from the database.  Options are:

    - Delete the items along with the owner
    - Reassign the items to a new owner before deleting the owner
    - Cancel deleting the owner
    """

    def __init__(self, db_sess, ownerCategoryStr, ownerDbType, displayField, itemCategoryStr, current_id):
        """
        Construct and return an instance of the DispositionItemsDialog class.

        Args:
            db_sess:    An open sqlalchemy session with the database on which database transactions can be executed.
            ownerCategoryStr:   A string describing the kind of database item that is about to be deleted.
            ownerDbType:    The class of database item that is being deleted.  This should be one of the classes defined in schema_sqlalchemy.py.
            displayField:   The field in the database used to populate the dialog's main comboBox
            itemCategoryStr:    The name of category of items owned by the item being deleted.
            current_id: The id of the item being deleted, so that it is not displayed as a possible new owner.

        """
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
        """
        Populate the main combobox, as specified by the displayField parameter supplied during construction
        of the class.
        """
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
        """
        Set self.new_owner_id in response to an entry in the assignToComboBox being selected.
        """
        self.new_owner_id = self.ui.assignToComboBox.currentData()

    @Slot()
    def reassign(self):
        """
        Reassign the owned items to the new owner held in self.new_owner_id.
        """
        self.done(self.new_owner_id)

    @Slot()
    def deleteItems(self):
        """
        Delete the owned items, after warning the user a second time, since this operation cannot be undone.
        """
        answer = QMessageBox.question(self, "Delete Confirmation", "You're about to delete items from the database!  Are you sure?")
        if answer == QMessageBox.StandardButton.Yes:
            self.done(DELETE_ITEMS)
        elif answer == QMessageBox.StandardButton.No:
            return
        else:
            raise Exception("Unexpected button response--shouldn't be possible.")


    @Slot()
    def reject(self):
        """
        Cancel the deletion of the item.
        """
        self.done(CANCEL_OPERATION)   # not okay to continue the delete of the owner

    @Slot()
    def accept(self):
        """
        This would get called by the default "OK" button of a normal dialog widget.
        This dialog widget has no default "OK" button, so this function should never
        be called.  If it is, it raises an Exception.
        """
        raise Exception("Shouldn't be possible to get here")

