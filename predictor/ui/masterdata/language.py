
from . import *
from predictor.model.predictor_model import LanguageDAO


class LanguageExtTreeview(ExtendedTreeView):

    dao_type = LanguageDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class LanguageWindow(MDOWindow):

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.commonname)

    def save_dao(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        language_uuid = None
        if self.dao is not None:
            language_uuid = self.dao.uuid

        language = LanguageDAO(language_uuid,
                             {"commonname": common_name})
        language.save()
        show_info_dialog(None, "Language  inserted")
        self.dao = language
        self.dao.load()
        self.parent_callback()
        self.load_dao()


class LanguageMask(AbstractMask):

    def __init__(self, main_window, dao=None):
        super(LanguageMask, self).__init__(main_window, dao, LanguageExtTreeview, LanguageWindow, LanguageDAO)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(LanguageWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()