# investigatorDialog.py

from db.investigatorDialog_ui import Ui_InvestigatorDialog
from db.dispositionItemsDialog import CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from db.dbDialog import DBDialog
from qtpy.QtCore import Qt, Signal, Slot
from qtpy.QtWidgets import QDialogButtonBox, QMessageBox

from db.schema_sqlalchemy import Investigator

class InvestigatorDialog(DBDialog):

    quitting = Signal()

    def __init__(self, bento):
        dialogConfig = {
            'newItemName': "New Investigator",
            'dbClass': "Investigator",
            'comboBoxName': "investigatorComboBox",
            'selectionKey': "user_name",
            'newOwnerAttr': 'investigator_id',
            'allFieldsBlankLambda': lambda ui : (
                not ui.usernameLineEdit.text() and
                not ui.lastNameLineEdit.text() and
                not ui.institutionLineEdit.text() and
                not ui.eMailLineEdit.text()
            ),
            'requiredFieldsLambda': lambda ui : (
                ui.usernameLineEdit.text() and
                ui.lastNameLineEdit.text() and
                ui.firstNameLineEdit.text()
            ),
            'requiredFieldsWarning': "You need to provide at least a user name, last name and first name",
            'toDisposition': [
                {
                    'field': 'sessions',
                    'description': "session and associated trials and data file references"
                },
                {
                    'field': 'animals',
                    'description': "animals"
                }
            ],
            'fields': [
                ('user_name', 'usernameLineEdit'),
                ('last_name', 'lastNameLineEdit'),
                ('first_name', 'firstNameLineEdit'),
                ('institution', 'institutionLineEdit'),
                ('e_mail', 'eMailLineEdit')]
        }
        super().__init__(bento, dialogConfig, Ui_InvestigatorDialog())

    # @Slot(object)
    # def update(self, button, preSelect=True):
    #     buttonRole = self.ui.buttonBox.buttonRole(button)
    #     need_to_add = False
    #     data_changed = False
    #     investigator = None
    #     with self.bento.db_sessionMaker() as db_sess:
    #         if self.item_id:
    #             investigator = db_sess.query(Investigator).filter(Investigator.id == self.item_id).scalar()
    #         if buttonRole == QDialogButtonBox.ActionRole:
    #             """
    #             Delete selected investigator after dispositioning any DB entries owned by him/her
    #             """
    #             if not investigator:
    #                 print("Nothing selected, so nothing to delete")
    #             else:
    #                 animals_result = NOTHING_TO_DO
    #                 sessions_result = self.dispositionOwnedItems(investigator.sessions, "sessions and associated trials "
    #                     "and data file references", db_sess)
    #                 if sessions_result == DELETE_ITEMS or sessions_result == NOTHING_TO_DO:
    #                     animals_result = self.dispositionOwnedItems(investigator.animals, "animals", db_sess)
    #                 elif sessions_result == CANCEL_OPERATION:
    #                     return
    #                 else:   # sessions were reassigned to new owner in sessions_result
    #                     animals_result = self.dispositionOwnedItems(investigator.animals, "animals", db_sess, sessions_result)
    #                 if animals_result != CANCEL_OPERATION:
    #                     db_sess.delete(investigator)
    #                     db_sess.commit()
    #                     self.item_id = None
    #                     self.showSelected()
    #                 self.populateComboBox()
    #         elif (buttonRole == QDialogButtonBox.AcceptRole or
    #             buttonRole == QDialogButtonBox.ApplyRole):
    #             if not investigator:
    #                 # if all fields are blank, silently do nothing
    #                 # (allow click of "Okay" to close dialog without
    #                 # creating a new blank Investigator)
    #                 if (not self.ui.usernameLineEdit.text() and
    #                     not self.ui.lastNameLineEdit.text() and
    #                     not self.ui.firstNameLineEdit.text() and
    #                     not self.ui.institutionLineEdit.text() and
    #                     not self.ui.eMailLineEdit.text()
    #                     ):  # do nothing and close dialog (if Okay was clicked)
    #                     return
    #                 # Require user name, last name and first name fields
    #                 elif not (
    #                         self.ui.usernameLineEdit.text() and
    #                         self.ui.lastNameLineEdit.text() and
    #                         self.ui.firstNameLineEdit.text()
    #                         ):
    #                     QMessageBox.warning(self, "Requirements", "You need to provide at least a user name, last name and first name")
    #                     return
    #                 else:
    #                     need_to_add = True
    #                     investigator = Investigator()
    #             if investigator.user_name != self.ui.usernameLineEdit.text():
    #                 investigator.user_name = self.ui.usernameLineEdit.text()
    #                 data_changed = True
    #             if investigator.last_name != self.ui.lastNameLineEdit.text():
    #                 investigator.last_name = self.ui.lastNameLineEdit.text()
    #                 data_changed = True
    #             if investigator.first_name != self.ui.firstNameLineEdit.text():
    #                 investigator.first_name = self.ui.firstNameLineEdit.text()
    #                 data_changed = True
    #             if investigator.institution != self.ui.institutionLineEdit.text():
    #                 investigator.institution = self.ui.institutionLineEdit.text()
    #                 data_changed = True
    #             if investigator.e_mail != self.ui.eMailLineEdit.text():
    #                 investigator.e_mail = self.ui.eMailLineEdit.text()
    #                 data_changed = True
    #             if need_to_add:
    #                 db_sess.add(investigator)
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
        if self.ui.investigatorComboBox.currentIndex() == 0:
            self.item_id = None
        else:
            with self.bento.db_sessionMaker() as db_sess:
                investigators = db_sess.query(Investigator).all()
                # -1 in the next two lines due to "New Investigator" first entry in combo box
                if len(investigators) >= self.ui.investigatorComboBox.count()-1:
                    investigator = investigators[self.ui.investigatorComboBox.currentIndex()-1]
                    self.item_id = investigator.id
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
