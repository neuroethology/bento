# behaviorsTableView.py

from qtpy.QtWidgets import QTableView
from qtpy.QtCore import Slot

class BehaviorsTableView(QTableView):
    def update(self, index):
        print(f"BehaviorsTableView.update(): index has {dir(index)}")
        super().update(index)

    @Slot(int, int)
    def rowCountChanged(self, oldCount: int, newCount: int):
        print(f"rowCountChanged: oldCount = {oldCount}, newCount = {newCount}")
        super().rowCountChanged(oldCount, newCount)