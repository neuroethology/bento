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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BTAFrame.sizePolicy().hasHeightForWidth())
        BTAFrame.setSizePolicy(sizePolicy)
        BTAFrame.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(BTAFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.userOptionLayout = QVBoxLayout()
        self.userOptionLayout.setObjectName(u"userOptionLayout")
        self.userOptionLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.userOptionLayout.addItem(self.verticalSpacer_2)

        self.behaviorTriggerLabel = QLabel(BTAFrame)
        self.behaviorTriggerLabel.setObjectName(u"behaviorTriggerLabel")
        sizePolicy.setHeightForWidth(self.behaviorTriggerLabel.sizePolicy().hasHeightForWidth())
        self.behaviorTriggerLabel.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.behaviorTriggerLabel)

        self.behaviorComboBox = QComboBox(BTAFrame)
        self.behaviorComboBox.setObjectName(u"behaviorComboBox")
        sizePolicy.setHeightForWidth(self.behaviorComboBox.sizePolicy().hasHeightForWidth())
        self.behaviorComboBox.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.behaviorComboBox)

        self.channelLabel_1 = QLabel(BTAFrame)
        self.channelLabel_1.setObjectName(u"channelLabel_1")
        sizePolicy.setHeightForWidth(self.channelLabel_1.sizePolicy().hasHeightForWidth())
        self.channelLabel_1.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.channelLabel_1)

        self.channelComboBox = QComboBox(BTAFrame)
        self.channelComboBox.setObjectName(u"channelComboBox")
        sizePolicy.setHeightForWidth(self.channelComboBox.sizePolicy().hasHeightForWidth())
        self.channelComboBox.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.channelComboBox)

        self.alignAtStartButton = QRadioButton(BTAFrame)
        self.alignAtStartButton.setObjectName(u"alignAtStartButton")
        sizePolicy.setHeightForWidth(self.alignAtStartButton.sizePolicy().hasHeightForWidth())
        self.alignAtStartButton.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.alignAtStartButton)

        self.alignAtEndButton = QRadioButton(BTAFrame)
        self.alignAtEndButton.setObjectName(u"alignAtEndButton")
        sizePolicy.setHeightForWidth(self.alignAtEndButton.sizePolicy().hasHeightForWidth())
        self.alignAtEndButton.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.alignAtEndButton)

        self.windowBinLayout = QGridLayout()
        self.windowBinLayout.setObjectName(u"windowBinLayout")
        self.secBeforeLabel = QLabel(BTAFrame)
        self.secBeforeLabel.setObjectName(u"secBeforeLabel")
        sizePolicy.setHeightForWidth(self.secBeforeLabel.sizePolicy().hasHeightForWidth())
        self.secBeforeLabel.setSizePolicy(sizePolicy)

        self.windowBinLayout.addWidget(self.secBeforeLabel, 0, 2, 1, 1)

        self.secAfterLabel = QLabel(BTAFrame)
        self.secAfterLabel.setObjectName(u"secAfterLabel")
        sizePolicy.setHeightForWidth(self.secAfterLabel.sizePolicy().hasHeightForWidth())
        self.secAfterLabel.setSizePolicy(sizePolicy)

        self.windowBinLayout.addWidget(self.secAfterLabel, 1, 2, 1, 1)

        self.binSizeLabel = QLabel(BTAFrame)
        self.binSizeLabel.setObjectName(u"binSizeLabel")
        sizePolicy.setHeightForWidth(self.binSizeLabel.sizePolicy().hasHeightForWidth())
        self.binSizeLabel.setSizePolicy(sizePolicy)

        self.windowBinLayout.addWidget(self.binSizeLabel, 2, 0, 1, 1)

        self.windowLabel = QLabel(BTAFrame)
        self.windowLabel.setObjectName(u"windowLabel")
        sizePolicy.setHeightForWidth(self.windowLabel.sizePolicy().hasHeightForWidth())
        self.windowLabel.setSizePolicy(sizePolicy)

        self.windowBinLayout.addWidget(self.windowLabel, 0, 0, 1, 1)

        self.windowTextEdit_2 = QTextEdit(BTAFrame)
        self.windowTextEdit_2.setObjectName(u"windowTextEdit_2")
        sizePolicy.setHeightForWidth(self.windowTextEdit_2.sizePolicy().hasHeightForWidth())
        self.windowTextEdit_2.setSizePolicy(sizePolicy)
        self.windowTextEdit_2.setMaximumSize(QSize(60, 30))
        self.windowTextEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.windowBinLayout.addWidget(self.windowTextEdit_2, 1, 1, 1, 1)

        self.windowTextEdit_1 = QTextEdit(BTAFrame)
        self.windowTextEdit_1.setObjectName(u"windowTextEdit_1")
        sizePolicy.setHeightForWidth(self.windowTextEdit_1.sizePolicy().hasHeightForWidth())
        self.windowTextEdit_1.setSizePolicy(sizePolicy)
        self.windowTextEdit_1.setMaximumSize(QSize(60, 30))
        self.windowTextEdit_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.windowBinLayout.addWidget(self.windowTextEdit_1, 0, 1, 1, 1)

        self.secondsLabel = QLabel(BTAFrame)
        self.secondsLabel.setObjectName(u"secondsLabel")
        sizePolicy.setHeightForWidth(self.secondsLabel.sizePolicy().hasHeightForWidth())
        self.secondsLabel.setSizePolicy(sizePolicy)

        self.windowBinLayout.addWidget(self.secondsLabel, 2, 2, 1, 1)

        self.binSizeTextEdit = QTextEdit(BTAFrame)
        self.binSizeTextEdit.setObjectName(u"binSizeTextEdit")
        sizePolicy.setHeightForWidth(self.binSizeTextEdit.sizePolicy().hasHeightForWidth())
        self.binSizeTextEdit.setSizePolicy(sizePolicy)
        self.binSizeTextEdit.setMaximumSize(QSize(60, 30))
        self.binSizeTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.windowBinLayout.addWidget(self.binSizeTextEdit, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.windowBinLayout.addItem(self.horizontalSpacer, 1, 3, 1, 1)


        self.userOptionLayout.addLayout(self.windowBinLayout)

        self.boutsLayout = QGridLayout()
        self.boutsLayout.setObjectName(u"boutsLayout")
        self.discardTextEdit = QTextEdit(BTAFrame)
        self.discardTextEdit.setObjectName(u"discardTextEdit")
        sizePolicy.setHeightForWidth(self.discardTextEdit.sizePolicy().hasHeightForWidth())
        self.discardTextEdit.setSizePolicy(sizePolicy)
        self.discardTextEdit.setMaximumSize(QSize(60, 30))
        self.discardTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.boutsLayout.addWidget(self.discardTextEdit, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.boutsLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.discardBoutsLabel = QLabel(BTAFrame)
        self.discardBoutsLabel.setObjectName(u"discardBoutsLabel")
        sizePolicy.setHeightForWidth(self.discardBoutsLabel.sizePolicy().hasHeightForWidth())
        self.discardBoutsLabel.setSizePolicy(sizePolicy)

        self.boutsLayout.addWidget(self.discardBoutsLabel, 0, 0, 1, 1)

        self.secLongLabel = QLabel(BTAFrame)
        self.secLongLabel.setObjectName(u"secLongLabel")
        sizePolicy.setHeightForWidth(self.secLongLabel.sizePolicy().hasHeightForWidth())
        self.secLongLabel.setSizePolicy(sizePolicy)

        self.boutsLayout.addWidget(self.secLongLabel, 0, 2, 1, 1)

        self.mergeTextEdit = QTextEdit(BTAFrame)
        self.mergeTextEdit.setObjectName(u"mergeTextEdit")
        sizePolicy.setHeightForWidth(self.mergeTextEdit.sizePolicy().hasHeightForWidth())
        self.mergeTextEdit.setSizePolicy(sizePolicy)
        self.mergeTextEdit.setMaximumSize(QSize(60, 30))
        self.mergeTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.boutsLayout.addWidget(self.mergeTextEdit, 1, 1, 1, 1)

        self.secApartLabel = QLabel(BTAFrame)
        self.secApartLabel.setObjectName(u"secApartLabel")
        sizePolicy.setHeightForWidth(self.secApartLabel.sizePolicy().hasHeightForWidth())
        self.secApartLabel.setSizePolicy(sizePolicy)

        self.boutsLayout.addWidget(self.secApartLabel, 1, 2, 1, 1)

        self.mergeBoutsLabel = QLabel(BTAFrame)
        self.mergeBoutsLabel.setObjectName(u"mergeBoutsLabel")
        sizePolicy.setHeightForWidth(self.mergeBoutsLabel.sizePolicy().hasHeightForWidth())
        self.mergeBoutsLabel.setSizePolicy(sizePolicy)

        self.boutsLayout.addWidget(self.mergeBoutsLabel, 1, 0, 1, 1)


        self.userOptionLayout.addLayout(self.boutsLayout)

        self.analyzeLabel = QLabel(BTAFrame)
        self.analyzeLabel.setObjectName(u"analyzeLabel")
        sizePolicy.setHeightForWidth(self.analyzeLabel.sizePolicy().hasHeightForWidth())
        self.analyzeLabel.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.analyzeLabel)

        self.analyzeComboBox = QComboBox(BTAFrame)
        self.analyzeComboBox.setObjectName(u"analyzeComboBox")
        sizePolicy.setHeightForWidth(self.analyzeComboBox.sizePolicy().hasHeightForWidth())
        self.analyzeComboBox.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.analyzeComboBox)

        self.channelLabel_2 = QLabel(BTAFrame)
        self.channelLabel_2.setObjectName(u"channelLabel_2")
        sizePolicy.setHeightForWidth(self.channelLabel_2.sizePolicy().hasHeightForWidth())
        self.channelLabel_2.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.channelLabel_2)

        self.channelsList = QListWidget(BTAFrame)
        self.channelsList.setObjectName(u"channelsList")
        self.channelsList.setMaximumSize(QSize(16777215, 80))

        self.userOptionLayout.addWidget(self.channelsList)

        self.zscoreLayout = QHBoxLayout()
        self.zscoreLayout.setObjectName(u"zscoreLayout")
        self.zscoreLabel = QLabel(BTAFrame)
        self.zscoreLabel.setObjectName(u"zscoreLabel")
        sizePolicy.setHeightForWidth(self.zscoreLabel.sizePolicy().hasHeightForWidth())
        self.zscoreLabel.setSizePolicy(sizePolicy)

        self.zscoreLayout.addWidget(self.zscoreLabel)

        self.zscoreCheckBox = QCheckBox(BTAFrame)
        self.zscoreCheckBox.setObjectName(u"zscoreCheckBox")
        sizePolicy.setHeightForWidth(self.zscoreCheckBox.sizePolicy().hasHeightForWidth())
        self.zscoreCheckBox.setSizePolicy(sizePolicy)
        self.zscoreCheckBox.setStyleSheet(u"")

        self.zscoreLayout.addWidget(self.zscoreCheckBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.zscoreLayout.addItem(self.horizontalSpacer_3)


        self.userOptionLayout.addLayout(self.zscoreLayout)

        self.behaviorShowLabel = QLabel(BTAFrame)
        self.behaviorShowLabel.setObjectName(u"behaviorShowLabel")
        sizePolicy.setHeightForWidth(self.behaviorShowLabel.sizePolicy().hasHeightForWidth())
        self.behaviorShowLabel.setSizePolicy(sizePolicy)

        self.userOptionLayout.addWidget(self.behaviorShowLabel)

        self.behaviorSelectLayout = QGridLayout()
        self.behaviorSelectLayout.setObjectName(u"behaviorSelectLayout")

        self.userOptionLayout.addLayout(self.behaviorSelectLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.saveToFileButton = QPushButton(BTAFrame)
        self.saveToFileButton.setObjectName(u"saveToFileButton")
        sizePolicy.setHeightForWidth(self.saveToFileButton.sizePolicy().hasHeightForWidth())
        self.saveToFileButton.setSizePolicy(sizePolicy)

        self.buttonsLayout.addWidget(self.saveToFileButton)

        self.saveFigureButton = QPushButton(BTAFrame)
        self.saveFigureButton.setObjectName(u"saveFigureButton")
        sizePolicy.setHeightForWidth(self.saveFigureButton.sizePolicy().hasHeightForWidth())
        self.saveFigureButton.setSizePolicy(sizePolicy)

        self.buttonsLayout.addWidget(self.saveFigureButton)


        self.userOptionLayout.addLayout(self.buttonsLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.userOptionLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.userOptionLayout)

        self.plotLayout = QVBoxLayout()
        self.plotLayout.setObjectName(u"plotLayout")
        self.plotLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.plotLayout.setContentsMargins(50, -1, -1, -1)

        self.horizontalLayout.addLayout(self.plotLayout)

        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(BTAFrame)

        QMetaObject.connectSlotsByName(BTAFrame)
    # setupUi

    def retranslateUi(self, BTAFrame):
        BTAFrame.setWindowTitle(QCoreApplication.translate("BTAFrame", u"Behavior Triggered Average", None))
        self.behaviorTriggerLabel.setText(QCoreApplication.translate("BTAFrame", u"Behavior trigger :", None))
        self.channelLabel_1.setText(QCoreApplication.translate("BTAFrame", u"in channel :", None))
        self.alignAtStartButton.setText(QCoreApplication.translate("BTAFrame", u"Align at start", None))
        self.alignAtEndButton.setText(QCoreApplication.translate("BTAFrame", u"Align at end", None))
        self.secBeforeLabel.setText(QCoreApplication.translate("BTAFrame", u"sec before", None))
        self.secAfterLabel.setText(QCoreApplication.translate("BTAFrame", u"sec after", None))
        self.binSizeLabel.setText(QCoreApplication.translate("BTAFrame", u"Bin size :", None))
        self.windowLabel.setText(QCoreApplication.translate("BTAFrame", u"Window : ", None))
        self.secondsLabel.setText(QCoreApplication.translate("BTAFrame", u"seconds", None))
        self.discardBoutsLabel.setText(QCoreApplication.translate("BTAFrame", u"Discards bouts under", None))
        self.secLongLabel.setText(QCoreApplication.translate("BTAFrame", u"sec long", None))
        self.secApartLabel.setText(QCoreApplication.translate("BTAFrame", u"sec apart", None))
        self.mergeBoutsLabel.setText(QCoreApplication.translate("BTAFrame", u"Merge bouts under", None))
        self.analyzeLabel.setText(QCoreApplication.translate("BTAFrame", u"Element to analyze :", None))
        self.channelLabel_2.setText(QCoreApplication.translate("BTAFrame", u"in channels(s) :", None))
        self.zscoreLabel.setText(QCoreApplication.translate("BTAFrame", u"Z-score traces : ", None))
        self.zscoreCheckBox.setText("")
        self.behaviorShowLabel.setText(QCoreApplication.translate("BTAFrame", u"Behaviors to show :", None))
        self.saveToFileButton.setText(QCoreApplication.translate("BTAFrame", u"Save BTA to h5 file", None))
        self.saveFigureButton.setText(QCoreApplication.translate("BTAFrame", u"Save Figure", None))
    # retranslateUi

