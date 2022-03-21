# channelDialog.py
"""
"""

from channelDialog_ui import Ui_ChannelDialog
from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QDialog

class ChannelDialog(QDialog):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_ChannelDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

    @Slot()
    def accept(self):
        self.bento.addChannel(self.ui.channelNameLineEdit.text())
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
