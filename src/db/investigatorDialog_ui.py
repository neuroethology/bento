# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'investigatorDialog.ui'
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


class Ui_investigatorDialog(object):
    def setupUi(self, investigatorDialog):
        if investigatorDialog.objectName():
            investigatorDialog.setObjectName(u"investigatorDialog")
        investigatorDialog.resize(511, 261)
        self.verticalLayout = QVBoxLayout(investigatorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBoxHorizontalLayout = QHBoxLayout()
        self.comboBoxHorizontalLayout.setObjectName(u"comboBoxHorizontalLayout")
        self.investigatorLabel = QLabel(investigatorDialog)
        self.investigatorLabel.setObjectName(u"investigatorLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.investigatorLabel.sizePolicy().hasHeightForWidth())
        self.investigatorLabel.setSizePolicy(sizePolicy)

        self.comboBoxHorizontalLayout.addWidget(self.investigatorLabel)

        self.investigatorComboBox = QComboBox(investigatorDialog)
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
        self.usernameLabel = QLabel(investigatorDialog)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.usernameHorizontalLayout.addWidget(self.usernameLabel)

        self.usernameLineEdit = QLineEdit(investigatorDialog)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.usernameHorizontalLayout.addWidget(self.usernameLineEdit)


        self.verticalLayout.addLayout(self.usernameHorizontalLayout)

        self.firstNameHorizontalLayout = QHBoxLayout()
        self.firstNameHorizontalLayout.setObjectName(u"firstNameHorizontalLayout")
        self.firstNameLabel = QLabel(investigatorDialog)
        self.firstNameLabel.setObjectName(u"firstNameLabel")

        self.firstNameHorizontalLayout.addWidget(self.firstNameLabel)

        self.firstNameLineEdit = QLineEdit(investigatorDialog)
        self.firstNameLineEdit.setObjectName(u"firstNameLineEdit")

        self.firstNameHorizontalLayout.addWidget(self.firstNameLineEdit)


        self.verticalLayout.addLayout(self.firstNameHorizontalLayout)

        self.lastNameHorizontalLayout = QHBoxLayout()
        self.lastNameHorizontalLayout.setObjectName(u"lastNameHorizontalLayout")
        self.lastNameLabel = QLabel(investigatorDialog)
        self.lastNameLabel.setObjectName(u"lastNameLabel")

        self.lastNameHorizontalLayout.addWidget(self.lastNameLabel)

        self.lastNameLineEdit = QLineEdit(investigatorDialog)
        self.lastNameLineEdit.setObjectName(u"lastNameLineEdit")

        self.lastNameHorizontalLayout.addWidget(self.lastNameLineEdit)


        self.verticalLayout.addLayout(self.lastNameHorizontalLayout)

        self.institutionHorizontalLayout = QHBoxLayout()
        self.institutionHorizontalLayout.setObjectName(u"institutionHorizontalLayout")
        self.institutionLabel = QLabel(investigatorDialog)
        self.institutionLabel.setObjectName(u"institutionLabel")

        self.institutionHorizontalLayout.addWidget(self.institutionLabel)

        self.institutionLineEdit = QLineEdit(investigatorDialog)
        self.institutionLineEdit.setObjectName(u"institutionLineEdit")

        self.institutionHorizontalLayout.addWidget(self.institutionLineEdit)


        self.verticalLayout.addLayout(self.institutionHorizontalLayout)

        self.eMailHorizontalLayout = QHBoxLayout()
        self.eMailHorizontalLayout.setObjectName(u"eMailHorizontalLayout")
        self.eMailLabel = QLabel(investigatorDialog)
        self.eMailLabel.setObjectName(u"eMailLabel")

        self.eMailHorizontalLayout.addWidget(self.eMailLabel)

        self.eMailLineEdit = QLineEdit(investigatorDialog)
        self.eMailLineEdit.setObjectName(u"eMailLineEdit")

        self.eMailHorizontalLayout.addWidget(self.eMailLineEdit)


        self.verticalLayout.addLayout(self.eMailHorizontalLayout)

        self.buttonBox = QDialogButtonBox(investigatorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Discard|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(investigatorDialog)
        self.buttonBox.accepted.connect(investigatorDialog.accept)
        self.buttonBox.rejected.connect(investigatorDialog.reject)
        self.buttonBox.clicked.connect(investigatorDialog.update)

        QMetaObject.connectSlotsByName(investigatorDialog)
    # setupUi

    def retranslateUi(self, investigatorDialog):
        investigatorDialog.setWindowTitle(QCoreApplication.translate("investigatorDialog", u"Investigator", None))
        self.investigatorLabel.setText(QCoreApplication.translate("investigatorDialog", u"Investigator: ", None))
        self.usernameLabel.setText(QCoreApplication.translate("investigatorDialog", u"Username: ", None))
        self.firstNameLabel.setText(QCoreApplication.translate("investigatorDialog", u"First Name: ", None))
        self.lastNameLabel.setText(QCoreApplication.translate("investigatorDialog", u"Last Name: ", None))
        self.institutionLabel.setText(QCoreApplication.translate("investigatorDialog", u"Institution: ", None))
        self.eMailLabel.setText(QCoreApplication.translate("investigatorDialog", u"eMail: ", None))
    # retranslateUi

