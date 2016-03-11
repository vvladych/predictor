from predictor.model.predictor_model import PublisherDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.masterdata.publisher.overview_window import PublisherOverviewWindow


class PublisherExtTreeview(ExtendedTreeView):

    dao_type = PublisherDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("URL", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.url])


class PublisherMask(AbstractMask):

    dao_type = PublisherDAO
    exttreeview = PublisherExtTreeview
    overview_window = PublisherOverviewWindow
    default_height = 500
    default_width = 200

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PublisherOverviewWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()