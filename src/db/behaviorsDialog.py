# behaviorsDialog.py

from db.behaviorsDialog_ui import Ui_BehaviorsDialog
from annot.behavior import Behavior, Behaviors
from PySide2.QtCore import QModelIndex, QSortFilterProxyModel, Signal, Slot
from PySide2.QtGui import Qt, QIntValidator
from PySide2.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QHeaderView, QMessageBox, QTableView
from widgets.tableModel import EditableTableModel
from os.path import expanduser, sep
# from caiman.utils.utils import load_dict_from_hdf5

class CheckableTableModel(EditableTableModel):
    def isCheckboxColumn(self, index):
        return (
            self.header[index.column()].lower() == 'visible' or
            self.header[index.column()].lower() == 'active'
            )

    def flags(self, index):
        f = super().flags(index)
        if self.isCheckboxColumn(index):
            return (f & ~Qt.ItemIsSelectable) | Qt.ItemIsUserCheckable
        return f

    def data(self, index, role):
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if role == Qt.CheckStateRole:
            row = self.mylist[index.row()]
            if isinstance(row, (tuple, list)):
                datum = row[index.column()]
            elif isinstance(row, dict):
                datum = row[self.header[index.column()]]
            else:
                raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
            if isinstance(datum, QCheckBox):
                if datum.isChecked():
                    return Qt.Checked
                else:
                    return Qt.Unchecked
        if self.isCheckboxColumn(index):
            return None
        return super().data(index, role)

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole and (
            self.header[index.column()].lower() == 'visible' or
            self.header[index.column()].lower() == 'active'):
            row = self.mylist[index.row()]
            if isinstance(row, list):
                item = row[index.column()]
            elif isinstance(row, dict):
                item = row[self.header[index.column()]]
            else:
                raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
            if not isinstance(item, QCheckBox):
                raise RuntimeError(f"Expected item of type QCheckBox, got {type(item)} instead")
            item.setChecked(bool(value))
            self.dataChanged.emit(index, index)
            return True
        return super().setData(index, value, role)

    def sort(self, col, order):
        # can't sort "visible" or "active" columns
        self.currentSortCol = col
        self.currentSortOrder = order
        if self.header[col].lower() == "visible" or self.header[col].lower() == "active":
            return
        return super().sort(col, order)

class CheckboxFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.filterActive = False
        self.filterColumn = None
        self.currentSortCol = -1
        self.currentSortOrder = Qt.AscendingOrder
        self.setFilterRole(Qt.ItemIsUserCheckable)
        self.setDynamicSortFilter(False)

    def __iter__(self):
        return CheckboxFilterProxyModelIterator(self)

    def setSourceModel(self, model):
        super().setSourceModel(model)
        if model:
            self.sourceModel().dataChanged.connect(self.noteDataChanged)

    def setFilterColumn(self, col):
        if col != self.filterColumn:
            self.filterColumn = col
            self.invalidateFilter()
            self.sort(self.currentSortCol, self.currentSortOrder)
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(self.sourceModel().rowCount(None)-1, self.sourceModel().columnCount(None)-1)
                )

    def setFilterActive(self, active):
        active = bool(active)
        if active != self.filterActive:
            self.filterActive = active
            self.invalidateFilter()
            self.sort(self.currentSortCol, self.currentSortOrder)
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(self.sourceModel().rowCount(None)-1, self.sourceModel().columnCount(None)-1)
                )

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not self.filterActive or self.filterColumn == None:
            return True
        srcIdx = self.sourceModel().index(source_row, self.filterColumn)
        if isinstance(srcIdx.data(), QCheckBox):
            return srcIdx.data().isChecked()
        elif srcIdx.data() is None:
            return False
        else:
            print(f"Unexpected data type: {type(srcIdx.data())}")
        return True

    def isDirty(self, index):
        srcIndex = self.mapToSource(index)
        return self.sourceModel().isDirty(srcIndex)

    def sort(self, col, order):
        self.currentSortCol = col
        self.currentSortOrder = order
        super().sort(col, order)

    @Slot(QModelIndex, QModelIndex)
    def noteDataChanged(self, indexStart, indexEnd):
        self.invalidateFilter()
        self.sort(self.currentSortCol, self.currentSortOrder)
        self.dataChanged.emit(self.mapFromSource(indexStart), self.mapFromSource(indexEnd))

    def removeRowSet(self, rows):
        srcRows = {self.mapToSource(self.index(row, 0)).row() for row in rows}
        self.sourceModel().removeRowSet(srcRows)

