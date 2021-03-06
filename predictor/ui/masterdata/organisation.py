from . import *
from predictor.model.predictor_model import OrganisationDAO, CountryDAO


class OrganisationExtTreeview(ExtendedTreeView):

    dao_type = OrganisationDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class OrganisationWindow(MDOWindow):

    def create_additional_widgets(self, additional_widgets_grid):
        self.country_combobox = ComboBoxWidget("Country",
                                               DAOList(CountryDAO, True),
                                               lambda x: ["%s" % x.uuid, "%s" % x.commonname])
        additional_widgets_grid.attach(self.country_combobox, 0, 0, 1, 1)

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

    def __init__(self, main_window, dao=None):
        super(OrganisationMask, self).__init__(main_window, dao, OrganisationExtTreeview, OrganisationWindow, OrganisationDAO)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.attach(OrganisationWindow(self.main_window, None, self.overview_treeview.reset_treemodel), 0, 0, 1, 1)
        self.main_middle_pane.show_all()

