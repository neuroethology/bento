# plugin_pose_MARS.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox
from pose.pose import PoseBase, PoseRegistry
import pymatreader as pmr
import warnings

"""
Bento plugin that provides support for MARS-style pose files
represented MatLab .mat files.

Implements a class derived from PoseBase, which is an abstract class.
"""

class PoseMARS(PoseBase):

    def __init__(self):
        super().__init__()
        self.pose_polys = []
        self.num_frames = 0
        self.pose_colors = [Qt.blue, Qt.green]

    def drawPoses(self, painter: QPainter, frame_ix: int):
        frame_ix = min(frame_ix, self.num_frames)
        try:
            for mouse_ix in range(len(self.pose_polys[frame_ix])):
                painter.setPen(QPen(self.pose_colors[mouse_ix], 2.0))
                painter.drawPolyline(self.pose_polys[frame_ix][mouse_ix])
                painter.setBrush(Qt.red)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(self.pose_polys[frame_ix][mouse_ix].first(), 5.0, 5.0) # red dot on nose
        except IndexError as e:
            # number of video frames is greater than number of pose frames.  Oh well!
            pass

    def getFileSearchDescription(self) -> str:
        return "MARS pose files"

    def getFileSearchPattern(self) -> str:
        return "*.mat"

    def getFileFormat(self) -> str:
        return "MARS"

    def validateFile(self, file_path) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            poseMat = pmr.read_mat(file_path)
        if 'keypoints' not in poseMat.keys():
            QMessageBox.warning(self, "Add Pose ...", "No keypoints found in pose file")
            return False
        return True

    def loadPoses(self, parent_widget, path: str):
        mat = None
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            mat = pmr.read_mat(path)
        try:
            keypoints = mat['keypoints']
        except Exception as e:
            QMessageBox.about(parent_widget, "Load Error", f"Error loading pose data from file {path}: {e}")
            return None
        self.pose_polys = []
        self.num_frames = len(keypoints)
        for frame_ix in range(self.num_frames):
            frame_keypoints = keypoints[frame_ix]
            frame_polys = []
            for mouse_ix in range(len(frame_keypoints)):
                mouse_keypoints = frame_keypoints[mouse_ix]
                pose_x = mouse_keypoints[0]
                pose_y = mouse_keypoints[1]
                poly = QPolygonF()
                nose = QPointF(pose_x[0], pose_y[0])
                poly.append(nose)    # nose
                poly.append(QPointF(pose_x[1], pose_y[1]))    # left ear
                poly.append(QPointF(pose_x[3], pose_y[3]))    # neck
                poly.append(QPointF(pose_x[4], pose_y[4]))    # left hip
                poly.append(QPointF(pose_x[6], pose_y[6]))    # tail
                poly.append(QPointF(pose_x[5], pose_y[5]))    # right hip
                poly.append(QPointF(pose_x[3], pose_y[3]))    # neck
                poly.append(QPointF(pose_x[2], pose_y[2]))    # right ear
                poly.append(nose)    # nose
                frame_polys.append(poly)
            self.pose_polys.append(frame_polys)

def register(registry):
    mars_pose_plugin = PoseMARS()
    registry.register(mars_pose_plugin.getFileFormat(), mars_pose_plugin)