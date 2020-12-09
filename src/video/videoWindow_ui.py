# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videoWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_videoDockWidget(object):
    def setupUi(self, videoDockWidget):
        if not videoDockWidget.objectName():
            videoDockWidget.setObjectName(u"videoDockWidget")
        videoDockWidget.resize(1024, 650)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.openButton = QPushButton(self.dockWidgetContents)
        self.openButton.setObjectName(u"openButton")
        self.openButton.setGeometry(QRect(780, 590, 171, 32))
        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1024, 575))
        self.label.setAlignment(Qt.AlignCenter)
        videoDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(videoDockWidget)

        QMetaObject.connectSlotsByName(videoDockWidget)
    # setupUi

    def retranslateUi(self, videoDockWidget):
        videoDockWidget.setWindowTitle(QCoreApplication.translate("videoDockWidget", u"video", None))
        self.openButton.setText(QCoreApplication.translate("videoDockWidget", u"Open...", None))
        self.label.setText(QCoreApplication.translate("videoDockWidget", u"video", None))
    # retranslateUi

