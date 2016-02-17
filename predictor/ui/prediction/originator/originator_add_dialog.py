"""
Created on 14.05.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.originator.originator_process_component import OriginatorProcessComponent


class OriginatorAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self, "Originator Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        self.layout_grid = Gtk.Grid()
        
        self.process_component = OriginatorProcessComponent(prediction)
        
        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label("Forecast originator(s)")
        self.layout_grid.attach(label, 0, row, 1, 1)
        
        row += 1
        row = self.process_component.create_layout(self.layout_grid, row)
        return row
