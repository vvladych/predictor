from gi.repository import Gtk
from predictor.ui.ui_tools import show_info_dialog, TextEntryWidget
from predictor.model.predictor_model import PublisherDAO


class PublisherOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, publisher=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.publisher = publisher
        self.create_layout()
        if publisher is not None:
            self.publisher.load()
            self.load_publisher()
        self.parent_callback = callback

    def create_layout(self):

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: uuid
        self.uuid_text_entry = TextEntryWidget("UUID", None, False)
        self.attach(self.uuid_text_entry, 0, row, 2, 1)

        row += 1
        # Row 1: common name
        self.common_name_text_entry = TextEntryWidget("Common name", None, True)
        self.attach(self.common_name_text_entry, 0, row, 2, 1)

        row += 1

        # Row 2: common name
        self.url_text_entry = TextEntryWidget("URL", None, True)
        self.attach(self.url_text_entry, 0, row, 2, 1)

        row += 1

        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_publisher)
        self.attach(save_button, 1, row, 1, 1)

    def load_publisher(self):
        self.uuid_text_entry.set_entry_value(self.publisher.uuid)
        self.common_name_text_entry.set_entry_value(self.publisher.commonname)
        self.url_text_entry.set_entry_value(self.publisher.url)

    def save_publisher(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()
        url = self.url_text_entry.get_entry_value()

        publisher_uuid = None
        if self.publisher is not None:
            publisher_uuid = self.publisher.uuid

        publisher = PublisherDAO(publisher_uuid,
                                 {"commonname": common_name,
                                  "url": url})
        publisher.save()
        show_info_dialog(None, "Publisher inserted")
        self.publisher = publisher
        self.publisher.load()
        self.parent_callback()