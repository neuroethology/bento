# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sessionWindow.ui'
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


class Ui_SessionDockWidget(object):
    def setupUi(self, SessionDockWidget):
        if SessionDockWidget.objectName():
            SessionDockWidget.setObjectName(u"SessionDockWidget")
        SessionDockWidget.resize(1055, 678)
        self.experimentDockWidgetContents = QWidget()
        self.experimentDockWidgetContents.setObjectName(u"experimentDockWidgetContents")
        self.gridLayout = QGridLayout(self.experimentDockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sessionsTableView = QTableView(self.experimentDockWidgetContents)
        self.sessionsTableView.setObjectName(u"sessionsTableView")
        self.sessionsTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.sessionsTableView, 4, 0, 1, 4)

        self.pushButtonsHorizontalLayout = QHBoxLayout()
        self.pushButtonsHorizontalLayout.setObjectName(u"pushButtonsHorizontalLayout")
        self.searchPushButton = QPushButton(self.experimentDockWidgetContents)
        self.searchPushButton.setObjectName(u"searchPushButton")

        self.pushButtonsHorizontalLayout.addWidget(self.searchPushButton)

        self.loadPushButton = QPushButton(self.experimentDockWidgetContents)
        self.loadPushButton.setObjectName(u"loadPushButton")

        self.pushButtonsHorizontalLayout.addWidget(self.loadPushButton)


        self.gridLayout.addLayout(self.pushButtonsHorizontalLayout, 5, 3, 1, 1)

        self.dateRangeGridLayout = QGridLayout()
        self.dateRangeGridLayout.setObjectName(u"dateRangeGridLayout")
        self.endCalendarWidget = QCalendarWidget(self.experimentDockWidgetContents)
        self.endCalendarWidget.setObjectName(u"endCalendarWidget")
        self.endCalendarWidget.setMinimumSize(QSize(379, 173))

        self.dateRangeGridLayout.addWidget(self.endCalendarWidget, 2, 0, 1, 1)

        self.trialDateStartLabel = QLabel(self.experimentDockWidgetContents)
        self.trialDateStartLabel.setObjectName(u"trialDateStartLabel")
        self.trialDateStartLabel.setAlignment(Qt.AlignCenter)

        self.dateRangeGridLayout.addWidget(self.trialDateStartLabel, 1, 0, 1, 1)

        self.useDateRangeCheckBox = QCheckBox(self.experimentDockWidgetContents)
        self.useDateRangeCheckBox.setObjectName(u"useDateRangeCheckBox")

        self.dateRangeGridLayout.addWidget(self.useDateRangeCheckBox, 0, 0, 1, 1)

        self.startCalendarWidget = QCalendarWidget(self.experimentDockWidgetContents)
        self.startCalendarWidget.setObjectName(u"startCalendarWidget")
        self.startCalendarWidget.setMinimumSize(QSize(375, 263))

        self.dateRangeGridLayout.addWidget(self.startCalendarWidget, 2, 1, 1, 1)

        self.trialDateEndLabel = QLabel(self.experimentDockWidgetContents)
        self.trialDateEndLabel.setObjectName(u"trialDateEndLabel")
        self.trialDateEndLabel.setAlignment(Qt.AlignCenter)

        self.dateRangeGridLayout.addWidget(self.trialDateEndLabel, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.dateRangeGridLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)


        self.gridLayout.addLayout(self.dateRangeGridLayout, 2, 0, 1, 2)

        self.investigatorHorizontalLayout = QHBoxLayout()
        self.investigatorHorizontalLayout.setObjectName(u"investigatorHorizontalLayout")
        self.useInvestigatorCheckBox = QCheckBox(self.experimentDockWidgetContents)
        self.useInvestigatorCheckBox.setObjectName(u"useInvestigatorCheckBox")

        self.investigatorHorizontalLayout.addWidget(self.useInvestigatorCheckBox)

        self.investigatorComboBox = QComboBox(self.experimentDockWidgetContents)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")

        self.investigatorHorizontalLayout.addWidget(self.investigatorComboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.investigatorHorizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.investigatorHorizontalLayout, 0, 0, 1, 2)

        self.gridLayout.setRowStretch(4, 1)
        SessionDockWidget.setWidget(self.experimentDockWidgetContents)

        self.retranslateUi(SessionDockWidget)

        QMetaObject.connectSlotsByName(SessionDockWidget)
    # setupUi

    def retranslateUi(self, SessionDockWidget):
        SessionDockWidget.setWindowTitle(QCoreApplication.translate("SessionDockWidget", u"Session Search Window", None))
        self.searchPushButton.setText(QCoreApplication.translate("SessionDockWidget", u"Search", None))
        self.loadPushButton.setText(QCoreApplication.translate("SessionDockWidget", u"Load Session", None))
        self.trialDateStartLabel.setText(QCoreApplication.translate("SessionDockWidget", u"Start", None))
        self.useDateRangeCheckBox.setText(QCoreApplication.translate("SessionDockWidget", u"Filter by Trial Date Range:", None))
        self.trialDateEndLabel.setText(QCoreApplication.translate("SessionDockWidget", u"End", None))
        self.useInvestigatorCheckBox.setText(QCoreApplication.translate("SessionDockWidget", u"Filter by Investigator:", None))
    # retranslateUi

