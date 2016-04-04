from . import *
from predictor.model.predictor_model import OrganisationDAO, CountryDAO


class CountryComboBoxWidget(DAOComboBoxWidget):
    dao = CountryDAO

    def add_entry(self, country):
        self.model.append(["%s" % country.uuid, "%s" % country.commonname])


class OrganisationExtTreeview(ExtendedTreeView):

    dao_type = OrganisationDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class OrganisationWindow(MDOWindow):

    def create_layout(self):

        placeholder_label = LabelWidget("")
        self.attach(placeholder_label, 0, 0, 1, 1)

        self.uuid_text_entry = TextEntryWidget("UUID", None, False)
        self.attach_next_to(self.uuid_text_entry, placeholder_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.common_name_text_entry = TextEntryWidget("Common name", None, True)
        self.attach_next_to(self.common_name_text_entry, self.uuid_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.country_combobox = CountryComboBoxWidget("Country")
        self.attach_next_to(self.country_combobox, self.common_name_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_dao)
        self.attach_next_to(save_button, self.country_combobox, Gtk.PositionType.BOTTOM, 1, 1)

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.commonname)
        country = self.dao.get_country()
        if country is not None:
            self.country_combobox.set_active_entry(country.uuid)

    def save_dao(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        organisation_uuid = None
        if self.dao is not None:
            organisation_uuid = self.dao.uuid

        organisation = OrganisationDAO(organisation_uuid,
                                       {"commonname": common_name})
        organisation.save()

        country_uuid = self.country_combobox.get_active_entry()
        country = CountryDAO(country_uuid)
        organisation.add_country(country)

        organisation.save()

        show_info_dialog(self.main_window, "Organisation inserted")
        self.dao = organisation
        self.dao.load()
        self.parent_callback()


class OrganisationMask(AbstractMask):

    dao_type = OrganisationDAO
    exttreeview = OrganisationExtTreeview
    overview_window = OrganisationWindow

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(OrganisationWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()