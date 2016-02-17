
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PublicationDAO, PredictionPublisherV, PredictionDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn


class PredictionPublicationExtTreeview(ExtendedTreeView):

    dao_type = PredictionPublisherV
    columns = [TreeviewColumn("prediction_uuid", 0, True),
               TreeviewColumn("Publisher", 1, False),
               TreeviewColumn("Title", 2, False, True),
               TreeviewColumn("Date", 3, False),
               TreeviewColumn("URL", 4, False),
               TreeviewColumn("publication_uuid", 5, True),
               ]

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
