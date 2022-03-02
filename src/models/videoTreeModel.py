# videoTreeModel.py

"""
This model provides a way to represent video data, including
associated pose data, in a form suitable for a QTreeView to
display it.

Each root-level row is represented by a dictionary, with a
key for each column.  A separate header list is used to
provide the order of the columns. The model data is a list
of these dictionaries.

The "pose_data" key is a list of pose_data dicts, which are
displayed in the treeView as children of the row
"""

from numpy import isin
from qtpy.QtCore import QAbstractItemModel, QModelIndex, Qt
from db.schema_sqlalchemy import VideoData, PoseData

class TreeItem:
    """
    Generic tree item for use in a Qt TreeModel derived from QAbstractItemModel (below)
    Index.row(i) accesses self._child[i]
    Index.column(j) indexes into elements of self._data.
    """
    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        self._data = {}
        self._dataKeys = None

    def appendChild(self, child):
        if not isinstance(child, TreeItem):
            raise TypeError(f"TreeItem.appendChild expected a TreeItem, got a {type(child)}")
        self._children.append(child)
    
    def childCount(self):
        return len(self._children)

    def columnCount(self):
        if not self._dataKeys:
            raise RuntimeError("columnCount called before dataKeys were set")
        return len(self._dataKeys)

    def data(self, column):
        if column < 0 or column >= self.columnCount():
            return None
        return self._data[self._dataKeys[column]]

    def setDataKeys(self, dataKeys):
        self._dataKeys = dataKeys

    def setDataDict(self, dataDict):
        self._data = dataDict

    def setData(self, column, data):
        if column < 0 or column >= self.columnCount():
            return
        self._data[self._dataKeys[column]] = data

    def child(self, row):
        if row < 0 or row >= self.childCount():
            return None
        return self._children[row]
    
    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._children.indexOf(self)
        return 0

class VideoTreeModel(QAbstractItemModel):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._header = VideoData.keys
        self._root = TreeItem()
        self._root.setDataKeys(self._header)

    def flags(self, index):
        if not isinstance(index, QModelIndex):
            raise TypeError(f"flags expected QModelIndex, got {type(index)}")
        if not index.isValid():
            return Qt.NoItemFlags
        flags = super().flags(index)
        flags |= Qt.ItemIsEditable
        return flags

    def rowCount(self, parent:QModelIndex = QModelIndex()):
        if not isinstance(parent, QModelIndex):
            raise TypeError(f"rowCount: expected parent to be a QModelIndex, got a {type(parent)}")
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent):
        if not isinstance(parent, QModelIndex):
            raise TypeError(f"columnCount: expected parent to ba a QModelIndex, got a {type(parent)}")
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self._root.columnCount()

    def index(self, row, column, parent=QModelIndex()):
        if not isinstance(parent, QModelIndex):
            raise TypeError(f"index: expected parent to be a QModelIndex, got a {type(parent)}")
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer
        
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def data(self, index, role):
        if not isinstance(index, QModelIndex):
            raise TypeError(f"data() expected index, got {type(index)}")
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[col]
        return None

    def parent(self, index):
        if not isinstance(index, QModelIndex):
            raise TypeError(f"parent: expected a QModelIndex, got a {type(index)}")
        if not index.isValid():
            return QModelIndex()
        item = index.internalPointer()
        parent = item.parent()
        if parent == self._root:
            return QModelIndex()
        return self.createIndex(parent.row(), 0, parent)

    def appendData(self, newData, parent=None):
        if not parent:
            parent = self._root
        if not isinstance(newData, (tuple, list)):
            newData = [newData]
        new_rows = len(newData)
        rows = parent.childCount()
        columns = len(self._header)
        first_new_index = self.index(rows, 0)
        last_new_index = self.index(rows + new_rows, columns-1)
        self.beginInsertRows(first_new_index, rows, rows + new_rows)
        for newDataDict in newData:
            if not isinstance(newDataDict, dict):
                raise TypeError(f"appendData expected dict, got {type(newDataDict)}")
            newChild = TreeItem(parent)
            newChild.setDataKeys(self._header)
            newChild.setDataDict(newDataDict)
            parent.appendChild(newChild)
        self.endInsertRows()
        self.dataChanged.emit(
            first_new_index,
            last_new_index,
            [Qt.DisplayRole])

    def setData(self, index, value, role=Qt.EditRole):
        if not isinstance(index, QModelIndex):
            raise TypeError(f"data() expected index, got {type(index)}")
        if not index.isValid() or role != Qt.EditRole:
            return False
        item = index.internalPointer()
        item.setData(index.column(), value)
        return True

    # def isDirty(self, index):
    #     # has 'dirty' key and its value is True
    #     return 'dirty' in self._rows[index.row()] and self._rows[index.row()]['dirty']

    # def setDirty(self, index):
    #     self._rows[index.row()]['dirty'] = True

    # def clearDirty(self, index):
    #     self._rows[index.row()]['dirty'] = False

    # def isImmutable(self, index):
    #     return index.column() in self.immutableColumns

    # def setImmutable(self, column):
    #     self.immutableColumns.add(column)



