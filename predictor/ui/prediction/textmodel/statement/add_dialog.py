"""
Created on 29.07.2015

@author: vvladych
"""
from gi.repository import Gtk
from predictor.ui.ui_tools import TextViewWidget, DateWidget, show_info_dialog
from predictor.ui.prediction.textmodel.statement.exttreeview import TextmodelStatementExtTreeview
import datetime
from predictor.model.predictor_model import TmstatementDAO
from predictor.helpers.transaction_broker import transactional


class TextmodelStatementAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, model):
        Gtk.Dialog.__init__(self, "Model Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        layout_grid = Gtk.Grid()
        
        self.textmodel = model
        self.main_window = parent

        self.overview_component = TextmodelStatementExtTreeview(self,
                                                                 0,
                                                                 20,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.noop,
                                                                 self.textmodel)

        box = self.get_content_area()

        box.add(layout_grid)

        row = 0
        label = Gtk.Label("prediction model(s)")
        layout_grid.attach(label, 0, row, 1, 1)

        row += 3

        statement_label=Gtk.Label("Statement")
        layout_grid.attach(statement_label, 0, row, 1, 1)

        self.prediction_model_textview = Gtk.TextView()
        self.prediction_model_textview_widget = TextViewWidget(self.prediction_model_textview)

        layout_grid.attach(self.prediction_model_textview_widget, 1, row, 2, 1)

        row += 2

        pit_label = Gtk.Label("Choose point-in-time")
        pit_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(pit_label,0,row,1,1)

        begin_pit_label = Gtk.Label("Begin")
        begin_pit_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(begin_pit_label,1,row,1,1)

        self.state_begin_date_day_textentry = Gtk.Entry()
        self.state_begin_date_month_textentry = Gtk.Entry()
        self.state_begin_date_year_textentry = Gtk.Entry()

        layout_grid.attach(DateWidget(self.state_begin_date_day_textentry,
                                                  self.state_begin_date_month_textentry,
                                                  self.state_begin_date_year_textentry),
                                                  2, row, 1, 1)

        row += 1

        end_pit_label=Gtk.Label("End")
        end_pit_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(end_pit_label, 1, row, 1, 1)

        self.state_end_date_day_textentry = Gtk.Entry()
        self.state_end_date_month_textentry = Gtk.Entry()
        self.state_end_date_year_textentry = Gtk.Entry()

        layout_grid.attach(DateWidget(self.state_end_date_day_textentry,
                                                  self.state_end_date_month_textentry,
                                                  self.state_end_date_year_textentry),
                                                  2, row, 1, 1)

        row += 2

        add_statement_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        layout_grid.attach(add_statement_button, 0, row, 1, 1)
        add_statement_button.connect("clicked", self.add_statement_action)

        delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        delete_button.connect("clicked", self.delete_action)
        layout_grid.attach(delete_button, 1, row, 1, 1)

        row += 3

        layout_grid.attach(self.overview_component, 0, row, 3, 1)

        row += 2
        layout_grid.attach(Gtk.Label(""), 0, row, 3, 1)

        self.show_all()

    def get_point_in_time_begin(self):
        return datetime.date(int(self.state_begin_date_year_textentry.get_text()),
                             int(self.state_begin_date_month_textentry.get_text()),
                             int(self.state_begin_date_day_textentry.get_text()))

    def get_point_in_time_end(self):
        return datetime.date(int(self.state_end_date_year_textentry.get_text()),
                             int(self.state_end_date_month_textentry.get_text()),
                             int(self.state_end_date_day_textentry.get_text()))

    def get_textmodel_statement_text(self):
        return self.prediction_model_textview_widget.get_textview_text()

    @transactional
    def add_statement_action(self, widget):
        tmstm = TmstatementDAO(None, self.get_textmodel_statement_text(),
                               self.get_point_in_time_begin(), self.get_point_in_time_end())
        tmstm.save()
        self.textmodel.add_tmstatement(tmstm)
        self.textmodel.save()
        show_info_dialog(None, "Add successful")
        self.overview_component.fill_treeview(0)

    def noop(self, widget):
        pass

    def delete_action(self, widget):
        pass