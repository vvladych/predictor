from predictor.model.predictor_model import OrganisationDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.masterdata.organisation.overview_window import OrganisationOverviewWindow


class OrganisationExtTreeview(ExtendedTreeView):

    dao_type = OrganisationDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname])


class OrganisationMask(AbstractMask):

    dao_type = OrganisationDAO
    exttreeview = OrganisationExtTreeview
    overview_window = OrganisationOverviewWindow
    default_height = 500
    default_width = 200

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(OrganisationOverviewWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()