# pose.py
from qtpy.QtCore import QPointF
from qtpy.QtGui import QPolygonF
from qtpy.QtWidgets import QMessageBox
import pymatreader as pmr
import warnings
import numpy as np
import h5py

def load_poses_MARS(parent_widget, path: str) -> list:
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

def load_poses_DeepLabCut(parent_widget, path: str) -> list:
    h5 = h5py.File(path, 'r')
    default_group = h5[list(h5.keys())[0]]
    table = default_group['table']
    polys = []
    for frame_ix in range(len(table)):
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
        polys.append(frame_polys)

    return polys

def load_poses(parent_widget, path: str, format: str) -> list:
    if format.lower() == 'deeplabcut' or format.lower() == 'dlc':
        return load_poses_DeepLabCut(parent_widget, path)
    return load_poses_MARS(parent_widget, path)
