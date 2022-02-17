# mainWindow.py

from mainWindow_ui import Ui_MainWindow
import timecode as tc

from qtpy.QtCore import Qt, QEvent, Signal, Slot
from qtpy.QtWidgets import QMainWindow, QMenuBar
from db.trialWindow import TrialDockWidget

class MainWindow(QMainWindow):

    quitting = Signal()

    def __init__(self, bento):
        super().__init__()

        self.bento = bento
        self.flag = "close"
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
        bento.quitting.connect(self.close)
        self.quitting.connect(bento.quit)

        self.ui.trialPushButton.clicked.connect(self.selectTrial)
        self.ui.playButton.clicked.connect(bento.player.togglePlayer)
        self.ui.halveFrameRateButton.clicked.connect(bento.player.halveFrameRate)
        self.ui.doubleFrameRateButton.clicked.connect(bento.player.doubleFrameRate)
        self.ui.oneXFrameRateButton.clicked.connect(bento.player.resetFrameRate)
        self.ui.annotationsView.set_bento(bento)
        self.ui.annotationsView.setScene(bento.annotationsScene)
        bento.annotationsScene.sceneRectChanged.connect(self.ui.annotationsView.update)
        self.ui.annotationsView.scale(10., self.ui.annotationsView.height())
        self.populateChannelsCombo()
        self.ui.channelComboBox.currentTextChanged.connect(bento.setActiveChannel)
        self.ui.newChannelPushButton.clicked.connect(bento.newChannel)

        # menus
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.fileMenu = self.menuBar.addMenu("File")
        self.saveAnnotationsAction = self.fileMenu.addAction("Save Annotations...")
        self.saveAnnotationsAction.triggered.connect(bento.save_annotations)
        self.fileMenuSeparatorAction = self.fileMenu.addSeparator()
        self.setInvestigatorAction = self.fileMenu.addAction("Set Investigator...")
        self.setInvestigatorAction.triggered.connect(bento.set_investigator)
        self.importTrialsAction = self.fileMenu.addAction("Import Trials...")
        self.importTrialsAction.triggered.connect(bento.import_trials)
        self.importAnimalsAction = self.fileMenu.addAction("Import Animals (Tomomi)...")
        self.importAnimalsAction.triggered.connect(bento.import_animals_tomomi)

        self.dbMenu = self.menuBar.addMenu("Database")
        self.animalAction = self.dbMenu.addAction("Animal...")
        self.animalAction.triggered.connect(bento.edit_animal)
        self.investigatorAction = self.dbMenu.addAction("Investigator...")
        self.investigatorAction.triggered.connect(bento.edit_investigator)
        self.cameraAction = self.dbMenu.addAction("Camera...")
        self.cameraAction.triggered.connect(bento.edit_camera)
        self.separatorAction = self.dbMenu.addSeparator()
        self.configAction = self.dbMenu.addAction("Host Config...")
        self.configAction.triggered.connect(bento.edit_config)
        self.createDBAction = self.dbMenu.addAction("Create Database")
        self.createDBAction.triggered.connect(bento.create_db)

        self.windowsMenu = self.menuBar.addMenu("Windows")
        self.toggleBehaviorVisibilityAction = self.windowsMenu.addAction("Show/Hide Behavior List")
        self.toggleBehaviorVisibilityAction.triggered.connect(bento.toggleBehaviorVisibility)

    def closeEvent(self, event):
        if event.type()==QEvent.Type.Close and self.flag=="close":
            self.bento.quit(event)
        else:
            pass
        event.accept()

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
        elif (not (event.modifiers() & ~Qt.ShiftModifier)  # not a modifier other than shift
         and (event.key() in range(Qt.Key_A, Qt.Key_Z) or
            event.key() == Qt.Key_Backspace or
            event.key() == Qt.Key_Escape)):
            self.bento.processHotKey(event)
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
    def selectTrial(self):
        self.bento.trialWindow = TrialDockWidget(self.bento)
        self.bento.trialWindow.show()

    def addChannelToCombo(self, chanName):
        if isinstance(chanName, list):
            for item in chanName:
                self.addChannelToCombo(item)
            return
        if not isinstance(chanName, str):
            raise RuntimeError("addChannelToCombo can only accept a string or list of strings")
        self.ui.channelComboBox.addItem(chanName)
        self.ui.channelComboBox.setCurrentText(chanName)

    def populateChannelsCombo(self):
        for chanName in self.bento.annotations.channel_names():
            self.ui.channelComboBox.addItem(chanName)

    def clearChannelsCombo(self):
        self.ui.channelComboBox.clear()

    @Slot(str)
    def selectChannelByName(self, chanName):
        self.ui.channelComboBox.setCurrentText(chanName)