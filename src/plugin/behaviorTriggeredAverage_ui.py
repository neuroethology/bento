# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'behaviorTriggeredAverage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_BTAFrame(object):
    def setupUi(self, BTAFrame):
        if not BTAFrame.objectName():
            BTAFrame.setObjectName(u"BTAFrame")
        BTAFrame.resize(945, 860)
        self.horizontalLayout = QHBoxLayout(BTAFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.userOptionsScrollArea = QScrollArea(BTAFrame)
        self.userOptionsScrollArea.setObjectName(u"userOptionsScrollArea")
        self.userOptionsScrollArea.setWidgetResizable(True)
        self.userOptionScrollAreaWidget = QWidget()
        self.userOptionScrollAreaWidget.setObjectName(u"userOptionScrollAreaWidget")
        self.userOptionScrollAreaWidget.setGeometry(QRect(0, 0, 302, 834))
        self.scrollAreaLayout = QVBoxLayout(self.userOptionScrollAreaWidget)
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scrollAreaLayout.addItem(self.verticalSpacer_2)

        self.saveButton = QToolButton(self.userOptionScrollAreaWidget)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(14)
        font.setBold(False)
        self.saveButton.setFont(font)
        self.saveButton.setIconSize(QSize(16, 16))
        self.saveButton.setPopupMode(QToolButton.InstantPopup)
        self.saveButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.saveButton.setArrowType(Qt.DownArrow)

        self.scrollAreaLayout.addWidget(self.saveButton)

        self.behaviorLabel = QLabel(self.userOptionScrollAreaWidget)
        self.behaviorLabel.setObjectName(u"behaviorLabel")

        self.scrollAreaLayout.addWidget(self.behaviorLabel)

        self.behaviorComboBox = QComboBox(self.userOptionScrollAreaWidget)
        self.behaviorComboBox.setObjectName(u"behaviorComboBox")

        self.scrollAreaLayout.addWidget(self.behaviorComboBox)

        self.channelLabel = QLabel(self.userOptionScrollAreaWidget)
        self.channelLabel.setObjectName(u"channelLabel")
        self.channelLabel.setMaximumSize(QSize(16777215, 80))

        self.scrollAreaLayout.addWidget(self.channelLabel)

        self.channelComboBox = QComboBox(self.userOptionScrollAreaWidget)
        self.channelComboBox.setObjectName(u"channelComboBox")

        self.scrollAreaLayout.addWidget(self.channelComboBox)

        self.alignAtStartButton = QRadioButton(self.userOptionScrollAreaWidget)
        self.alignAtStartButton.setObjectName(u"alignAtStartButton")
        self.alignAtStartButton.setChecked(True)

        self.scrollAreaLayout.addWidget(self.alignAtStartButton)

        self.alignAtEndButton = QRadioButton(self.userOptionScrollAreaWidget)
        self.alignAtEndButton.setObjectName(u"alignAtEndButton")

        self.scrollAreaLayout.addWidget(self.alignAtEndButton)

        self.windowBinLayout = QGridLayout()
        self.windowBinLayout.setObjectName(u"windowBinLayout")
        self.windowLabel = QLabel(self.userOptionScrollAreaWidget)
        self.windowLabel.setObjectName(u"windowLabel")

        self.windowBinLayout.addWidget(self.windowLabel, 0, 0, 1, 1)

        self.secAfterLabel = QLabel(self.userOptionScrollAreaWidget)
        self.secAfterLabel.setObjectName(u"secAfterLabel")
        self.secAfterLabel.setMinimumSize(QSize(60, 30))

        self.windowBinLayout.addWidget(self.secAfterLabel, 1, 2, 1, 1)

        self.binSizeLabel = QLabel(self.userOptionScrollAreaWidget)
        self.binSizeLabel.setObjectName(u"binSizeLabel")

        self.windowBinLayout.addWidget(self.binSizeLabel, 2, 0, 1, 1)

        self.secBeforeLabel = QLabel(self.userOptionScrollAreaWidget)
        self.secBeforeLabel.setObjectName(u"secBeforeLabel")

        self.windowBinLayout.addWidget(self.secBeforeLabel, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.windowBinLayout.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.binSizeBox = QDoubleSpinBox(self.userOptionScrollAreaWidget)
        self.binSizeBox.setObjectName(u"binSizeBox")
        self.binSizeBox.setMinimumSize(QSize(60, 30))
        self.binSizeBox.setDecimals(4)
        self.binSizeBox.setMinimum(0.000100000000000)
        self.binSizeBox.setSingleStep(0.000100000000000)
        self.binSizeBox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.binSizeBox.setValue(0.033300000000000)

        self.windowBinLayout.addWidget(self.binSizeBox, 2, 1, 1, 1)

        self.windowBox_2 = QDoubleSpinBox(self.userOptionScrollAreaWidget)
        self.windowBox_2.setObjectName(u"windowBox_2")
        self.windowBox_2.setMinimumSize(QSize(60, 30))
        self.windowBox_2.setSingleStep(0.010000000000000)
        self.windowBox_2.setStepType(QAbstractSpinBox.DefaultStepType)
        self.windowBox_2.setValue(10.000000000000000)

        self.windowBinLayout.addWidget(self.windowBox_2, 1, 1, 1, 1)

        self.windowBox_1 = QDoubleSpinBox(self.userOptionScrollAreaWidget)
        self.windowBox_1.setObjectName(u"windowBox_1")
        self.windowBox_1.setMinimumSize(QSize(60, 30))
        self.windowBox_1.setDecimals(2)
        self.windowBox_1.setSingleStep(0.010000000000000)
        self.windowBox_1.setStepType(QAbstractSpinBox.DefaultStepType)
        self.windowBox_1.setValue(10.000000000000000)

        self.windowBinLayout.addWidget(self.windowBox_1, 0, 1, 1, 1)


        self.scrollAreaLayout.addLayout(self.windowBinLayout)

        self.boutsLayout = QGridLayout()
        self.boutsLayout.setObjectName(u"boutsLayout")
        self.secApartLabel = QLabel(self.userOptionScrollAreaWidget)
        self.secApartLabel.setObjectName(u"secApartLabel")

        self.boutsLayout.addWidget(self.secApartLabel, 1, 2, 1, 1)

        self.secLongLabel = QLabel(self.userOptionScrollAreaWidget)
        self.secLongLabel.setObjectName(u"secLongLabel")

        self.boutsLayout.addWidget(self.secLongLabel, 0, 2, 1, 1)

        self.discardBoutsLabel = QLabel(self.userOptionScrollAreaWidget)
        self.discardBoutsLabel.setObjectName(u"discardBoutsLabel")

        self.boutsLayout.addWidget(self.discardBoutsLabel, 0, 0, 1, 1)

        self.mergeBoutsLabel = QLabel(self.userOptionScrollAreaWidget)
        self.mergeBoutsLabel.setObjectName(u"mergeBoutsLabel")
        self.mergeBoutsLabel.setMinimumSize(QSize(0, 0))

        self.boutsLayout.addWidget(self.mergeBoutsLabel, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.boutsLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.discardBoutsBox = QDoubleSpinBox(self.userOptionScrollAreaWidget)
        self.discardBoutsBox.setObjectName(u"discardBoutsBox")
        self.discardBoutsBox.setMinimumSize(QSize(60, 30))
        self.discardBoutsBox.setSingleStep(0.010000000000000)
        self.discardBoutsBox.setStepType(QAbstractSpinBox.DefaultStepType)

        self.boutsLayout.addWidget(self.discardBoutsBox, 0, 1, 1, 1)

        self.mergeBoutsBox = QDoubleSpinBox(self.userOptionScrollAreaWidget)
        self.mergeBoutsBox.setObjectName(u"mergeBoutsBox")
        self.mergeBoutsBox.setMinimumSize(QSize(60, 30))
        self.mergeBoutsBox.setSingleStep(0.010000000000000)
        self.mergeBoutsBox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.mergeBoutsBox.setValue(2.000000000000000)

        self.boutsLayout.addWidget(self.mergeBoutsBox, 1, 1, 1, 1)


        self.scrollAreaLayout.addLayout(self.boutsLayout)

        self.analyzeLabel = QLabel(self.userOptionScrollAreaWidget)
        self.analyzeLabel.setObjectName(u"analyzeLabel")

        self.scrollAreaLayout.addWidget(self.analyzeLabel)

        self.analyzeComboBox = QComboBox(self.userOptionScrollAreaWidget)
        self.analyzeComboBox.setObjectName(u"analyzeComboBox")

        self.scrollAreaLayout.addWidget(self.analyzeComboBox)

        self.channelLabel_2 = QLabel(self.userOptionScrollAreaWidget)
        self.channelLabel_2.setObjectName(u"channelLabel_2")

        self.scrollAreaLayout.addWidget(self.channelLabel_2)

        self.channelsList = QListView(self.userOptionScrollAreaWidget)
        self.channelsList.setObjectName(u"channelsList")
        self.channelsList.setMaximumSize(QSize(16777215, 80))

        self.scrollAreaLayout.addWidget(self.channelsList)

        self.zscoreLayout = QHBoxLayout()
        self.zscoreLayout.setObjectName(u"zscoreLayout")
        self.zscoreLabel = QLabel(self.userOptionScrollAreaWidget)
        self.zscoreLabel.setObjectName(u"zscoreLabel")

        self.zscoreLayout.addWidget(self.zscoreLabel)

        self.zscoreCheckBox = QCheckBox(self.userOptionScrollAreaWidget)
        self.zscoreCheckBox.setObjectName(u"zscoreCheckBox")

        self.zscoreLayout.addWidget(self.zscoreCheckBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.zscoreLayout.addItem(self.horizontalSpacer_3)


        self.scrollAreaLayout.addLayout(self.zscoreLayout)

        self.behaviorSelectionLabel = QLabel(self.userOptionScrollAreaWidget)
        self.behaviorSelectionLabel.setObjectName(u"behaviorSelectionLabel")

        self.scrollAreaLayout.addWidget(self.behaviorSelectionLabel)

        self.behaviorSelectLayout = QGridLayout()
        self.behaviorSelectLayout.setObjectName(u"behaviorSelectLayout")

        self.scrollAreaLayout.addLayout(self.behaviorSelectLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scrollAreaLayout.addItem(self.verticalSpacer)

        self.userOptionsScrollArea.setWidget(self.userOptionScrollAreaWidget)

        self.horizontalLayout.addWidget(self.userOptionsScrollArea)

        self.plotScrollArea = QScrollArea(BTAFrame)
        self.plotScrollArea.setObjectName(u"plotScrollArea")
        self.plotScrollArea.setWidgetResizable(True)
        self.plotScrollAreaWidget = QWidget()
        self.plotScrollAreaWidget.setObjectName(u"plotScrollAreaWidget")
        self.plotScrollAreaWidget.setGeometry(QRect(0, 0, 605, 834))
        self.plotScrollAreaLayout = QHBoxLayout(self.plotScrollAreaWidget)
        self.plotScrollAreaLayout.setObjectName(u"plotScrollAreaLayout")
        self.plotLayout = QVBoxLayout()
        self.plotLayout.setObjectName(u"plotLayout")

        self.plotScrollAreaLayout.addLayout(self.plotLayout)

        self.plotScrollArea.setWidget(self.plotScrollAreaWidget)

        self.horizontalLayout.addWidget(self.plotScrollArea)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(BTAFrame)

        QMetaObject.connectSlotsByName(BTAFrame)
    # setupUi

    def retranslateUi(self, BTAFrame):
        BTAFrame.setWindowTitle(QCoreApplication.translate("BTAFrame", u"Behavior Triggered Average", None))
        self.saveButton.setText(QCoreApplication.translate("BTAFrame", u"Save", None))
        self.behaviorLabel.setText(QCoreApplication.translate("BTAFrame", u"Behavior trigger :", None))
        self.channelLabel.setText(QCoreApplication.translate("BTAFrame", u"in channel :", None))
        self.alignAtStartButton.setText(QCoreApplication.translate("BTAFrame", u"Align at start", None))
        self.alignAtEndButton.setText(QCoreApplication.translate("BTAFrame", u"Align at end", None))
        self.windowLabel.setText(QCoreApplication.translate("BTAFrame", u"Window :", None))
        self.secAfterLabel.setText(QCoreApplication.translate("BTAFrame", u"sec after", None))
        self.binSizeLabel.setText(QCoreApplication.translate("BTAFrame", u"Bin size :", None))
        self.secBeforeLabel.setText(QCoreApplication.translate("BTAFrame", u"sec before", None))
        self.secApartLabel.setText(QCoreApplication.translate("BTAFrame", u"sec apart", None))
        self.secLongLabel.setText(QCoreApplication.translate("BTAFrame", u"sec long", None))
        self.discardBoutsLabel.setText(QCoreApplication.translate("BTAFrame", u"Discard bouts under", None))
        self.mergeBoutsLabel.setText(QCoreApplication.translate("BTAFrame", u"Merge bouts under", None))
        self.analyzeLabel.setText(QCoreApplication.translate("BTAFrame", u"Element to analyze :", None))
        self.channelLabel_2.setText(QCoreApplication.translate("BTAFrame", u"in channel(s) :", None))
        self.zscoreLabel.setText(QCoreApplication.translate("BTAFrame", u"z-score traces :", None))
        self.zscoreCheckBox.setText("")
        self.behaviorSelectionLabel.setText(QCoreApplication.translate("BTAFrame", u"Behaviors to show :", None))
    # retranslateUi

