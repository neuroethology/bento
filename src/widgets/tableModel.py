# tableModel.py

from PySide2.QtCore import QAbstractTableModel, QModelIndex
from PySide2.QtGui import Qt, QColor
import operator

class TableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        super().__init__(parent, *args)
        self.mylist = mylist
        self.header = header
        self.colorRoleColumns = set()

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if role not in (Qt.DisplayRole, Qt.BackgroundRole):
            return None
        row = self.mylist[index.row()]
        if isinstance(row, (tuple, list)):
            datum = row[index.column()]
        elif isinstance(row, dict):
            datum = row[self.header[index.column()]]
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        if (index.column() in self.colorRoleColumns) and (role == Qt.BackgroundRole):
            return QColor(datum)
        elif (index.column() not in self.colorRoleColumns) and (role == Qt.DisplayRole):
            return datum
        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]

    def sort(self, col, order):
        """ sort table by given column number col """
        if len(self.mylist) == 0:
            return
        self.layoutAboutToBeChanged.emit()
        if isinstance(self.mylist[0], dict):
            col = self.header[col]
        self.mylist = sorted(
            self.mylist,
            key=lambda elem: elem[col].name() if isinstance(elem[col], QColor) else elem[col],
            reverse=(order == Qt.DescendingOrder)
            )
        self.layoutChanged.emit()

    def appendData(self, newData):
        print(f"appendData: adding {newData}")
        rows = len(self.mylist)
        columns = len(self.header)
        new_rows = len(newData)
        first_new_index = self.index(rows, 0)
        last_new_index = self.index(rows + new_rows, columns-1)
        self.beginInsertRows(QModelIndex(), rows, rows + new_rows)
        self.mylist.append(newData)
        self.endInsertRows()
        self.dataChanged.emit(
            first_new_index,
            last_new_index,
            [Qt.DisplayRole])

    def __iter__(self):
        return TableModelIterator(self.mylist)

    def setColorRoleColumn(self, column):
        self.colorRoleColumns.add(column)

    def clearColorRoleColumn(self, column):
        self.colorRoleColumns.discard(column)

class EditableTableModel(TableModel):
    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if (len(self.mylist) < index.row()+1 or
            not isinstance(self.mylist[index.row()], (list, dict)) or
            len(self.mylist[index.row()]) < index.column()+1
            ):
            raise RuntimeError("Index is out of range")
        row = self.mylist[index.row()]
        if isinstance(row, list):
            row[index.column()] = value
        elif isinstance(row, dict):
            row[self.header[index.column()]] = value
            row['dirty'] = True
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        # self.dataChanged.emit()
        return True

    def isDirty(self, index):
        # has "dirty' key and its value is True
        print(f"EditableTableModel.isDirty(): index = {index}")
        return 'dirty' in self.mylist[index.row()] and self.mylist[index.row()]['dirty']

    def setDirty(self, index):
        self.mylist[index.row()]['dirty'] = True

    def clearDirty(self, index):
        self.mylist[index.row()]['dirty'] = False

class TableModelIterator():
    def __init__(self, mylist):
        print("Creating TableModelIterator")
        self.mylist = mylist
        self.ix = 0

    def __iter__(self):
        self.ix = 0
        return self

    def __next__(self):
        if self.ix >= len(self.mylist):
            raise StopIteration
        item = self.mylist[self.ix]
        print(f"TableModelIterator.__next__ called with ix {self.ix}, item is {item}")
        self.ix += 1
        return item

