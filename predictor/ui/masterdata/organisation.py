from gi.repository import Gtk

from predictor.model.predictor_model import OrganisationDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.ui_tools import show_info_dialog, TextEntryWidget


class OrganisationExtTreeview(ExtendedTreeView):

    dao_type = OrganisationDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class OrganisationWindow(Gtk.Grid):

    def __init__(self, main_window, organisation=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.organisation = organisation
        self.create_layout()
        if organisation is not None:
            self.organisation.load()
            self.load_organisation()
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

        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_organisation)
        self.attach(save_button, 1, row, 1, 1)

    def load_organisation(self):
        self.uuid_text_entry.set_entry_value(self.organisation.uuid)
        self.common_name_text_entry.set_entry_value(self.organisation.commonname)

    def save_organisation(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        organisation_uuid = None
        if self.organisation is not None:
            organisation_uuid = self.organisation.uuid

        organisation = OrganisationDAO(organisation_uuid,
                                       {"commonname": common_name})
        organisation.save()
        show_info_dialog(None, "Organisation inserted")
        self.organisation = organisation
        self.organisation.load()
        self.parent_callback()


class OrganisationMask(AbstractMask):

    dao_type = OrganisationDAO
    exttreeview = OrganisationExtTreeview
    overview_window = OrganisationWindow
    default_height = 500
    default_width = 200

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(OrganisationWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()