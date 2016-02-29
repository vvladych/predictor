"""
Created on 27.05.2015

@author: vvladych
"""

from gi.repository import Gtk
from predictor.ui.ui_tools import show_info_dialog
from predictor.ui.prediction.textmodel.exttreeview import PredictionTextmodelExtTreeview
from predictor.model.predictor_model import TextmodelDAO
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.textmodel.statement.add_dialog import TextmodelStatementAddDialog


class TextModelAddDialog(Gtk.Dialog):
    
    def __init__(self, main_window, prediction):
        Gtk.Dialog.__init__(self, "Text model dialog", None, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.main_window = main_window
        
        self.set_default_size(150, 400)

        self.prediction = prediction
        self.overview_component = PredictionTextmodelExtTreeview(self,
                                                                 0,
                                                                 20,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.on_edit,
                                                                 self.prediction)

        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()

        layout_grid = Gtk.Grid()
        
        box.add(layout_grid)
        
        row = 0
        label = Gtk.Label("Prediction model(s)")
        layout_grid.attach(label, 0, row, 1, 1)

        row += 3
        model_uuid_label = Gtk.Label("Model UUID")
        model_uuid_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(model_uuid_label, 0, row, 1, 1)

        self.model_uuid_entry = Gtk.Entry()
        self.model_uuid_entry.set_editable(False)
        layout_grid.attach(self.model_uuid_entry, 1, row, 1, 1)

        row += 1

        model_short_desc_label = Gtk.Label("Short description")
        model_short_desc_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(model_short_desc_label, 0, row, 1, 1)

        self.model_short_desc_entry = Gtk.Entry()
        layout_grid.attach(self.model_short_desc_entry, 1, row, 1, 1)

        row += 1

        add_textmodel_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        layout_grid.attach(add_textmodel_button, 1, row, 1, 1)
        add_textmodel_button.connect("clicked", self.add_model_action)

        row += 2

        layout_grid.attach(self.overview_component, 0, row, 2, 1)


    @transactional
    def add_model_action(self, widget):
        textmodel = TextmodelDAO()
        textmodel.short_description = self.model_short_desc_entry.get_text()
        textmodel.save()
        self.prediction.add_textmodel(textmodel)
        self.prediction.save()
        show_info_dialog(None, "Add successful")
        self.overview_component.fill_treeview(0)

    def on_edit(self):
        textmodel_row = self.overview_component.get_selected_row()
        print(textmodel_row[1])
        textmodel = TextmodelDAO(textmodel_row[1])
        textmodel.load()
        dialog = TextmodelStatementAddDialog(self.main_window, textmodel)
        dialog.run()
        dialog.destroy()

    def noop(self, widget=None):
        pass


