# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editSessionDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore


class Ui_EditSessionDialog(object):
    def setupUi(self, EditSessionDialog):
        if not EditSessionDialog.objectName():
            EditSessionDialog.setObjectName(u"EditSessionDialog")
        EditSessionDialog.resize(684, 469)
        self.gridLayout = QGridLayout(EditSessionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sessionDateHorizontalLayout = QHBoxLayout()
        self.sessionDateHorizontalLayout.setObjectName(u"sessionDateHorizontalLayout")
        self.sessionNumLabel = QLabel(EditSessionDialog)
        self.sessionNumLabel.setObjectName(u"sessionNumLabel")

        self.sessionDateHorizontalLayout.addWidget(self.sessionNumLabel)

        self.sessionNumLineEdit = QLineEdit(EditSessionDialog)
        self.sessionNumLineEdit.setObjectName(u"sessionNumLineEdit")

        self.sessionDateHorizontalLayout.addWidget(self.sessionNumLineEdit)

        self.dateLabel = QLabel(EditSessionDialog)
        self.dateLabel.setObjectName(u"dateLabel")

        self.sessionDateHorizontalLayout.addWidget(self.dateLabel)

        self.dateEdit = QDateEdit(EditSessionDialog)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)

        self.sessionDateHorizontalLayout.addWidget(self.dateEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.sessionDateHorizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.sessionDateHorizontalLayout, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(EditSessionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.animalHorizontalLayout = QHBoxLayout()
        self.animalHorizontalLayout.setObjectName(u"animalHorizontalLayout")
        self.animalLabel = QLabel(EditSessionDialog)
        self.animalLabel.setObjectName(u"animalLabel")
        self.animalLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.animalHorizontalLayout.addWidget(self.animalLabel)

        self.animalTableView = QTableView(EditSessionDialog)
        self.animalTableView.setObjectName(u"animalTableView")
        self.animalTableView.horizontalHeader().setStretchLastSection(True)

        self.animalHorizontalLayout.addWidget(self.animalTableView)


        self.gridLayout.addLayout(self.animalHorizontalLayout, 0, 0, 1, 1)

        self.baseDirHorizontalLayout = QHBoxLayout()
        self.baseDirHorizontalLayout.setObjectName(u"baseDirHorizontalLayout")
        self.baseDirLabel = QLabel(EditSessionDialog)
        self.baseDirLabel.setObjectName(u"baseDirLabel")

        self.baseDirHorizontalLayout.addWidget(self.baseDirLabel)

        self.baseDirLineEdit = QLineEdit(EditSessionDialog)
        self.baseDirLineEdit.setObjectName(u"baseDirLineEdit")

        self.baseDirHorizontalLayout.addWidget(self.baseDirLineEdit)

        self.selectBaseDirPushButton = QPushButton(EditSessionDialog)
        self.selectBaseDirPushButton.setObjectName(u"selectBaseDirPushButton")

        self.baseDirHorizontalLayout.addWidget(self.selectBaseDirPushButton)


        self.gridLayout.addLayout(self.baseDirHorizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(EditSessionDialog)
        self.buttonBox.accepted.connect(EditSessionDialog.accept)
        self.buttonBox.rejected.connect(EditSessionDialog.reject)

        QMetaObject.connectSlotsByName(EditSessionDialog)
    # setupUi

    def retranslateUi(self, EditSessionDialog):
        EditSessionDialog.setWindowTitle(QCoreApplication.translate("EditSessionDialog", u"Add or Edit Session", None))
        self.sessionNumLabel.setText(QCoreApplication.translate("EditSessionDialog", u"Session #: ", None))
        self.sessionNumLineEdit.setInputMask("")
        self.dateLabel.setText(QCoreApplication.translate("EditSessionDialog", u" Date: ", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("EditSessionDialog", u"yyyy-MM-dd", None))
        self.animalLabel.setText(QCoreApplication.translate("EditSessionDialog", u"Animal: ", None))
        self.baseDirLabel.setText(QCoreApplication.translate("EditSessionDialog", u"Base Directory: ", None))
        self.selectBaseDirPushButton.setText(QCoreApplication.translate("EditSessionDialog", u"Select...", None))
    # retranslateUi

