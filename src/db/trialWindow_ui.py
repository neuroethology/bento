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
        TrialDockWidget.resize(723, 850)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.annotationTableView = QTableView(self.dockWidgetContents)
        self.annotationTableView.setObjectName(u"annotationTableView")
        self.annotationTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.annotationTableView.setProperty("showDropIndicator", False)
        self.annotationTableView.setDragDropOverwriteMode(False)
        self.annotationTableView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.annotationTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.annotationTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.annotationTableView, 9, 0, 1, 3)

        self.videoViewLabel = QLabel(self.dockWidgetContents)
        self.videoViewLabel.setObjectName(u"videoViewLabel")

        self.gridLayout.addWidget(self.videoViewLabel, 6, 0, 1, 1)

        self.trialTableView = QTableView(self.dockWidgetContents)
        self.trialTableView.setObjectName(u"trialTableView")
        self.trialTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trialTableView.setProperty("showDropIndicator", False)
        self.trialTableView.setDragDropOverwriteMode(False)
        self.trialTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.trialTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.trialTableView.setTextElideMode(Qt.ElideNone)
        self.trialTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.trialTableView, 5, 0, 1, 3)

        self.sessionViewLabel = QLabel(self.dockWidgetContents)
        self.sessionViewLabel.setObjectName(u"sessionViewLabel")

        self.gridLayout.addWidget(self.sessionViewLabel, 2, 0, 1, 1)

        self.annotationsViewLabel = QLabel(self.dockWidgetContents)
        self.annotationsViewLabel.setObjectName(u"annotationsViewLabel")

        self.gridLayout.addWidget(self.annotationsViewLabel, 8, 0, 1, 1)

        self.trialViewLabel = QLabel(self.dockWidgetContents)
        self.trialViewLabel.setObjectName(u"trialViewLabel")

        self.gridLayout.addWidget(self.trialViewLabel, 4, 0, 1, 1)

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


        self.gridLayout.addLayout(self.loadCheckBoxesVerticalLayout, 13, 0, 1, 1)

        self.videoTableView = QTableView(self.dockWidgetContents)
        self.videoTableView.setObjectName(u"videoTableView")
        self.videoTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.videoTableView.setProperty("showDropIndicator", False)
        self.videoTableView.setDragDropOverwriteMode(False)
        self.videoTableView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.videoTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.videoTableView.setTextElideMode(Qt.ElideNone)
        self.videoTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.videoTableView, 7, 0, 1, 3)

        self.sessionTableView = QTableView(self.dockWidgetContents)
        self.sessionTableView.setObjectName(u"sessionTableView")
        self.sessionTableView.horizontalHeader().setDefaultSectionSize(60)
        self.sessionTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.sessionTableView, 3, 0, 1, 3)

        self.investigatorHorizontalLayout = QHBoxLayout()
        self.investigatorHorizontalLayout.setObjectName(u"investigatorHorizontalLayout")
        self.useInvestigatorCheckBox = QCheckBox(self.dockWidgetContents)
        self.useInvestigatorCheckBox.setObjectName(u"useInvestigatorCheckBox")
        self.useInvestigatorCheckBox.setChecked(True)

        self.investigatorHorizontalLayout.addWidget(self.useInvestigatorCheckBox)

        self.investigatorComboBox = QComboBox(self.dockWidgetContents)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")

        self.investigatorHorizontalLayout.addWidget(self.investigatorComboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.investigatorHorizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.investigatorHorizontalLayout, 0, 0, 1, 3)

        self.dateRangeHorizontalLayout = QHBoxLayout()
        self.dateRangeHorizontalLayout.setObjectName(u"dateRangeHorizontalLayout")
        self.useDateRangeCheckBox = QCheckBox(self.dockWidgetContents)
        self.useDateRangeCheckBox.setObjectName(u"useDateRangeCheckBox")

        self.dateRangeHorizontalLayout.addWidget(self.useDateRangeCheckBox)

        self.startDateEdit = QDateEdit(self.dockWidgetContents)
        self.startDateEdit.setObjectName(u"startDateEdit")

        self.dateRangeHorizontalLayout.addWidget(self.startDateEdit)

        self.dateRangeToLabel = QLabel(self.dockWidgetContents)
        self.dateRangeToLabel.setObjectName(u"dateRangeToLabel")

        self.dateRangeHorizontalLayout.addWidget(self.dateRangeToLabel)

        self.endDateEdit = QDateEdit(self.dockWidgetContents)
        self.endDateEdit.setObjectName(u"endDateEdit")

        self.dateRangeHorizontalLayout.addWidget(self.endDateEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.dateRangeHorizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.dateRangeHorizontalLayout, 1, 0, 1, 3)

        self.addOrEditTrialPushButton = QPushButton(self.dockWidgetContents)
        self.addOrEditTrialPushButton.setObjectName(u"addOrEditTrialPushButton")

        self.gridLayout.addWidget(self.addOrEditTrialPushButton, 4, 2, 1, 1)

        self.addOrEditSessionPushButton = QPushButton(self.dockWidgetContents)
        self.addOrEditSessionPushButton.setObjectName(u"addOrEditSessionPushButton")

        self.gridLayout.addWidget(self.addOrEditSessionPushButton, 2, 2, 1, 1)

        self.loadTrialPushButton = QPushButton(self.dockWidgetContents)
        self.loadTrialPushButton.setObjectName(u"loadTrialPushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadTrialPushButton.sizePolicy().hasHeightForWidth())
        self.loadTrialPushButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.loadTrialPushButton, 14, 2, 1, 1)

        TrialDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(TrialDockWidget)

        QMetaObject.connectSlotsByName(TrialDockWidget)
    # setupUi

    def retranslateUi(self, TrialDockWidget):
        TrialDockWidget.setWindowTitle(QCoreApplication.translate("TrialDockWidget", u"Trial Selection Window", None))
        self.videoViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Videos to Display", None))
        self.sessionViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Session:", None))
        self.annotationsViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Annotation to Display", None))
        self.trialViewLabel.setText(QCoreApplication.translate("TrialDockWidget", u"Select Trial to Load:", None))
        self.loadPoseCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Pose Data", None))
        self.loadNeuralCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Neural Data", None))
        self.loadAudioCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Load Audio Data", None))
        self.useInvestigatorCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Filter by Investigator:", None))
        self.useDateRangeCheckBox.setText(QCoreApplication.translate("TrialDockWidget", u"Filter by Trial Date Range from: ", None))
        self.startDateEdit.setDisplayFormat(QCoreApplication.translate("TrialDockWidget", u"yyyy-MM-dd", None))
        self.dateRangeToLabel.setText(QCoreApplication.translate("TrialDockWidget", u" to: ", None))
        self.endDateEdit.setDisplayFormat(QCoreApplication.translate("TrialDockWidget", u"yyyy-MM-dd", None))
        self.addOrEditTrialPushButton.setText(QCoreApplication.translate("TrialDockWidget", u"Add or Edit Trial...", None))
        self.addOrEditSessionPushButton.setText(QCoreApplication.translate("TrialDockWidget", u"Add or Edit Session...", None))
        self.loadTrialPushButton.setText(QCoreApplication.translate("TrialDockWidget", u"Load Trial", None))
    # retranslateUi

