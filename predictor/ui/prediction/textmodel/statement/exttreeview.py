
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import TextmodelDAO, TextmodelStatementV, TmstatementDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn


class TextmodelStatementExtTreeview(ExtendedTreeView):

    dao_type = TextmodelStatementV
    columns = [TreeviewColumn("textmodel_uuid", 0, True),
               TreeviewColumn("tmstatement_uuid", 1, True),
               TreeviewColumn("State PIT begin", 2, False),
               TreeviewColumn("State PIT end", 3, False),
               TreeviewColumn("Statement", 4, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.tmstatement_uuid,
                                        "%s" % row.tmbegin,
                                        "%s" % row.tmend,
                                        "%s" % row.text])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(TextmodelStatementExtTreeview, self).get_selected_row()
        if row is not None:
            textmodel = TextmodelDAO(row[0])
            textmodel.load()
            tmstatement = TmstatementDAO(row[1])
            textmodel.remove_tmstatement(tmstatement)
            textmodel.save()
            self.fill_treeview(0)
