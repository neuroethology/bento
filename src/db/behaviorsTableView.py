# behaviorsTableView.py

from PySide6.QtWidgets import QTableView

class BehaviorsTableView(QTableView):
    def update(self, index):
        print(f"BehaviorsTableView.update(): index has {dir(index)}")
        super().update(index)