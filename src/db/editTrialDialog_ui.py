# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editTrialDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_EditTrialDialog(object):
    def setupUi(self, EditTrialDialog):
        if not EditTrialDialog.objectName():
            EditTrialDialog.setObjectName(u"EditTrialDialog")
        EditTrialDialog.resize(774, 728)
        self.verticalLayout = QVBoxLayout(EditTrialDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.generalInfoHorizontalLayout = QHBoxLayout()
        self.generalInfoHorizontalLayout.setObjectName(u"generalInfoHorizontalLayout")
        self.trialNumLabel = QLabel(EditTrialDialog)
        self.trialNumLabel.setObjectName(u"trialNumLabel")
        self.trialNumLabel.setMinimumSize(QSize(103, 0))

        self.generalInfoHorizontalLayout.addWidget(self.trialNumLabel)

        self.trialNumLineEdit = QLineEdit(EditTrialDialog)
        self.trialNumLineEdit.setObjectName(u"trialNumLineEdit")

        self.generalInfoHorizontalLayout.addWidget(self.trialNumLineEdit)

        self.stimulusLabel = QLabel(EditTrialDialog)
        self.stimulusLabel.setObjectName(u"stimulusLabel")

        self.generalInfoHorizontalLayout.addWidget(self.stimulusLabel)

        self.stimulusLineEdit = QLineEdit(EditTrialDialog)
        self.stimulusLineEdit.setObjectName(u"stimulusLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stimulusLineEdit.sizePolicy().hasHeightForWidth())
        self.stimulusLineEdit.setSizePolicy(sizePolicy)

        self.generalInfoHorizontalLayout.addWidget(self.stimulusLineEdit)


        self.verticalLayout.addLayout(self.generalInfoHorizontalLayout)

        self.videosHorizontalLayout = QHBoxLayout()
        self.videosHorizontalLayout.setObjectName(u"videosHorizontalLayout")
        self.videosLabel = QLabel(EditTrialDialog)
        self.videosLabel.setObjectName(u"videosLabel")
        self.videosLabel.setMinimumSize(QSize(103, 0))
        self.videosLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.videosHorizontalLayout.addWidget(self.videosLabel)

        self.videosFileTableView = QTableView(EditTrialDialog)
        self.videosFileTableView.setObjectName(u"videosFileTableView")

        self.videosHorizontalLayout.addWidget(self.videosFileTableView)

        self.videosSearchVerticalLayout = QVBoxLayout()
        self.videosSearchVerticalLayout.setObjectName(u"videosSearchVerticalLayout")
        self.videosSearchPushButton = QPushButton(EditTrialDialog)
        self.videosSearchPushButton.setObjectName(u"videosSearchPushButton")

        self.videosSearchVerticalLayout.addWidget(self.videosSearchPushButton)

        self.videosSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.videosSearchVerticalLayout.addItem(self.videosSearchVerticalSpacer)


        self.videosHorizontalLayout.addLayout(self.videosSearchVerticalLayout)


        self.verticalLayout.addLayout(self.videosHorizontalLayout)

        self.annotationsHorizontalLayout = QHBoxLayout()
        self.annotationsHorizontalLayout.setObjectName(u"annotationsHorizontalLayout")
        self.annotationsLabel = QLabel(EditTrialDialog)
        self.annotationsLabel.setObjectName(u"annotationsLabel")
        self.annotationsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.annotationsHorizontalLayout.addWidget(self.annotationsLabel)

        self.annotationsTableView = QTableView(EditTrialDialog)
        self.annotationsTableView.setObjectName(u"annotationsTableView")

        self.annotationsHorizontalLayout.addWidget(self.annotationsTableView)

        self.annotationsSearchVerticalLayout = QVBoxLayout()
        self.annotationsSearchVerticalLayout.setObjectName(u"annotationsSearchVerticalLayout")
        self.annotationsSearchPushButton = QPushButton(EditTrialDialog)
        self.annotationsSearchPushButton.setObjectName(u"annotationsSearchPushButton")

        self.annotationsSearchVerticalLayout.addWidget(self.annotationsSearchPushButton)

        self.annotationsSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.annotationsSearchVerticalLayout.addItem(self.annotationsSearchVerticalSpacer)


        self.annotationsHorizontalLayout.addLayout(self.annotationsSearchVerticalLayout)


        self.verticalLayout.addLayout(self.annotationsHorizontalLayout)

        self.posesHorizontalLayout = QHBoxLayout()
        self.posesHorizontalLayout.setObjectName(u"posesHorizontalLayout")
        self.posesLabel = QLabel(EditTrialDialog)
        self.posesLabel.setObjectName(u"posesLabel")
        self.posesLabel.setMinimumSize(QSize(103, 0))
        self.posesLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.posesHorizontalLayout.addWidget(self.posesLabel)

        self.posesTableView = QTableView(EditTrialDialog)
        self.posesTableView.setObjectName(u"posesTableView")

        self.posesHorizontalLayout.addWidget(self.posesTableView)

        self.posesSearchVerticalLayout = QVBoxLayout()
        self.posesSearchVerticalLayout.setObjectName(u"posesSearchVerticalLayout")
        self.posesSearchPushButton = QPushButton(EditTrialDialog)
        self.posesSearchPushButton.setObjectName(u"posesSearchPushButton")

        self.posesSearchVerticalLayout.addWidget(self.posesSearchPushButton)

        self.posesSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.posesSearchVerticalLayout.addItem(self.posesSearchVerticalSpacer)


        self.posesHorizontalLayout.addLayout(self.posesSearchVerticalLayout)


        self.verticalLayout.addLayout(self.posesHorizontalLayout)

        self.neuralsHorizontalLayout = QHBoxLayout()
        self.neuralsHorizontalLayout.setObjectName(u"neuralsHorizontalLayout")
        self.neuralsLabel = QLabel(EditTrialDialog)
        self.neuralsLabel.setObjectName(u"neuralsLabel")
        self.neuralsLabel.setMinimumSize(QSize(103, 0))
        self.neuralsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.neuralsHorizontalLayout.addWidget(self.neuralsLabel)

        self.neuralsTableView = QTableView(EditTrialDialog)
        self.neuralsTableView.setObjectName(u"neuralsTableView")

        self.neuralsHorizontalLayout.addWidget(self.neuralsTableView)

        self.neuralsSearchVerticalLayout = QVBoxLayout()
        self.neuralsSearchVerticalLayout.setObjectName(u"neuralsSearchVerticalLayout")
        self.neuralsSearchPushButton = QPushButton(EditTrialDialog)
        self.neuralsSearchPushButton.setObjectName(u"neuralsSearchPushButton")

        self.neuralsSearchVerticalLayout.addWidget(self.neuralsSearchPushButton)

        self.neuralsSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.neuralsSearchVerticalLayout.addItem(self.neuralsSearchVerticalSpacer)


        self.neuralsHorizontalLayout.addLayout(self.neuralsSearchVerticalLayout)


        self.verticalLayout.addLayout(self.neuralsHorizontalLayout)

        self.audiosHorizontalLayout = QHBoxLayout()
        self.audiosHorizontalLayout.setObjectName(u"audiosHorizontalLayout")
        self.audiosLabel = QLabel(EditTrialDialog)
        self.audiosLabel.setObjectName(u"audiosLabel")
        self.audiosLabel.setMinimumSize(QSize(103, 0))
        self.audiosLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.audiosHorizontalLayout.addWidget(self.audiosLabel)

        self.audiosTreeView = QTreeView(EditTrialDialog)
        self.audiosTreeView.setObjectName(u"audiosTreeView")

        self.audiosHorizontalLayout.addWidget(self.audiosTreeView)

        self.audiosSearchVerticalLayout = QVBoxLayout()
        self.audiosSearchVerticalLayout.setObjectName(u"audiosSearchVerticalLayout")
        self.audiosSearchPushButton = QPushButton(EditTrialDialog)
        self.audiosSearchPushButton.setObjectName(u"audiosSearchPushButton")

        self.audiosSearchVerticalLayout.addWidget(self.audiosSearchPushButton)

        self.audiosSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.audiosSearchVerticalLayout.addItem(self.audiosSearchVerticalSpacer)


        self.audiosHorizontalLayout.addLayout(self.audiosSearchVerticalLayout)


        self.verticalLayout.addLayout(self.audiosHorizontalLayout)

        self.othersHorizontalLayout = QHBoxLayout()
        self.othersHorizontalLayout.setObjectName(u"othersHorizontalLayout")
        self.othersLabel = QLabel(EditTrialDialog)
        self.othersLabel.setObjectName(u"othersLabel")
        self.othersLabel.setMinimumSize(QSize(103, 0))
        self.othersLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.othersHorizontalLayout.addWidget(self.othersLabel)

        self.othersTableView = QTableView(EditTrialDialog)
        self.othersTableView.setObjectName(u"othersTableView")

        self.othersHorizontalLayout.addWidget(self.othersTableView)

        self.othersSearchVerticalLayout = QVBoxLayout()
        self.othersSearchVerticalLayout.setObjectName(u"othersSearchVerticalLayout")
        self.othersSearchPushButton = QPushButton(EditTrialDialog)
        self.othersSearchPushButton.setObjectName(u"othersSearchPushButton")

        self.othersSearchVerticalLayout.addWidget(self.othersSearchPushButton)

        self.othersSearchVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.othersSearchVerticalLayout.addItem(self.othersSearchVerticalSpacer)


        self.othersHorizontalLayout.addLayout(self.othersSearchVerticalLayout)


        self.verticalLayout.addLayout(self.othersHorizontalLayout)

        self.buttonBox = QDialogButtonBox(EditTrialDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EditTrialDialog)
        self.buttonBox.accepted.connect(EditTrialDialog.accept)
        self.buttonBox.rejected.connect(EditTrialDialog.reject)

        QMetaObject.connectSlotsByName(EditTrialDialog)
    # setupUi

    def retranslateUi(self, EditTrialDialog):
        EditTrialDialog.setWindowTitle(QCoreApplication.translate("EditTrialDialog", u"Add or Edit Trial", None))
        self.trialNumLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Trial Num: ", None))
        self.stimulusLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Stimulus: ", None))
        self.videosLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Video Files: ", None))
        self.videosSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
        self.annotationsLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Annotation Files: ", None))
        self.annotationsSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
        self.posesLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Pose Files: ", None))
        self.posesSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
        self.neuralsLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Neural Files: ", None))
        self.neuralsSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
        self.audiosLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Audio Files: ", None))
        self.audiosSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
        self.othersLabel.setText(QCoreApplication.translate("EditTrialDialog", u"Other Files: ", None))
        self.othersSearchPushButton.setText(QCoreApplication.translate("EditTrialDialog", u"Search...", None))
    # retranslateUi

