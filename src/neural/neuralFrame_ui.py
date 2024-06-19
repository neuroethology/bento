# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neuralFrame.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from widgets.annotationsWidget import AnnotationsView
from widgets.neuralWidget import NeuralView


class Ui_neuralFrame(object):
    def setupUi(self, neuralFrame):
        if not neuralFrame.objectName():
            neuralFrame.setObjectName(u"neuralFrame")
        neuralFrame.resize(945, 869)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(neuralFrame.sizePolicy().hasHeightForWidth())
        neuralFrame.setSizePolicy(sizePolicy)
        neuralFrame.setFrameShape(QFrame.Panel)
        self.verticalLayout = QVBoxLayout(neuralFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.leftHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.leftHorizontalSpacer)

        self.launchPlugin = QToolButton(neuralFrame)
        self.launchPlugin.setObjectName(u"launchPlugin")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.launchPlugin.sizePolicy().hasHeightForWidth())
        self.launchPlugin.setSizePolicy(sizePolicy1)
        self.launchPlugin.setMinimumSize(QSize(0, 0))
        self.launchPlugin.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(13)
        self.launchPlugin.setFont(font)
        self.launchPlugin.setFocusPolicy(Qt.StrongFocus)
        self.launchPlugin.setAutoFillBackground(False)
        self.launchPlugin.setIconSize(QSize(8, 8))
        self.launchPlugin.setPopupMode(QToolButton.InstantPopup)
        self.launchPlugin.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.launchPlugin.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.launchPlugin)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.showTraceRadioButton = QRadioButton(neuralFrame)
        self.showTraceRadioButton.setObjectName(u"showTraceRadioButton")
        self.showTraceRadioButton.setChecked(True)

        self.horizontalLayout.addWidget(self.showTraceRadioButton)

        self.showHeatMapRadioButton = QRadioButton(neuralFrame)
        self.showHeatMapRadioButton.setObjectName(u"showHeatMapRadioButton")

        self.horizontalLayout.addWidget(self.showHeatMapRadioButton)

        self.showAnnotationsCheckBox = QCheckBox(neuralFrame)
        self.showAnnotationsCheckBox.setObjectName(u"showAnnotationsCheckBox")
        self.showAnnotationsCheckBox.setChecked(True)

        self.horizontalLayout.addWidget(self.showAnnotationsCheckBox)

        self.rightHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.rightHorizontalSpacer)

        self.dataMinLabel = QLabel(neuralFrame)
        self.dataMinLabel.setObjectName(u"dataMinLabel")
        self.dataMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.dataMinLabel)

        self.colormapImageLabel = QLabel(neuralFrame)
        self.colormapImageLabel.setObjectName(u"colormapImageLabel")
        self.colormapImageLabel.setMinimumSize(QSize(200, 0))
        self.colormapImageLabel.setScaledContents(True)
        self.colormapImageLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.colormapImageLabel)

        self.dataMaxLabel = QLabel(neuralFrame)
        self.dataMaxLabel.setObjectName(u"dataMaxLabel")

        self.horizontalLayout.addWidget(self.dataMaxLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.neuralView = NeuralView(neuralFrame)
        self.neuralView.setObjectName(u"neuralView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.neuralView.sizePolicy().hasHeightForWidth())
        self.neuralView.setSizePolicy(sizePolicy2)
        self.neuralView.setFrameShape(QFrame.NoFrame)
        self.neuralView.setFrameShadow(QFrame.Plain)
        self.neuralView.setLineWidth(0)
        self.neuralView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.neuralView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.neuralView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.neuralView.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.neuralView.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.verticalLayout.addWidget(self.neuralView)

        self.annotationsView = AnnotationsView(neuralFrame)
        self.annotationsView.setObjectName(u"annotationsView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(4)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.annotationsView.sizePolicy().hasHeightForWidth())
        self.annotationsView.setSizePolicy(sizePolicy3)
        self.annotationsView.setMinimumSize(QSize(0, 64))
        self.annotationsView.setMaximumSize(QSize(16777215, 64))
        self.annotationsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.annotationsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.verticalLayout.addWidget(self.annotationsView)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(neuralFrame)

        QMetaObject.connectSlotsByName(neuralFrame)
    # setupUi

    def retranslateUi(self, neuralFrame):
        neuralFrame.setWindowTitle(QCoreApplication.translate("neuralFrame", u"Neural Data", None))
#if QT_CONFIG(tooltip)
        self.launchPlugin.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.launchPlugin.setText(QCoreApplication.translate("neuralFrame", u"Launch Neural Plugin", None))
        self.showTraceRadioButton.setText(QCoreApplication.translate("neuralFrame", u"Show Trace", None))
        self.showHeatMapRadioButton.setText(QCoreApplication.translate("neuralFrame", u"Show HeatMap", None))
        self.showAnnotationsCheckBox.setText(QCoreApplication.translate("neuralFrame", u"Show Annotations", None))
        self.dataMinLabel.setText(QCoreApplication.translate("neuralFrame", u"data min", None))
        self.colormapImageLabel.setText(QCoreApplication.translate("neuralFrame", u"Colormap Image", None))
        self.dataMaxLabel.setText(QCoreApplication.translate("neuralFrame", u"data max", None))
    # retranslateUi

