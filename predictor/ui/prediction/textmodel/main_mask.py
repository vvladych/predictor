"""
Created on 20.05.2015

@author: vvladych
"""
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import TextmodelDAO, PredictionTextmodelV, PredictionDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.prediction.textmodel.add_dialog import TextModelAddDialog
from predictor.ui.prediction.textmodel.statement.add_dialog import TextmodelStatementAddDialog


class PredictionTextmodelExtTreeview(ExtendedTreeView):

    dao_type = PredictionTextmodelV
    columns = [TreeviewColumn("prediction_uuid", 0, True),
               TreeviewColumn("Date", 1, False),
               TreeviewColumn("Description", 2, False),
               TreeviewColumn("textmodel_uuid", 3, True),
               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.date,
                                        "%s" % row.short_description,
                                        "%s" % row.textmodel_uuid])

    def on_row_select_callback(self, dao_uuid):
        pass

    def on_menu_item_edit(self, widget):
        textmodel_row = self.get_selected_row()
        tm = TextmodelDAO(textmodel_row[3])
        tm.load()
        dialog = TextmodelStatementAddDialog(self, tm)
        dialog.run()
        dialog.destroy()

        self.fill_treeview(0)

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionTextmodelExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            textmodel = TextmodelDAO(row[3])
            prediction.remove_publication(textmodel)
            prediction.save()
            self.fill_treeview(0)


class PredictionTextmodelMask(AbstractMask):

    dao_type = PredictionTextmodelV
    exttreeview = PredictionTextmodelExtTreeview
    default_height = 80
    default_width = 400

    def __init__(self, main_window, prediction):
        super(PredictionTextmodelMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = TextModelAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)


