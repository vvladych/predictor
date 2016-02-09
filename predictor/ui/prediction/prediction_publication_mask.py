"""
Created on 20.05.2015

@author: vvladych
"""
from predictor.model.predictor_model import PublicationDAO, PredictionPublisherV, PredictionDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.publication_add_dialog import PublicationAddDialog


class PredictionPublicationExtTreeview(ExtendedTreeView):

    dao_type = PredictionPublisherV

    def __init__(self, main_window, columns, start_row=0, rows_per_page=0, on_row_select_callback=None, on_new_callback=None, concrete_dao=None):
        super(PredictionPublicationExtTreeview, self).__init__(main_window, columns, start_row, rows_per_page, self.on_row_select_callback, on_new_callback, concrete_dao)

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.commonname,
                                        "%s" % row.title,
                                        "%s" % row.date,
                                        "%s" % row.url,
                                        "%s" % row.publication_uuid])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionPublicationExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            publication = PublicationDAO(row[5])
            prediction.remove_publication(publication)
            prediction.save()
            self.fill_treeview(0)


class PredictionPublicationMask(AbstractMask):

    dao_type = PredictionPublisherV
    exttreeview = PredictionPublicationExtTreeview

    treecolumns = [TreeviewColumn("prediction_uuid", 0, True),
                   TreeviewColumn("Publisher", 1, False),
                   TreeviewColumn("Title", 2, False, True),
                   TreeviewColumn("Date", 3, False),
                   TreeviewColumn("URL", 4, False),
                   TreeviewColumn("publication_uuid", 5, False),
                   ]

    def __init__(self, main_window, prediction):
        super(PredictionPublicationMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = PublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)


