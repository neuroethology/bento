# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trialWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_TrialDockWidget(object):
    def setupUi(self, TrialDockWidget):
        if not TrialDockWidget.objectName():
            TrialDockWidget.setObjectName(u"TrialDockWidget")
        TrialDockWidget.resize(725, 511)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.newTrialPushButton = QPushButton(self.dockWidgetContents)
        self.newTrialPushButton.setObjectName(u"newTrialPushButton")

        self.gridLayout.addWidget(self.newTrialPushButton, 10, 1, 1, 1)

        self.videoViewLabel = QLabel(self.dockWidgetContents)
        self.videoViewLabel.setObjectName(u"videoViewLabel")

        self.gridLayout.addWidget(self.videoViewLabel, 2, 0, 1, 1)

        self.trialTableView = QTableView(self.dockWidgetContents)
        self.trialTableView.setObjectName(u"trialTableView")
        self.trialTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trialTableView.setProperty("showDropIndicator", False)
        self.trialTableView.setDragDropOverwriteMode(False)
        self.trialTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.trialTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.trialTableView.setTextElideMode(Qt.ElideNone)
        self.trialTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.trialTableView, 1, 0, 1, 3)

        self.loadTrialPushButton = QPushButton(self.dockWidgetContents)
        self.loadTrialPushButton.setObjectName(u"loadTrialPushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadTrialPushButton.sizePolicy().hasHeightForWidth())
        self.loadTrialPushButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.loadTrialPushButton, 10, 2, 1, 1)

        self.videoTableView = QTableView(self.dockWidgetContents)
        self.videoTableView.setObjectName(u"videoTableView")
        self.videoTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.videoTableView.setProperty("showDropIndicator", False)
        self.videoTableView.setDragDropOverwriteMode(False)
        self.videoTableView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.videoTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.videoTableView.setTextElideMode(Qt.ElideNone)
        self.videoTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.videoTableView, 3, 0, 1, 3)

        self.annotationTableView = QTableView(self.dockWidgetContents)
        self.annotationTableView.setObjectName(u"annotationTableView")
        self.annotationTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.annotationTableView.setProperty("showDropIndicator", False)
        self.annotationTableView.setDragDropOverwriteMode(False)
        self.annotationTableView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.annotationTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.annotationTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.annotationTableView, 5, 0, 1, 3)

        self.trialViewLabel = QLabel(self.dockWidgetContents)
        self.trialViewLabel.setObjectName(u"trialViewLabel")

        self.gridLayout.addWidget(self.trialViewLabel, 0, 0, 1, 1)

        self.loadCheckBoxesVerticalLayout = QVBoxLayout()
        self.loadCheckBoxesVerticalLayout.setObjectName(u"loadCheckBoxesVerticalLayout")
        self.loadPoseCheckBox = QCheckBox(self.dockWidgetContents)
        self.loadPoseCheckBox.setObjectName(u"loadPoseCheckBox")

        self.loadCheckBoxesVerticalLayout.addWidget(self.loadPoseCheckBox)

        self.loadNeuralCheckBox = QCheckBox(self.dockWidgetContents)
        self.loadNeuralCheckBox.setObjectName(u"loadNeuralCheckBox")

        self.loadCheckBoxesVerticalLayout.addWidget(self.loadNeuralCheckBox)

        self.loadAudioCheckBox = QCheckBox(self.dockWidgetContents)
        self.loadAudioCheckBox.setObjectName(u"loadAudioCheckBox")

        self.loadCheckBoxesVerticalLayout.addWidget(self.loadAudioCheckBox)


        self.gridLayout.addLayout(self.loadCheckBoxesVerticalLayout, 9, 0, 1, 1)

        self.annotationsViewLabel = QLabel(self.dockWidgetContents)
        self.annotationsViewLabel.setObjectName(u"annotationsViewLabel")

        self.gridLayout.addWidget(self.annotationsViewLabel, 4, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(5, 1)
        TrialDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(TrialDockWidget)

        QMetaObject.connectSlotsByName(TrialDockWidget)
    # setupUi

    def retranslateUi(self, TrialDockWidget):
        TrialDockWidget.setWindowTitle(QCoreApplication.translate("TrialDockWidget", u"Trial Selection Window", None))
        self.newTrialPushButton.setText(QCoreApplication.translate("TrialDockWidget", u"Add or Edit Trial...", None))
        self.videoViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Videos to Display", None))
        self.loadTrialPushButton.setText(QCoreApplication.translate("TrialDockWidget", u"Load Trial", None))
        self.trialViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Trial to Load", None))
        self.loadPoseCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Pose Data", None))
        self.loadNeuralCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Neural Data", None))
        self.loadAudioCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Audio Data", None))
        self.annotationsViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Annotation to Display", None))
    # retranslateUi

