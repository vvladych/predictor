"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.prediction_overview_window import PredictionOverviewWindow
from predictor.ui.prediction.prediction_new_dialog import PredictionNewDialog
from predictor.ui.ui_tools import add_column_to_treeview, show_info_dialog
from predictor.model.predictor_model import PredictionDAO

from predictor.model.DAO import DAOList
from predictor.ui.abstract_mask import AbstractMask


class PredictionMask(AbstractMask):
    
    def __init__(self, main_window):
        super(PredictionMask, self).__init__(main_window)

    def create_overview_treeview(self):
        self.predictions_treestore = Gtk.TreeStore(str, str, str, str)
        self.__populate_predictions_treestore()
        self.overview_treeview = Gtk.TreeView(self.predictions_treestore)
        self.overview_treeview.append_column(add_column_to_treeview("uuid", 0, True))
        self.overview_treeview.append_column(add_column_to_treeview("Publisher", 1, False))
        self.overview_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.overview_treeview.append_column(add_column_to_treeview("Predictions", 3, False))

    def add_context_menu_overview_treeview(self):
        menu = Gtk.Menu()
        menu_item_create_new_prediction = Gtk.MenuItem("Add new prediction...")
        menu_item_create_new_prediction.connect("activate", self.on_menu_item_create_new_prediction_click)
        menu.append(menu_item_create_new_prediction)
        menu_item_create_new_prediction.show()
        menu_item_delete_prediction = Gtk.MenuItem("Delete prediction...")
        menu_item_delete_prediction.connect("activate", self.on_menu_item_delete_prediction_click)
        menu.append(menu_item_delete_prediction)
        menu_item_delete_prediction.show()
        self.overview_treeview.connect("button_press_event", self.on_treeview_button_press_event, menu)

    def on_menu_item_create_new_prediction_click(self, widget):
        new_prediction_dialog = PredictionNewDialog(None)
        response = new_prediction_dialog.run()
        
        if response == Gtk.ResponseType.OK:
            new_prediction_dialog.perform_insert()
                
        elif response == Gtk.ResponseType.CANCEL:
            show_info_dialog(self.main_window, "Canceled")
        else:
            show_info_dialog(self.main_window, "Unknown action")
        
        new_prediction_dialog.destroy()
        self.__populate_predictions_treestore()

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

    def on_treeview_button_press_event(self, treeview, event, widget):
        x = int(event.x)
        y = int(event.y)
        pthinfo = treeview.get_path_at_pos(x, y)
        if event.button == 1:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
                prediction_uuid = self.predictions_treestore.get(self.predictions_treestore.get_iter(pthinfo[0]), 0)[0]
                prediction = PredictionDAO(prediction_uuid)
                prediction.load()
                self.clear_main_middle_pane()
                self.main_middle_pane.pack_start(PredictionOverviewWindow(self, prediction), False, False, 0)
                self.main_middle_pane.show_all()
        
        if event.button == 3:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
            widget.popup(None, None, None, None, event.button, event.time)    
        return True
