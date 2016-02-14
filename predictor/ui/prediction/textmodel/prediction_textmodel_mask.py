"""
Created on 20.05.2015

@author: vvladych
"""
from predictor.model.predictor_model import TextmodelDAO, PredictionTextmodelV, PredictionDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.textmodel.textmodel_add_dialog import TextModelAddDialog


class PredictionTextmodelExtTreeview(ExtendedTreeView):

    dao_type = PredictionTextmodelV

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.date,
                                        "%s" % row.short_description,
                                        "%s" % row.textmodel_uuid])

    def on_row_select_callback(self, dao_uuid):
        pass

    def on_menu_item_edit(self, widget):
        print("edit!!!")

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

    treecolumns = [TreeviewColumn("prediction_uuid", 0, True),
                   TreeviewColumn("Date", 1, False),
                   TreeviewColumn("Description", 2, False),
                   TreeviewColumn("textmodel_uuid", 3, True),
                   ]

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


