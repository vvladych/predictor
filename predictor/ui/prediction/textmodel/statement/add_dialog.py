"""
Created on 29.07.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataProcessComponent

from predictor.ui.prediction.textmodel.statement.process_component import TextmodelStatementManipulationComponent, TextmodelStatementOverviewComponent


class TextmodelStatementAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, model):
        Gtk.Dialog.__init__(self, "Model Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        self.layout_grid = Gtk.Grid()
        
        self.textmodel = model
        
        self.process_component = AbstractDataProcessComponent(TextmodelStatementManipulationComponent(self.textmodel,
                                                                                                      TextmodelStatementOverviewComponent(self.textmodel)))
        
        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label("prediction model(s)")
        self.layout_grid.attach(label, 0, row, 1, 1)
        
        row += 3
        row = self.process_component.create_layout(self.layout_grid, row)
        
        return row