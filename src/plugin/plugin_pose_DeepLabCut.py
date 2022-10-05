# plugin_pose_DeepLabCut.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase
from collections import OrderedDict
from utils import get_colormap
import csv
import os
import numpy as np
import pandas as pd
import h5py
from pynwb import NWBFile
from ndx_pose import PoseEstimationSeries, PoseEstimation
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
                header1[1] != 'body_parts' or
                (len(header1) - 2) % 3 != 0):   # "", "body_parts", 3 x <bodypart_name>, ...
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

    def _loadPoses_h5(self, parent_widget: QWidget, path: str, video_path: str):
        raise NotImplementedError("Please implement this in your derived class")

    def _loadPoses_csv(self, parent_widget: QWidget, path: str, video_path: str):
        raise NotImplementedError("Please implement this in your derived class")

    def loadPoses(self, parent_widget: QWidget, path: str, video_path: str):
        _, self.file_extension = splitext(path)
        self.file_extension = self.file_extension.lower()
        if self.file_extension == '.h5':
            self._loadPoses_h5(parent_widget, path, video_path)
        elif self.file_extension == '.csv':
            self._loadPoses_csv(parent_widget, path, video_path)
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {self.file_extension} is not supported.")

class PoseDLC_generic(PoseDLCBase):

    def __init__(self):
        super().__init__()
        self.file_extension = None
        self.frame_points = []
        self.pose_data = np.array([])
        self.body_parts = np.array([])
        self.video_path = None    
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

    def _loadPoses_h5(self, parent_widget, path: str, video_path: str):
        # TODO: need to change this from the mouse form to a more generic
        # version that just stores the points.
        df = pd.read_hdf(path)
        self.body_parts = np.array(df.columns.get_level_values(1))
        self.pose_data = np.array(df)
        self.video_path = video_path
        self.num_frames = self.pose_data.shape[0]
        isColorsGenerated = False
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as row of a table
            this_frame_data = self.pose_data[frame_ix]
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

    def _loadPoses_csv(self, parent_widget, path: str, video_path: str):
        df = pd.read_csv(path, header=[0,1], index_col=0)
        self.body_parts = np.array(df.columns.get_level_values(0))
        self.pose_data = np.array(df)
        self.video_path = video_path
        self.num_frames = self.pose_data.shape[0]
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as row of a table
            this_frame_data = self.pose_data[frame_ix]
            this_frame_points = []
            vals_per_pt = 3
            num_points = int(len(this_frame_data) / vals_per_pt)
            self.generatePoseColors(num_points)
            for point_ix in range(num_points):
                # each pose point has x, y and confidence
                # we don't care about confidence
                pt_x_ix = (vals_per_pt * point_ix) + 0
                pt_y_ix = (vals_per_pt * point_ix) + 1
                this_frame_points.append(QPointF(this_frame_data[pt_x_ix], this_frame_data[pt_y_ix]))
            self.frame_points.append(this_frame_points)
    
    def exportPosesToNWBFile(self, id: int, nwbFile: NWBFile):
        processing_module_name = f"Pose data for video {os.path.basename(self.video_path)}"
        #reshape pose data to [frames, body_parts, points]
        pose_data = self.pose_data.reshape(self.num_frames, -1, 3) # 3 because x, y, confidence
        # maintain bodyparts order
        order_dict = OrderedDict()
        for node in self.body_parts:
            order_dict[node] = 1
        body_parts = np.array(list(order_dict.keys()))
        
        
        pose_estimation_series = []
        for nodes_ix in range(body_parts.shape[0]):
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = f"{body_parts[nodes_ix]}",
                    description = f"Pose keypoint placed aroud {body_parts[nodes_ix]}",
                    data = pose_data[:,nodes_ix,:2],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float), 
                    confidence = pose_data[:,nodes_ix,2]
                )
            )
        pose_estimation = PoseEstimation(
            pose_estimation_series = pose_estimation_series,
            name = f"animal_0",
            description = f"Estimated position for animal_0 in video {os.path.basename(self.video_path)}",
            nodes = body_parts,
        )
        if processing_module_name in nwbFile.processing:
            nwbFile.processing[processing_module_name].add(pose_estimation)
        else:
            pose_pm = nwbFile.create_processing_module(
                name = processing_module_name,
                description = f"Pose Data from {self.getFileFormat().split('_')[0]}"
            )
            pose_pm.add(pose_estimation)
        
        return nwbFile
    
