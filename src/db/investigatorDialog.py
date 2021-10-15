# investigatorDialog.py

from db.investigatorDialog_ui import Ui_InvestigatorDialog
from db.dispositionItemsDialog import DispositionItemsDialog, CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from PySide6.QtCore import Qt, QMetaMethod, Signal, Slot, SIGNAL
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from db.schema_sqlalchemy import Investigator

class InvestigatorDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_InvestigatorDialog()
        self.ui.setupUi(self)
        self.ui.deleteButton = self.ui.buttonBox.addButton("Delete...", QDialogButtonBox.ActionRole)
        self.quitting.connect(self.bento.quit)

        self.investigator_id = None
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.showSelected)
        self.populateComboBox(False)

    def populateComboBox(self, preSelect):
        # prevent unwanted side effects while we're populating the combo box
        self.ui.investigatorComboBox.blockSignals(True)
        if preSelect:
            selection = self.ui.investigatorComboBox.currentText()
            selection_username = None
        self.ui.investigatorComboBox.clear()
        # For some unknown reason, addItem resets self.investigator_id to None!
        # So we need to preserve and restore it
        investigator_id = self.investigator_id
        self.ui.investigatorComboBox.addItem("New Investigator")
        self.investigator_id = investigator_id
        with self.bento.db_sessionMaker() as db_sess:
            try:
                investigators = db_sess.query(Investigator).distinct().all()
                self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
                if preSelect and self.investigator_id:
                    selection_username = investigators[self.investigator_id-1].user_name
            except Exception as e:
                pass # no database yet?

        self.ui.investigatorComboBox.setEditable(False)
        self.ui.investigatorComboBox.blockSignals(False)
        if preSelect:
            if self.investigator_id and self.investigator_id > 0 and selection_username == selection:
                self.ui.investigatorComboBox.setCurrentIndex(self.investigator_id)
            else:
                self.ui.investigatorComboBox.setCurrentText(selection)

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
                    "Investigator",
                    Investigator,
                    "user_name",
                    category_str,
                    self.investigator_id
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
                new_owner = db_sess.query(Investigator).filter(Investigator.id == result).scalar()
                if not new_owner:
                    print(f"Internal Error: New owner with ID {result} not in database.")
                    raise Exception(f"InternalError: New owner with ID {result} not in database.")
                for item in items:
                    if hasattr(item, "investigator_id"):
                        item.investigator_id = result
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
        investigator = None
        with self.bento.db_sessionMaker() as db_sess:
            if self.investigator_id:
                investigator = db_sess.query(Investigator).filter(Investigator.id == self.investigator_id).scalar()
            if buttonRole == QDialogButtonBox.ActionRole:
                """
                Delete selected investigator after dispositioning any DB entries owned by him/her
                """
                if not investigator:
                    print("Nothing selected, so nothing to delete")
                else:
                    animals_result = NOTHING_TO_DO
                    sessions_result = self.dispositionOwnedItems(investigator.sessions, "sessions and associated trials "
                        "and data file references", db_sess)
                    if sessions_result == DELETE_ITEMS or sessions_result == NOTHING_TO_DO:
                        animals_result = self.dispositionOwnedItems(investigator.animals, "animals", db_sess)
                    elif sessions_result == CANCEL_OPERATION:
                        return
                    else:   # sessions were reassigned to new owner in sessions_result
                        animals_result = self.dispositionOwnedItems(investigator.animals, "animals", db_sess, sessions_result)
                    if animals_result != CANCEL_OPERATION:
                        db_sess.delete(investigator)
                        db_sess.commit()
                        self.investigator_id = None
                        self.showSelected()
                    self.populateComboBox(False)
            elif (buttonRole == QDialogButtonBox.AcceptRole or
                buttonRole == QDialogButtonBox.ApplyRole):
                if not investigator:
                    need_to_add = True
                    investigator = Investigator()
                if investigator.user_name != self.ui.usernameLineEdit.text():
                    investigator.user_name = self.ui.usernameLineEdit.text()
                    data_changed = True
                if investigator.last_name != self.ui.lastNameLineEdit.text():
                    investigator.last_name = self.ui.lastNameLineEdit.text()
                    data_changed = True
                if investigator.first_name != self.ui.firstNameLineEdit.text():
                    investigator.first_name = self.ui.firstNameLineEdit.text()
                    data_changed = True
                if investigator.institution != self.ui.institutionLineEdit.text():
                    investigator.institution = self.ui.institutionLineEdit.text()
                    data_changed = True
                if investigator.e_mail != self.ui.eMailLineEdit.text():
                    investigator.e_mail = self.ui.eMailLineEdit.text()
                    data_changed = True
                if need_to_add:
                    db_sess.add(investigator)
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
        super().accept()

    @Slot()
    def reject(self):
        super().reject()

    @Slot()
    def showSelected(self):
        if self.ui.investigatorComboBox.currentIndex() == 0:
            self.investigator_id = None
        else:
            with self.bento.db_sessionMaker() as db_sess:
                investigators = db_sess.query(Investigator).all()
                # -1 in the next two lines due to "New Investigator" first entry in combo box
                if len(investigators) >= self.ui.investigatorComboBox.count()-1:
                    investigator = investigators[self.ui.investigatorComboBox.currentIndex()-1]
                    self.investigator_id = investigator.id
                    self.ui.usernameLineEdit.setText(investigator.user_name)
                    self.ui.lastNameLineEdit.setText(investigator.last_name)
                    self.ui.firstNameLineEdit.setText(investigator.first_name)
                    self.ui.institutionLineEdit.setText(investigator.institution)
                    self.ui.eMailLineEdit.setText(investigator.e_mail)
                    return
        self.ui.usernameLineEdit.clear()
        self.ui.lastNameLineEdit.clear()
        self.ui.firstNameLineEdit.clear()
        self.ui.institutionLineEdit.clear()
        self.ui.eMailLineEdit.clear()
