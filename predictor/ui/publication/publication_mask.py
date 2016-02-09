"""
Created on 20.10.2015

@author: vvladych
"""

from predictor.model.predictor_model import PublicationDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.publication.publication_overview_window import PublicationOverviewWindow


class PublicationExtTreeview(ExtendedTreeView):

    dao_type = PublicationDAO

    def __init__(self, main_window, columns, start_row=0, rows_per_page=0, on_row_select_callback=None, on_new_callback=None):
        super(PublicationExtTreeview, self).__init__(main_window, columns, start_row, rows_per_page, on_row_select_callback, on_new_callback)

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.title, "%s" % row.date, "%s" % row.url])


class PublicationMask(AbstractMask):

    dao_type = PublicationDAO
    exttreeview = PublicationExtTreeview
    overview_window = PublicationOverviewWindow
    treecolumns = [TreeviewColumn("uuid", 0, True),
                   TreeviewColumn("Title", 1, False),
                   TreeviewColumn("Date", 2, False),
                   TreeviewColumn("URL", 3, False)]

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PublicationOverviewWindow(self, None, self.overview_treeview.reset_treemodel), False, False, 0)
        self.main_middle_pane.show_all()
