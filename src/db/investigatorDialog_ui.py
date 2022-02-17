# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'investigatorDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_InvestigatorDialog(object):
    def setupUi(self, InvestigatorDialog):
        if not InvestigatorDialog.objectName():
            InvestigatorDialog.setObjectName(u"InvestigatorDialog")
        InvestigatorDialog.resize(511, 261)
        self.verticalLayout = QVBoxLayout(InvestigatorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBoxHorizontalLayout = QHBoxLayout()
        self.comboBoxHorizontalLayout.setObjectName(u"comboBoxHorizontalLayout")
        self.investigatorLabel = QLabel(InvestigatorDialog)
        self.investigatorLabel.setObjectName(u"investigatorLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.investigatorLabel.sizePolicy().hasHeightForWidth())
        self.investigatorLabel.setSizePolicy(sizePolicy)

        self.comboBoxHorizontalLayout.addWidget(self.investigatorLabel)

        self.investigatorComboBox = QComboBox(InvestigatorDialog)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.investigatorComboBox.sizePolicy().hasHeightForWidth())
        self.investigatorComboBox.setSizePolicy(sizePolicy1)

        self.comboBoxHorizontalLayout.addWidget(self.investigatorComboBox)


        self.verticalLayout.addLayout(self.comboBoxHorizontalLayout)

        self.usernameHorizontalLayout = QHBoxLayout()
        self.usernameHorizontalLayout.setObjectName(u"usernameHorizontalLayout")
        self.usernameLabel = QLabel(InvestigatorDialog)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.usernameHorizontalLayout.addWidget(self.usernameLabel)

        self.usernameLineEdit = QLineEdit(InvestigatorDialog)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.usernameHorizontalLayout.addWidget(self.usernameLineEdit)


        self.verticalLayout.addLayout(self.usernameHorizontalLayout)

        self.firstNameHorizontalLayout = QHBoxLayout()
        self.firstNameHorizontalLayout.setObjectName(u"firstNameHorizontalLayout")
        self.firstNameLabel = QLabel(InvestigatorDialog)
        self.firstNameLabel.setObjectName(u"firstNameLabel")

        self.firstNameHorizontalLayout.addWidget(self.firstNameLabel)

        self.firstNameLineEdit = QLineEdit(InvestigatorDialog)
        self.firstNameLineEdit.setObjectName(u"firstNameLineEdit")

        self.firstNameHorizontalLayout.addWidget(self.firstNameLineEdit)


        self.verticalLayout.addLayout(self.firstNameHorizontalLayout)

        self.lastNameHorizontalLayout = QHBoxLayout()
        self.lastNameHorizontalLayout.setObjectName(u"lastNameHorizontalLayout")
        self.lastNameLabel = QLabel(InvestigatorDialog)
        self.lastNameLabel.setObjectName(u"lastNameLabel")

        self.lastNameHorizontalLayout.addWidget(self.lastNameLabel)

        self.lastNameLineEdit = QLineEdit(InvestigatorDialog)
        self.lastNameLineEdit.setObjectName(u"lastNameLineEdit")

        self.lastNameHorizontalLayout.addWidget(self.lastNameLineEdit)


        self.verticalLayout.addLayout(self.lastNameHorizontalLayout)

        self.institutionHorizontalLayout = QHBoxLayout()
        self.institutionHorizontalLayout.setObjectName(u"institutionHorizontalLayout")
        self.institutionLabel = QLabel(InvestigatorDialog)
        self.institutionLabel.setObjectName(u"institutionLabel")

        self.institutionHorizontalLayout.addWidget(self.institutionLabel)

        self.institutionLineEdit = QLineEdit(InvestigatorDialog)
        self.institutionLineEdit.setObjectName(u"institutionLineEdit")

        self.institutionHorizontalLayout.addWidget(self.institutionLineEdit)


        self.verticalLayout.addLayout(self.institutionHorizontalLayout)

        self.eMailHorizontalLayout = QHBoxLayout()
        self.eMailHorizontalLayout.setObjectName(u"eMailHorizontalLayout")
        self.eMailLabel = QLabel(InvestigatorDialog)
        self.eMailLabel.setObjectName(u"eMailLabel")

        self.eMailHorizontalLayout.addWidget(self.eMailLabel)

        self.eMailLineEdit = QLineEdit(InvestigatorDialog)
        self.eMailLineEdit.setObjectName(u"eMailLineEdit")

        self.eMailHorizontalLayout.addWidget(self.eMailLineEdit)


        self.verticalLayout.addLayout(self.eMailHorizontalLayout)

        self.buttonBox = QDialogButtonBox(InvestigatorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(InvestigatorDialog)
        self.buttonBox.accepted.connect(InvestigatorDialog.accept)
        self.buttonBox.rejected.connect(InvestigatorDialog.reject)
        self.buttonBox.clicked.connect(InvestigatorDialog.update)

        QMetaObject.connectSlotsByName(InvestigatorDialog)
    # setupUi

    def retranslateUi(self, InvestigatorDialog):
        InvestigatorDialog.setWindowTitle(QCoreApplication.translate("InvestigatorDialog", u"Investigator", None))
        self.investigatorLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"Investigator: ", None))
        self.usernameLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"Username: ", None))
        self.firstNameLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"First Name: ", None))
        self.lastNameLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"Last Name: ", None))
        self.institutionLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"Institution: ", None))
        self.eMailLabel.setText(QCoreApplication.translate("InvestigatorDialog", u"eMail: ", None))
    # retranslateUi

