# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videoWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_videoFrame(object):
    def setupUi(self, videoFrame):
        if not videoFrame.objectName():
            videoFrame.setObjectName(u"videoFrame")
        videoFrame.resize(798, 542)
        self.verticalLayout = QVBoxLayout(videoFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftSpacer = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.leftSpacer)

        self.showPoseCheckBox = QCheckBox(videoFrame)
        self.showPoseCheckBox.setObjectName(u"showPoseCheckBox")
        self.showPoseCheckBox.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showPoseCheckBox.sizePolicy().hasHeightForWidth())
        self.showPoseCheckBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.showPoseCheckBox)

        self.rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.rightSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.videoView = QGraphicsView(videoFrame)
        self.videoView.setObjectName(u"videoView")
        self.videoView.setInteractive(False)

        self.verticalLayout.addWidget(self.videoView)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(videoFrame)

        QMetaObject.connectSlotsByName(videoFrame)
    # setupUi

    def retranslateUi(self, videoFrame):
        videoFrame.setWindowTitle(QCoreApplication.translate("videoFrame", u"Video Viewer", None))
        self.showPoseCheckBox.setText(QCoreApplication.translate("videoFrame", u"Show Pose", None))
    # retranslateUi

