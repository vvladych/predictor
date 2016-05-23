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

        placeholder_label = LabelWidget("")
        self.attach(placeholder_label, 0, 0, 1, 1)

        self.uuid_text_entry = TextEntryWidget("UUID", None, False)
        self.attach_next_to(self.uuid_text_entry, placeholder_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.common_name_text_entry = TextEntryWidget("Common name", None, True)
        self.attach_next_to(self.common_name_text_entry, self.uuid_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        add_widgets_grid = Gtk.Grid()
        self.create_additional_widgets(add_widgets_grid)

        self.attach_next_to(add_widgets_grid, self.common_name_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        save_button = ButtonWidget("Save", Gtk.STOCK_SAVE, self.save_dao)
        self.attach_next_to(save_button, add_widgets_grid, Gtk.PositionType.BOTTOM, 1, 1)

    def create_additional_widgets(self, additional_widgets_grid):
        pass

    def load_dao(self):
        raise NotImplementedError("load dao still not implemented")

    def save_dao(self):
        raise NotImplementedError("save dao still not implemented")
