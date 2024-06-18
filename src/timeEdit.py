from qtpy.QtWidgets import QTimeEdit


class CustomTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bento = None
        self.setDisplayFormat("HH:mm:ss.zzz")
    
    def set_bento(self, bento):
        self.bento = bento
    
    def keyPressEvent(self, event):
        # Override keyPressEvent to capture changes when keys are pressed
        super().keyPressEvent(event)
        self.bento.jumpToTime()

    def mousePressEvent(self, event):
        # Override keyPressEvent to capture changes when keys are pressed
        super().mousePressEvent(event)
        self.bento.jumpToTime()
    
    