# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videoWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class ConstantAspectGridLayout(QGridLayout):
    """
    Layout class that keeps the corresponding widget's aspect ratio constant
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aspect_ratio = 1.

    def hasHeightFromWidth(self):
        return True

    def heightFromWidth(self, width: int):
        return int(float(width) * self.aspectRatio + 0.5)

    def setAspectRatio(self, ratio: float):
        self.aspect_ratio = ratio
class Ui_videoFrame(object):
    def setupUi(self, videoFrame):
        if videoFrame.objectName():
            videoFrame.setObjectName(u"videoFrame")
        videoFrame.resize(761, 628)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(videoFrame.sizePolicy().hasHeightForWidth())
        videoFrame.setSizePolicy(sizePolicy)
        self.gridLayout = ConstantAspectGridLayout(videoFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(videoFrame)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(videoFrame)

        QMetaObject.connectSlotsByName(videoFrame)
    # setupUi

    def retranslateUi(self, videoFrame):
        videoFrame.setWindowTitle(QCoreApplication.translate("videoFrame", u"Video Viewer", None))
        self.label.setText(QCoreApplication.translate("videoFrame", u"Video", None))
    # retranslateUi

