'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from predictor.ui.masterdata.masterdata_abstract_window import MasterdataAbstractWindow, AbstractAddMask, AbstractListMask
from predictor.model.predictor_model import PublisherDAO
from predictor.model.DAO import DAOList

class PublisherAddMask(AbstractAddMask):
    def __init__(self, main_window, reset_callback):
        super(PublisherAddMask, self).__init__(main_window, reset_callback)

    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: publisher uuid
        self.add_uuid_row("Publisher UUID", row)

        row += 1

        self.add_common_name_row("Common name", row)

        row += 1

        url_label = Gtk.Label("URL")
        url_label.set_justify(Gtk.Justification.LEFT)
        self.attach(url_label, 0, row, 1, 1)
        self.url_text_entry = Gtk.Entry()
        self.attach(self.url_text_entry, 1, row, 1, 1)

        row += 1

        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button, 1, row, 1, 1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button, 2, row, 1, 1)

    def fill_mask_from_current_object(self):
        if self.current_object is not None:
            self.uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
            if self.current_object.url is not None:
                self.url_text_entry.set_text(self.current_object.url)
            else:
                self.url_text_entry.set_text("")
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
            self.url_text_entry.set_text("")

    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        publisher_url = self.url_text_entry.get_text()
        publisher_uuid = None
        if self.current_object is not None:
            publisher_uuid = self.current_object.uuid

        publisher = PublisherDAO(publisher_uuid,common_name,publisher_url)
        return publisher


class PublisherListMask(AbstractListMask):

    treeview_columns=[
                      {"column": "common_name", "hide": False},
                      {"column": "URL", "hide": False},
                      {"column": "publisher uuid", "hide": False}
                      ]

    def __init__(self):
        super(PublisherListMask, self).__init__(PublisherListMask.treeview_columns)

    def populate_object_view_table(self):
        self.store.clear()
        publishers = DAOList(PublisherDAO)
        publishers.load()
        for publisher in publishers:
            self.store.append(["%s" % publisher.commonname, "%s" % publisher.url, "%s" % publisher.uuid])

    def delete_object(self):
        (publisher, tree_iter) = self.get_current_object()
        publisher.delete()
        self.store.remove(tree_iter)

    def get_current_object(self):
        (model, tree_iter) = self.tree.get_selection().get_selected()
        publisher_uuid = model.get(tree_iter, 2)[0]
        return PublisherDAO(publisher_uuid), tree_iter


class PublisherWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PublisherWindow, self).__init__(main_window, PublisherListMask(), PublisherAddMask(main_window, self.add_working_area))
