# behavior.py
"""
Overview comment here
"""

from PySide6.QtCore import QAbstractTableModel, QObject, Qt, Slot
from PySide6.QtGui import QColor
import os

class Behavior(QObject):
    """
    An annotation behavior, which is quite simple.  It comprises:
    name        The name of the behavior, which is displayed on various UI widgets
    hot_key     The case-sensitive key stroke used to start and stop instances of the behavior
    color       The color with which to display this behavior
    """

    def __init__(self, name: str, hot_key: str = '', color: QColor = None):
        super().__init__()
        self._name = name
        self._hot_key = '' if hot_key == '_' else hot_key
        self._color = color
        self._visible = True
        self._active = False

    def __repr__(self):
        return f"Behavior: name={self._name}, hot_key={self._hot_key}, color={self._color}, active={self._active}, visible={self._visible}"

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
    Use from_hot_key(key) to get the behavior given the hot key.
        Returns None if the hot_key isn't defined.
    """

    def __init__(self):
        super().__init__()
        self._items = []
        self._by_name = {}
        self._by_hot_key = {}
        self._header = ['hot_key', 'color', 'name', 'active', 'visible']
        self._delete_behavior = Behavior('_delete')

    def load(self, f):
        line = f.readline()
        while line:
            hot_key, name, r, g, b = line.strip().split(' ')
            beh = Behavior(name, hot_key, QColor.fromRgbF(float(r), float(g), float(b)))
            self._items.append(beh)
            self._by_name[name] = beh
            if hot_key == '_':
                hot_key = ''
            else:
                self._hot_keys[hot_key] = beh
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
        if nameToAdd not in self._items.keys():
            self._items[nameToAdd] = Behavior(nameToAdd, '', QColor.gray)
            return True
        return False

    # QAbstractTableModel API methods

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[col]
        return None

    def rowCount(self):
        return len(self._items)

    def columnCount(self):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        return self._item[index.row()][self._header[index.column()]]

    def setData(self, index, value, role=Qt.EditRole):
        beh = self._items[index.row()]
        key = self._header[index.column()]
        name = beh['name']
        hot_key = beh['hot_key']
        beh[key] = value
        if key == 'hot_key' and value != hot_key:
            # disassociate this behavior from the hot_key
            # and associate with the new hot_key if not ''
            del(self._by_hot_key[hot_key])
            if value != '':
                self._by_hot_key[value] = beh
        elif key == 'name' and value != name:
            del(self._by_name[name])
            self._by_name[value] = beh

# class BehaviorsIterator():
#     def __init__(self, behaviors):
#         self.behaviors = behaviors
#         self.keyIter = behaviors._items.__iter__()

#     def __next__(self):
#         return self.behaviors._items[self.keyIter.__next__()]
