# plugin_pose_DeepLabCut.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase
from utils import get_colormap
import csv
import numpy as np
import h5py
from os.path import splitext


"""
Bento plugin that provides support for MARS-style pose files
represented MatLab .mat files.

Implements a class derived from PoseBase, which is an abstract class.
"""

class PoseDLCBase(PoseBase):
    """
    Base class for DeepLabCut pose support

    Includes implementation common to generic and mouse-specific DLC files
    """

    def __init__(self):
        super().__init__()

    def getFileSearchPattern(self) -> str:
        return "*.h5 *.csv"

    def _validateFileH5(self, parent_widget, file_path: str) -> bool:
        h5 = h5py.File(file_path, 'r')
        default_group = h5[list(h5.keys())[0]]
        if 'table' not in default_group.keys():
            QMessageBox.warning(parent_widget, "Add Pose ...", "No pose data found in pose file")
            return False
        return True

    def _validateFileCSV(self, parent_widget, file_path: str) -> bool:
        result = True
        with open(file_path, 'r') as csvFile:
            reader = csv.reader(csvFile)
            header1 = next(reader)
            if (not isinstance(header1[1], str) or
                header1[1] != 'bodyparts' or
                (len(header1) - 2) % 3 != 0):   # "", "bodyparts", 3 x <bodypart_name>, ...
                result = False
            csvFile.seek(0)
        return result

    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        _, ext = splitext(file_path)
        ext = ext.lower()
        if ext == '.h5':
            return self._validateFileH5(parent_widget, file_path)
        elif ext == '.csv':
            return self._validateFileCSV(parent_widget, file_path)
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {ext} is not supported.")

    def _loadPoses_h5(self, parent_widget: QWidget, path: str):
        raise NotImplementedError("Please implement this in your derived class")

    def _loadPoses_csv(self, parent_widget: QWidget, path: str):
        raise NotImplementedError("Please implement this in your derived class")

    def loadPoses(self, parent_widget: QWidget, path: str):
        _, self.file_extension = splitext(path)
        self.file_extension = self.file_extension.lower()
        if self.file_extension == '.h5':
            self._loadPoses_h5(parent_widget, path)
        elif self.file_extension == '.csv':
            self._loadPoses_csv(parent_widget, path)
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {self.file_extension} is not supported.")

class PoseDLC_generic(PoseDLCBase):

    def __init__(self):
        super().__init__()
        self.file_extension = None
        self.frame_points = []
        self.num_frames = 0
        # Construct colors based on the number of body parts and the color map
        self.colormap_data = get_colormap('turbo')
        self.pose_colors = None

    def generatePoseColors(self, n):
        if n < 1 or n > 256:
            raise ValueError("generatePoseColors: n must be between 1 and 256 inclusive")
        if n == 1:
            self.pose_colors = [QColor(self.colormap_data[127])]
        else:
            step = 255. / (n - 1)
            self.pose_colors = [QColor(self.colormap_data[round(ix * step)]) for ix in range(n)]

    def drawPoses(self, painter: QPainter, frame_ix: int):
        frame_ix = min(frame_ix, self.num_frames)
        painter.setPen(Qt.NoPen)
        if len(self.frame_points[frame_ix]) > len(self.pose_colors):
            raise ValueError("drawPoses: number of points t draw exceeds number of body parts")
        for ix, point in enumerate(self.frame_points[frame_ix]):
            painter.setBrush(self.pose_colors[ix])
            painter.drawEllipse(point, 5.0, 5.0)

    def getFileSearchDescription(self) -> str:
        return "DeepLabCut generic pose files"

    def getFileFormat(self) -> str:
        return "DeepLabCut_generic"

    def _loadPoses_h5(self, parent_widget, path: str):
        # TODO: need to change this from the mouse form to a more generic
        # version that just stores the points.
        h5 = h5py.File(path, 'r')
        default_group = h5[list(h5.keys())[0]]
        table = default_group['table']
        self.num_frames = len(table)
        isColorsGenerated = False
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as (frame_idx, (pose_array))
            # we don't care about the frame_idx
            this_frame_data = table[frame_ix][1]
            this_frame_points = []
            vals_per_pt = 3
            num_points = int(len(this_frame_data) / vals_per_pt)
            if not isColorsGenerated:
                self.generatePoseColors(num_points)
            for point_ix in range(num_points):
                # each pose point has x, y and confidence
                # we don't care about confidence
                pt_x_ix = (vals_per_pt * point_ix) + 0
                pt_y_ix = (vals_per_pt * point_ix) + 1
                this_frame_points.append(QPointF(this_frame_data[pt_x_ix], this_frame_data[pt_y_ix]))
            self.frame_points.append(this_frame_points)

    def _loadPoses_csv(self, parent_widget, path: str):
        with open(path, 'r') as csvFile:
            vals_per_pt = 3 # x, y, confidence.  We don't care about confidence.
            reader = csv.reader(csvFile)
            header1 = next(reader)
            num_pts = int((len(header1) - 2) / vals_per_pt)
            self.generatePoseColors(num_pts)
            _ = next(reader)    # skip over second row of header
            while True:
                try:
                    row = next(reader)
                except StopIteration:
                    break
                this_frame_points = []
                for point_ix in range(num_pts):
                    pt_x_ix = (vals_per_pt * point_ix) + 2
                    pt_y_ix = (vals_per_pt * point_ix) + 3
                    this_frame_points.append(QPointF(float(row[pt_x_ix]), float(row[pt_y_ix])))
                self.frame_points.append(this_frame_points)
            self.num_frames = len(self.frame_points)

