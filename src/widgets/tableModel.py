# tableModel.py

from PySide2.QtCore import QAbstractTableModel, QModelIndex, SIGNAL
from PySide2.QtGui import Qt
import operator

class TableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        super().__init__(parent, *args)
        self.mylist = mylist
        self.header = header
            
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.header)
    def data(self, index, role):
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if role != Qt.DisplayRole:
            return None
        row = self.mylist[index.row()]
        if isinstance(row, (tuple, list)):
            return row[index.column()]
        elif isinstance(row, dict):
            return row[self.header[index.column()]]
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
    def sort(self, col, order):
        """ sort table by given column number col """
        self.layoutAboutToBeChanged.emit()
        self.mylist == sorted(self.mylist, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.layoutChanged.emit()
    def appendData(self, newData):
        print(f"appendData: adding {newData}")
        rows = len(self.mylist)
        columns = len(self.header)
        self.mylist.append(newData)
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(rows+1, columns-1),
            [Qt.DisplayRole])
    def getIterator(self):
        return TableModelIterator(self.mylist)

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
        return 'dirty' in self.mylist[index.row()] and self.mylist[index.row()]['dirty']

    def setDirty(self, index):
        self.mylist[index.row()]['dirty'] = True
    def clearDirty(self, index):
        self.mylist[index.row()]['dirty'] = False

class TableModelIterator():
    def __init__(self, mylist):
        print(f"creating TableModelIterator with mylist = {mylist}")
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

