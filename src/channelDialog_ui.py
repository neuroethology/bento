# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'channelDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_ChannelDialog(object):
    def setupUi(self, ChannelDialog):
        if not ChannelDialog.objectName():
            ChannelDialog.setObjectName(u"ChannelDialog")
        ChannelDialog.resize(408, 90)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChannelDialog.sizePolicy().hasHeightForWidth())
        ChannelDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ChannelDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(ChannelDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.channelNameLineEdit = QLineEdit(ChannelDialog)
        self.channelNameLineEdit.setObjectName(u"channelNameLineEdit")

        self.horizontalLayout.addWidget(self.channelNameLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(ChannelDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ChannelDialog)
        self.buttonBox.accepted.connect(ChannelDialog.accept)
        self.buttonBox.rejected.connect(ChannelDialog.reject)

        QMetaObject.connectSlotsByName(ChannelDialog)
    # setupUi

    def retranslateUi(self, ChannelDialog):
        ChannelDialog.setWindowTitle(QCoreApplication.translate("ChannelDialog", u"New Channel Dialog", None))
        self.label.setText(QCoreApplication.translate("ChannelDialog", u"Channel name: ", None))
    # retranslateUi

