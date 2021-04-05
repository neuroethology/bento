# mainWindow.py

from mainWindow_ui import Ui_MainWindow
import timecode as tc

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from db.sessionWindow import SessionDockWidget

class MainWindow(QMainWindow):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stepButton.clicked.connect(bento.incrementTime)
        self.ui.backButton.clicked.connect(bento.decrementTime)
        self.ui.ffButton.clicked.connect(bento.skipForward)
        self.ui.fbButton.clicked.connect(bento.skipBackward)
        self.ui.toStartButton.clicked.connect(bento.toStart)
        self.ui.toEndButton.clicked.connect(bento.toEnd)
        self.ui.nextButton.clicked.connect(bento.toNextEvent)
        self.ui.previousButton.clicked.connect(bento.toPrevEvent)
        self.ui.quitButton.clicked.connect(bento.quit)
        self.quitting.connect(bento.quit)
        self.ui.sessionPushButton.clicked.connect(self.selectSession)
        self.ui.playButton.clicked.connect(bento.player.togglePlayer)
        self.ui.halveFrameRateButton.clicked.connect(bento.player.halveFrameRate)
        self.ui.doubleFrameRateButton.clicked.connect(bento.player.doubleFrameRate)
        self.ui.oneXFrameRateButton.clicked.connect(bento.player.resetFrameRate)
        self.ui.annotationsView.set_bento(bento)
        self.ui.annotationsView.setScene(bento.annotationsScene)
        self.ui.annotationsView.scale(10., self.ui.annotationsView.height())

        self.bento = bento

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.skipBackward()
            else:
                self.bento.decrementTime()
        elif event.key() == Qt.Key_Right:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.skipForward()
            else:
                self.bento.incrementTime()
        elif event.key() == Qt.Key_Up:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.player.doubleFrameRate()
            else:
                self.bento.toPrevEvent()
        elif event.key() == Qt.Key_Down:
            if event.modifiers() & Qt.ShiftModifier:
                self.bento.player.halveFrameRate()
            else:
                self.bento.toNextEvent()
        elif event.key() in range(Qt.Key_A, Qt.Key_Z):
            self.bento.processHotKey(event.key())
        elif event.key() == Qt.Key_Space and self.bento.player:
            self.bento.player.togglePlayer()
        event.accept()

    @Slot(tc.Timecode)
    def updateTime(self, t):
        self.ui.timeLabel.setText(f"{t} ({t.frame_number})")
        self.ui.annotationsView.updatePosition(t)
        self.show()

    @Slot(list)
    def updateAnnotLabel(self, annots):
        entries = [a[0] + ': ' + a[1] for a in annots]
        label = '\n'.join(entries)
        self.ui.annotLabel.setText(label)
        self.show()

    @Slot()
    def selectSession(self):
        self.bento.sessionWindow = SessionDockWidget(self.bento)
        self.bento.sessionWindow.show()
