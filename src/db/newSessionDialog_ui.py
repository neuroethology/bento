# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newSessionDialog.ui'
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


class Ui_NewSessionDialog(object):
    def setupUi(self, NewSessionDialog):
        if NewSessionDialog.objectName():
            NewSessionDialog.setObjectName(u"NewSessionDialog")
        NewSessionDialog.resize(684, 469)
        self.gridLayout = QGridLayout(NewSessionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sessionNumHorizontalLayout = QHBoxLayout()
        self.sessionNumHorizontalLayout.setObjectName(u"sessionNumHorizontalLayout")
        self.sessionNumLabel = QLabel(NewSessionDialog)
        self.sessionNumLabel.setObjectName(u"sessionNumLabel")

        self.sessionNumHorizontalLayout.addWidget(self.sessionNumLabel)

        self.sessionNumLineEdit = QLineEdit(NewSessionDialog)
        self.sessionNumLineEdit.setObjectName(u"sessionNumLineEdit")

        self.sessionNumHorizontalLayout.addWidget(self.sessionNumLineEdit)


        self.gridLayout.addLayout(self.sessionNumHorizontalLayout, 3, 0, 1, 1)

        self.dateHorizontalLayout = QHBoxLayout()
        self.dateHorizontalLayout.setObjectName(u"dateHorizontalLayout")
        self.dateLabel = QLabel(NewSessionDialog)
        self.dateLabel.setObjectName(u"dateLabel")

        self.dateHorizontalLayout.addWidget(self.dateLabel)

        self.dateEdit = QDateEdit(NewSessionDialog)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)

        self.dateHorizontalLayout.addWidget(self.dateEdit)


        self.gridLayout.addLayout(self.dateHorizontalLayout, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(NewSessionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.animalHorizontalLayout = QHBoxLayout()
        self.animalHorizontalLayout.setObjectName(u"animalHorizontalLayout")
        self.animalLabel = QLabel(NewSessionDialog)
        self.animalLabel.setObjectName(u"animalLabel")
        self.animalLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.animalHorizontalLayout.addWidget(self.animalLabel)

        self.animalTableView = QTableView(NewSessionDialog)
        self.animalTableView.setObjectName(u"animalTableView")
        self.animalTableView.horizontalHeader().setStretchLastSection(True)

        self.animalHorizontalLayout.addWidget(self.animalTableView)


        self.gridLayout.addLayout(self.animalHorizontalLayout, 0, 0, 1, 1)

        self.baseDirHorizontalLayout = QHBoxLayout()
        self.baseDirHorizontalLayout.setObjectName(u"baseDirHorizontalLayout")
        self.baseDirLabel = QLabel(NewSessionDialog)
        self.baseDirLabel.setObjectName(u"baseDirLabel")

        self.baseDirHorizontalLayout.addWidget(self.baseDirLabel)

        self.baseDirLineEdit = QLineEdit(NewSessionDialog)
        self.baseDirLineEdit.setObjectName(u"baseDirLineEdit")

        self.baseDirHorizontalLayout.addWidget(self.baseDirLineEdit)


        self.gridLayout.addLayout(self.baseDirHorizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(NewSessionDialog)
        self.buttonBox.accepted.connect(NewSessionDialog.accept)
        self.buttonBox.rejected.connect(NewSessionDialog.reject)

        QMetaObject.connectSlotsByName(NewSessionDialog)
    # setupUi

    def retranslateUi(self, NewSessionDialog):
        NewSessionDialog.setWindowTitle(QCoreApplication.translate("NewSessionDialog", u"New Session", None))
        self.sessionNumLabel.setText(QCoreApplication.translate("NewSessionDialog", u"Session #: ", None))
        self.sessionNumLineEdit.setInputMask(QCoreApplication.translate("NewSessionDialog", u"######", None))
        self.dateLabel.setText(QCoreApplication.translate("NewSessionDialog", u"Date: ", None))
        self.animalLabel.setText(QCoreApplication.translate("NewSessionDialog", u"Animal: ", None))
        self.baseDirLabel.setText(QCoreApplication.translate("NewSessionDialog", u"Base Directory: ", None))
    # retranslateUi

