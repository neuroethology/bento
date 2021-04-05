# tableModel.py

from PySide2.QtCore import QAbstractTableModel, SIGNAL
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
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
    def sort(self, col, order):
        """ sort table by given column number col """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist == sorted(self.mylist, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))
