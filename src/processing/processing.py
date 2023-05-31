from qtpy.QtWidgets import QFrame
from qtpy.QtCore import Slot
from pynwb import NWBFile
from qtpy.QtWidgets import QFileDialog, QMessageBox, QWidget
from os import curdir, listdir
from os.path import abspath, sep, splitext, expanduser
from importlib import import_module
from pynwb import NWBFile
import numpy as np
import sys



class ProcessingBase():
    """
    Abstract class from which to derive post processing plug-ins
    """

    def __init__(self, nwbFile, bento):
        self.nwbFile = nwbFile
        self.bento = bento
        self.neuralExists = False
        self.annotationsExists = False
        self.poseExists = False
    
    def checkData(self):
        """
        Base class template for checking if the required data exists
        in the NWBFile object for launching a selected post-processing
        module.
        """
        if list(self.nwbFile.acquisition.keys()):
            self.neuralExists = True
        if list(self.nwbFile.intervals.keys()):
            self.annotationsExists = True
        if list(self.nwbFile.processing.keys()):
            self.poseExists = True
    
    @Slot()
    def getAnnotationsData(self):
        """
        Base class template for getting annotations data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
        self.channels = list(self.nwbFile.intervals.keys())
        self.annotationsData = {}
        self.behaviorNames = {}
        for ch in self.channels:
            channelName = ch.split('_', 1)[-1]
            self.annotationsData[channelName] = self.nwbFile.intervals[ch].to_dataframe()
            if 'behaviorName' in list(self.annotationsData[channelName].columns):
                self.behaviorNames[channelName] = np.unique(np.array(self.annotationsData[channelName]['behaviorName']))
    
    def getNeuralData(self):
        """
        Base class template for getting neural data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
        self.neuralData = self.nwbFile.acquisition['neural_data'].data[:]
        self.neuralSampleRate = self.nwbFile.acquisition['neural_data'].rate
        self.neuralStartTime = self.nwbFile.acquisition['neural_data'].starting_time
        print('neural start time : ', self.neuralStartTime)
    

    def getPoseData(self):
        """
        Base class template for getting pose data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
    
    @Slot()
    def getBehaviors(self):
        """
        Base class template for getting behavior names and color codes 
        from the color_profiles file.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
        path = expanduser("~") + sep + ".bento" + sep
        profilePaths = [path, ""]
        self.behaviors = {}
        for path in profilePaths:
            try:
                fn = path + 'color_profiles.txt'
                with open(fn,'r') as f:
                    line = f.readline()
                    while line:
                        hot_key, name, r, g, b = line.strip().split(' ')
                        if hot_key == '_':
                            hot_key = ''
                        self.behaviors[name] = [float(r), float(g), float(b)]
                        line = f.readline()
                break   # no exception, so success
            except Exception as e:
                print(f"Exception caught: {e}")
                continue


    def invokeUI(self) -> QFrame:
        """
        Base class template to invoke the UI with all the necessary user-defined
        options, necessary to process the data
        """


class ProcessingRegistry():
    """
    Class that loads and manages processing plug-ins
    """

    def __init__(self, nwbFile=None, bento=None):
        self.processing_modules = {}
        self.plugin_dir = None
        self.nwbFile = nwbFile
        self.bento = bento

    def __call__(self, type: str):
        if not type in self.processing_modules:
            return None
        return self.processing_modules[type]

    def register(self, type: str, module):
        self.processing_modules[type] = module

    def load_plugins(self):
        """
        Search the plugin directory for python files of
        the form "plugin_processing_*.py"
        Import any that are found, and call their "register" function if there is one
        If no "register" function exists, the plugin will not be available for use.
        """
        plugin_dir = sys.path[0]
        if 'src' in listdir(plugin_dir):
            plugin_dir += sep + 'src'
        if 'plugin' in listdir(plugin_dir):
            plugin_dir += sep + 'plugin'
        else:
            return
        self.plugin_dir = abspath(plugin_dir)
        sys.path.append(self.plugin_dir)
        paths = listdir(self.plugin_dir)
        for path in paths:
            if not path.lower().startswith('plugin_processing_'):
                continue
            stem, _ = splitext(path)
            m = import_module(stem)
            if 'register' not in dir(m):
                continue
            m.register(self, self.nwbFile, self.bento)

    def getPluginDir(self) -> str:
        return self.plugin_dir
