from typing import List, Tuple
from qtpy.QtCore import QPointF, QLineF
from qtpy.QtGui import QColor, QPolygonF, QPainter, QPen
from qtpy.QtWidgets import QMessageBox, QWidget
from pose.pose import PoseBase, PoseRegistry
from os.path import splitext
from pynwb import NWBFile
from ndx_pose import PoseEstimationSeries, PoseEstimation
import os
import numpy as np
import h5py


class PoseSLEAP(PoseBase):
    """
    SLEAP plugin that provides support for SLEAP-style pose files
    represented as HDF5 .h5 files.

    Implements a class derived from PoseBase, which is an abstract class.
    """

    def __init__(self):
        super().__init__()
        self.pose_colors: List[QColor] = [
            QColor(0, 144, 189),  # Blue
            QColor(217, 83, 25),  # Orange
            QColor(237, 177, 32),  # Green
            QColor(126, 47, 142),  # Purple
            QColor(119, 172, 48),  # Light green
            QColor(77, 190, 238),  # Light blue
            QColor(162, 20, 47),  # Red
        ]  # Standard SLEAP colors
        self.pose_polys: List = []
        self.num_frames: int = 0
        self.num_nodes: int = 0
        self.num_instances: int = 0
        self.has_edges: bool = False
        self.pose_data: np.ndarray = np.array([])
        self.node_names: List = []

    def _drawPoses_noEdges(self, painter: QPainter, frame_ix: int):
        """
        Draw poses for SLEAP analysis files with no edge data in analysis file.
        """
        for instance_ix in range(len(self.pose_polys[frame_ix])):
            instance_color = self.pose_colors[instance_ix % len(self.pose_colors)]
            instance_poly = self.pose_polys[frame_ix][instance_ix]
            if not instance_poly.isEmpty():
                painter.setPen(QPen(instance_color, 1.5))
                painter.drawPolyline(instance_poly)
                painter.setBrush(instance_color)
                for node in instance_poly:
                    painter.drawEllipse(node, 5.0, 5.0)

    def _drawPoses_hasEdges(self, painter: QPainter, frame_ix: int):
        """
        Draw poses for SLEAP analysis files with edge data in analysis file.
        """
        frame_polys, frame_edges = self.pose_polys[frame_ix]
        for instance_ix in range(len(frame_polys)):
            instance_color = self.pose_colors[instance_ix % len(self.pose_colors)]
            instance_poly = frame_polys[instance_ix]
            instance_edges = frame_edges[instance_ix]
            if not instance_poly.isEmpty():
                # Draw nodes
                painter.setPen(QPen(instance_color, 1.5))
                painter.setBrush(instance_color)
                for node in instance_poly:
                    painter.drawEllipse(node, 5.0, 5.0)
                # Draw edges
                painter.drawLines(instance_edges)

    def drawPoses(self, painter: QPainter, frame_ix: int):
        """
        Determines if edge data is available and calls respective pose drawing methods.
        """
        if self.has_edges:
            self._drawPoses_hasEdges(painter, frame_ix)
        else:
            self._drawPoses_noEdges(painter, frame_ix)

    def getFileSearchDescription(self) -> str:
        """
        Defines the name of this file class, supported by this derived class. This
        description will be desplayed as part of the "OpenFile" dialog.
        """
        return "SLEAP analysis HDF5 file"

    def getFileSearchPattern(self) -> str:
        """
        Defines the file search pattern that should be used to filter files that
        contain pose data supported by the PoseSLEAP class.
        """
        return "*.analysis.h5"

    def getFileFormat(self) -> str:
        """
        Defines the file format as a string.
        """
        return "SLEAP_analysis_HDF5"

    def _validateFileH5(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Validates that h5 file loaded has necessary pose data. For SLEAP Anlysis HDF5
        files, the pose data information is stored in the "tracks" dataset.
        """
        with h5py.File(file_path, "r") as f:
            dset_names = list(f.keys())

        try:
            assert "tracks" and "node_names" in dset_names
        except AssertionError:
            QMessageBox.warning(
                parent_widget,
                "Add Pose ...",
                "No SLEAP pose data found in pose file. Ensure loaded as correct file format.",
            )
            return False

        return True

    def validateFile(self, parent_widget: QWidget, file_path: str) -> bool:
        """
        Check which extension is used, then perform validation specific to file type.
        """
        _, ext = splitext(file_path.lower())
        if ext == ".h5":
            return self._validateFileH5(parent_widget, file_path)
        else:
            QMessageBox.warning(
                parent_widget,
                "Extension not supported",
                f"The fileextension {ext} is not supported for SLEAP pose data.",
            )
            return False

    def _loadPoses_noEdges_h5(self, parent_widget: QWidget, file_path: str, video_path: str):
        """
        Method for parsing and importing pose data when no edge data is available.
        Save all pose information in self.pose_polys, self.num_frames, self.num_nodes,
        and self.num_instances.
        """

        def append_keypoints(body: QPolygonF, appendage: np.ndarray):
            """
            Append nodes to instance poly.
            """
            if not np.any(np.isnan(appendage)):
                body.append(QPointF(appendage[0], appendage[1]))

        with h5py.File(file_path, "r") as f:
            self.pose_data = f["tracks"][:].T
            self.node_names = [n.decode() for n in f["node_names"][:]]

        self.pose_polys: List[List[QPolygonF]] = []
        self.num_frames, self.num_nodes, _, self.num_instances = self.pose_data.shape
        self.video_path = video_path

        for frame_ix in range(self.num_frames):
            # Get all keypoints in current frame using self.pose_data[frame, node, coor, tracks]
            frame_keypoints = self.pose_data[frame_ix, :, :, :]
            frame_polys: List[QPolygonF] = []
            for instance_ix in range(self.num_instances):
                # Get all points for selected instance
                instance_keypoints = frame_keypoints[:, :, instance_ix]
                first_node = instance_keypoints[0, :]
                poly = QPolygonF()
                for node_ix in range(self.num_nodes):
                    # Get points for specific node
                    node_keypoints = instance_keypoints[node_ix, :]
                    append_keypoints(poly, node_keypoints)
                append_keypoints(poly, first_node)  # Complete the poly
                frame_polys.append(poly)  # Add instance poly to current frame polys
            self.pose_polys.append(frame_polys)  # Add frame polys to all pose polys

    def _loadPoses_hasEdges_h5(self, parent_widget: QWidget, file_path: str, video_path: str):
        """
        Method for parsing and importing pose data when edge data is available.
        Save all pose information in self.pose_polys, self.num_frames, self.num_nodes,
        and self.num_instances.
        """

        def append_keypoints(
            body: QPolygonF, appendage: np.ndarray, node_lookup: dict, node_name: str
        ):
            """
            Append nodes to instance poly. Also add node to dictionary for creating edges
            """
            if not np.any(np.isnan(appendage)):
                point = QPointF(appendage[0], appendage[1])
                body.append(point)
                node_lookup[node_name] = point

        with h5py.File(file_path, "r") as f:
            self.pose_data = f["tracks"][:].T
            if self.has_edges:
                self.node_names = [n.decode() for n in f["node_names"][:]]
                edge_names = [(s.decode(), d.decode()) for (s, d) in f["edge_names"][:]]

        self.pose_polys: List[Tuple[List[QPolygonF], List[QLineF]]] = []
        self.num_frames, self.num_nodes, _, self.num_instances = self.pose_data.shape
        self.video_path = video_path

        for frame_ix in range(self.num_frames):
            # Get all keypoints in current frame using self.pose_data[frame,node,coor,tracks]
            frame_keypoints = self.pose_data[frame_ix, :, :, :]
            frame_polys: List[QPolygonF] = []
            frame_edges: List[QLineF] = []
            for instance_ix in range(self.num_instances):
                # Get all nodes for selected instance
                instance_keypoints = frame_keypoints[:, :, instance_ix]
                node_dict = {}  # Temporary dict to help build edges
                instance_edges = []  # All edges in an instance
                poly = QPolygonF()  # Polygon for nodes in instance
                for node_ix, node_nombre in enumerate(self.node_names):
                    # Get points for specific node
                    node_keypoints = instance_keypoints[node_ix, :]
                    append_keypoints(poly, node_keypoints, node_dict, node_nombre)
                for (src_node, des_node) in edge_names:
                    if (src_node in node_dict) and (des_node in node_dict):
                        # Add edges using node points
                        edge = QLineF()
                        edge.setPoints(node_dict[src_node], node_dict[des_node])
                        instance_edges.append(edge)
                frame_edges.append(instance_edges)
                frame_polys.append(poly)
            self.pose_polys.append(
                (frame_polys, frame_edges)
            )  # Add frame polys to all pose polys

    def loadPoses(self, parent_widget: QWidget, file_path: str, video_path: str):
        """
        Method for parsing and importing all the pose data. Determines whether edge
        data is present and calls respective method for loading poses.
        """
        # Determine if edge data is available in analysis file.
        self.has_edges = False
        with h5py.File(file_path, "r") as f:
            dset_names = list(f.keys())
        if "edge_names" in dset_names:
            self.has_edges = True

        if self.has_edges:
            # Load poses with edge data available.
            self._loadPoses_hasEdges_h5(parent_widget, file_path, video_path)
        else:
            # Load poses without edge data available.
            self._loadPoses_noEdges_h5(parent_widget, file_path, video_path)
    
    def exportPosesToNWBFile(self, id: int, nwbFile: NWBFile):
        processing_module_name = f"Pose data for video {os.path.basename(self.video_path)}"

        for instance_ix in range(self.num_instances):
            pose_estimation_series = []
            for nodes_ix in range(self.num_nodes):
                pose_estimation_series.append(
                    PoseEstimationSeries(
                        name = f"{self.node_names[nodes_ix]}",
                        description = f"Pose keypoint placed aroud {self.node_names[nodes_ix]}",
                        data =self.pose_data[:,nodes_ix,:,instance_ix],
                        reference_frame = "The coordinates are in (x, y) relative to the top-left of the image",
                        timestamps = np.arange(self.num_frames, dtype=float), 
                        confidence = np.arange(self.num_frames, dtype=float) # dummy confidence - needs to change
                    )
                )
            pose_estimation = PoseEstimation(
                pose_estimation_series = pose_estimation_series,
                name = f"animal_{instance_ix}",
                description = f"Estimated position for animal_{instance_ix} in video {os.path.basename(self.video_path)}",
                nodes = self.node_names,
                # edges need to be added
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


def register(registry: PoseRegistry):
    """
    Method to register pose plugin in pose registry.
    """
    pose_plugin = PoseSLEAP()
    registry.register(pose_plugin.getFileFormat(), pose_plugin)
