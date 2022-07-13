# investigatorDialog.py

from db.investigatorDialog_ui import Ui_InvestigatorDialog
from db.dispositionItemsDialog import CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from db.dbDialog import DBDialog
from qtpy.QtCore import Qt, Signal, Slot
from qtpy.QtWidgets import QDialogButtonBox, QMessageBox

from db.schema_sqlalchemy import Investigator

class InvestigatorDialog(DBDialog):
    """
    Dialog Box class for access to the Investigator class in Bento's experiments database.

    This class derives from DBDialog, and only provides the configuration dict "dialogConfig".
    All actual implementation code is in the base class.
    """

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
                not ui.firstNameLineEdit.text() and
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