class PoseDLC_mouse(PoseDLCBase):

    def __init__(self):
        super().__init__()
        self.pose_polys = []
        self.body_parts = np.array([])
        self.pose_data = np.array([])
        self.num_frames = 0
        self.num_mice = 0
        self.video_path = None
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

    def _loadPoses_h5(self, parent_widget: QWidget, path: str, video_path: str):
        df = pd.read_hdf(path)
        self.body_parts = np.array(df.columns.get_level_values(1))
        self.pose_data = np.array(df)
        self.pose_polys = []
        self.video_path = video_path
        self.num_frames = self.pose_data.shape[0]
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as row of a table
            this_frame_data = self.pose_data[frame_ix]
            frame_polys = []
            vals_per_pt = 3
            pts_per_mouse = 7
            vals_per_mouse = vals_per_pt * pts_per_mouse   #21
            self.num_mice = int(len(this_frame_data) / vals_per_mouse)  
            num_pts = int(self.pose_data.shape[1]/vals_per_pt)
            if num_pts % pts_per_mouse != 0:
                QMessageBox.warning(parent_widget, "Improper number of points for mice",
                    f"Expected a multiple of 7 points, got {num_pts}")
                break
            for mouse_ix in range(self.num_mice):
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

    def _loadPoses_csv(self, parent_widget: QWidget, path: str, video_path: str):
        # reading multi-index csv file with first three rows
        # as header and first column as row index
        df = pd.read_csv(path, header=[0,1,2], index_col=0)
        self.body_parts = np.array(df.columns.get_level_values(1))
        self.pose_data = np.array(df)
        self.pose_polys = []
        self.video_path = video_path
        self.num_frames = self.pose_data.shape[0]
        for frame_ix in range(self.num_frames):
            # DLC stores each frame as row of a table
            this_frame_data = self.pose_data[frame_ix]
            frame_polys = []
            vals_per_pt = 3
            pts_per_mouse = 7
            vals_per_mouse = vals_per_pt * pts_per_mouse
            self.num_mice = int(len(this_frame_data) / vals_per_mouse)
            num_pts = int(self.pose_data.shape[1]/vals_per_pt)
            if num_pts % pts_per_mouse != 0:
                QMessageBox.warning(parent_widget, "Improper number of points for mice",
                    f"Expected a multiple of 7 points, got {num_pts}")
                break
            for mouse_ix in range(self.num_mice):
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
    
    def exportPosesToNWBFile(self, id: int, nwbFile: NWBFile):
        processing_module_name = f"Pose data for video {os.path.basename(self.video_path)}"
        #reshape pose data to [frames, numOfMice, body_parts, points]
        pose_data = self.pose_data.reshape(self.num_frames, self.num_mice, -1, 3) # 3 because x, y, confidence
        # maintain bodyparts order
        order_dict = OrderedDict()
        for node in self.body_parts:
            order_dict[node] = 1
        body_parts = np.array(list(order_dict.keys())).reshape(-1, pose_data.shape[2])

        for mouse_ix in range(self.num_mice):
            pose_estimation_series = []
            for nodes_ix in range(body_parts.shape[1]):
                pose_estimation_series.append(
                    PoseEstimationSeries(
                        name = f"{body_parts[mouse_ix, nodes_ix]}",
                        description = f"Pose keypoint placed aroud {body_parts[mouse_ix, nodes_ix]}",
                        data = pose_data[:,mouse_ix,nodes_ix,:2],
                        reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                        timestamps = np.arange(self.num_frames, dtype=float), 
                        confidence = pose_data[:,mouse_ix,nodes_ix,2]
                    )
                )
            pose_estimation = PoseEstimation(
                pose_estimation_series = pose_estimation_series,
                name = f"animal_{mouse_ix}",
                description = f"Estimated position for animal_{mouse_ix} in video {os.path.basename(self.video_path)}",
                nodes = body_parts[mouse_ix,:],
                edges = np.array([[0,1], [1,3], [3,4], [4,6], [6,5], [5,3], [3,2], [2,0]], dtype='uint8')
            )
            if processing_module_name in nwbFile.processing:
                nwbFile.processing[processing_module_name].add(pose_estimation)
            else:
                pose_pm = nwbFile.create_processing_module(
                    name = processing_module_name,
                    description = f"Pose Data from {self.getFileFormat().split('_')[0]}"
                )
                pose_pm.add(pose_estimation)
        
        return nwbFile

def register(registry):
    # construct and register the generic plugin
    pose_plugin_generic = PoseDLC_generic()
    registry.register(pose_plugin_generic.getFileFormat(), pose_plugin_generic)

    # construct and register the MARS-style mouse-specific plugin
    pose_plugin_mouse = PoseDLC_mouse()
    registry.register(pose_plugin_mouse.getFileFormat(), pose_plugin_mouse)