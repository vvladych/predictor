"""
Created on 20.05.2015

@author: vvladych
"""
from predictor.model.predictor_model import PredictionPublisherV
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.prediction.publication.add_dialog import PublicationAddDialog
from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview


class PredictionPublicationMask(AbstractMask):

    dao_type = PredictionPublisherV
    exttreeview = PredictionPublicationExtTreeview

    default_height = 80
    default_width = 400

    def __init__(self, main_window, prediction):
        super(PredictionPublicationMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = PublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)
