# behavior.py
"""
Overview comment here
"""

from PySide2.QtGui import QColor
import os

class Behavior(object):
    """
    An annotation behavior, which is quite simple.  It comprises:
    name        The name of the behavior, which is displayed on various UI widgets
    hot_key     The case-sensitive key stroke used to start and stop instances of the behavior
    color       The color with which to display this behavior
    """

    def __init__(self, name: str, hot_key: str = '', color: QColor = None):
        super(Behavior, self).__init__()
        self.name = name
        self.hot_key = '' if hot_key == '_' else hot_key
        self.color = color
        self.visible = True

    def set_hot_key(self, hot_key: str):
        self.hot_key = hot_key

    def set_color(self, color: QColor):
        self.color = color

    def set_visible(self, visible):
        self.visible = visible

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def is_visible(self):
        return self.visible

    def toDict(self):
        return {
            'hot_key': '_' if self.hot_key == '' else self.hot_key,
            'color': self.color,
            'name': self.name
            }

class Behaviors(object):
    """
    A set of behaviors, which represent "all" possible behaviors.
    The class supports reading from and writing to profile files that specify the default
    hot_key and color for each behavior, along with the name.

    Use getattr(name) to get the Behavior instance for a given name.
    Use from_hot_key(key) to get the behavior given the hot key.
        Returns None if the hot_key isn't defined.
    """

    def __init__(self):
        super(Behaviors, self).__init__()
        self._hot_keys = {}
        self._items = {}

    def load(self, f):
        line = f.readline()
        while line:
            hot_key, name, r, g, b = line.strip().split(' ')
            if hot_key == '_':
                hot_key = ''
            else:
                self._hot_keys[hot_key] = name
            self._items[name] = Behavior(name, hot_key, QColor.fromRgbF(float(r), float(g), float(b)))
            # setattr(self, name, Behavior(name, hot_key, QColor.fromRgbF(float(r), float(g), float(b))))
            line = f.readline()

    def save(self, f):
        for key in self._items.keys():
            beh = self._items[key]
        # for item in self.__dict__.keys():
        #     beh = getattr(self, item)
            if beh.hot_key == '':
                h = '_'
            else:
                h = beh.hot_key
            f.write(f"{h} {beh.name} {beh.color.redF()} {beh.color.greenF()} {beh.color.blueF()}" + os.linesep)

    def from_hot_key(self, key):
        try:
            # print(f"available hot keys: {self._hot_keys}")
            return self._items[self._hot_keys[key]]
            # return getattr(self, self._hot_keys[key])
        except KeyError:
            return None

    def len(self):
        return len(self._items)

    def header(self):
        return ['hot_key', 'color', 'name']

    def __iter__(self):
        print(f'in Behaviors.__iter__(),')
        return BehaviorsIterator(self)

class BehaviorsIterator():
    def __init__(self, behaviors):
        self.behaviors = behaviors
        self.keyIter = behaviors._items.__iter__()

    def __next__(self):
        return self.behaviors._items[self.keyIter.__next__()]
