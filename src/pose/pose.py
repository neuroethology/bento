# pose.py
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
    return keypoints