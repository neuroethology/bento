# deleteableTableView.py

from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QTableView, QMessageBox, QTreeWidget, QTreeWidgetItem

class DeleteableTableView(QTableView):

    def keyPressEvent(self, event):
        """
        Handle key press events in the view
        """
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            # figure out which row we're on and hide it
            msgBox = QMessageBox(
                QMessageBox.Question,
                "Delete Rows",
                "This will delete the selected file(s) from the database and cannot be undone.  Okay to continue?",
                buttons=QMessageBox.Yes | QMessageBox.Cancel)
            result = msgBox.exec()
            if result == QMessageBox.Yes:
                for ix in self.selectedIndexes():
                    self.hideRow(ix.row())
            event.accept()

class DeleteableTreeWidget(QTreeWidget):

    PoseHeaderType = QTreeWidgetItem.UserType + 10

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle key press events
        """
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            # figure out which row we're on and hide it
            msgBox = QMessageBox(
                QMessageBox.Question,
                "Delete Rows",
                "This will delete the selected file(s) along with any dependent "
                "items from the database and cannot be undone.  Okay to continue?",
                buttons=QMessageBox.Yes | QMessageBox.Cancel)
            result = msgBox.exec()
            if result == QMessageBox.Yes:
                for item in self.selectedItems():
                    item.setHidden(True)
                    if bool(item.parent()):
                        # pose item: hide the header if no children remain unhidden
                        nonHeaderChildCount = 0
                        poseHeaderIx = -1
                        parentChildCount = item.parent().childCount()
                        for child_ix in range(parentChildCount):
                            child = item.parent().child(child_ix)
                            if child.type() == DeleteableTreeWidget.PoseHeaderType:
                                poseHeaderIx = child_ix
                            elif not child.isHidden():
                                nonHeaderChildCount += 1
                        if nonHeaderChildCount == 0 and poseHeaderIx >= 0:
                            item.parent().child(poseHeaderIx).setHidden(True)

            event.accept()
            return
        return super().keyPressEvent(event)
