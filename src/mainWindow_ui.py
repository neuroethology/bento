# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from widgets.annotationsWidget import AnnotationsView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(460, 328)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(460, 328))
        MainWindow.setMaximumSize(QSize(457, 328))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")

        self.verticalLayout.addWidget(self.timeLabel)

        self.annotLabel = QLabel(self.centralwidget)
        self.annotLabel.setObjectName(u"annotLabel")
        self.annotLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.annotLabel)

        self.annotationsView = AnnotationsView(self.centralwidget)
        self.annotationsView.setObjectName(u"annotationsView")
        self.annotationsView.setMinimumSize(QSize(0, 50))
        self.annotationsView.setAcceptDrops(False)
        self.annotationsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.annotationsView.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.verticalLayout.addWidget(self.annotationsView)

        self.controlButtonLayout = QHBoxLayout()
        self.controlButtonLayout.setObjectName(u"controlButtonLayout")
        self.toStartButton = QPushButton(self.centralwidget)
        self.toStartButton.setObjectName(u"toStartButton")

        self.controlButtonLayout.addWidget(self.toStartButton)

        self.fbButton = QPushButton(self.centralwidget)
        self.fbButton.setObjectName(u"fbButton")

        self.controlButtonLayout.addWidget(self.fbButton)

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")

        self.controlButtonLayout.addWidget(self.backButton)

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setObjectName(u"playButton")

        self.controlButtonLayout.addWidget(self.playButton)

        self.stepButton = QPushButton(self.centralwidget)
        self.stepButton.setObjectName(u"stepButton")

        self.controlButtonLayout.addWidget(self.stepButton)

        self.ffButton = QPushButton(self.centralwidget)
        self.ffButton.setObjectName(u"ffButton")

        self.controlButtonLayout.addWidget(self.ffButton)

        self.toEndButton = QPushButton(self.centralwidget)
        self.toEndButton.setObjectName(u"toEndButton")

        self.controlButtonLayout.addWidget(self.toEndButton)


        self.verticalLayout.addLayout(self.controlButtonLayout)

        self.nextPrevLayout = QHBoxLayout()
        self.nextPrevLayout.setObjectName(u"nextPrevLayout")
        self.previousButton = QPushButton(self.centralwidget)
        self.previousButton.setObjectName(u"previousButton")

        self.nextPrevLayout.addWidget(self.previousButton)

        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")

        self.nextPrevLayout.addWidget(self.nextButton)


        self.verticalLayout.addLayout(self.nextPrevLayout)

        self.playbackSpeedLayout = QHBoxLayout()
        self.playbackSpeedLayout.setObjectName(u"playbackSpeedLayout")
        self.halveFrameRateButton = QPushButton(self.centralwidget)
        self.halveFrameRateButton.setObjectName(u"halveFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.halveFrameRateButton)

        self.oneXFrameRateButton = QPushButton(self.centralwidget)
        self.oneXFrameRateButton.setObjectName(u"oneXFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.oneXFrameRateButton)

        self.doubleFrameRateButton = QPushButton(self.centralwidget)
        self.doubleFrameRateButton.setObjectName(u"doubleFrameRateButton")

        self.playbackSpeedLayout.addWidget(self.doubleFrameRateButton)


        self.verticalLayout.addLayout(self.playbackSpeedLayout)

        self.mainButtonLayout = QHBoxLayout()
        self.mainButtonLayout.setObjectName(u"mainButtonLayout")
        self.channelComboBox = QComboBox(self.centralwidget)
        self.channelComboBox.setObjectName(u"channelComboBox")

        self.mainButtonLayout.addWidget(self.channelComboBox)

        self.newChannelPushButton = QPushButton(self.centralwidget)
        self.newChannelPushButton.setObjectName(u"newChannelPushButton")

        self.mainButtonLayout.addWidget(self.newChannelPushButton)

        self.channelHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.mainButtonLayout.addItem(self.channelHorizontalSpacer)

        self.sessionPushButton = QPushButton(self.centralwidget)
        self.sessionPushButton.setObjectName(u"sessionPushButton")

        self.mainButtonLayout.addWidget(self.sessionPushButton)

        self.quitButton = QPushButton(self.centralwidget)
        self.quitButton.setObjectName(u"quitButton")

        self.mainButtonLayout.addWidget(self.quitButton)


        self.verticalLayout.addLayout(self.mainButtonLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 460, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Current Time", None))
        self.annotLabel.setText(QCoreApplication.translate("MainWindow", u"annotation label", None))
        self.toStartButton.setText(QCoreApplication.translate("MainWindow", u"|<", None))
        self.fbButton.setText(QCoreApplication.translate("MainWindow", u"<<", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play/Stop", None))
        self.stepButton.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.ffButton.setText(QCoreApplication.translate("MainWindow", u">>", None))
        self.toEndButton.setText(QCoreApplication.translate("MainWindow", u">|", None))
        self.previousButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.halveFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"/2", None))
        self.oneXFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"1x", None))
        self.doubleFrameRateButton.setText(QCoreApplication.translate("MainWindow", u"* 2", None))
        self.newChannelPushButton.setText(QCoreApplication.translate("MainWindow", u"New Channel", None))
        self.sessionPushButton.setText(QCoreApplication.translate("MainWindow", u"Select Session...", None))
        self.quitButton.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
    # retranslateUi

