"""
Created on 03.05.2015

@author: vvladych
"""

from gi.repository import Gtk
from predictor.model.predictor_model import OrganisationDAO
from predictor.model.DAO import DAOList
from predictor.ui.masterdata.masterdata_abstract_window import AbstractAddMask, AbstractListMask, MasterdataAbstractWindow
from predictor.ui.ui_tools import show_error_dialog, show_info_dialog


class OrganisationAddMask(AbstractAddMask):
    def __init__(self, main_window, reset_callback):
        self.common_name_text_entry = Gtk.Entry()
        super(OrganisationAddMask, self).__init__(main_window, None)
        self.create_layout()
        self.show_all()


    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: organisation uuid
        self.add_uuid_row("Organisation UUID", row)

        row += 1
        # Row 1: common name
        self.add_common_name_row("Common Name", row)

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
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")

    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        organisation = OrganisationDAO(None, common_name)
        return organisation


class OrganisationListMask(AbstractListMask):

    treeview_columns = [
                        {"column": "organisation uuid", "hide": False},
                        {"column": "common_name", "hide": False}
                        ]

    def __init__(self, main_window):
        super(OrganisationListMask, self).__init__(OrganisationListMask.treeview_columns, "organisation")
        self.main_window = main_window

    def populate_object_view_table(self):
        self.store.clear()
        organisations = DAOList(OrganisationDAO)
        organisations.load()
        for organisation in organisations:
            self.store.append(["%s" % organisation.uuid, "%s" % organisation.commonname])

    def get_current_object(self):
        (model, tree_iter) = self.tree.get_selection().get_selected()
        if tree_iter is not None:
            organisation_uuid = model.get(tree_iter, 0)[0]
            return OrganisationDAO(organisation_uuid), tree_iter
        else:
            show_info_dialog("Please choose an organisation!")

    def on_menu_item_create_new_masterdataid_click(self, widget):
        organisation_add_dialog = Gtk.Dialog("Organisation Dialog",
                                             None,
                                             0,
                                             (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        organisation_add_dialog.set_default_size(150, 400)
        publisher_add_mask = OrganisationAddMask(self.main_window, None)
        organisation_add_dialog.get_content_area().add(publisher_add_mask)
        organisation_add_dialog.run()
        organisation_add_dialog.destroy()
        self.populate_object_view_table()


class OrganisationWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(OrganisationWindow, self).__init__(main_window, OrganisationListMask(main_window), None)
