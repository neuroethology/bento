# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videoWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QFrame,
    QGraphicsView, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_videoFrame(object):
    def setupUi(self, videoFrame):
        if not videoFrame.objectName():
            videoFrame.setObjectName(u"videoFrame")
        videoFrame.resize(798, 542)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(videoFrame.sizePolicy().hasHeightForWidth())
        videoFrame.setSizePolicy(sizePolicy)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.showPoseCheckBox.sizePolicy().hasHeightForWidth())
        self.showPoseCheckBox.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.showPoseCheckBox)

        self.rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.rightSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.videoView = QGraphicsView(videoFrame)
        self.videoView.setObjectName(u"videoView")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.videoView.sizePolicy().hasHeightForWidth())
        self.videoView.setSizePolicy(sizePolicy2)
        self.videoView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.videoView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.videoView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.videoView.setInteractive(False)
        self.videoView.setAlignment(Qt.AlignCenter)
        self.videoView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.verticalLayout.addWidget(self.videoView)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(videoFrame)

        QMetaObject.connectSlotsByName(videoFrame)
    # setupUi

    def retranslateUi(self, videoFrame):
        videoFrame.setWindowTitle(QCoreApplication.translate("videoFrame", u"Video Viewer", None))
        self.showPoseCheckBox.setText(QCoreApplication.translate("videoFrame", u"Show Pose", None))
    # retranslateUi

