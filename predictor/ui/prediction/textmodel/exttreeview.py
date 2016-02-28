from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import TextmodelDAO, PredictionTextmodelV, PredictionDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn


class PredictionTextmodelExtTreeview(ExtendedTreeView):

    dao_type = PredictionTextmodelV
    columns = [TreeviewColumn("prediction_uuid", 0, True),
               TreeviewColumn("textmodel_uuid", 1, True),
               TreeviewColumn("Date", 2, False),
               TreeviewColumn("Short desc.", 3, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.textmodel_uuid,
                                        "%s" % row.date,
                                        "%s" % row.short_description])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionTextmodelExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            textmodel = TextmodelDAO(row[1])
            prediction.remove_textmodel(textmodel)
            prediction.save()
            self.fill_treeview(0)