# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'behaviorsDialog.ui'
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


class Ui_BehaviorsDialog(object):
    def setupUi(self, BehaviorsDialog):
        if BehaviorsDialog.objectName():
            BehaviorsDialog.setObjectName(u"BehaviorsDialog")
        BehaviorsDialog.resize(434, 1107)
        self.verticalLayout = QVBoxLayout(BehaviorsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.behaviorsTableView = QTableView(BehaviorsDialog)
        self.behaviorsTableView.setObjectName(u"behaviorsTableView")

        self.verticalLayout.addWidget(self.behaviorsTableView)

        self.buttonBox = QDialogButtonBox(BehaviorsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(BehaviorsDialog)
        self.buttonBox.accepted.connect(BehaviorsDialog.accept)
        self.buttonBox.rejected.connect(BehaviorsDialog.reject)

        QMetaObject.connectSlotsByName(BehaviorsDialog)
    # setupUi

    def retranslateUi(self, BehaviorsDialog):
        BehaviorsDialog.setWindowTitle(QCoreApplication.translate("BehaviorsDialog", u"Behaviors", None))
    # retranslateUi

