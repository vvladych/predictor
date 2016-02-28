"""
Created on 27.05.2015

@author: vvladych
"""

from gi.repository import Gtk
from predictor.ui.prediction.abstract_data_process_component import AbstractDataManipulationComponent, AbstractDataProcessComponent
from predictor.ui.ui_tools import show_info_dialog
from predictor.ui.prediction.textmodel.exttreeview import PredictionTextmodelExtTreeview
from predictor.model.predictor_model import TextmodelDAO


class TextModelAddDialog(Gtk.Dialog):
    
    def __init__(self, main_window, prediction):
        Gtk.Dialog.__init__(self, "Text model dialog", None, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.main_window = main_window
        
        self.set_default_size(150, 400)
        self.layout_grid = Gtk.Grid()
        
        self.prediction = prediction
        self.overview_component = PredictionTextmodelExtTreeview(self,
                                                                 0,
                                                                 20,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.prediction)

        self.process_component = AbstractDataProcessComponent(TextModelManipulationComponent(prediction,
                                                                                             self.overview_component))
        
        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label("Prediction model(s)")
        self.layout_grid.attach(label, 0, row, 1, 1)

        row += 3
        row = self.process_component.create_layout(self.layout_grid, row)

        return row

    def noop(self, widget=None):
        pass


class TextModelManipulationComponent(AbstractDataManipulationComponent):

    def __init__(self, prediction, overview_component):
        super(TextModelManipulationComponent, self).__init__(overview_component)
        self.prediction = prediction

    def create_layout(self, parent_layout_grid, row):
        self.parent_layout_grid = parent_layout_grid

        row += 1
        model_uuid_label = Gtk.Label("Model UUID")
        model_uuid_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(model_uuid_label, 0, row, 1, 1)

        self.model_uuid_entry = Gtk.Entry()
        self.model_uuid_entry.set_editable(False)
        parent_layout_grid.attach(self.model_uuid_entry, 1, row, 1, 1)

        row += 1

        model_short_desc_label = Gtk.Label("Short description")
        model_short_desc_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(model_short_desc_label, 0, row, 1, 1)

        self.model_short_desc_entry = Gtk.Entry()
        parent_layout_grid.attach(self.model_short_desc_entry, 1, row, 1, 1)

        row += 2

        add_state_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(add_state_button, 0, row, 1, 1)
        add_state_button.connect("clicked", self.add_model_action)

        delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        delete_button.connect("clicked", self.delete_action)
        parent_layout_grid.attach(delete_button, 1, row, 1, 1)

        row += 3

        row = self.overview_component.create_layout(parent_layout_grid, row)

        row += 1

        return row

    def add_model_action(self, widget):
        textmodel = TextmodelDAO()
        textmodel.short_description = self.model_short_desc_entry.get_text()
        textmodel.save()
        self.prediction.add_textmodel(textmodel)
        self.prediction.save()
        show_info_dialog(None, "Add successful")
        self.overview_component.clean_and_populate_model()

    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        tm = TextmodelDAO(model.get(tree_iter, 1)[0])
        tm.delete()
        self.prediction.load()
        show_info_dialog(None, "Delete successful")
        self.overview_component.clean_and_populate_model()

