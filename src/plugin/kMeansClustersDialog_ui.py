# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kMeansClustersDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_kMeansClustersDialog(object):
    def setupUi(self, kMeansClustersDialog):
        if not kMeansClustersDialog.objectName():
            kMeansClustersDialog.setObjectName(u"kMeansClustersDialog")
        kMeansClustersDialog.resize(619, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(kMeansClustersDialog.sizePolicy().hasHeightForWidth())
        kMeansClustersDialog.setSizePolicy(sizePolicy)
        kMeansClustersDialog.setMinimumSize(QSize(0, 0))
        kMeansClustersDialog.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(kMeansClustersDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.numOfClustersLayout = QHBoxLayout()
        self.numOfClustersLayout.setObjectName(u"numOfClustersLayout")
        self.numOfClusterRadioButton = QRadioButton(kMeansClustersDialog)
        self.numOfClusterRadioButton.setObjectName(u"numOfClusterRadioButton")

        self.numOfClustersLayout.addWidget(self.numOfClusterRadioButton)

        self.numOfClustersLabel = QLabel(kMeansClustersDialog)
        self.numOfClustersLabel.setObjectName(u"numOfClustersLabel")
        self.numOfClustersLabel.setMinimumSize(QSize(0, 25))

        self.numOfClustersLayout.addWidget(self.numOfClustersLabel)

        self.numOfClustersBox = QSpinBox(kMeansClustersDialog)
        self.numOfClustersBox.setObjectName(u"numOfClustersBox")
        self.numOfClustersBox.setMinimum(1)
        self.numOfClustersBox.setValue(3)

        self.numOfClustersLayout.addWidget(self.numOfClustersBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.numOfClustersLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.numOfClustersLayout)

        self.gofLayout = QHBoxLayout()
        self.gofLayout.setObjectName(u"gofLayout")
        self.gofRadioButton = QRadioButton(kMeansClustersDialog)
        self.gofRadioButton.setObjectName(u"gofRadioButton")
        self.gofRadioButton.setChecked(True)

        self.gofLayout.addWidget(self.gofRadioButton)

        self.gofLabel1 = QLabel(kMeansClustersDialog)
        self.gofLabel1.setObjectName(u"gofLabel1")

        self.gofLayout.addWidget(self.gofLabel1)

        self.clusterRangeBox1 = QSpinBox(kMeansClustersDialog)
        self.clusterRangeBox1.setObjectName(u"clusterRangeBox1")
        self.clusterRangeBox1.setMinimum(1)

        self.gofLayout.addWidget(self.clusterRangeBox1)

        self.gofLabel2 = QLabel(kMeansClustersDialog)
        self.gofLabel2.setObjectName(u"gofLabel2")

        self.gofLayout.addWidget(self.gofLabel2)

        self.clusterRangeBox2 = QSpinBox(kMeansClustersDialog)
        self.clusterRangeBox2.setObjectName(u"clusterRangeBox2")
        self.clusterRangeBox2.setMinimum(1)
        self.clusterRangeBox2.setValue(11)

        self.gofLayout.addWidget(self.clusterRangeBox2)

        self.gofLabel3 = QLabel(kMeansClustersDialog)
        self.gofLabel3.setObjectName(u"gofLabel3")

        self.gofLayout.addWidget(self.gofLabel3)

        self.crossValidationFoldsBox = QSpinBox(kMeansClustersDialog)
        self.crossValidationFoldsBox.setObjectName(u"crossValidationFoldsBox")
        self.crossValidationFoldsBox.setMinimum(2)
        self.crossValidationFoldsBox.setValue(5)

        self.gofLayout.addWidget(self.crossValidationFoldsBox)

        self.gofLabel4 = QLabel(kMeansClustersDialog)
        self.gofLabel4.setObjectName(u"gofLabel4")

        self.gofLayout.addWidget(self.gofLabel4)


        self.verticalLayout.addLayout(self.gofLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(kMeansClustersDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(kMeansClustersDialog)
        self.buttonBox.accepted.connect(kMeansClustersDialog.accept)
        self.buttonBox.rejected.connect(kMeansClustersDialog.reject)

        QMetaObject.connectSlotsByName(kMeansClustersDialog)
    # setupUi

    def retranslateUi(self, kMeansClustersDialog):
        kMeansClustersDialog.setWindowTitle(QCoreApplication.translate("kMeansClustersDialog", u"Clusters Input For K-Means Clustering", None))
        self.numOfClusterRadioButton.setText("")
        self.numOfClustersLabel.setText(QCoreApplication.translate("kMeansClustersDialog", u"Number of Clusters : ", None))
        self.gofRadioButton.setText("")
        self.gofLabel1.setText(QCoreApplication.translate("kMeansClustersDialog", u"Evaluate goodness of fit from", None))
        self.gofLabel2.setText(QCoreApplication.translate("kMeansClustersDialog", u"to", None))
        self.gofLabel3.setText(QCoreApplication.translate("kMeansClustersDialog", u"clusters using ", None))
        self.gofLabel4.setText(QCoreApplication.translate("kMeansClustersDialog", u"folds cross validation", None))
    # retranslateUi

