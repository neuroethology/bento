# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sessionWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SessionDockWidget(object):
    def setupUi(self, SessionDockWidget):
        if not SessionDockWidget.objectName():
            SessionDockWidget.setObjectName(u"SessionDockWidget")
        SessionDockWidget.resize(787, 678)
        self.experimentDockWidgetContents = QWidget()
        self.experimentDockWidgetContents.setObjectName(u"experimentDockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.experimentDockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.investigatorHorizontalLayout = QHBoxLayout()
        self.investigatorHorizontalLayout.setObjectName(u"investigatorHorizontalLayout")
        self.useInvestigatorCheckBox = QCheckBox(self.experimentDockWidgetContents)
        self.useInvestigatorCheckBox.setObjectName(u"useInvestigatorCheckBox")
        self.useInvestigatorCheckBox.setChecked(True)

        self.investigatorHorizontalLayout.addWidget(self.useInvestigatorCheckBox)

        self.investigatorComboBox = QComboBox(self.experimentDockWidgetContents)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")

        self.investigatorHorizontalLayout.addWidget(self.investigatorComboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.investigatorHorizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.investigatorHorizontalLayout)

        self.dateRangeHorizontalLayout = QHBoxLayout()
        self.dateRangeHorizontalLayout.setObjectName(u"dateRangeHorizontalLayout")
        self.useDateRangeCheckBox = QCheckBox(self.experimentDockWidgetContents)
        self.useDateRangeCheckBox.setObjectName(u"useDateRangeCheckBox")

        self.dateRangeHorizontalLayout.addWidget(self.useDateRangeCheckBox)

        self.startDateEdit = QDateEdit(self.experimentDockWidgetContents)
        self.startDateEdit.setObjectName(u"startDateEdit")

        self.dateRangeHorizontalLayout.addWidget(self.startDateEdit)

        self.dateRangeToLabel = QLabel(self.experimentDockWidgetContents)
        self.dateRangeToLabel.setObjectName(u"dateRangeToLabel")

        self.dateRangeHorizontalLayout.addWidget(self.dateRangeToLabel)

        self.endDateEdit = QDateEdit(self.experimentDockWidgetContents)
        self.endDateEdit.setObjectName(u"endDateEdit")

        self.dateRangeHorizontalLayout.addWidget(self.endDateEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.dateRangeHorizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.dateRangeHorizontalLayout)

        self.sessionsTableView = QTableView(self.experimentDockWidgetContents)
        self.sessionsTableView.setObjectName(u"sessionsTableView")
        self.sessionsTableView.horizontalHeader().setDefaultSectionSize(60)
        self.sessionsTableView.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.sessionsTableView)

        self.pushButtonsHorizontalLayout = QHBoxLayout()
        self.pushButtonsHorizontalLayout.setObjectName(u"pushButtonsHorizontalLayout")
        self.addOrEditSessionPushButton = QPushButton(self.experimentDockWidgetContents)
        self.addOrEditSessionPushButton.setObjectName(u"addOrEditSessionPushButton")

        self.pushButtonsHorizontalLayout.addWidget(self.addOrEditSessionPushButton)

        self.loadPushButton = QPushButton(self.experimentDockWidgetContents)
        self.loadPushButton.setObjectName(u"loadPushButton")

        self.pushButtonsHorizontalLayout.addWidget(self.loadPushButton)


        self.verticalLayout.addLayout(self.pushButtonsHorizontalLayout)

        SessionDockWidget.setWidget(self.experimentDockWidgetContents)

        self.retranslateUi(SessionDockWidget)

        QMetaObject.connectSlotsByName(SessionDockWidget)
    # setupUi

    def retranslateUi(self, SessionDockWidget):
        SessionDockWidget.setWindowTitle(QCoreApplication.translate("SessionDockWidget", u"Session Search Window", None))
        self.useInvestigatorCheckBox.setText(QCoreApplication.translate("SessionDockWidget", u"Filter by Investigator:", None))
        self.useDateRangeCheckBox.setText(QCoreApplication.translate("SessionDockWidget", u"Filter by Trial Date Range from: ", None))
        self.startDateEdit.setDisplayFormat(QCoreApplication.translate("SessionDockWidget", u"yyyy-MM-dd", None))
        self.dateRangeToLabel.setText(QCoreApplication.translate("SessionDockWidget", u" to: ", None))
        self.endDateEdit.setDisplayFormat(QCoreApplication.translate("SessionDockWidget", u"yyyy-MM-dd", None))
        self.addOrEditSessionPushButton.setText(QCoreApplication.translate("SessionDockWidget", u"Add or Edit Session...", None))
        self.loadPushButton.setText(QCoreApplication.translate("SessionDockWidget", u"Load Session", None))
    # retranslateUi

