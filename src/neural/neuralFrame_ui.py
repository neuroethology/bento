# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neuralFrame.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

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

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.neuralView = NeuralView(neuralFrame)
        self.neuralView.setObjectName(u"neuralView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.neuralView.sizePolicy().hasHeightForWidth())
        self.neuralView.setSizePolicy(sizePolicy1)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.annotationsView.sizePolicy().hasHeightForWidth())
        self.annotationsView.setSizePolicy(sizePolicy2)
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
        self.showTraceRadioButton.setText(QCoreApplication.translate("neuralFrame", u"Show Trace", None))
        self.showHeatMapRadioButton.setText(QCoreApplication.translate("neuralFrame", u"Show HeatMap", None))
        self.showAnnotationsCheckBox.setText(QCoreApplication.translate("neuralFrame", u"Show Annotations", None))
    # retranslateUi

