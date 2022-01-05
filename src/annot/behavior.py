# behavior.py
"""
Overview comment here
"""

from qtpy.QtCore import QAbstractItemModel, QAbstractTableModel, QModelIndex, QObject, Qt, Signal, Slot
from qtpy.QtGui import QColor
import os

class Behavior(QObject):
    """
    An annotation behavior, which is quite simple.  It comprises:
    name        The name of the behavior, which is displayed on various UI widgets
    hot_key     The case-sensitive key stroke used to start and stop instances of the behavior
    color       The color with which to display this behavior
    """

    def __init__(self, name: str, hot_key: str = '', color: QColor = None, active = False, visible = True):
        super().__init__()
        self._name = name
        self._hot_key = '' if hot_key == '_' else hot_key
        self._color = color
        self._visible = visible
        self._active = active
        self._get_functions = {
            'hot_key': self.get_hot_key,
            'name': self.get_name,
            'color': self.get_color,
            'active': self.is_active,
            'visible': self.is_visible
            }
        self._set_functions = {
            'hot_key': self.set_hot_key,
            'name': self.set_name,
            'color': self.set_color,
            'active': self.set_active,
            'visible': self.set_visible
            }

    def __repr__(self):
        return f"Behavior: name={self._name}, hot_key={self._hot_key}, color={self._color}, active={self._active}, visible={self._visible}"

    def get(self, key):
        # may raise KeyError
        return self._get_functions[key]()

    def set(self, key, value):
        # may raise KeyError
        self._set_functions[key](value)

    def get_hot_key(self):
        return self._hot_key

    def set_hot_key(self, hot_key: str):
        self._hot_key = hot_key

    def get_color(self):
        return self._color

    def set_color(self, color: QColor):
        self._color = color

    def is_active(self):
        return self._active

    @Slot(bool)
    def set_active(self, active):
        self._active = active

    def is_visible(self):
        return self._visible

    @Slot(bool)
    def set_visible(self, visible):
        self._visible = visible

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def toDict(self):
        return {
            'hot_key': '_' if self._hot_key == '' else self._hot_key,
            'color': self._color,
            'name': self._name,
            'active': self._active,
            'visible': self._visible
            }

