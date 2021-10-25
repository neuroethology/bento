# behaviorsTableView.py

from qtpy.QtWidgets import QTableView

class BehaviorsTableView(QTableView):
    def update(self, index):
        print(f"BehaviorsTableView.update(): index has {dir(index)}")
        super().update(index)
