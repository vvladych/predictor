"""
Created on 27.05.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.model.predictor_model import TextmodelDAO, PredictionDAO
from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent
from predictor.ui.prediction.textmodel.statement.add_dialog import TextmodelStatementAddDialog
from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog


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
        p = PredictionDAO(self.prediction.uuid)
        p.load()
        for p_to_tm in p.PredictiontoTextmodel:
            textmodel = TextmodelDAO(p_to_tm.secDAO_uuid)
            textmodel.load()
            self.treemodel.append(["%s" % p.uuid, "%s" % textmodel.uuid, textmodel.date, textmodel.short_description])

    def on_row_select(self, widget, path, data):
        tm = TextmodelDAO(self.get_active_textmodel())
        tm.load()
        dialog = TextmodelStatementAddDialog(self, tm)
        dialog.run()
        dialog.destroy()

    def get_active_textmodel(self):
        (model, tree_iter) = self.treeview.get_selection().get_selected()
        textmodel_uuid = model.get(tree_iter, 1)[0]
        return textmodel_uuid
