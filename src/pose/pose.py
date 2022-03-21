# pose.py
from qtpy.QtCore import QPointF
from qtpy.QtGui import QPolygonF
from qtpy.QtWidgets import QMessageBox
import pymatreader as pmr
import warnings
import numpy as np

def load_poses(parent_widget, path: str) -> np.ndarray:
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
    polys = []
    for frame_ix in range(len(keypoints)):
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
        polys.append(frame_polys)

    return polys