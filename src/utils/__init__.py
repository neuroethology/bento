# __init__.py for utils

from os.path import abspath, sep
from PySide2.QtCore import QMarginsF, QRectF

def fix_path(path):
    return abspath(path.replace('\\', sep).replace('/', sep))

SCENE_PADDING = 200.
def padded_rectf(rectf: QRectF):
    return rectf + QMarginsF(SCENE_PADDING, 0., SCENE_PADDING, 0.)
