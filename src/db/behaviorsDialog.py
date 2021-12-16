# behaviorsDialog.py

from annot.behavior import Behavior
from db.behaviorsDialog_ui import Ui_BehaviorsDialog
from qtpy.QtCore import (QAbstractItemModel, QModelIndex, QPersistentModelIndex,
    QSortFilterProxyModel, Signal, Slot)
from qtpy.QtGui import QColor, QIntValidator, Qt
from qtpy.QtWidgets import (QColorDialog, QDialog, QHeaderView, QLineEdit,
    QMessageBox, QStyledItemDelegate, QStyleOptionViewItem, QWidget)
from os.path import expanduser, sep
from typing import List, Union

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
            self.sourceModel().layoutChanged.connect(self.noteLayoutChanged)

    def setFilterColumn(self, col):
        if col != self.filterColumn:
            self.filterColumn = col
            self.invalidateFilter()
            self.sort(self.currentSortCol, self.currentSortOrder)
            self.layoutChanged.emit()

    def setFilterActive(self, active):
        active = bool(active)
        if active != self.filterActive:
            self.filterActive = active
            self.invalidateFilter()
            self.sort(self.currentSortCol, self.currentSortOrder)
            self.layoutChanged.emit()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not self.filterActive or self.filterColumn == None:
            return True
        srcIdx = self.sourceModel().index(source_row, self.filterColumn)
        datum = srcIdx.data(role=Qt.CheckStateRole)
        if isinstance(datum, int):
            return bool(datum)
        elif srcIdx.data() is None:
            return False
        else:
            print(f"Unexpected data type: {type(srcIdx.data())}")
        return True

    def sort(self, col, order):
        self.currentSortCol = col
        self.currentSortOrder = order
        super().sort(col, order)

    @Slot(QModelIndex, QModelIndex)
    def noteDataChanged(self, indexStart, indexEnd):
        self.invalidateFilter()
        self.sort(self.currentSortCol, self.currentSortOrder)
        self.dataChanged.emit(self.mapFromSource(indexStart), self.mapFromSource(indexEnd))

    @Slot(list)
    def noteLayoutChanged(self, parents=list(), hint=QAbstractItemModel.NoLayoutChangeHint):
        self.invalidateFilter()
        self.sort(self.currentSortCol, self.currentSortOrder)
        self.layoutChanged.emit(parents=parents, hint=hint)

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

class BehaviorItemDelegate(QStyledItemDelegate):
    """
    Delegate class that renders QColor objects as colors
    and instantiates a QColorDialog when the user wants to edit them.
    Most everything else is handled by the QStyledItemDelegate superclass.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """
        Override behavior for QColor objects
        """
        if isinstance(index.data(), QColor):
            painter.fillRect(option.rect, index.data())
            return
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> QWidget:
        if isinstance(index.data(), QColor):
            editor = QColorDialog(index.data(), parent=parent)
            return editor
        editor = super().createEditor(parent, option, index)
        if (isinstance(editor, QLineEdit) and
            index.model().headerData(index.column(), Qt.Horizontal, Qt.DisplayRole) == 'hot_key'):
            editor.setInputMask('a')    # restrict user input to no more than a single upper or lower case character
        return editor

    def setModelData(self, editor, model, index):
        if isinstance(index.data(), QColor):
            if editor.result() == QDialog.Accepted:
                model.setData(index, editor.currentColor(), role=Qt.EditRole)
            return
        super().setModelData(editor, model, index)

class BehaviorsDialog(QDialog):

    quitting = Signal()
    trialsChanged = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_BehaviorsDialog()
        self.ui.setupUi(self)
        bento.quitting.connect(self.quit)
        self.quitting.connect(self.bento.quit)

        self.base_model = self.createBehaviorsTableModel()
        self.proxy_model = CheckboxFilterProxyModel()
        self.proxy_model.setSourceModel(self.base_model)
        try:
            activeColumn = self.base_model.header().index("active")
        except ValueError:
            activeColumn = None
        self.proxy_model.setFilterColumn(activeColumn)

        self.ui.hideInactiveBehaviorsCheckBox.stateChanged.connect(self.updateRowVisibility)
        self.ui.addBehaviorPushButton.clicked.connect(self.addNewRow)
        self.updateRowVisibility(self.ui.hideInactiveBehaviorsCheckBox.isChecked())
        self.setBehaviorsModel(self.proxy_model)
        self.proxy_model.sort(self.base_model.header().index("name"), Qt.AscendingOrder)

    # Behaviors Data

    def setBehaviorsModel(self, model):
        oldModel = self.ui.behaviorsTableView.selectionModel()
        self.ui.behaviorsTableView.setItemDelegate(BehaviorItemDelegate())
        self.ui.behaviorsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.behaviorsTableView.resizeColumnsToContents()
        self.ui.behaviorsTableView.setSortingEnabled(True)
        self.ui.behaviorsTableView.setAutoScroll(False)
        self.ui.behaviorsTableView.setModel(model)
        if oldModel:
            oldModel.deleteLater()

    def createBehaviorsTableModel(self):
        model = self.bento.behaviors
        header = model.header()
        # model.setImmutable(header.index('name'))
        return model

    @Slot(int)
    def updateRowVisibility(self, filterRows):
        self.proxy_model.setFilterActive(bool(filterRows))

    def keyPressEvent(self, event):
        """
        Handle key press events in the dialog (but not individual items)
        """
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.deleteRows()
            event.accept()

    def addNewRow(self):
        """
        Add a row to the model initialized as "New Behavior"
        """
        print(f"addNewRow: behaviors.len = {self.bento.behaviors.len()+1}")
        self.bento.behaviors.addIfMissing("New_Behavior")
        self.ui.behaviorsTableView.selectRow(0)

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
    def quit(self):
        self.done(0)

    @Slot()
    def toggleVisibility(self):
        if self.isVisible():
            self.geometry = self.saveGeometry()
        else:
            self.restoreGeometry(self.geometry)
        self.setVisible(not self.isVisible())
