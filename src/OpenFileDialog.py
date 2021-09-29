# OpenFileDialog.py

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class FileDialog(QFileDialog):
    """
    """

    def __init__(self, parent):
        super(FileDialog, self).__init__(self)
