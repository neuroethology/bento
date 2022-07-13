# dbDialog.py

from db.dispositionItemsDialog import DispositionItemsDialog, CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from qtpy.QtCore import Qt, Signal, Slot
from qtpy.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

import db.schema_sqlalchemy as sa

class DBDialog(QDialog):
    """
    Implementation of a parameterizable dialog box base class used for a variety of interactions with Bento's experiments database.

    The class is parameterized using a "dialogConfig" dict that must be supplied at the construction of an instance of this class.
    The dialogConfig dict will generally be defined in the __init__() function of the deriving class.

    The dialogConfig dict should include the following keys:

    Args:
        <newItemName> str:  What a new instance of the class is called, e.g. "New Investigator"
        dbClass str: The name of the class as found in schema_sqlalchemy, e.g. "Investigator"
        comboBoxName str: The name of a comboBox UI element to populate. found in the dialog's .ui file, e.g. "investigatorComboBox"
        selectionKey str: The field of the database class to be used to select an entry, e.g. "user_name"
        newOwnerAttr str: The database entry of the possible new owners of items owned by the entry being deleted, e.g. 'investigator_id',
        allFieldsBlankLambda lambda: a lambda function that takes the ui as input and returns True only if all relevant fields in the ui are blank.
        requiredFieldsLambda lambda: a lambda function that takes the ui as input and returns True only if all the required fields have been provided.
        requiredFieldsWarning str: The text to display if not all required fields have been provided, e.g. "You need to provide at least a user name, last name and first name",
        toDisposition list: a list of dicts, where each dict contains a "field" key consisting of the name of
        the field in the database to find items that need to be dispositioned, and a "description" key describing that field in common English, e.g.'fields' (list of tuples): A list of tuples where the first element if each tuple is a field name to be populated from the dialog, and the second element is
        the name of the ui element/widget (typically a QLineEdit widget) from which to get the data, e.g.

    """
    quitting = Signal()

    def __init__(self, bento, dialogConfig, ui):
        super().__init__()
        self.bento = bento
        self.dialogConfig = dialogConfig
        self.ui = ui
        self.ui.setupUi(self)
        self.ui.deleteButton = self.ui.buttonBox.addButton("Delete...", QDialogButtonBox.ActionRole)
        self.quitting.connect(self.bento.quit)

        self.item_id = None
        try:
            self.dbClass = getattr(sa, self.dialogConfig['dbClass'])
        except KeyError:
            self.dbClass = None
        try:
            self.comboBox = getattr(self.ui, self.dialogConfig['comboBoxName'])
            self.comboBox.setEditable(False)
            self.comboBox.currentIndexChanged.connect(self.showSelected)
            self.populateComboBox()
        except KeyError:
            self.comboBox = None

    def populateComboBox(self, preSelect: bool=False):
        """
        Populate the dialog's comboBox from the database based on the dialogConfig dict provided at construction.

        This involves database queries.
        """
        # prevent unwanted side effects while we're populating the combo box
        self.comboBox.blockSignals(True)
        if preSelect:
            selection = self.comboBox.currentText()
            selection_key = None
        self.comboBox.clear()
        self.comboBox.addItem(self.dialogConfig['newItemName'])
        with self.bento.db_sessionMaker() as db_sess:
            try:
                items = db_sess.query(self.dbClass).distinct().all()
                for item in items:
                    self.comboBox.addItem(getattr(item, self.dialogConfig['selectionKey']))
                    if preSelect and self.item_id == item.id:
                        selection_key = getattr(item, self.dialogConfig['selectionKey'])
            except Exception as e:
                pass # no database yet?

        if preSelect:
            if selection_key:
                self.comboBox.setCurrentText(selection_key)
            else:
                self.comboBox.setCurrentText(self.dialogConfig['newItemName'])
            self.showSelected()
        # reenable signals so that showSelected will be invoked when the combo box selection changes
        self.comboBox.blockSignals(False)

    def dispositionOwnedItems(self, items: list, category_str: str, db_sess, default_action=None) -> int:
        """
        Delete or reassign items owned by this investigator

        Which to do depends on what the user selects in the disposition box
        """
        if items:
            if default_action:
                result = default_action
            else:
                dispositionItemsDialog = DispositionItemsDialog(
                    db_sess,
                    self.dialogConfig['dbClass'],
                    self.dbClass,
                    self.dialogConfig['selectionKey'],
                    category_str,
                    self.item_id
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
                new_owner = db_sess.query(self.dbClass).filter(self.dbClass.id == result).scalar()
                if not new_owner:
                    print(f"Internal Error: New owner with ID {result} not in database.")
                    raise Exception(f"InternalError: New owner with ID {result} not in database.")
                newOwnerAttr = self.dialogConfig['newOwnerAttr']
                for item in items:
                    if hasattr(item, newOwnerAttr):
                        setattr(item, newOwnerAttr, result)
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
        item = None
        with self.bento.db_sessionMaker() as db_sess:
            if self.item_id:
                item = db_sess.query(self.dbClass).filter(self.dbClass.id == self.item_id).scalar()
            if buttonRole == QDialogButtonBox.ActionRole:
                """
                Delete selected item after dispositioning any DB entries owned/referenced by him/her/it
                """
                if not item:
                    print("Nothing selected, so nothing to delete")
                else:
                    overall_result = NOTHING_TO_DO
                    default_action = None
                    for toDisposition in self.dialogConfig['toDisposition']:
                        this_result = self.dispositionOwnedItems(
                            getattr(item, toDisposition['field']),
                            toDisposition['description'],
                            db_sess,
                            default_action)
                        if this_result == CANCEL_OPERATION:
                            return
                        elif this_result == DELETE_ITEMS or this_result == NOTHING_TO_DO:
                            overall_result = this_result
                        else:
                            # owned items were reassigned to new owner (in this_result)
                            # so do that for dependent items too
                            default_action = this_result
                            overall_result = this_result
                    if overall_result != CANCEL_OPERATION:
                        db_sess.delete(item)
                        db_sess.commit()
                        self.item_id = None
                        self.showSelected()
                    self.populateComboBox()
            elif (buttonRole == QDialogButtonBox.AcceptRole or
                buttonRole == QDialogButtonBox.ApplyRole):
                if not item:
                    # if all fields are blank, silently do nothing
                    # (allow click of "Okay" to close dialog without
                    # creating a new blank dbClass item)
                    if self.dialogConfig['allFieldsBlankLambda'](self.ui):  # do nothing and close dialog (if Okay was clicked)
                        return
                    # Require user name, last name and first name fields
                    elif not self.dialogConfig['requiredFieldsLambda'](self.ui):
                        QMessageBox.warning(
                            self,
                            "Requirements",
                            self.dialogConfig['requiredFieldsWarning'])
                        return
                    else:
                        need_to_add = True
                        item = self.dbClass()
                for fieldMapping in self.dialogConfig['fields']:
                    if getattr(item, fieldMapping[0]) != getattr(self.ui, fieldMapping[1]).text():
                        setattr(item, fieldMapping[0], getattr(self.ui, fieldMapping[1]).text())
                        data_changed = True
                if need_to_add:
                    db_sess.add(item)
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
        """
        Process a click of the "OK" button or equivalent.
        """
        # implicitly calls self.update()
        super().accept()

    @Slot()
    def reject(self):
        """
        Process a click of the "Cancel" button or equivalent.
        """
        super().reject()

    def clearFields(self):
        for field in self.dialogConfig['fields']:
            getattr(self.ui, field[1]).clear()

    @Slot()
    def showSelected(self):
        """
        Populate widgets in the dialog (typically QLineEdit widgets) from the database when a new item
        of the main comboBox has been selected.
        This happens by iterating through the dialogConfig's "fields" entry, which is a list of (field_name, description) tuples.
        """
        if not self.comboBox or self.comboBox.currentIndex() == 0:
            self.item_id = None
        else:
            with self.bento.db_sessionMaker() as db_sess:
                items = db_sess.query(self.dbClass).all()
                # -1 in the next two lines due to "New <Item>" first entry in combo box
                if len(items) >= self.comboBox.count()-1:
                    item = items[self.comboBox.currentIndex()-1]
                    self.item_id = item.id
                    for field in self.dialogConfig['fields']:
                        getattr(self.ui, field[1]).setText(getattr(item, field[0]))
                    return
        self.clearFields()
