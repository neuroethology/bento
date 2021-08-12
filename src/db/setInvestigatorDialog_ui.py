# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setInvestigatorDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SetInvestigatorDialog(object):
    def setupUi(self, SetInvestigatorDialog):
        if not SetInvestigatorDialog.objectName():
            SetInvestigatorDialog.setObjectName(u"SetInvestigatorDialog")
        SetInvestigatorDialog.resize(400, 96)
        self.verticalLayout = QVBoxLayout(SetInvestigatorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.investigatorLabel = QLabel(SetInvestigatorDialog)
        self.investigatorLabel.setObjectName(u"investigatorLabel")

        self.horizontalLayout.addWidget(self.investigatorLabel)

        self.investigatorComboBox = QComboBox(SetInvestigatorDialog)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.investigatorComboBox.sizePolicy().hasHeightForWidth())
        self.investigatorComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.investigatorComboBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(SetInvestigatorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SetInvestigatorDialog)
        self.buttonBox.accepted.connect(SetInvestigatorDialog.accept)
        self.buttonBox.rejected.connect(SetInvestigatorDialog.reject)

        QMetaObject.connectSlotsByName(SetInvestigatorDialog)
    # setupUi

    def retranslateUi(self, SetInvestigatorDialog):
        SetInvestigatorDialog.setWindowTitle(QCoreApplication.translate("SetInvestigatorDialog", u"Set Investigator", None))
        self.investigatorLabel.setText(QCoreApplication.translate("SetInvestigatorDialog", u"Investigator: ", None))
    # retranslateUi

