# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cameraDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_CameraDialog(object):
    def setupUi(self, CameraDialog):
        if not CameraDialog.objectName():
            CameraDialog.setObjectName(u"CameraDialog")
        CameraDialog.resize(420, 228)
        self.verticalLayout = QVBoxLayout(CameraDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cameraHorizontalLayout = QHBoxLayout()
        self.cameraHorizontalLayout.setObjectName(u"cameraHorizontalLayout")
        self.cameraLabel = QLabel(CameraDialog)
        self.cameraLabel.setObjectName(u"cameraLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraLabel.sizePolicy().hasHeightForWidth())
        self.cameraLabel.setSizePolicy(sizePolicy)

        self.cameraHorizontalLayout.addWidget(self.cameraLabel)

        self.cameraComboBox = QComboBox(CameraDialog)
        self.cameraComboBox.setObjectName(u"cameraComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cameraComboBox.sizePolicy().hasHeightForWidth())
        self.cameraComboBox.setSizePolicy(sizePolicy1)
        self.cameraComboBox.setEditable(True)
        self.cameraComboBox.setCurrentText(u"")

        self.cameraHorizontalLayout.addWidget(self.cameraComboBox)


        self.verticalLayout.addLayout(self.cameraHorizontalLayout)

        self.nameHorizontalLayout = QHBoxLayout()
        self.nameHorizontalLayout.setObjectName(u"nameHorizontalLayout")
        self.nameLabel = QLabel(CameraDialog)
        self.nameLabel.setObjectName(u"nameLabel")

        self.nameHorizontalLayout.addWidget(self.nameLabel)

        self.nameLineEdit = QLineEdit(CameraDialog)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.nameHorizontalLayout.addWidget(self.nameLineEdit)


        self.verticalLayout.addLayout(self.nameHorizontalLayout)

        self.modelHorizontalLayout = QHBoxLayout()
        self.modelHorizontalLayout.setObjectName(u"modelHorizontalLayout")
        self.modelLabel = QLabel(CameraDialog)
        self.modelLabel.setObjectName(u"modelLabel")

        self.modelHorizontalLayout.addWidget(self.modelLabel)

        self.modelLineEdit = QLineEdit(CameraDialog)
        self.modelLineEdit.setObjectName(u"modelLineEdit")

        self.modelHorizontalLayout.addWidget(self.modelLineEdit)


        self.verticalLayout.addLayout(self.modelHorizontalLayout)

        self.lensHorizontalLayout = QHBoxLayout()
        self.lensHorizontalLayout.setObjectName(u"lensHorizontalLayout")
        self.lensLabel = QLabel(CameraDialog)
        self.lensLabel.setObjectName(u"lensLabel")

        self.lensHorizontalLayout.addWidget(self.lensLabel)

        self.lensLineEdit = QLineEdit(CameraDialog)
        self.lensLineEdit.setObjectName(u"lensLineEdit")

        self.lensHorizontalLayout.addWidget(self.lensLineEdit)


        self.verticalLayout.addLayout(self.lensHorizontalLayout)

        self.positionHorizontalLayout = QHBoxLayout()
        self.positionHorizontalLayout.setObjectName(u"positionHorizontalLayout")
        self.positionLabel = QLabel(CameraDialog)
        self.positionLabel.setObjectName(u"positionLabel")

        self.positionHorizontalLayout.addWidget(self.positionLabel)

        self.positionLineEdit = QLineEdit(CameraDialog)
        self.positionLineEdit.setObjectName(u"positionLineEdit")

        self.positionHorizontalLayout.addWidget(self.positionLineEdit)


        self.verticalLayout.addLayout(self.positionHorizontalLayout)

        self.buttonBox = QDialogButtonBox(CameraDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CameraDialog)
        self.buttonBox.accepted.connect(CameraDialog.accept)
        self.buttonBox.rejected.connect(CameraDialog.reject)
        self.buttonBox.clicked.connect(CameraDialog.update)

        QMetaObject.connectSlotsByName(CameraDialog)
    # setupUi

    def retranslateUi(self, CameraDialog):
        CameraDialog.setWindowTitle(QCoreApplication.translate("CameraDialog", u"Camera", None))
        self.cameraLabel.setText(QCoreApplication.translate("CameraDialog", u"Camera: ", None))
        self.nameLabel.setText(QCoreApplication.translate("CameraDialog", u"Name: ", None))
        self.modelLabel.setText(QCoreApplication.translate("CameraDialog", u"Model: ", None))
        self.lensLabel.setText(QCoreApplication.translate("CameraDialog", u"Lens: ", None))
        self.positionLabel.setText(QCoreApplication.translate("CameraDialog", u"Position: ", None))
    # retranslateUi

