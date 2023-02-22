from qtpy.QtWidgets import QWidget
from qtpy.QtCore import Slot
from pynwb import NWBFile



class PostProcessingBase():
    """
    Abstract class from which to derive post processing plug-ins
    """
    def __init__(self):
        pass
    
    def checkData(self, nwbFile: NWBFile):
        """
        Base class template for checking if the required data exists
        in the NWBFile object for launching a selected post-processing
        module.
        """
    
    def getAnnotationsData(self, nwbFile: NWBFile):
        """
        Base class template for getting annotations data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
    
    def getNeuralData(self, nwbFile: NWBFile):
        """
        Base class template for getting neural data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
    

    def getPoseData(self, nwbFile: NWBFile):
        """
        Base class template for getting pose data from the NWBFile object.
        Implementation should save all the required information in class 
        variables in order to be able to plot the results
        """
    
    
    @Slot()
    def invokeUI(self, parent_widget: QWidget) -> QWidget:
        """
        Base class template to invoke the UI with all the necessary user-defined
        options, necessary to process the data
        """

