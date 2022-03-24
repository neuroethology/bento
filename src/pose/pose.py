# pose.py
from qtpy.QtCore import QPointF
from qtpy.QtGui import QPolygonF, QPainter
from qtpy.QtWidgets import QFileDialog, QMessageBox, QWidget
from os import curdir, listdir
from os.path import abspath, sep, splitext
from importlib import import_module
import sys

class PoseBase():
    """
    Abstract class from which to derive pose support plug-ins
    """
    def __init__(self):
        pass

    def drawPoses(self, painter: QPainter, frame_ix: int):
        raise NotImplementedError("PoseBase: abstract base class.  ",
            "Please implement this in your derived class")

    def getFileSearchDescription(self) -> str:
        """
        Base class template for defining the name of this file class,
        supported by this derived class, e.g. 'MARS pose files'. This
        description will be desplayed as part of the "OpenFile" dialog.
        """
        raise NotImplementedError("PoseBase: abstract base class.  ",
            "Please implement this in your derived class")

    def getFileSearchPattern(self) -> str:
        """
        Base class template for defining the file search pattern,
        e.g. '*.h5', that should be used to filter files that
        contain pose data supported by this class.
        """
        raise NotImplementedError("PoseBase: abstract base class.  ",
            "Please implement this in your derived class")

    def getFileFormat(self) -> str:
        """
        Base class template for defining the file format as a string,
        e.g. "MARS" or "DeepLabCut"
        """
        raise NotImplementedError("PoseBase: abstract base class.  ",
            "Please implement this in your derived class")

    def validateFile(self, file_path) -> bool:
        """
        Default implementation does no checking
        """
        return True

    def loadPoses(self, parent_widget, file_path: str):
        """
        Base class template for parsing and importing all the
        pose data.  Real implementations should save away everything
        needed in class variables in order to be able to drawPoses().
        """
        raise NotImplementedError("PoseBase: abstract base class.  ",
            "Please implement this in your derived class")

class PoseRegistry():
    """
    Class that loads and manages pose plug-ins
    """

    def __init__(self):
        self.pose_modules = {}
        self.plugin_dir = None

    def __call__(self, format: str) -> PoseBase:
        if not format in self.pose_modules:
            return None
        return self.pose_modules[format]

    def register(self, format: str, module):
        self.pose_modules[format] = module

    def load_plugins(self):
        """
        Search the plugin directory for python files of
        the form "pose_plugin_*.py"
        Import any that are found, and call their "register" function if there is one
        If no "register" function exists, the plugin will not be available for use.
        """
        plugin_dir = curdir
        if 'src' in listdir(plugin_dir):
            plugin_dir += sep + 'src'
        if 'plugin' in listdir(plugin_dir):
            plugin_dir += sep + 'plugin'
        else:
            # pose plugin directory not found
            return
        self.plugin_dir = abspath(plugin_dir)
        sys.path.append(self.plugin_dir)

        paths = listdir(self.plugin_dir)
        for path in paths:
            # Pose plugin file names must start with "plugin_pose_"
            if not path.lower().startswith('plugin_pose_'):
                continue
            stem, _ = splitext(path)
            m = import_module(stem)
            if 'register' not in dir(m):
                continue
            m.register(self)

    def getPluginDir(self) -> str:
        """
        The location in the file system of the plugin folder.
        Plugins that need this, for example to find a configuration file,
        should capture it at time of plugin registration, when the registry
        class is available.  Otherwise, access will need to come from whatever
        is holding onto the PoseRegistry instance.
        """
        return self.plugin_dir

    def getPoseFilePath(self, parent_widget: QWidget, baseDir: str) -> tuple:
        """
        Presents OpenFile dialog, with file search options built from
        the registered pose plugins.

        returns: file path and format, as strings
        """
        selectionFilters = []
        module_dict = {}
        for format in self.pose_modules:
            module = self.pose_modules[format]
            filepath_filter = (f"{module.getFileSearchDescription()} " +
                f"({module.getFileSearchPattern()})")
            selectionFilters.append(filepath_filter)
            module_dict[filepath_filter] = module
        if len(selectionFilters) == 0:
            QMessageBox.warning("Add Pose ...", "No pose plugins found")
            return None
        default_string = selectionFilters[0]
        options_string = ';;'.join([path_filter for path_filter in selectionFilters])
        poseFilePath, selectedFilter = QFileDialog.getOpenFileName(
            parent_widget,
            "Select a Pose file to add to this video",
            baseDir,
            options_string,
            default_string)
        if not poseFilePath:
            return None # getOpenFileName returned with nothing selected == operation cancelled
        # do a sanity check on the returned file

        selectedModule = module_dict[selectedFilter]
        if not selectedModule.validateFile(poseFilePath):
            return None, None
        return poseFilePath, selectedModule.getFileFormat()
