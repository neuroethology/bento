# tableModel.py

from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt, QColor
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
        if role not in (Qt.DisplayRole, Qt.BackgroundRole, Qt.EditRole):
            return None
        row = self.mylist[index.row()]
        if isinstance(row, (tuple, list)):
            datum = row[index.column()]
        elif isinstance(row, dict):
            datum = row[self.header[index.column()]]
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        if (index.column() in self.colorRoleColumns) and (role == Qt.BackgroundRole or role == Qt.EditRole):
            return QColor(datum)
        elif (index.column() not in self.colorRoleColumns) and (role in (Qt.DisplayRole, Qt.EditRole)):
            return str(datum)
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
        rows = len(self.mylist)
        columns = len(self.header)
        new_rows = len(newData)
        first_new_index = self.index(rows, 0)
        last_new_index = self.index(rows + new_rows, columns-1)
        self.beginInsertRows(self.index(), rows, rows + new_rows)
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
    """
    Version of TableModel class that supports updating of the underlying data
    """
    def __init__(self, parent, mylist, header, *args):
        super().__init__(parent, mylist, header, *args)
        self.immutableColumns = set()

    def flags(self, index):
        flags = super().flags(index)
        if index.column() not in self.immutableColumns:
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role=Qt.EditRole):
        print(f"setData called with index ({index.row()}, {index.column()}), value {value}")
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if (len(self.mylist) < index.row()+1 or
            not isinstance(self.mylist[index.row()], (list, dict)) or
            len(self.mylist[index.row()]) < index.column()+1
            ):
            raise RuntimeError("Index is out of range")
        row = self.mylist[index.row()]
        if isinstance(row, list):
            print("(list)")
            row[index.column()] = value
        elif isinstance(row, dict):
            key = self.header[index.column()]
            print(f"(dict) key = {key}")
            row[self.header[index.column()]] = value
            row['dirty'] = True
            print(f"row value: {row[key]}, mylist value: {self.mylist[index.row()][key]}")
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        # self.dataChanged.emit()
        return True

    def isDirty(self, index):
        # has "dirty' key and its value is True
        return 'dirty' in self.mylist[index.row()] and self.mylist[index.row()]['dirty']

    def setDirty(self, index):
        self.mylist[index.row()]['dirty'] = True

    def clearDirty(self, index):
        self.mylist[index.row()]['dirty'] = False

    def isImmutable(self, index):
        return index.column() in self.immutableColumns

    def setImmutable(self, column):
        self.immutableColumns.add(column)

    def removeRowSet(self, rows):
        l = list(rows)
        l.sort()
        for row in reversed(l): # reversed so that the removal process doesn't change later indices
            self.beginRemoveRows(self.index(row, 0), row, row)
            del self.mylist[row]
            self.endRemoveRows()
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(len(self.mylist)-1, len(self.header)-1),
            [Qt.DisplayRole])

class TableModelIterator():
    def __init__(self, mylist):
        self.mylist = mylist
        self.ix = 0

    def __iter__(self):
        self.ix = 0
        return self

    def __next__(self):
        if self.ix >= len(self.mylist):
            raise StopIteration
        item = self.mylist[self.ix]
        self.ix += 1
        return item

