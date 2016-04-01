from . import *


class MDOWindow(Gtk.Grid):

    def __init__(self, main_window, dao=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.dao = dao
        self.create_layout()
        if dao is not None:
            self.dao.load()
            self.load_dao()
        self.parent_callback = callback

    def create_layout(self):
        raise NotImplementedError("create layout still not implemented")

    def load_dao(self):
        raise NotImplementedError("load dao still not implemented")

    def save_dao(self):
        raise NotImplementedError("save dao still not implemented")
