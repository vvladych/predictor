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

        self.create_additional_widgets()

        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_dao)
        self.attach_next_to(save_button, None, Gtk.PositionType.BOTTOM, 1, 1)

    def create_additional_widgets(self):
        pass

    def load_dao(self):
        raise NotImplementedError("load dao still not implemented")

    def save_dao(self):
        raise NotImplementedError("save dao still not implemented")
