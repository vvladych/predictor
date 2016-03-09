from predictor.model.predictor_model import PersonDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.masterdata.person.overview_window import PersonOverviewWindow


class PersonExtTreeview(ExtendedTreeView):

    dao_type = PersonDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("Birth date", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.common_name, "%s" % row.birth_date])


class PersonMask(AbstractMask):

    dao_type = PersonDAO
    exttreeview = PersonExtTreeview
    overview_window = PersonOverviewWindow
    default_height = 500
    default_width = 200

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PersonOverviewWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()