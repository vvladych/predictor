from gi.repository import Gtk

from predictor.model.predictor_model import PublisherDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.ui_tools import show_info_dialog, TextEntryWidget
from predictor.ui.masterdata.mdo_window import MDOWindow


class PublisherExtTreeview(ExtendedTreeView):

    dao_type = PublisherDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("URL", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.url])


class PublisherWindow(MDOWindow):

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
        save_button.connect("clicked", self.save_dao)
        self.attach(save_button, 1, row, 1, 1)

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.commonname)
        self.url_text_entry.set_entry_value(self.dao.url)

    def save_dao(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()
        url = self.url_text_entry.get_entry_value()

        publisher_uuid = None
        if self.dao is not None:
            publisher_uuid = self.dao.uuid

        publisher = PublisherDAO(publisher_uuid,
                                 {"commonname": common_name,
                                  "url": url})
        publisher.save()
        show_info_dialog(None, "Publisher inserted")
        self.dao = publisher
        self.dao.load()
        self.parent_callback()


class PublisherMask(AbstractMask):

    dao_type = PublisherDAO
    exttreeview = PublisherExtTreeview
    overview_window = PublisherWindow

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PublisherWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()