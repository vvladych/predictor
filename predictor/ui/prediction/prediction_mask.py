"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.model.predictor_model import PredictionDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.prediction.prediction_new_dialog import PredictionNewDialog
from predictor.ui.prediction.prediction_overview_window import PredictionOverviewWindow
from predictor.ui.ui_tools import show_info_dialog


class PredictionExtTreeview(ExtendedTreeView):

    dao_type = PredictionDAO

    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Publisher", 1, False),
               TreeviewColumn("Date", 2, False),
               TreeviewColumn("Prediction", 3, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "publisher", "%s" % row.created_date, "%s" % row.commonname])

    def on_menu_item_new(self, widget):
        new_prediction_dialog = PredictionNewDialog(self.main_window)
        response = new_prediction_dialog.run()

        if response == Gtk.ResponseType.OK:
            new_prediction_dialog.perform_insert()

        elif response == Gtk.ResponseType.CANCEL:
            show_info_dialog(self.main_window, "Canceled")
        else:
            show_info_dialog(self.main_window, "Unknown action")

        new_prediction_dialog.destroy()
        self.reset_treemodel()


class PredictionMask(AbstractMask):

    dao_type = PredictionDAO
    overview_window = PredictionOverviewWindow
    exttreeview = PredictionExtTreeview
    default_height = 500
    default_width = 300
