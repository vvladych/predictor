"""
Created on 20.05.2015

@author: vvladych
"""
from predictor.model.predictor_model import PredictionTextmodelV
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.prediction.textmodel.add_dialog import TextModelAddDialog
from predictor.ui.prediction.textmodel.exttreeview import PredictionTextmodelExtTreeview


class PredictionTextmodelMask(AbstractMask):

    dao_type = PredictionTextmodelV
    exttreeview = PredictionTextmodelExtTreeview

    def __init__(self, main_window, prediction):
        super(PredictionTextmodelMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = TextModelAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)


