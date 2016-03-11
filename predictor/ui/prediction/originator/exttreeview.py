
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PredictionOriginatorV, PredictionDAO, OriginatorDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn


class PredictionOriginatorExtTreeview(ExtendedTreeView):

    dao_type = PredictionOriginatorV
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("originator_uuid", 1, True),
               TreeviewColumn("concrete_uuid", 2, True),
               TreeviewColumn("common_name", 3, False, True),
               TreeviewColumn("person", 4, False),
               TreeviewColumn("organisation", 5, False),

               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.originator_uuid,
                                        "%s" % row.concrete_uuid,
                                        "%s" % row.common_name,
                                        "%s" % row.is_person,
                                        "%s" % row.is_organisation
                                        ])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionOriginatorExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            originator = OriginatorDAO(row[1])
            originator.load()
            prediction.remove_originator(originator)
            originator.delete()
            prediction.save()
            self.fill_treeview(0)