class Behaviors(QAbstractTableModel):
    """
    A set of behaviors, which represent "all" possible behaviors.
    The class supports reading from and writing to profile files that specify
    the default hot_key and color for each behavior, along with the name.

    Derives from QAbstractTableModel so that it can be viewed and edited
    directly in a QTableView widget.

    Use getattr(name) to get the Behavior instance for a given name.
    Use from_hot_key(key) to get the behavior(s) given the hot key.
        Returns None if the hot_key isn't defined.
    """

    behaviors_changed = Signal()
    layout_changed = Signal()

    def __init__(self):
        super().__init__()
        self._items = []
        self._by_name = {}
        self._by_hot_key = {}
        self._header = ['hot_key', 'color', 'name', 'active', 'visible']
        self._delete_behavior = Behavior('_delete', color = QColor('black'))
        self._immutableColumns = set()
        self._booleanColumns = set([self._header.index('active'), self._header.index('visible')])
        self._role_to_str = {
            Qt.DisplayRole: "DisplayRole",
            Qt.DecorationRole: "DecorationRole",
            Qt.EditRole: "EditRole",
            Qt.ToolTipRole: "ToolTipRole",
            Qt.StatusTipRole: "StatusTipRole",
            Qt.WhatsThisRole: "WhatsThisRole",
            Qt.SizeHintRole: "SizeHintRole",
            Qt.FontRole: "FontRole",
            Qt.TextAlignmentRole: "TextAlignmentRole",
            Qt.BackgroundRole: "BackgroundRole",
            Qt.ForegroundRole: "ForegroundRole",
            Qt.CheckStateRole: "CheckStateRole",
            Qt.InitialSortOrderRole: "InitialSortOrderRole",
            Qt.AccessibleTextRole: "AccessibleTextRole",
            Qt.UserRole: "UserRole"
        }

    def add(self, beh: Behavior):
        oldRowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), oldRowCount, oldRowCount)
        self._items.append(beh)
        self._by_name[beh.get_name()] = beh
        hot_key = beh.get_hot_key()
        if hot_key:
            if hot_key not in self._by_hot_key.keys():
                self._by_hot_key[hot_key] = []
            assert(isinstance(self._by_hot_key[hot_key], list))
            self._by_hot_key[hot_key].append(beh)
        newRowCount = self.rowCount()
        self.endInsertRows()
        if newRowCount != oldRowCount:
            self.behaviors_changed.emit()
            self.layoutChanged.emit()

    def load(self, f):
        line = f.readline()
        while line:
            hot_key, name, r, g, b = line.strip().split(' ')
            if hot_key == '_':
                hot_key = ''
            self.add(Behavior(name, hot_key, QColor.fromRgbF(float(r), float(g), float(b))))
            line = f.readline()

    def save(self, f):
        for beh in self._items:
            h = beh.get_hot_key()
            if h == '':
                h = '_'
            color = beh.get_color()
            f.write(f"{h} {beh.get_name()} {color.redF()} {color.greenF()} {color.blueF()}" + os.linesep)

    def get(self, name):
        return self._by_name[name]

    def from_hot_key(self, key):
        """
        Return the list of behaviors associated with this hot key, if any
        """
        try:
            return self._by_hot_key[key]
        except KeyError:
            return None

    def len(self):
        return len(self._items)

    def header(self):
        return self._header

    def colorColumns(self):
        return [self._header.index('color')]

    def __iter__(self):
        return iter(self._items)

    def getDeleteBehavior(self):
        return self._delete_behavior

    def addIfMissing(self, nameToAdd):
        if nameToAdd not in self._by_name:
            self.add(Behavior(nameToAdd, '', QColor('gray')))
            return True
        return False

    def isImmutable(self, index):
        return index.column() in self._immutableColumns

    def setImmutable(self, column):
        self._immutableColumns.add(column)

    # QAbstractTableModel API methods

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[col]
        return None

    def rowCount(self, parent=None):
        # if parent:
        #     return 0
        return len(self._items)

    def columnCount(self, parent=None):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        datum = self._items[index.row()].get(self._header[index.column()])
        if isinstance(datum, bool):
            if role in [Qt.CheckStateRole, Qt.EditRole]:
                return Qt.Checked if datum else Qt.Unchecked
            return None
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return self._items[index.row()].get(self._header[index.column()])
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not role in [Qt.CheckStateRole, Qt.EditRole]:
            return False
        if role == Qt.CheckStateRole:
            value = bool(value)
        beh = self._items[index.row()]
        key = self._header[index.column()]
        name = beh.get_name()
        hot_key = beh.get_hot_key()
        beh.set(key, value)
        if key == 'hot_key' and value != hot_key:
            # disassociate this behavior from the hot_key
            # and associate with the new hot_key if not ''
            if hot_key != '':
                del(self._by_hot_key[hot_key])
            if value != '':
                if value not in self._by_hot_key.keys():
                    self._by_hot_key[value] = []
                assert(isinstance(self._by_hot_key[value], list))
                self._by_hot_key[value].append(beh)
        elif key == 'name' and value != name:
            del(self._by_name[name])
            self._by_name[value] = beh
        self.behaviors_changed.emit()
        self.dataChanged.emit(index, index, [role])
        return True

    def flags(self, index):
        f = super().flags(index)
        if index.column() not in self._immutableColumns:
            f |= Qt.ItemIsEditable
        if index.column() in self._booleanColumns:
            f = (f & ~(Qt.ItemIsSelectable | Qt.ItemIsEditable)) | Qt.ItemIsUserCheckable
        return f
