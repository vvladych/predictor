from . import *


class TextmodelStatementExtTreeview(ExtendedTreeView):

    dao_type = PredictionStatementV
    columns = [TreeviewColumn("prediction_uuid", 0, True),
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
            prediction = PredictionDAO(row[0])
            prediction.load()
            tmstatement = TmstatementDAO(row[1])
            prediction.remove_tmstatement(tmstatement)
            prediction.save()
            self.fill_treeview(0)


class TextmodelStatementAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self, "Model Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        layout_grid = Gtk.Grid()

        layout_grid.set_column_spacing(5)
        layout_grid.set_row_spacing(3)
        
        self.prediction = prediction
        self.main_window = parent

        self.overview_component = TextmodelStatementExtTreeview(self,
                                                                 0,
                                                                 20,
                                                                 self.load_tmstatement,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.prediction)

        box = self.get_content_area()

        box.add(layout_grid)

        stm_label = LabelWidget("Statement(s)")
        layout_grid.attach(stm_label, 0, 0, 1, 1)

        pit_label = LabelWidget("Point-in-time")
        layout_grid.attach_next_to(pit_label, stm_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.state_begin_date_widget = DateWidget("Begin")
        layout_grid.attach_next_to(self.state_begin_date_widget, pit_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.state_end_date_widget = DateWidget("End")
        layout_grid.attach_next_to(self.state_end_date_widget, self.state_begin_date_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.prediction_model_textview_widget = TextViewWidget(None, None, "Statement")
        layout_grid.attach_next_to(self.prediction_model_textview_widget, self.state_end_date_widget, Gtk.PositionType.BOTTOM, 1, 1)

        add_statement_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_statement_button.connect("clicked", self.add_statement_action)
        layout_grid.attach_next_to(add_statement_button, self.prediction_model_textview_widget, Gtk.PositionType.BOTTOM, 1, 1)

        layout_grid.attach_next_to(self.overview_component, add_statement_button, Gtk.PositionType.BOTTOM, 1, 1)

        self.show_all()

    @transactional
    def add_statement_action(self, widget):
        tmstm = TmstatementDAO(None,
                               {"text": self.prediction_model_textview_widget.get_textview_text(),
                               "tmbegin": self.state_begin_date_widget.get_date(),
                               "tmend": self.state_end_date_widget.get_date()})
        tmstm.save()
        self.prediction.add_tmstatement(tmstm)
        self.prediction.save()
        show_info_dialog(self.main_window, "Add successful")
        self.overview_component.fill_treeview(0)

    def noop(self, widget):
        pass

    def load_tmstatement(self, widget):
        row = self.overview_component.get_selected_row()
        self.state_begin_date_widget.set_date_from_string(row[2])
        self.state_end_date_widget.set_date_from_string(row[3])
        self.prediction_model_textview_widget.set_text(row[4])
