from . import *

from predictor.model.predictor_model import PublisherDAO


class PublisherExtTreeview(ExtendedTreeView):

    dao_type = PublisherDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("URL", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.url])


class PublisherWindow(MDOWindow):

    def create_layout(self):

        placeholder_label = LabelWidget("")
        self.attach(placeholder_label, 0, 0, 1, 1)

        self.uuid_text_entry = TextEntryWidget("UUID", None, False)
        self.attach_next_to(self.uuid_text_entry, placeholder_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.common_name_text_entry = TextEntryWidget("Common name", None, True)
        self.attach_next_to(self.common_name_text_entry, self.uuid_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.url_text_entry = TextEntryWidget("URL", None, True)
        self.attach_next_to(self.url_text_entry, self.common_name_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_dao)
        self.attach_next_to(save_button, self.url_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

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
        self.main_middle_pane.pack_start(PublisherWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()