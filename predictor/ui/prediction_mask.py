"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.prediction_overview_window import PredictionOverviewWindow
from predictor.ui.prediction.prediction_new_dialog import PredictionNewDialog
from predictor.ui.ui_tools import show_info_dialog
from predictor.model.predictor_model import PredictionDAO

from predictor.model.DAO import DAOList
from predictor.ui.abstract_mask import AbstractMask
from predictor.ui.exttreeview import ExtendedTreeView, TreedataContainer, TreeviewColumn


class PredictionExtTreeview(ExtendedTreeView):

    def __init__(self, columns, treedata, start_row=0, rows_per_page=0, on_row_select_callback=None):
        super(PredictionExtTreeview, self).__init__(columns, treedata, start_row, rows_per_page, on_row_select_callback)

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "publisher", "%s" % row.created_date, "%s" % row.commonname])

    def on_menu_item_new(self, widget):
        new_prediction_dialog = PredictionNewDialog(None)
        response = new_prediction_dialog.run()

        if response == Gtk.ResponseType.OK:
            new_prediction_dialog.perform_insert()

        elif response == Gtk.ResponseType.CANCEL:
            show_info_dialog(self.main_window, "Canceled")
        else:
            show_info_dialog(self.main_window, "Unknown action")

        new_prediction_dialog.destroy()
        self.reset_treemodel()

    def on_menu_item_delete(self, widget):
        (model, tree_iter) = self.treeview.get_selection().get_selected()
        prediction_uuid = model.get_value(tree_iter, 0)
        nd = Gtk.Dialog("Delete prediction?",
                        None,
                        0,
                        ("OK", Gtk.ResponseType.OK, "CANCEL", Gtk.ResponseType.CANCEL))
        ret = nd.run()
        nd.destroy()
        if ret == Gtk.ResponseType.OK:
            prediction = PredictionDAO(prediction_uuid)
            prediction.delete()
            self.reset_treemodel()
        else:
            show_info_dialog(None, "Canceled")


class PredictionMask(AbstractMask):
    
    def __init__(self, main_window):
        self.dao_type = PredictionDAO
        super(PredictionMask, self).__init__(main_window)

    def create_overview_treeview(self):
        treedata = TreedataContainer(self.dao_type)
        treecolumns = [TreeviewColumn("uuid", 0, True),
                       TreeviewColumn("Publisher", 1, False),
                       TreeviewColumn("Date", 2, False),
                       TreeviewColumn("Prediction", 3, False)]
        self.overview_treeview = PredictionExtTreeview(treecolumns, treedata, 0, 20, self.on_row_select)


    def add_context_menu_overview_treeview(self):
        pass

    def on_row_select(self, prediction_uuid):
        self.clear_main_middle_pane()
        prediction = PredictionDAO(prediction_uuid)
        prediction.load()
        self.main_middle_pane.pack_start(PredictionOverviewWindow(self, prediction), False, False, 0)
        self.main_middle_pane.show_all()

    def __populate_predictions_treestore(self):
        self.predictions_treestore.clear()
        predictions = DAOList(PredictionDAO)
        predictions.load()
        for prediction in predictions:
            self.predictions_treestore.append(None,
                                              ["%s" % prediction.uuid,
                                               "",
                                               "%s" % prediction.created_date,
                                               prediction.commonname])

    def on_menu_item_delete_prediction_click(self, widget):
        (model, tree_iter) = self.overview_treeview.get_selection().get_selected()
        prediction_uuid = model.get_value(tree_iter, 0)
        nd = Gtk.Dialog("Delete prediction?",
                        self.main_window,
                        0,
                        ("OK", Gtk.ResponseType.OK, "CANCEL", Gtk.ResponseType.CANCEL))
        ret = nd.run()
        nd.destroy()
        if ret == Gtk.ResponseType.OK:
            prediction = PredictionDAO(prediction_uuid)
            prediction.delete()
            self.__populate_predictions_treestore()
        else:
            show_info_dialog(self.main_window, "Canceled")

