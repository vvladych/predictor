"""
Created on 27.05.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent

from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog

from predictor.model.predictor_model import TextmodelDAO, PredictiontoTextmodel

from predictor.ui.prediction.textmodel.textmodel_statement_add_dialog import TextmodelStatementAddDialog


class TextModelProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, prediction):
        super(TextModelProcessComponent, self).__init__(TextModelManipulationComponent(prediction, TextModelOverviewComponent(prediction)))
        

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
        p_to_tm = PredictiontoTextmodel(self.prediction.uuid, textmodel.uuid)
        self.prediction.add_textmodel(p_to_tm)
        self.prediction.save()
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()

    def delete_action(self, widget):
        pass
        """
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        (model_sid)=model.get(tree_iter, 1)
        FCTextModel(model_sid).delete()
        model.remove(tree_iter)   
        show_info_dialog("Delete successful")   
        """


class TextModelOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns = [TreeviewColumn("prediction_uuid", 0, True),
                   TreeviewColumn("model_uuid", 1, False),
                   TreeviewColumn("Date", 2, False),
                   TreeviewColumn("Short desc.", 3, False)]
    
    def __init__(self, prediction):
        self.prediction = prediction
        super(TextModelOverviewComponent, self).__init__(TextModelOverviewComponent.treecolumns)

    def create_layout(self, parent_layout_grid, row):
        row += 1
        parent_layout_grid.attach(self.treeview, 0, row, 4, 1)
        return row
        
    def populate_model(self):
        self.treemodel.clear()
        for p_to_tm in self.prediction.PredictiontoTextmodel:
            textmodel = TextmodelDAO(p_to_tm.secDAO_uuid)
            textmodel.load()
            self.treemodel.append(["%s" % self.prediction.uuid, "%s" % textmodel.uuid, textmodel.date, textmodel.short_description])

    def on_row_select(self, widget, path, data):
        dialog = TextmodelStatementAddDialog(self, self.get_active_textmodel())
        dialog.run()
        dialog.destroy()

    def get_active_textmodel(self):
        (model, tree_iter) = self.treeview.get_selection().get_selected()
        textmodel_uuid = model.get(tree_iter, 1)[0]
        return textmodel_uuid
