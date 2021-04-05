# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
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

from widgets.annotationsWidget import AnnotationsView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(457, 328)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(457, 328))
        MainWindow.setMaximumSize(QSize(457, 328))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.annotLabel = QLabel(self.centralwidget)
        self.annotLabel.setObjectName(u"annotLabel")
        self.annotLabel.setGeometry(QRect(10, 20, 271, 101))
        self.annotLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(10, 0, 301, 16))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 120, 454, 32))
        self.controlButtonLayout = QHBoxLayout(self.layoutWidget)
        self.controlButtonLayout.setObjectName(u"controlButtonLayout")
        self.controlButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.toStartButton = QPushButton(self.layoutWidget)
        self.toStartButton.setObjectName(u"toStartButton")

        self.controlButtonLayout.addWidget(self.toStartButton)

        self.fbButton = QPushButton(self.layoutWidget)
        self.fbButton.setObjectName(u"fbButton")

        self.controlButtonLayout.addWidget(self.fbButton)

        self.backButton = QPushButton(self.layoutWidget)
        self.backButton.setObjectName(u"backButton")

        self.controlButtonLayout.addWidget(self.backButton)

        self.playButton = QPushButton(self.layoutWidget)
        self.playButton.setObjectName(u"playButton")

        self.controlButtonLayout.addWidget(self.playButton)

        self.stepButton = QPushButton(self.layoutWidget)
        self.stepButton.setObjectName(u"stepButton")

        self.controlButtonLayout.addWidget(self.stepButton)

        self.ffButton = QPushButton(self.layoutWidget)
        self.ffButton.setObjectName(u"ffButton")

        self.controlButtonLayout.addWidget(self.ffButton)

        self.toEndButton = QPushButton(self.layoutWidget)
        self.toEndButton.setObjectName(u"toEndButton")

        self.controlButtonLayout.addWidget(self.toEndButton)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(240, 240, 210, 32))
        self.mainButtonLayout = QHBoxLayout(self.layoutWidget1)
        self.mainButtonLayout.setObjectName(u"mainButtonLayout")
        self.mainButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.sessionPushButton = QPushButton(self.layoutWidget1)
        self.sessionPushButton.setObjectName(u"sessionPushButton")

        self.mainButtonLayout.addWidget(self.sessionPushButton)

        self.quitButton = QPushButton(self.layoutWidget1)
        self.quitButton.setObjectName(u"quitButton")

        self.mainButtonLayout.addWidget(self.quitButton)

        self.layoutWidget2 = QWidget(self.centralwidget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(90, 160, 280, 32))
        self.nextPrevLayout = QHBoxLayout(self.layoutWidget2)
        self.nextPrevLayout.setObjectName(u"nextPrevLayout")
        self.nextPrevLayout.setContentsMargins(0, 0, 0, 0)
        self.previousButton = QPushButton(self.layoutWidget2)
        self.previousButton.setObjectName(u"previousButton")

        self.nextPrevLayout.addWidget(self.previousButton)

        self.nextButton = QPushButton(self.layoutWidget2)
        self.nextButton.setObjectName(u"nextButton")

        self.nextPrevLayout.addWidget(self.nextButton)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(98, 200, 261, 32))
        self.playbackSpeedLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.playbackSpeedLayout.setObjectName(u"playbackSpeedLayout")
        self.playbackSpeedLayout.setContentsMargins(0, 0, 0, 0)
        self.halveFrameRateButton = QPushButton(self.horizontalLayoutWidget)
        self.halveFrameRateButton.setObjectName(u"halveFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.halveFrameRateButton)

        self.oneXFrameRateButton = QPushButton(self.horizontalLayoutWidget)
        self.oneXFrameRateButton.setObjectName(u"oneXFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.oneXFrameRateButton)

        self.doubleFrameRateButton = QPushButton(self.horizontalLayoutWidget)
        self.doubleFrameRateButton.setObjectName(u"doubleFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.doubleFrameRateButton)

        self.annotationsView = AnnotationsView(self.centralwidget)
        self.annotationsView.setObjectName(u"annotationsView")
        self.annotationsView.setGeometry(QRect(0, 60, 451, 51))
        self.annotationsView.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 457, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.annotLabel.setText(QCoreApplication.translate("MainWindow", u"annotation label", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Current Time", None))
        self.toStartButton.setText(QCoreApplication.translate("MainWindow", u"|<", None))
        self.fbButton.setText(QCoreApplication.translate("MainWindow", u"<<", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play/Stop", None))
        self.stepButton.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.ffButton.setText(QCoreApplication.translate("MainWindow", u">>", None))
        self.toEndButton.setText(QCoreApplication.translate("MainWindow", u">|", None))
        self.sessionPushButton.setText(QCoreApplication.translate("MainWindow", u"Select Session...", None))
        self.quitButton.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.previousButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.halveFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"/2", None))
        self.oneXFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"1x", None))
        self.doubleFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"* 2", None))
    # retranslateUi

