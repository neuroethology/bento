# plugin_pose_MARS.py

from qtpy.QtCore import Qt, QPointF
from qtpy.QtGui import QPainter, QPen, QPolygonF
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase
import h5py as h5
import os
import json
from os.path import splitext
import numpy as np
from pynwb import NWBFile
from ndx_pose import PoseEstimationSeries, PoseEstimation
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
        self.confidence = None
        self.video_path = None

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
        return "*.mat *.json"

    def getFileFormat(self) -> str:
        return "MARS"

    def _validateFileJSON(self, parent_widget: QWidget, file_path: str) -> bool:
        with open(file_path, 'r') as f:
            keys = list(json.load(f).keys())
        if 'keypoints' not in keys:
            QMessageBox.warning(parent_widget, "Add Pose ...", "No keypoints found in pose file")
            return False
        return True
    
    def _validateFileMAT(self, parent_widget: QWidget, file_path: str) -> bool:
        with warnings.catch_warnings():
            # suppress warning coming from checking the mat file contents
            warnings.simplefilter('ignore', category=UserWarning)
            keys = list(pmr.read_mat(file_path).keys())
        if 'keypoints' not in keys:
            QMessageBox.warning(parent_widget, "Add Pose ...", "No keypoints found in pose file")
            return False
        return True
     
    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Default implementation does no checking,
        but we can do better than that
        """
        _, ext = splitext(file_path)
        ext = ext.lower()
        if ext == '.mat':
            return self._validateFileMAT(parent_widget, file_path)
        elif ext == '.json':
            return self._validateFileJSON(parent_widget, file_path)
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {ext} is not supported.")

    def loadPoses(self, parent_widget: QWidget, path: str, video_path: str):
        data = None
        _, ext = splitext(path)
        ext = ext.lower()
        if ext == '.mat':
            with warnings.catch_warnings():
                # suppress warning coming from checking the mat file contents
                warnings.simplefilter('ignore', category=UserWarning)
                data = pmr.read_mat(path)
        elif ext == '.json':
            with open(path, 'r') as f:
                data = json.load(f)
        else:
            QMessageBox.warning(parent_widget, "Extension not supported",
                f"The file extension {self.file_extension} is not supported.")
        try:
            self.keypoints = np.array(data['keypoints'])
            self.confidence = np.array(data['scores'])
        except Exception as e:
            QMessageBox.about(parent_widget, "Load Error", f"Error loading pose data from file {path}: {e}")
            return None
        self.pose_polys = []
        self.video_path = video_path
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

    def exportPosesToNWBFile(self, nwbFile: NWBFile):

        processing_module_name = f"Pose data for video {os.path.basename(self.video_path)}"
        for mouse_ix in range(self.num_mice):
            pose_estimation_series = []
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'nose',
                    description = 'Pose keypoint placed around nose',
                    data = self.keypoints[:,mouse_ix,:,0],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float), 
                    confidence = self.confidence[:,mouse_ix,0]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'left ear',
                    description = 'Pose keypoint placed around left ear',
                    data = self.keypoints[:,mouse_ix,:,1],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,1]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'right ear',
                    description = 'Pose keypoint placed around right ear',
                    data = self.keypoints[:,mouse_ix,:,2],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,2]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'neck',
                    description = 'Pose keypoint placed around neck',
                    data = self.keypoints[:,mouse_ix,:,3],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,3]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'left hip',
                    description = 'Pose keypoint placed around left hip',
                    data = self.keypoints[:,mouse_ix,:,4],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,4]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'right hip',
                    description = 'Pose keypoint placed around right hip',
                    data = self.keypoints[:,mouse_ix,:,5],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,5]
                )
            )
            pose_estimation_series.append(
                PoseEstimationSeries(
                    name = 'tail',
                    description = 'Pose keypoint placed around tail',
                    data = self.keypoints[:,mouse_ix,:,6],
                    reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                    timestamps = np.arange(self.num_frames, dtype=float),
                    confidence = self.confidence[:,mouse_ix,6]
                )
            )
            pose_estimation = PoseEstimation(
                pose_estimation_series = pose_estimation_series,
                name = f"animal_{mouse_ix}",
                description = f"Estimated position for animal_{mouse_ix} in video {os.path.basename(self.video_path)}",
                nodes = ['nose', 'left ear', 'right ear', 'neck', 'left hip', 'right hip', 'tail'],
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
    mars_pose_plugin = PoseMARS()
    registry.register(mars_pose_plugin.getFileFormat(), mars_pose_plugin)