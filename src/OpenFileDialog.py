# OpenFileDialog.py

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class FileDialog(QFileDialog):
    """
    """

    def __init__(self, parent):
        super(FileDialog, self).__init__(self)
        