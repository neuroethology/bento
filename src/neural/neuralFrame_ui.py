# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neuralFrame.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QFrame,
    QGraphicsView, QHBoxLayout, QLabel, QLayout,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

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
        self.dataMinLabel.setText(QCoreApplication.translate("neuralFrame", u"data min", None))
        self.colormapImageLabel.setText(QCoreApplication.translate("neuralFrame", u"Colormap Image", None))
        self.dataMaxLabel.setText(QCoreApplication.translate("neuralFrame", u"data max", None))
    # retranslateUi

