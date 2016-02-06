"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.prediction_overview_window import PredictionOverviewWindow
from predictor.ui.prediction.prediction_new_dialog import PredictionNewDialog
from predictor.ui.ui_tools import show_info_dialog
from predictor.model.predictor_model import PredictionDAO

from predictor.ui.abstract_mask import AbstractMask
from predictor.ui.exttreeview import ExtendedTreeView, TreeviewColumn


class PredictionExtTreeview(ExtendedTreeView):

    dao_type = PredictionDAO

    def __init__(self, main_window, columns, start_row=0, rows_per_page=0, on_row_select_callback=None):
        super(PredictionExtTreeview, self).__init__(main_window, columns, start_row, rows_per_page, on_row_select_callback)

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

    def __init__(self, main_window):
        super(PredictionMask, self).__init__(main_window)

    def create_overview_treeview(self):
        treecolumns = [TreeviewColumn("uuid", 0, True),
                       TreeviewColumn("Publisher", 1, False),
                       TreeviewColumn("Date", 2, False),
                       TreeviewColumn("Prediction", 3, False)]
        self.overview_treeview = PredictionExtTreeview(self.main_window, treecolumns, 0, 20, self.on_row_select)

    def on_row_select(self, prediction_uuid):
        self.clear_main_middle_pane()
        prediction = self.__class__.dao_type(prediction_uuid)
        prediction.load()
        self.main_middle_pane.pack_start(PredictionOverviewWindow(self, prediction), False, False, 0)
        self.main_middle_pane.show_all()

