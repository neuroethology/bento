# animalDialog.py

from db.schema_sqlalchemy import Animal, Investigator, SexEnum, Surgery
from db.animalDialog_ui import Ui_AnimalDialog
from db.surgeryDialog import SurgeryDialog
from db.dispositionItemsDialog import DispositionItemsDialog, CANCEL_OPERATION, DELETE_ITEMS, NOTHING_TO_DO
from db.dbDialog import DBDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import QIntValidator
from qtpy.QtWidgets import (QDialog, QDialogButtonBox, QAbstractItemView, QHeaderView,
    QMessageBox)

from models.tableModel import TableModel
import datetime

class AnimalDialog(DBDialog):
    """
    A dialog widget for viewing, adding, deleting and editing instances of Animal
    data in Bento's experiments database.

    This class derives from the DBDialog class, so it needs to provide a dialogConfig dict,
    but the operation of the AnimalDialog differs enough from other similar database fields
    that this class implements most of its own functionality.

    The key additional need is to support the viewing and editing the surgery log.
    """

    quitting = Signal()

    def __init__(self, bento):
        """
        Construct and return an instance of the AnimalDialog class.

        Since the Animal db class mostly implements its own functionality, the it doesn't call some of the parameterized functions
        provided by DBDialog, and so the dialogConfig doesn't need to provide as many parameterizations.  The dialogConfig dict
        for AnimalDialog only defines these dialogConfig keys:
        - newItemName
        - dbClass
        - selectionKey
        - newOwnerAttr
        """
        dialogConfig = {
            'newItemName': "New Animal",
            'dbClass': "Animal",
            'selectionKey': "animal_id",
            'newOwnerAttr': 'animal_id'
        }
        super().__init__(bento, dialogConfig, Ui_AnimalDialog())
        self.ui.asiLineEdit.setValidator(QIntValidator())

        with self.bento.db_sessionMaker() as db_sess:
            username = self.bento.config.username()
            query = db_sess.query(Investigator).distinct()
            investigators = query.all()
            self.ui.investigatorComboBox.addItems([elem.user_name for elem in investigators])
            self.ui.investigatorComboBox.setEditable(False)
            self.ui.investigatorComboBox.setCurrentText(username) # may not exist
        self.investigatorChanged()
        self.ui.investigatorComboBox.currentIndexChanged.connect(self.investigatorChanged)
        self.animal_id = None
        self.ui.addSurgeryPushButton.clicked.connect(self.addSurgeryAction)
        self.ui.buttonBox.clicked.connect(self.update)

    def populateAnimalTable(self, investigator_id, db_sess):
        """
        Populate the animalTableView UI element.

        When a new row is selected, trigger populateFields to populate the other fields with
        data for the selected animal.
        """
        results = db_sess.query(Animal).filter(Animal.investigator_id == investigator_id).all()
        header = ['id', 'Animal Services ID', 'Nickname', 'Date of Birth', 'Sex', 'Genotype']
        data_list = [(
            elem.id,
            elem.animal_services_id,
            elem.nickname,
            elem.dob.isoformat(),
            elem.sex.value,
            elem.genotype
            ) for elem in results]
        data_list.insert(0, (None, None, "New Animal", "", "", ""))
        oldModel = self.ui.animalTableView.selectionModel()
        # prevent unwanted side effects while we're populating the combo box
        if oldModel:
            oldModel.blockSignals(True)
        model = TableModel(self, data_list, header)
        self.ui.animalTableView.setModel(model)
        self.ui.animalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.animalTableView.resizeColumnsToContents()
        self.ui.animalTableView.hideColumn(0)   # don't show the animal's ID field, but we need it for Load
        self.ui.animalTableView.setSortingEnabled(False)
        self.ui.animalTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.animalTableView.setAutoScroll(False)
        selectionModel = self.ui.animalTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateFields)
        if oldModel:
            oldModel.deleteLater()

    @Slot()
    def investigatorChanged(self):
        """
        Handle the situation when the user selects a different investigator, which involves starting
        over, repopulating the dialog's main animal table.
        """
        username = self.ui.investigatorComboBox.currentText()
        with self.bento.db_sessionMaker() as db_sess:
            investigators = db_sess.query(Investigator).filter(Investigator.user_name == username).distinct().all()
            if investigators:
                if len(investigators) > 1:
                    QMessageBox.warning(
                        self,
                        "Duplicate Investigators",
                        "Multiple investigators have the same selected investigator username.\n"
                        "I'll use the first one I found, but you should clean that up!"
                    )
                self.investigator_id = investigators[0].id
                self.populateAnimalTable(self.investigator_id, db_sess)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Investigator",
                    "The selected investigator doesn't exist in the database."
                    )
        self.ui.animalTableView.selectRow(0)

    def clearFields(self):
        """
        Clear all of UI fields that are specific to a particular animal, e.g. when
        no animal is currently selected.
        """
        self.ui.nicknameLineEdit.clear()
        self.ui.asiLineEdit.clear()
        self.ui.dobDateEdit.setDate(datetime.date.today())
        self.ui.unknownRadioButton.click()
        self.ui.genotypeLineEdit.clear()
        oldModel = self.ui.surgeryTableView.selectionModel()
        self.ui.surgeryTableView.setModel(None)
        if oldModel:
            oldModel.deleteLater()

    def populateFields(self):
        """
        Populate the dialog box fields specific to a particular animal in response
        to a different animal being selected in the main animal table.
        """
        animal_id = None
        current_animal_row = self.ui.animalTableView.currentIndex().row()
        if current_animal_row > 0:  # not "New Animal" row
            animal_id = self.ui.animalTableView.currentIndex().siblingAtColumn(0).data()
        if animal_id:
            with self.bento.db_sessionMaker() as db_sess:
                animal = db_sess.query(Animal).filter(Animal.id == animal_id).scalar()
                if not animal:
                    print("Invalid animal ID")
                    return
                self.ui.nicknameLineEdit.setText(animal.nickname)
                self.ui.asiLineEdit.setText(str(animal.animal_services_id))
                self.ui.dobDateEdit.setDate(animal.dob)
                sex = animal.sex
                if sex == SexEnum.M:
                    self.ui.maleRadioButton.click()
                elif sex == SexEnum.F:
                    self.ui.femaleRadioButton.click()
                else:
                    self.ui.unknownRadioButton.click()
                self.ui.genotypeLineEdit.setText(animal.genotype)
                self.populateSurgeryLog(animal_id, db_sess)
            self.animal_id = animal_id
            self.ui.addSurgeryPushButton.setDisabled(False)
        else:
            self.animal_id = None
            self.clearFields()
            self.ui.addSurgeryPushButton.setDisabled(True)

    def populateSurgeryLog(self, animal_id, db_sess):
        """
        Populate the surgery log for the selected animal.
        """
        results = db_sess.query(Surgery).filter(Surgery.animal_id == animal_id).all()
        header = ['Date', 'Implant Side', 'Injection Side', 'Procedure', 'Anesthesia', 'Follow-up Care']
        data_list = [(
            elem.date.isoformat(),
            elem.implant_side.value,
            elem.injection_side.value,
            elem.procedure,
            elem.anesthesia,
            elem.follow_up_care
            ) for elem in results]
        oldModel = self.ui.surgeryTableView.selectionModel()
        model = TableModel(self, data_list, header)
        self.ui.surgeryTableView.setModel(model)
        self.ui.surgeryTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.surgeryTableView.resizeColumnsToContents()
        self.ui.surgeryTableView.setSortingEnabled(False)
        self.ui.surgeryTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.surgeryTableView.setAutoScroll(False)
        selectionModel = self.ui.surgeryTableView.selectionModel()
        selectionModel.selectionChanged.connect(self.populateFields)
        if oldModel:
            oldModel.deleteLater()

    @Slot()
    def addSurgeryAction(self):
        """
        Display the SurgeryDialog to add a new surgery item.

        When the SurgeryDialog returns, repopulate the surgery log field of the AnimalDialog
        to reflect the new or edited data.
        """
        surgeryDialog = SurgeryDialog(self.bento, self.investigator_id, self.animal_id)
        surgeryDialog.exec()
        with self.bento.db_sessionMaker() as db_sess:
            self.populateSurgeryLog(self.animal_id, db_sess)

    @Slot(object)
    def update(self, button) -> bool:   # returns successful update
        """
        Update the database with new or edited data for this animal.

        Args:
            button: The UI button that was clicked to close the dialog.

        Returns:
            Whether the database was successfully updated or not.
        """
        buttonRole = self.ui.buttonBox.buttonRole(button)
        if not self.investigator_id:
            QMessageBox.warning(self, "Warning", "No valid investigator.  Please select one.")
            return False
        need_commit = False
        need_to_add = False
        with self.bento.db_sessionMaker() as db_sess:
            animals = None
            if self.animal_id:
                animals = db_sess.query(Animal).filter(Animal.id == self.animal_id).all()
                if not animals:
                    QMessageBox.critical(self, "Internal Error", "No animal in database matching selection.")
                    return False
            if buttonRole == QDialogButtonBox.ActionRole:
                # delete the selected animal(s)
                default_action = None
                for animal in animals:
                    # disposition any sessions this animal participated in
                    result = self.dispositionOwnedItems(animal.sessions,
                        "sessions",
                        db_sess,
                        default_action)
                    if result == CANCEL_OPERATION:
                        return False
                    # delete the animal from the database
                    db_sess.delete(animal)
                    db_sess.commit()
                    self.animal_id = None
                self.showSelected()
                self.populateAnimalTable(self.investigator_id, db_sess)
            elif (buttonRole == QDialogButtonBox.AcceptRole or
                buttonRole == QDialogButtonBox.ApplyRole):
                if not animals:
                    if (not self.ui.asiLineEdit.text() and
                        not self.ui.genotypeLineEdit.text() and
                        not self.ui.nicknameLineEdit.text()):
                        return True
                    if not (self.ui.asiLineEdit.text() and self.ui.nicknameLineEdit.text()):
                        QMessageBox.warning(
                            self,
                            "Requirements",
                            "You must supply at least an Animal Services ID and a nickname")
                        return False
                    animal = Animal()
                    need_to_add = True
                    need_commit = True
                else:
                    animal = animals[0]

                if animal.investigator_id != self.investigator_id:
                    animal.investigator_id = self.investigator_id
                    need_commit = True
                if animal.nickname != self.ui.nicknameLineEdit.text():
                    animal.nickname = self.ui.nicknameLineEdit.text()
                    need_commit = True
                if animal.animal_services_id != int(self.ui.asiLineEdit.text()):
                    animal.animal_services_id = int(self.ui.asiLineEdit.text())
                    need_commit = True
                if animal.dob != self.ui.dobDateEdit.date().toPython():
                    animal.dob = self.ui.dobDateEdit.date().toPython()
                    need_commit = True
                if not (
                    animal.sex == SexEnum.M and self.ui.maleRadioButton.isChecked() or
                    animal.sex == SexEnum.F and self.ui.femaleRadioButton.isChecked() or
                    animal.sex == SexEnum.U and self.ui.unknownRadioButton.isChecked()
                    ):
                    if self.ui.maleRadioButton.isChecked():
                        animal.sex = SexEnum.M
                    elif self.ui.femaleRadioButton.isChecked():
                        animal.sex = SexEnum.F
                    else:
                        animal.sex = SexEnum.U
                    need_commit = True
                if animal.genotype != self.ui.genotypeLineEdit.text():
                    animal.genotype = self.ui.genotypeLineEdit.text()
                    need_commit = True
                if need_to_add:
                    db_sess.add(animal)
                if need_commit:
                    db_sess.commit()
                    db_sess.flush()
                self.populateAnimalTable(self.investigator_id, db_sess)
                self.animal_id = None
                self.clearFields()
                return True

    # @Slot()
    # def accept(self):
    #     super().accept()

    # @Slot()
    # def reject(self):
    #     super().reject()
