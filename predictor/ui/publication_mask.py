"""
Created on 20.10.2015

@author: vvladych
"""

from predictor.ui.abstract_mask import AbstractMask
from predictor.model.predictor_model import PublicationDAO
from predictor.ui.publication.publication_overview_window import PublicationOverviewWindow

from predictor.ui.exttreeview import ExtendedTreeView, TreeviewColumn


class PublicationExtTreeview(ExtendedTreeView):

    dao_type = PublicationDAO

    def __init__(self, main_window, columns, start_row=0, rows_per_page=0, on_row_select_callback=None, on_item_new_callback=None):
        super(PublicationExtTreeview, self).__init__(main_window, columns, start_row, rows_per_page, on_row_select_callback)
        self.on_item_new_callback = on_item_new_callback

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.title, "%s" % row.date, "%s" % row.url])

    def on_menu_item_new(self, widget):
        self.on_item_new_callback()


class PublicationMask(AbstractMask):

    dao_type = PublicationDAO
    
    def __init__(self, main_window):
        super(PublicationMask, self).__init__(main_window)

    def create_overview_treeview(self):
        treecolumns = [TreeviewColumn("uuid", 0, True),
                       TreeviewColumn("Title", 1, False),
                       TreeviewColumn("Date", 2, False),
                       TreeviewColumn("URL", 3, False)]
        self.overview_treeview = PublicationExtTreeview(self.main_window, treecolumns, 0, 20, self.on_row_select, self.add_new_publication)

    def on_row_select(self, publication_uuid):
        self.clear_main_middle_pane()
        publication = self.__class__.dao_type(publication_uuid)
        publication.load()
        self.main_middle_pane.pack_start(PublicationOverviewWindow(self,
                                                                   publication,
                                                                   self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()

    def add_new_publication(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PublicationOverviewWindow(self, None, self.overview_treeview.reset_treemodel), False, False, 0)
        self.main_middle_pane.show_all()


