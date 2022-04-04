# plugin_pose_DeepLabCut.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase
import numpy as np
import h5py
from os.path import splitext

"""
Bento plugin that provides support for MARS-style pose files
represented MatLab .mat files.

Implements a class derived from PoseBase, which is an abstract class.
"""

class PoseDLC_mouse(PoseBase):

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
        return "DeepLabCut mouse pose files"

    def getFileSearchPattern(self) -> str:
        return "*.h5"

    def getFileFormat(self) -> str:
        return "DeepLabCut_mouse"

    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        h5 = h5py.File(file_path, 'r')
        default_group = h5[list(h5.keys())[0]]
        if 'table' not in default_group.keys():
            QMessageBox.warning(parent_widget, "Add Pose ...", "No pose data found in pose file")
            return False
        return True

    def loadPoses(self, parent_widget: QWidget, path: str):
        h5 = h5py.File(path, 'r')
        default_group = h5[list(h5.keys())[0]]
        table = default_group['table']
        self.pose_polys = []
        self.num_frames = len(table)
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as (frame_idx, (pose_array))
            # we don't care about the frame_idx
            this_frame_data = table[frame_ix][1]
            frame_polys = []
            vals_per_pt = 3
            pts_per_mouse = 7
            vals_per_mouse = vals_per_pt * pts_per_mouse
            num_mice = int(len(this_frame_data) / vals_per_mouse)
            for mouse_ix in range(num_mice):
                # each pose point has x, y and confidence
                # we don't care about confidence
                poly = QPolygonF()
                pt_x_ix = (vals_per_mouse * mouse_ix) + 0
                pt_y_ix = (vals_per_mouse * mouse_ix) + 1
                nose = QPointF(this_frame_data[pt_x_ix], this_frame_data[pt_y_ix])
                poly.append(nose)
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (1 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (1 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (3 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (3 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (4 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (4 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (6 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (6 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (5 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (5 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (3 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (3 * vals_per_pt)]))
                poly.append(QPointF(
                    this_frame_data[pt_x_ix + (2 * vals_per_pt)],
                    this_frame_data[pt_y_ix + (2 * vals_per_pt)]))
                poly.append(nose)
                frame_polys.append(poly)
            self.pose_polys.append(frame_polys)

class PoseDLC_generic(PoseBase):

    def __init__(self):
        super().__init__()
        self.file_extension = None
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
        return "DeepLabCut geenric pose files"

    def getFileSearchPattern(self) -> str:
        return "*.h5"

    def getFileFormat(self) -> str:
        return "DeepLabCut_generic"

    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        _, ext = splitext(file_path)
        ext = ext.lower()
        if ext == 'h5':
            h5 = h5py.File(file_path, 'r')
            default_group = h5[list(h5.keys())[0]]
            if 'table' not in default_group.keys():
                QMessageBox.warning(parent_widget, "Add Pose ...", "No pose data found in pose file")
                return False
            return True
        elif ext == 'csv':
            #TODO: validate .csv file
            return True
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {ext} is not supported.")

    def loadPoses(self, parent_widget: QWidget, path: str):
        _, self.file_extension = splitext(path)
        self.file_extension = self.file_extension.lower()
        if self.file_extension == 'h5':
            # TODO: need to change this from the mouse form to a more generic
            # version that just stores the points.
            h5 = h5py.File(path, 'r')
            default_group = h5[list(h5.keys())[0]]
            table = default_group['table']
            self.pose_polys = []
            self.num_frames = len(table)
            for frame_ix in range(self.num_frames):
                # DLC stores each frame as (frame_idx, (pose_array))
                # we don't care about the frame_idx
                this_frame_data = table[frame_ix][1]
                frame_polys = []
                vals_per_pt = 3
                pts_per_mouse = 7
                vals_per_mouse = vals_per_pt * pts_per_mouse
                num_mice = int(len(this_frame_data) / vals_per_mouse)
                for mouse_ix in range(num_mice):
                    # each pose point has x, y and confidence
                    # we don't care about confidence
                    poly = QPolygonF()
                    pt_x_ix = (vals_per_mouse * mouse_ix) + 0
                    pt_y_ix = (vals_per_mouse * mouse_ix) + 1
                    nose = QPointF(this_frame_data[pt_x_ix], this_frame_data[pt_y_ix])
                    poly.append(nose)
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (1 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (1 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (3 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (3 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (4 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (4 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (6 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (6 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (5 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (5 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (3 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (3 * vals_per_pt)]))
                    poly.append(QPointF(
                        this_frame_data[pt_x_ix + (2 * vals_per_pt)],
                        this_frame_data[pt_y_ix + (2 * vals_per_pt)]))
                    poly.append(nose)
                    frame_polys.append(poly)
                self.pose_polys.append(frame_polys)
        elif self.file_extension == 'csv':
            # open and parse comma-separated-value files ala Excel
            pass
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {self.file_extension} is not supported.")

def register(registry):
    # construct and register the generic plugin
    # pose_plugin = PoseDLC_generic()
    # registry.register(pose_plugin.getFileFormat(), pose_plugin)

    # construct and register the MARS-style mouse-specific plugin
    pose_plugin = PoseDLC_mouse()
    registry.register(pose_plugin.getFileFormat(), pose_plugin)