# neuralFrame.py

from neural.neuralFrame_ui import Ui_neuralFrame
from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QFrame
import time
from timecode import Timecode
from widgets.neuralWidget import NeuralScene
from utils import fix_path
from os.path import isabs

class NeuralFrame(QFrame):

    openReader = Signal(str)
    quitting = Signal()
    neuralSceneUpdated = Signal()
    active_channel_changed = Signal(str)

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
        self.active_channel_changed.connect(self.neuralScene.setActiveChannel)
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
        self.ui.neuralView.hScaleChanged.connect(self.ui.annotationsView.setHScaleAndShow)
        self.annotations = self.bento.annotations
        self.activeChannel = None 

    def load(self, neuralData, base_dir):
        if isabs(neuralData.file_path):
            neural_path = neuralData.file_path
        else:
            neural_path = base_dir + neuralData.file_path
        neural_path = fix_path(neural_path)
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
        self.neuralScene.overlayAnnotations(annotationsScene, 
                                            self.neuralScene,
                                            self.ui.annotationsView,
                                            self.annotations)

    @Slot(str)
    def setActiveChannel(self, chan):
        self.activeChannel = chan
        self.active_channel_changed.emit(self.activeChannel)

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

