from qtpy.QtWidgets import QFrame, QMessageBox, QCheckBox, QMenu, QFileDialog, QLabel
from plugin.behaviorTriggeredAverage_ui import Ui_BTAFrame
from qtpy.QtCore import Slot
from os.path import expanduser, sep
from qtpy.QtGui import QColor
import numpy as np
import pandas as pd
from scipy import signal
import math
import os
import timecode as tc
from processing.processing import ProcessingBase
from vispy.scene import SceneCanvas, visuals, AxisWidget
from vispy.visuals.transforms import STTransform
from PIL import Image


class behaviorTriggeredAverage(QFrame, ProcessingBase):
    def __init__(self, nwbFile, bento):
        QFrame.__init__(self)
        ProcessingBase.__init__(self, nwbFile, bento)
        self.bento = bento
        self.checkData()
        if not self.annotationsExists or not self.neuralExists:
            msgBox = QMessageBox(QMessageBox.Warning, 
                                 "Required Data not found", 
                                 "Both neural data and annotation data \
                                  must exist for this plugin to work")
            msgBox.exec()
            raise RuntimeError("Either Neural data or Annotation data does not exist for this plugin to work.")
        self.bento.nwbFileUpdated.connect(self.getAnnotationsData)
        self.bento.behaviorsChanged.connect(self.getBehaviors)
        self.bento.behaviorsChanged.connect(self.populateBehaviorSelection)
        self.bento.behaviorsChanged.connect(self.getBehaviorTriggeredTrials)
        
        self.getAnnotationsData()
        self.getNeuralData()
        self.getBehaviors()
        self.offset = self.neuralStartTime - \
                      self.bento.time_start_end_timecode['annotations'][0][0].float
        self.invokeUI()
        
    def invokeUI(self):
        #setting up UI
        self.ui = Ui_BTAFrame()
        self.ui.setupUi(self)
        # initialize few variables
        self.checkboxState = {}
        self.bev, self.ch = None, None
        self.combineBehaviorNames, self.combineChannels = [], []

        # populating combo boxes
        self.populateBehaviorCombo()
        self.populateChannelsCombo()
        self.populateAnalyzeCombo()

        # connect nwb file update signal to populate functions
        self.bento.nwbFileUpdated.connect(self.populateBehaviorCombo)
        self.bento.nwbFileUpdated.connect(self.populateChannelsCombo)

        # creating save menu and connect them to saving functions
        self.saveMenu = QMenu("Save Options")
        self.ui.saveButton.setMenu(self.saveMenu)
        self.ui.saveButton.setToolTip("click to see save options")
        self.saveh5 = self.saveMenu.addAction("Save BTA to h5 file")
        self.saveFigure = self.saveMenu.addAction("Save Figure")
        self.saveh5.triggered.connect(self.saveBTAtoh5)
        self.saveFigure.triggered.connect(self.savePlots)

        # setting minimum and default value for bin size
        self.ui.binSizeBox.setMinimum(float(1/self.neuralSampleRate))
        self.ui.binSizeBox.setValue(float(1/self.neuralSampleRate))

        # connecting different user options getBehaviorTriggeredTrials function
        self.ui.mergeBoutsBox.textChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.discardBoutsBox.textChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.channelComboBox.currentTextChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.behaviorComboBox.currentTextChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.analyzeComboBox.currentTextChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.alignAtStartButton.toggled.connect(self.getBehaviorTriggeredTrials)
        self.ui.alignAtEndButton.toggled.connect(self.getBehaviorTriggeredTrials)
        self.ui.windowBox_1.textChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.windowBox_2.textChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.binSizeBox.textChanged.connect(self.getBehaviorTriggeredTrials)
        self.ui.zscoreCheckBox.stateChanged.connect(self.getBehaviorTriggeredTrials)

        # populating behavior selection checkboxes
        self.populateBehaviorSelection()
        
        self.getBehaviorTriggeredTrials()

    @Slot()
    def populateBehaviorCombo(self):
        for channel in list(self.behaviorNames.keys()):
            for item in self.behaviorNames[channel]:
                if item in self.combineBehaviorNames:
                    continue
                else:
                    self.ui.behaviorComboBox.addItem(item)
                    self.combineBehaviorNames.append(item)
    
    @Slot()
    def populateChannelsCombo(self):
        for channel in list(self.behaviorNames.keys()):
            if channel in self.combineChannels:
                continue
            else: 
                self.ui.channelComboBox.addItem(channel)
                self.combineChannels.append(channel)
    
    @Slot()
    def populateBehaviorSelection(self):
        for bev in self.combineBehaviorNames:
            checkbox = QCheckBox(bev, self)
            if bev in list(self.behaviors.keys()):
                r, g, b = self.behaviors[bev][0], self.behaviors[bev][1], self.behaviors[bev][2]
                color = QColor.fromRgbF(float(r), float(g), float(b)).name()
                checkbox.setStyleSheet(
                                "QCheckBox{"
                                "spacing 5px"
                                "}"
                                "QCheckBox::indicator"
                                "{"
                                "width: 13px;"
                                "height: 13px;"
                                "background-color : white"
                                "}"
                                "QCheckBox::indicator:checked"
                                "{"
                                "background-color : "+color+
                                "}")
                checkbox.setChecked(True)
            else:
                checkbox.setStyleSheet(
                                "QCheckBox{"
                                "spacing 5px"
                                "}"
                                "QCheckBox::indicator"
                                "{"
                                "width: 13px;"
                                "height: 13px;"
                                "background-color : white"
                                "}"
                                )
            if bev in list(self.checkboxState.keys()):
                self.ui.behaviorSelectLayout.replaceWidget(self.checkboxState[bev], checkbox)
            else:
                self.ui.behaviorSelectLayout.addWidget(checkbox)
            self.checkboxState[bev] = checkbox
            checkbox.stateChanged.connect(self.getBehaviorTriggeredTrials)
    
    def populateAnalyzeCombo(self):
        self.analyzeOptions = ['Population Average']
        for i in range(1,self.neuralData.shape[0]+1):
            self.analyzeOptions.append('Unit {}'.format(str(i)))
        self.ui.analyzeComboBox.addItems(self.analyzeOptions)
    
    def checkAnalyzeComboAndGetData(self):
        analyzeOption = self.ui.analyzeComboBox.currentText()
        if analyzeOption=='Population Average':
            return np.mean(self.neuralData, axis=0)
        else:
            num = int(analyzeOption.split()[-1])
            return self.neuralData[num-1,:]
        
    def createTrial(self, neuralData, index, window):
        if window[0]<index and neuralData.shape[0]>(index+window[1]):
            trial = neuralData[index-window[0]-1:index+window[1]]
        elif window[0]>=index and neuralData.shape[0]>(index+window[1]):
            mismatch = window[0]-index+1
            trial = np.zeros(window[0]+window[1]+1)
            trial[:mismatch] = np.nan
            trial[mismatch:] = neuralData[:index+window[1]]
        else:
            mismatch = (index+window[1])-neuralData.shape[0]
            trial1 = np.zeros(mismatch)
            trial1[:] = np.nan
            trial2 = neuralData[index-window[0]-1:neuralData.shape[0]]
            trial = np.concatenate((trial2, trial1))

        return trial

    def mergeAndDiscardBouts(self, startTime, stopTime):
        self.mergeBoutsTime = float(self.ui.mergeBoutsBox.value())
        self.discardBoutsTime = float(self.ui.discardBoutsBox.value())
        startTime, stopTime = np.array(startTime), np.array(stopTime)
        keptIndicesStart = [0]
        flag = None
        for i in range(startTime.shape[0]-1):
            if startTime[i+1]-stopTime[i]<self.mergeBoutsTime:
                if flag=='merged':
                    continue
                else:
                    keptIndicesStart.append(i)
                flag = 'merged'
            else:
                keptIndicesStart.append(i+1)
                flag = 'not merged'
        
        keptIndicesStart = np.unique(np.array(keptIndicesStart))
        keptIndicesStop = []
        for i in range(keptIndicesStart.shape[0]-1):
            if keptIndicesStart[i+1]-keptIndicesStart[i]==1:
                keptIndicesStop.append(keptIndicesStart[i])
            else:
                keptIndicesStop.append(keptIndicesStart[i+1]-1)
        if keptIndicesStart[-1]<stopTime.shape[0]:
            keptIndicesStop.append(stopTime.shape[0]-1)

        keptIndicesStop = np.array(keptIndicesStop)
        if keptIndicesStart.shape[0]!=keptIndicesStop.shape[0]:
            raise Exception('Start time and stop time are different in number after merging bouts.')
        
        deleteIndices = []
        for i in range(keptIndicesStart.shape[0]):
            if stopTime[keptIndicesStop[i]]-startTime[keptIndicesStart[i]]<self.discardBoutsTime:
                deleteIndices.append(i)
        
        keptIndicesStart = np.delete(keptIndicesStart, deleteIndices, 0)
        keptIndicesStop = np.delete(keptIndicesStop, deleteIndices, 0)

        return keptIndicesStart, keptIndicesStop
    
    def zscore(self, arr):
        zscore = np.divide(arr - np.nanmean(arr), np.nanstd(arr))
        return zscore

    def checkChannelAndData(self, behaviorName, channel):
        ts = np.arange(self.neuralData.shape[1])/self.neuralSampleRate
        if channel:
            data = self.annotationsData[self.ch].loc[self.annotationsData[self.ch]['behaviorName'] == behaviorName]
            if self.ui.alignAtStartButton.isChecked():
                data = data[data['start_time']<ts[-1]]
            if self.ui.alignAtEndButton.isChecked():
                data = data[data['stop_time']<ts[-1]]
            if data.empty:
                return  False
            else:
                return True
        else:
            return False
    
    @Slot()
    def getBehaviorTriggeredTrials(self):
        # getting behavior name and channel
        self.bev = self.ui.behaviorComboBox.currentText()
        self.ch = self.ui.channelComboBox.currentText()

        # getting bin size and calculate sampling rate
        # and number of data points for resampling
        binSize = float(self.ui.binSizeBox.value())
        if binSize==0:
            self.sampleRate = self.neuralSampleRate
        else:
            self.sampleRate = 1/binSize
        self.neuralDataTs = np.arange(self.neuralData.shape[1])/self.neuralSampleRate
        num = int(round(self.neuralDataTs[-1])*self.sampleRate)

        # getting window values and calculate total window length
        self.window = [float(self.ui.windowBox_1.value()), 
                       float(self.ui.windowBox_2.value())]
        self.windowNumTs = [int(round(self.window[0]*self.sampleRate)), 
                            int(round(self.window[1]*self.sampleRate))]
        self.trialsTotalTs = self.windowNumTs[0] + self.windowNumTs[1]
        self.trialsTs = np.linspace(-self.window[0], self.window[1], self.trialsTotalTs+1)
        if self.checkChannelAndData(self.bev, self.ch):
            # getting anntations data for a particular behavior 
            self.data = self.annotationsData[self.ch].loc[self.annotationsData[self.ch]['behaviorName'] == self.bev]

            # compute align time based on align at start or align at end
            if self.ui.alignAtStartButton.isChecked():
                self.data = self.data[self.data['start_time']<self.neuralDataTs[-1]]
                keptIndicesStart, _ = self.mergeAndDiscardBouts(self.data['start_time'], self.data['stop_time'])
                self.alignTime = np.array(self.data['start_time'])[keptIndicesStart]
            if self.ui.alignAtEndButton.isChecked():
                self.data = self.data[self.data['stop_time']<self.neuralDataTs[-1]]
                _, keptIndicesStop = self.mergeAndDiscardBouts(self.data['start_time'], self.data['stop_time'])
                self.alignTime = np.array(self.data['stop_time'])[keptIndicesStop]
            
            # considering offset and resampling neural data
            self.alignTime = self.alignTime - self.offset
            self.alignTime = self.alignTime[np.where(self.alignTime > 0)[0]]
            self.trials = np.full((self.alignTime.shape[0], self.trialsTs.shape[0]), np.nan)
            self.backgroundAnnotations = dict()
            resampledData = signal.resample(self.checkAnalyzeComboAndGetData(),
                                            num=num, t=self.neuralDataTs)[0]

            # getting all the trials along with background annotations for each trial
            for ix in range(self.alignTime.shape[0]):
                idx = int(round((self.alignTime[ix])*self.sampleRate))
                if self.ui.zscoreCheckBox.isChecked():
                    self.trials[ix, :] = self.zscore(self.createTrial(resampledData, 
                                                        idx, 
                                                        self.windowNumTs))
                else:
                    self.trials[ix, :] = self.createTrial(resampledData, 
                                                        idx, 
                                                        self.windowNumTs)
                start_time = np.array(self.annotationsData[self.ch]['start_time']) - self.alignTime[ix]
                stop_time = np.array(self.annotationsData[self.ch]['stop_time']) - self.alignTime[ix]
                temp_df = self.annotationsData[self.ch].iloc[np.where((stop_time>=-self.window[0]) 
                                                                 & (start_time<=self.window[1]))[0],:]
                copy_df = temp_df.copy()
                copy_df.loc[:,'start_time'] = temp_df['start_time'] - self.alignTime[ix]
                copy_df.loc[:,'stop_time'] = temp_df['stop_time'] - self.alignTime[ix]
                for bev in list(self.checkboxState.keys()):
                    if not self.checkboxState[bev].isChecked():
                        copy_df.drop(copy_df[copy_df['behaviorName']==bev].index, inplace=True)
                self.backgroundAnnotations[str(ix)] = copy_df
            
            # handling a case when there is only one trial
            if self.trials.shape[0]==1:
                self.avgTrials = self.trials[0]
                self.errTrials = np.zeros(self.trialsTs.shape[0])
            else:
                self.avgTrials = np.nanmean(self.trials, axis=0)
                self.errTrials = np.nanstd(self.trials, axis=0)/math.sqrt(self.trials.shape[0])
            
            # plotting trials along with annotations in the background
            self.plotBTA()
        else:
            self.clearPlotLayout()
            self.label_top = QLabel("Data corresponding to this behavior/channel does not exist")
            self.label_bot = QLabel("Data corresponding to this behavior/channel does not exist")
            self.ui.plotLayout.addWidget(self.label_top, stretch=1)
            self.ui.plotLayout.addWidget(self.label_bot, stretch=2)

        
        
    
    def clearPlotLayout(self):
        for i in reversed(range(self.ui.plotLayout.count())): 
            self.ui.plotLayout.itemAt(i).widget().deleteLater()
    
    def plotBTA(self):
        self.clearPlotLayout()
        self.createAnnotationsImgArray()
        self.canvas_top = SceneCanvas(size=(self.width,200))
        self.grid_top = self.canvas_top.central_widget.add_grid()
        self.xaxis_top = AxisWidget(orientation='bottom',
                                axis_label='Time (s)',
                                axis_color='black',
                                tick_color='black',
                                text_color='black',
                                axis_font_size=12,
                                font_size= 8,
                                axis_label_margin=16,
                                tick_label_margin=14)
        self.xaxis_top.height_max = 35
        self.xaxis_top.bgcolor = 'white'
        self.grid_top.add_widget(self.xaxis_top, row=1, col=1)

        self.yaxis_top = AxisWidget(orientation='left',
                                axis_color='black',
                                tick_color='black',
                                text_color='black',
                                axis_font_size=12,
                                font_size= 8,
                                axis_label_margin=16,
                                tick_label_margin=8)
        self.yaxis_top.width_max = 35
        self.yaxis_top.bgcolor = 'white'
        self.grid_top.add_widget(self.yaxis_top, row=0, col=0)

        self.view_top = self.grid_top.add_view(0, 1, bgcolor='white')
        self.lineAvgTrials = visuals.Line(
            np.column_stack((self.trialsTs, self.avgTrials)),
            parent=self.view_top.scene,
            color='black'
        )
        errPosValues = self.avgTrials + self.errTrials
        errNegValues = self.avgTrials - self.errTrials
        if np.count_nonzero(self.errTrials)!=0:
            notZeroIndices = np.where(~(self.errTrials==0))[0]
            # handing a case when there are two trials and one has few NaN values
            errPosValues = self.avgTrials[notZeroIndices] + self.errTrials[notZeroIndices]
            errNegValues = self.avgTrials[notZeroIndices] - self.errTrials[notZeroIndices]
            self.errPosLine = visuals.Line(
                np.column_stack((self.trialsTs[notZeroIndices], errPosValues)),
                parent=self.view_top.scene,
                color='white'
            )
            self.errNegLine = visuals.Line(
                np.column_stack((self.trialsTs[notZeroIndices], errNegValues)),
                parent=self.view_top.scene,
                color='white'
            )
            self.fillBetween = visuals.Polygon(
                pos=np.vstack((self.errPosLine.pos, self.errNegLine.pos[::-1])),
                color=(0.85, 0.85, 0.85, 1),
                parent=self.view_top.scene
            )
        self.centerLineTop = visuals.InfiniteLine(0, 
                                               color=[0,0,0,1], 
                                               vertical=True,
                                               line_width=2,
                                               parent=self.view_top.scene)
        self.view_top.camera = "panzoom"
        self.view_top.interactive = False
        self.view_top.camera.set_range(x=(self.trialsTs[0], self.trialsTs[-1]),
                                       y=(np.nanmin(errNegValues), np.nanmax(errPosValues)))
        self.xaxis_top.link_view(self.view_top)
        self.yaxis_top.link_view(self.view_top)

        self.rememberPos = []
        height = 0
        for t in range(self.trials.shape[0]):
            pos = np.empty((self.trials.shape[1], 2), dtype=np.float32)
            pos[:, 0] = self.trialsTs
            pos[:, 1] = np.interp(self.trials[t,:], 
                                  (np.nanmin(self.trials[t,:]), np.nanmax(self.trials[t,:])), 
                                  (height+2, height+self.trialHeight-2))
            self.rememberPos.append(pos)
            height += self.trialHeight
        
        self.canvas_bot = SceneCanvas(size=(self.width,self.height))
        self.grid_bot = self.canvas_bot.central_widget.add_grid()
        self.xaxis_bot = AxisWidget(orientation='bottom',
                                axis_label='Time (s)',
                                axis_color='black',
                                tick_color='black',
                                text_color='black',
                                axis_font_size=12,
                                font_size= 8,
                                axis_label_margin=16,
                                tick_label_margin=14)
        self.xaxis_bot.height_max = 35
        self.xaxis_bot.bgcolor = 'white'
        self.grid_bot.add_widget(self.xaxis_bot, row=1, col=0)
        self.view_bot = self.grid_bot.add_view(0, 0, bgcolor='white')
        for p in range(len(self.rememberPos)):
            nanIndices = np.where(~np.isnan(self.rememberPos[p]))[0]
            self.lineTrials = visuals.Line(self.rememberPos[p][nanIndices,:], 
                                           parent=self.view_bot.scene, 
                                           color='black', 
                                           width=1)
        self.annotationsImage = visuals.Image(self.imgArray, 
                                              texture_format="auto", 
                                              parent=self.view_bot.scene)
        self.annotationsImage.transform = STTransform(scale=((self.window[0]+self.window[1])/self.width), 
                                                      translate=(-(self.window[0]), 0))
        self.centerLineBot = visuals.InfiniteLine(0, 
                                               color=[0,0,0,1], 
                                               vertical=True,
                                               line_width=2,
                                               parent=self.view_bot.scene)
        self.view_bot.camera = "panzoom"
        self.view_bot.camera.interactive = False
        self.view_bot.camera.set_range(x=(-self.window[0], self.window[1]), 
                                       y=(0, self.height))
        self.xaxis_bot.link_view(self.view_bot)

        self.ui.plotLayout.addWidget(self.canvas_top.native, stretch=1)
        self.ui.plotLayout.addWidget(self.canvas_bot.native, stretch=2)
    
    def createAnnotationsImgArray(self):
        self.trialHeight = 10
        self.height, self.width, channels = self.trials.shape[0]*self.trialHeight, int((self.trials.shape[1])*(self.window[0]+self.window[1])), 3
        secondLength = int(self.width/(self.window[0]+self.window[1]))
        self.imgArray = np.ones((self.height, self.width, channels), dtype=np.float32)
        height = 0
        for t in range(self.trials.shape[0]):
            annotations = np.array(self.backgroundAnnotations[str(t)])
            annotations[:,0], annotations[:,1] = annotations[:,0] - self.offset + self.window[0], annotations[:,1] - self.offset + self.window[0]
            for j in range(annotations.shape[0]):
                start = int(round((annotations[j,0]) * secondLength))
                end = int(round((annotations[j,1] +
                                 tc.Timecode(self.bento.annotationsScene.sample_rate, frames=1).float) * secondLength))
                bev = self.behaviors[annotations[j,2]]
                self.imgArray[height:int(height+self.trialHeight),start:end,0] = bev[0]
                self.imgArray[height:int(height+self.trialHeight),start:end,1] = bev[1]
                self.imgArray[height:int(height+self.trialHeight),start:end,2] = bev[2]
            height += self.trialHeight

    def saveBTAtoh5(self):
        fileName, selectedFilter = QFileDialog.getSaveFileName(
            self,
            caption="Save Behavior Triggered Average Plots",
            filter="h5 file (*.h5)",
            selectedFilter="h5 file (*.h5)",
            dir=expanduser('~'))
        if selectedFilter == "h5 file (*.h5)":
            cols = ['Bout_'+str(i) for i in np.arange(1,self.trials.shape[0]+1)]
            df = pd.DataFrame(self.trials.T, columns=cols)
            df.to_hdf(fileName, key='dataframe', mode='w')
            print("BTA saved to h5 file")
        else:
            raise NotImplementedError(f"File format {selectedFilter} not supported")

    def savePlots(self):
        fileName, selectedFilter = QFileDialog.getSaveFileName(
            self,
            caption="Save Behavior Triggered Average Plots",
            filter="eps file (*.eps)",
            selectedFilter="eps file (*.eps)",
            dir=expanduser('~'))
        if selectedFilter == "eps file (*.eps)":
            dirname = os.path.dirname(fileName)
            files = [os.path.join(dirname, os.path.basename(fileName).split('.')[0]+'_top.eps'), 
                     os.path.join(dirname, os.path.basename(fileName).split('.')[0]+'_bottom.eps')]
            print(files)
            self.imageArr = [self.canvas_top.render(alpha=False), self.canvas_bot.render(alpha=False)]
            for i in range(len(self.imageArr)):
                print(i)
                img = Image.fromarray(self.imageArr[i])
                img.save(files[i], format='eps', resolution=100.)
            print("BTA plots saved.")
        else:
            raise NotImplementedError(f"File format {selectedFilter} not supported")

        


def register(registry, nwbFile=None, bento=None):
    bta_processing_plugin = behaviorTriggeredAverage(nwbFile, bento)
    registry.register('BTA', bta_processing_plugin)
        