class PoseDLC_mouse(PoseDLCBase):

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

    def getFileFormat(self) -> str:
        return "DeepLabCut_mouse"

    def _loadPoses_h5(self, parent_widget: QWidget, path: str):
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

    def _loadPoses_csv(self, parent_widget: QWidget, path: str):
        with open(path, 'r') as csvFile:
            vals_per_pt = 3 # x, y, confidence.  We don't care about confidence.
            vals_per_mouse = 7
            reader = csv.reader(csvFile)
            header1 = next(reader)
            num_pts = int((len(header1) - 2) / vals_per_pt)
            if num_pts % vals_per_mouse != 0:
                QMessageBox.warning(parent_widget, "Improper number of points for mice",
                    f"Expected a multiple of 7 points, got {num_pts}")
                return
            _ = next(reader)    # skip over second row of header
            while True:
                try:
                    row = next(reader)
                except StopIteration:
                    break
                num_mice = int(num_pts / vals_per_mouse)
                frame_polys = []
                for mouse_ix in range(num_mice):
                    # each pose point has x, y and confidence
                    # we don't care about confidence
                    poly = QPolygonF()
                    pt_x_ix = (vals_per_mouse * mouse_ix) + 2
                    pt_y_ix = (vals_per_mouse * mouse_ix) + 3
                    nose = QPointF(row[pt_x_ix], row[pt_y_ix])
                    poly.append(nose)
                    poly.append(QPointF(
                        row[pt_x_ix + (1 * vals_per_pt)],
                        row[pt_y_ix + (1 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (3 * vals_per_pt)],
                        row[pt_y_ix + (3 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (4 * vals_per_pt)],
                        row[pt_y_ix + (4 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (6 * vals_per_pt)],
                        row[pt_y_ix + (6 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (5 * vals_per_pt)],
                        row[pt_y_ix + (5 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (3 * vals_per_pt)],
                        row[pt_y_ix + (3 * vals_per_pt)]))
                    poly.append(QPointF(
                        row[pt_x_ix + (2 * vals_per_pt)],
                        row[pt_y_ix + (2 * vals_per_pt)]))
                    poly.append(nose)
                    frame_polys.append(poly)
                self.pose_polys.append(frame_polys)
            self.num_frames = len(self.frame_points)

def register(registry):
    # construct and register the generic plugin
    pose_plugin_generic = PoseDLC_generic()
    registry.register(pose_plugin_generic.getFileFormat(), pose_plugin_generic)

    # construct and register the MARS-style mouse-specific plugin
    pose_plugin_mouse = PoseDLC_mouse()
    registry.register(pose_plugin_mouse.getFileFormat(), pose_plugin_mouse)