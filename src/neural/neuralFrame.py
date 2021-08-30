# neuralFrame.py

from neural.neuralFrame_ui import Ui_neuralFrame
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFrame
import time
from timecode import Timecode
from widgets.neuralWidget import NeuralScene
from utils import fix_path

class NeuralFrame(QFrame):

    openReader = Signal(str)
    quitting = Signal()
    neuralSceneUpdated = Signal()

    def __init__(self, bento):
        # super(NeuralDockWidget, self).__init__()
        super(NeuralFrame, self).__init__()
        self.bento = bento
        # self.ui = Ui_NeuralDockWidget()
        self.ui = Ui_neuralFrame()
        self.ui.setupUi(self)
        bento.quitting.connect(self.close)
        self.quitting.connect(self.bento.quit)
        self.neuralScene = NeuralScene()
        self.ui.neuralView.setScene(self.neuralScene)
        self.ui.neuralView.set_bento(bento)
        self.ui.neuralView.scale(10., self.ui.neuralView.height())
        self.ui.showTraceRadioButton.toggled.connect(self.showNeuralTraces)
        self.ui.showHeatMapRadioButton.toggled.connect(self.showNeuralHeatMap)
        self.ui.showAnnotationsCheckBox.stateChanged.connect(self.showNeuralAnnotations)
        self.neuralSceneUpdated.connect(self.ui.neuralView.updateScene)
        self.ui.annotationsView.set_bento(bento)
        self.ui.annotationsView.setScene(bento.annotationsScene)
        self.ui.annotationsView.scale(10., self.ui.annotationsView.height())
        bento.annotationsSceneUpdated.connect(self.ui.annotationsView.updateScene)
        self.ui.neuralView.hScaleChanged.connect(self.ui.annotationsView.setHScaleAndShow)

    def load(self, neuralData, base_dir):
        neural_path = fix_path(base_dir + neuralData.file_path)
        print(f"Load neural from {neural_path}")
        self.neuralScene.loadNeural(
            neural_path,
            neuralData.sample_rate,
            neuralData.start_frame,
            neuralData.stop_frame,
            self.bento.time_start,
            self.ui.showTraceRadioButton.isChecked(),
            self.ui.showHeatMapRadioButton.isChecked(),
            self.ui.showAnnotationsCheckBox.checkState()
            )
        self.neuralSceneUpdated.emit()
        self.ui.neuralView.synchronizeHScale()
        # synchronize viewer times
        self.updateTime(self.bento.time_start)

    def overlayAnnotations(self, annotationsScene):
        self.neuralScene.overlayAnnotations(annotationsScene, self.neuralScene)

    @Slot(Timecode)
    def updateTime(self, t):
        self.ui.neuralView.updatePosition(t)
        self.ui.annotationsView.updatePosition(t)

    @Slot(int)
    def showNeuralTraces(self, checked):
        if isinstance(self.neuralScene, NeuralScene):
            self.neuralScene.showTraces(checked)
            if checked:
                self.ui.showAnnotationsCheckBox.setEnabled(True)
                self.neuralScene.showAnnotations(
                    self.ui.showAnnotationsCheckBox.isChecked()
            )

    @Slot(int)
    def showNeuralHeatMap(self, checked):
        if isinstance(self.neuralScene, NeuralScene):
            self.neuralScene.showHeatmap(checked)
            if checked:
                self.ui.showAnnotationsCheckBox.setEnabled(False)
                self.neuralScene.showAnnotations(False)

    @Slot(int)
    def showNeuralAnnotations(self, state):
        if isinstance(self.neuralScene, NeuralScene):
            self.neuralScene.showAnnotations(state > 0)

