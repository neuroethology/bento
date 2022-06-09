# plugin_pose_MARS.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase
import h5py as h5
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
        self.num_mice = 0
        self.pose_colors = [Qt.blue, Qt.green]
        self.keypoints = None

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

    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            poseMat = pmr.read_mat(file_path)
        if 'keypoints' not in poseMat.keys():
            QMessageBox.warning(parent_widget, "Add Pose ...", "No keypoints found in pose file")
            return False
        return True

    def loadPoses(self, parent_widget: QWidget, path: str):
        mat = None
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            mat = pmr.read_mat(path)
        try:
            self.keypoints = mat['keypoints']
        except Exception as e:
            QMessageBox.about(parent_widget, "Load Error", f"Error loading pose data from file {path}: {e}")
            return None
        self.pose_polys = []
        self.num_frames = len(self.keypoints)
        for frame_ix in range(self.num_frames):
            frame_keypoints = self.keypoints[frame_ix]
            frame_polys = []
            self.num_mice = len(frame_keypoints)
            for mouse_ix in range(self.num_mice):
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

    def exportPosesToH5(self, id: int, openH5File: h5.File):
        if not 'pose_data' in openH5File or not f'id_{id}' in openH5File['pose_data']:
            openH5File.create_group(f'pose_data/id_{id}')
        pose_data_group = openH5File[f'pose_data/id_{id}']
        pose_nodes = pose_data_group.create_dataset('pose_nodes', shape=(7,), dtype='S10')
        pose_nodes[0] = b'nose'
        pose_nodes[1] = b'left ear'
        pose_nodes[2] = b'right ear'
        pose_nodes[3] = b'neck'
        pose_nodes[4] = b'left hip'
        pose_nodes[5] = b'right hip'
        pose_nodes[6] = b'tail'
        for mouse_ix in range(self.num_mice):
            pose_data_group.create_dataset(f"mouse_{mouse_ix}", data=self.keypoints[:,mouse_ix,:,:])

def register(registry):
    mars_pose_plugin = PoseMARS()
    registry.register(mars_pose_plugin.getFileFormat(), mars_pose_plugin)