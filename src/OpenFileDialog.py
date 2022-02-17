# OpenFileDialog.py

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

class FileDialog(QFileDialog):
    """
    """

    def __init__(self, parent):
        super(FileDialog, self).__init__(self)
