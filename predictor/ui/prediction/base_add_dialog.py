from . import *


class BaseAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction, dialog_title):
        Gtk.Dialog.__init__(self,
                            dialog_title,
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.main_window = parent
        self.prediction = prediction
        self.set_default_size(400, 400)
        self.set_overview_component()
        box = self.get_content_area()
        layout_grid = self.create_layout()
        box.add(layout_grid)
        self.show_all()

    def set_overview_component(self):
        raise NotImplementedError("set_overview_component still not implemented")

    def create_layout(self):
        raise NotImplementedError("create layout not implemented")

    def noop(self, widget):
        pass