class CheckboxFilterProxyModelIterator():
    def __init__(self, model):
        self.model = model

    def __iter__(self):
        self.sourceIter = iter(self.model.sourceModel())
        self.ix = 0
        return self

    def __next__(self):
        item = next(self.sourceIter)
        while not self.model.filterAcceptsRow(self.ix, None):
            self.ix += 1
            item = next(self.sourceIter)
        self.ix += 1
        return item

class BehaviorsDialog(QDialog):

    quitting = Signal()
    trialsChanged = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_BehaviorsDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.quitting.connect(self.bento.quit)

        self.base_model = self.createBehaviorsTableModel()
        self.proxy_model = CheckboxFilterProxyModel()
        self.proxy_model.setSourceModel(self.base_model)
        activeColumn = None
        try:
            activeColumn = self.base_model.header.index("active")
        except ValueError:
            pass
        self.proxy_model.setFilterColumn(activeColumn)

        self.ui.hideInactiveBehaviorsCheckBox.stateChanged.connect(self.updateRowVisibility)
        self.updateRowVisibility(self.ui.hideInactiveBehaviorsCheckBox.isChecked())
        self.setBehaviorsModel(self.proxy_model)
        self.proxy_model.sort(self.base_model.header.index("name"), Qt.AscendingOrder)

    # Behaviors Data

    def setBehaviorsModel(self, model):
        oldModel = self.ui.behaviorsTableView.selectionModel()
        self.ui.behaviorsTableView.setModel(model)
        self.ui.behaviorsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.behaviorsTableView.resizeColumnsToContents()
        self.ui.behaviorsTableView.setSortingEnabled(True)
        self.ui.behaviorsTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def createBehaviorsTableModel(self):
        header = self.bento.behaviors.header()
        header.extend(["visible", "active"])
        data_list = []
        for behavior in self.bento.behaviors:
            behaviorDict = behavior.toDict()
            visibilityCheckBox = QCheckBox("visible")
            visibilityCheckBox.setChecked(True)
            behaviorDict['visible'] = visibilityCheckBox
            activeCheckBox = QCheckBox("active")
            activeCheckBox.setChecked(False)
            behaviorDict['active'] = activeCheckBox
            data_list.append(behaviorDict)
        model = CheckableTableModel(self, data_list, header)
        model.setImmutable(header.index('name'))
        for column in self.bento.behaviors.colorColumns():
            model.setColorRoleColumn(column)
        return model

    @Slot(int)
    def updateRowVisibility(self, filterRows):
        self.proxy_model.setFilterActive(bool(filterRows))

    def updateBehaviors(self):
        """
        Update Bento's active behaviors based on the changes made to "Active" checkboxes
        in this dialog.  Remove annotations that use behaviors that are being made
        inactive.
        """
        model = self.ui.behaviorsTableView.model().sourceModel()
        for ix, entry in enumerate(iter(model)):
            tableIndex = model.createIndex(ix, 0)
            if model.isDirty(tableIndex):
                print(f"item at row {ix} is dirty")
                beh = self.bento.behaviors.get(entry['name'])
                # update color and hotkey
                beh.set_color(entry['color'])
                beh.set_hot_key(entry['hot_key'])
                # update visibility
                beh.set_visible(entry['visible'].isChecked())
                # update active
                active = entry['active'].isChecked()
                if not active:
                    self.bento.annotations.delete_all_bouts(entry['name'])
                beh.set_active(active)
                # if the behavior is being made inactive, delete bouts using this behavior
                model.clearDirty(tableIndex)
            # else:
            #     print(f"item at row {ix} wasn't dirty, so did nothing")

    def keyPressEvent(self, event):
        """
        Handle key press events in the dialog (but not individual items)
        """
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.deleteRows()
            event.accept()

    def deleteRows(self):
        """
        Delete all the selected rows from the model
        """
        model = self.ui.behaviorsTableView.model()
        rows = {index.row() for index in self.ui.behaviorsTableView.selectedIndexes()}
        model.removeRowSet(rows)
        self.ui.behaviorsTableView.clearSelection()

    @Slot()
    def accept(self):
        self.bento.saveBehaviors()
        # super().accept()  # don't close the window on accept

    @Slot()
    def reject(self):
        #TODO: Figure out a way to cancel updates.  Maybe an undo facility?
        pass
        # super().reject()  # don't close the window on reject (== discard, cancel)

    @Slot()
    def apply(self):
        """
        Update Bento's group of active behaviors per changes to the table in this dialog
        """
        self.updateBehaviors()

    @Slot()
    def toggleVisibility(self):
        if self.isVisible():
            self.geometry = self.saveGeometry()
            print(f"geometry: {self.geometry}, type: {type(self.geometry)}")
        else:
            pass
            self.restoreGeometry(self.geometry)
        self.setVisible(not self.isVisible())
