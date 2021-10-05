# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dispositionItemsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_DispositionItemsDialog(object):
    def setupUi(self, DispositionItemsDialog):
        if not DispositionItemsDialog.objectName():
            DispositionItemsDialog.setObjectName(u"DispositionItemsDialog")
        DispositionItemsDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DispositionItemsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dispositionLabel = QLabel(DispositionItemsDialog)
        self.dispositionLabel.setObjectName(u"dispositionLabel")
        self.dispositionLabel.setText(u"TextLabel")
        self.dispositionLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.dispositionLabel)

        self.assignToComboBox = QComboBox(DispositionItemsDialog)
        self.assignToComboBox.setObjectName(u"assignToComboBox")

        self.verticalLayout.addWidget(self.assignToComboBox)

        self.buttonBox = QDialogButtonBox(DispositionItemsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Discard)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DispositionItemsDialog)
        self.buttonBox.accepted.connect(DispositionItemsDialog.accept)
        self.buttonBox.rejected.connect(DispositionItemsDialog.reject)

        QMetaObject.connectSlotsByName(DispositionItemsDialog)
    # setupUi

    def retranslateUi(self, DispositionItemsDialog):
        DispositionItemsDialog.setWindowTitle(QCoreApplication.translate("DispositionItemsDialog", u"Dialog", None))
    # retranslateUi

