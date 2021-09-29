# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        if not ConfigDialog.objectName():
            ConfigDialog.setObjectName(u"ConfigDialog")
        ConfigDialog.resize(400, 216)
        self.verticalLayout = QVBoxLayout(ConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.usePrivateDBHorizontalLayout = QHBoxLayout()
        self.usePrivateDBHorizontalLayout.setObjectName(u"usePrivateDBHorizontalLayout")
        self.usePrivateDBCheckBox = QCheckBox(ConfigDialog)
        self.usePrivateDBCheckBox.setObjectName(u"usePrivateDBCheckBox")
        self.usePrivateDBCheckBox.setChecked(True)

        self.usePrivateDBHorizontalLayout.addWidget(self.usePrivateDBCheckBox)


        self.verticalLayout.addLayout(self.usePrivateDBHorizontalLayout)

        self.usernameHorizontalLayout = QHBoxLayout()
        self.usernameHorizontalLayout.setObjectName(u"usernameHorizontalLayout")
        self.usernameLabel = QLabel(ConfigDialog)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.usernameHorizontalLayout.addWidget(self.usernameLabel)

        self.usernameLineEdit = QLineEdit(ConfigDialog)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.usernameHorizontalLayout.addWidget(self.usernameLineEdit)


        self.verticalLayout.addLayout(self.usernameHorizontalLayout)

        self.passwordHorizontalLayout = QHBoxLayout()
        self.passwordHorizontalLayout.setObjectName(u"passwordHorizontalLayout")
        self.passwordLabel = QLabel(ConfigDialog)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.passwordHorizontalLayout.addWidget(self.passwordLabel)

        self.passwordLineEdit = QLineEdit(ConfigDialog)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")

        self.passwordHorizontalLayout.addWidget(self.passwordLineEdit)


        self.verticalLayout.addLayout(self.passwordHorizontalLayout)

        self.hostHorizontalLayout = QHBoxLayout()
        self.hostHorizontalLayout.setObjectName(u"hostHorizontalLayout")
        self.hostLabel = QLabel(ConfigDialog)
        self.hostLabel.setObjectName(u"hostLabel")

        self.hostHorizontalLayout.addWidget(self.hostLabel)

        self.hostLineEdit = QLineEdit(ConfigDialog)
        self.hostLineEdit.setObjectName(u"hostLineEdit")

        self.hostHorizontalLayout.addWidget(self.hostLineEdit)


        self.verticalLayout.addLayout(self.hostHorizontalLayout)

        self.portHorizontalLayout = QHBoxLayout()
        self.portHorizontalLayout.setObjectName(u"portHorizontalLayout")
        self.portLabel = QLabel(ConfigDialog)
        self.portLabel.setObjectName(u"portLabel")

        self.portHorizontalLayout.addWidget(self.portLabel)

        self.portLineEdit = QLineEdit(ConfigDialog)
        self.portLineEdit.setObjectName(u"portLineEdit")

        self.portHorizontalLayout.addWidget(self.portLineEdit)


        self.verticalLayout.addLayout(self.portHorizontalLayout)

        self.buttonBox = QDialogButtonBox(ConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConfigDialog)
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)

        QMetaObject.connectSlotsByName(ConfigDialog)
    # setupUi

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QCoreApplication.translate("ConfigDialog", u"Config", None))
        self.usePrivateDBCheckBox.setText(QCoreApplication.translate("ConfigDialog", u" Use private database", None))
        self.usernameLabel.setText(QCoreApplication.translate("ConfigDialog", u"Username: ", None))
        self.passwordLabel.setText(QCoreApplication.translate("ConfigDialog", u"Password: ", None))
        self.hostLabel.setText(QCoreApplication.translate("ConfigDialog", u"Host name: ", None))
        self.hostLineEdit.setText(QCoreApplication.translate("ConfigDialog", u"storage1-andersonlab.caltech.edu", None))
        self.portLabel.setText(QCoreApplication.translate("ConfigDialog", u"Port Number: ", None))
        self.portLineEdit.setText(QCoreApplication.translate("ConfigDialog", u"3307", None))
    # retranslateUi

