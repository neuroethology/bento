# deleteableTableView.py

from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QTableView, QMessageBox, QTreeWidget

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
            event.accept()
            return
        return super().keyPressEvent(event)
