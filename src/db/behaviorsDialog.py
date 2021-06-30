# behaviorsDialog.py

from db.schema_sqlalchemy import Camera, Trial, Session, VideoData, NeuralData, AnnotationsData, Investigator
from sqlalchemy import func, select
from db.behaviorsDialog_ui import Ui_BehaviorsDialog
from annot.behavior import Behavior, Behaviors
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import QDialog, QFileDialog, QHeaderView, QMessageBox
from widgets.tableModel import EditableTableModel
from os.path import expanduser, sep
# from caiman.utils.utils import load_dict_from_hdf5

class BehaviorsDialog(QDialog):

    quitting = Signal()
    trialsChanged = Signal()

    def __init__(self, bento):
        super().__init__()
        self.bento = bento
        self.ui = Ui_BehaviorsDialog()
        self.ui.setupUi(self)
        self.quitting.connect(self.bento.quit)

        self.populateBehaviorsTableView()

    # Behaviors Data

    def setBehaviorsModel(self, model):
        oldModel = self.ui.behaviorsTableView.selectionModel()
        self.ui.behaviorsTableView.setModel(model)
        self.ui.behaviorsTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.behaviorsTableView.resizeColumnsToContents()
        self.ui.behaviorsTableView.setSortingEnabled(False)
        self.ui.behaviorsTableView.setAutoScroll(False)
        if oldModel:
            oldModel.deleteLater()

    def populateBehaviorsTableView(self):
        header = self.bento.behaviors.header()
        print(f"Type of self.bento.behaviors is {type(self.bento.behaviors)}")
        data_list = [behavior.toDict() for behavior in self.bento.behaviors]
        model = EditableTableModel(self, data_list, header)
        self.setBehaviorsModel(model)

    def updateBehaviors(self, trial, db_sess):
        model = self.ui.behaviorsTableView.model()
        for ix, entry in enumerate(model.getIterator()):
            tableIndex = model.createIndex(ix, 0)
            if model.isDirty(tableIndex):
                print(f"item at row {ix} is dirty")
                #TODO: update from table model back into bento's behaviors
                """
                if ix < len(trial.video_data) and trial.video_data[ix].id == entry['id']:
                    trial.video_data[ix].fromDict(entry, db_sess)
                else:
                    # new item
                    item = VideoData(entry, db_sess) # update everything in the item and let the transaction figure out what changed.
                    db_sess.add(item)
                    trial.video_data.append(item)
                """
                model.clearDirty(tableIndex)
            else:
                print(f"item at row {ix} wasn't dirty, so did nothing")

    @Slot()
    def accept(self):
        #TODO: update bento's behaviors here and save to file (or database?)
        super().accept()

    @Slot()
    def reject(self):
        super().reject()
