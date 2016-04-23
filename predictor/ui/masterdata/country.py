
from . import *
from predictor.model.predictor_model import CountryDAO


class CountryExtTreeview(ExtendedTreeView):

    dao_type = CountryDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class CountryWindow(MDOWindow):

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.commonname)

    def save_dao(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        country_uuid = None
        if self.dao is not None:
            country_uuid = self.dao.uuid

        country = CountryDAO(country_uuid,
                             {"commonname": common_name})
        country.save()
        show_info_dialog(None, "Country inserted")
        self.dao = country
        self.dao.load()
        self.parent_callback()
        self.load_dao()


class CountryMask(AbstractMask):

    def __init__(self, main_window, dao=None):
        super(CountryMask, self).__init__(main_window, dao, CountryExtTreeview, CountryWindow, CountryDAO)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(CountryWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()