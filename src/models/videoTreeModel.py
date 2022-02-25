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

from qtpy.QtCore import QAbstractItemModel, QModelIndex, Qt
from db.schema_sqlalchemy import VideoData, PoseData

class VideoTreeModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self._rows = []
        self._header = VideoData.keys

    # def flags(self, index):
    #     flags = super().flags(index)
    #     if index.column() not in self.immutableColumns:
    #         flags |= Qt.ItemIsEditable
    #     return flags

    def rowCount(self, parent):
        return len(self._rows)

    def columnCount(self, parent):
        return len(self._header)

    def data(self, index, role):
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if role not in (Qt.DisplayRole, Qt.BackgroundRole, Qt.EditRole):
            return None
        print(f"Index row: {index.row()}, column: {index.column()}, role: {role}")
        row = self._rows[index.row()]
        if isinstance(row, (tuple, list)):
            datum = row[index.column()]
        elif isinstance(row, dict):
            datum = row[self._header[index.column()]]
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        if role in (Qt.DisplayRole, Qt.EditRole):
            return str(datum)
        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[col]

    # def sort(self, col, order):
    #     """ sort table by given column number col """
    #     if len(self.mylist) == 0:
    #         return
    #     self.layoutAboutToBeChanged.emit()
    #     if isinstance(self.mylist[0], dict):
    #         col = self.header[col]
    #     self.mylist = sorted(
    #         self.mylist,
    #         key=lambda elem: elem[col].name() if isinstance(elem[col], QColor) else elem[col],
    #         reverse=(order == Qt.DescendingOrder)
    #         )
    #     self.layoutChanged.emit()

    def index(self, row, column, parent=QModelIndex()):
        # if row >= len(self._rows) or column >= len(self._header):
        #     return QModelIndex()
        if parent != QModelIndex():
            print(f"videoTreeModel: index called with parent {parent}")
        return self.createIndex(row, column, self)

    def parent(self, child):
        return QModelIndex()

    def appendData(self, newData):
        rows = len(self._rows)
        columns = len(self._header)
        new_rows = len(newData)
        first_new_index = self.index(rows, 0)
        last_new_index = self.index(rows + new_rows, columns-1)
        self.beginInsertRows(first_new_index, rows, rows + new_rows)
        self._rows.append(newData)
        self.endInsertRows()
        self.dataChanged.emit(
            first_new_index,
            last_new_index,
            [Qt.DisplayRole])

    def setData(self, index, value, role=Qt.EditRole):
        print(f"setData called with index ({index.row()}, {index.column()}), value {value}")
        if not isinstance(index, QModelIndex) or not index.isValid():
            raise RuntimeError("Index is not valid")
        if (len(self._rows) < index.row()+1 or
            not isinstance(self._rows[index.row()], (list, dict)) or
            len(self._rows[index.row()]) < index.column()+1
            ):
            raise RuntimeError("Index is out of range")
        row = self._rows[index.row()]
        if isinstance(row, list):
            print("(list)")
            row[index.column()] = value
        elif isinstance(row, dict):
            key = self._header[index.column()]
            print(f"(dict) key = {key}")
            row[self._header[index.column()]] = value
            row['dirty'] = True
            print(f"row value: {row[key]}, mylist value: {self._rows[index.row()][key]}")
        else:
            raise RuntimeError(f"Can't handle indexing with data of type {type(row)}")
        # self.dataChanged.emit()
        return True

    def isDirty(self, index):
        # has 'dirty' key and its value is True
        return 'dirty' in self._rows[index.row()] and self._rows[index.row()]['dirty']

    def setDirty(self, index):
        self._rows[index.row()]['dirty'] = True

    def clearDirty(self, index):
        self._rows[index.row()]['dirty'] = False

    # def isImmutable(self, index):
    #     return index.column() in self.immutableColumns

    # def setImmutable(self, column):
    #     self.immutableColumns.add(column)



