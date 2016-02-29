"""
Created on 29.07.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataManipulationComponent, AbstractDataOverviewComponent
from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog, DateWidget, TextViewWidget
import datetime
from predictor.model.predictor_model import TmstatementDAO


class TextmodelStatementManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, textmodel, overview_component):
        super(TextmodelStatementManipulationComponent, self).__init__(overview_component)
        self.textmodel = textmodel
        
    def create_layout(self, parent_layout_grid, row):
        self.parent_layout_grid = parent_layout_grid
        row += 1
        
        statement_label=Gtk.Label("Statement")
        parent_layout_grid.attach(statement_label, 0, row, 1, 1)
        
        self.prediction_model_textview = Gtk.TextView()
        self.prediction_model_textview_widget = TextViewWidget(self.prediction_model_textview)
        
        parent_layout_grid.attach(self.prediction_model_textview_widget, 1, row, 2, 1)

        row += 2
                
        pit_label = Gtk.Label("Choose point-in-time")
        pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(pit_label,0,row,1,1)

        begin_pit_label = Gtk.Label("Begin")
        begin_pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(begin_pit_label,1,row,1,1)

        self.state_begin_date_day_textentry = Gtk.Entry()
        self.state_begin_date_month_textentry = Gtk.Entry()
        self.state_begin_date_year_textentry = Gtk.Entry()

        self.parent_layout_grid.attach(DateWidget(self.state_begin_date_day_textentry,
                                                  self.state_begin_date_month_textentry,
                                                  self.state_begin_date_year_textentry),
                                       2, row, 1, 1)

        row += 1

        end_pit_label=Gtk.Label("End")
        end_pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(end_pit_label, 1, row, 1, 1)

        self.state_end_date_day_textentry = Gtk.Entry()
        self.state_end_date_month_textentry = Gtk.Entry()
        self.state_end_date_year_textentry = Gtk.Entry()

        self.parent_layout_grid.attach(DateWidget(self.state_end_date_day_textentry,
                                                  self.state_end_date_month_textentry,
                                                  self.state_end_date_year_textentry),
                                       2, row, 1, 1)

        row += 2

        add_statement_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(add_statement_button, 0, row, 1, 1)
        add_statement_button.connect("clicked", self.add_statement_action)

        delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        delete_button.connect("clicked", self.delete_action)
        parent_layout_grid.attach(delete_button, 1, row, 1, 1)

        row += 3
        
        row = self.overview_component.create_layout(parent_layout_grid, row)
        
        row += 1

        return row

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
    
    def add_statement_action(self, widget):
        tmstm = TmstatementDAO(None, self.get_textmodel_statement_text(),
                               self.get_point_in_time_begin(), self.get_point_in_time_end())
        tmstm.save()
        self.textmodel.add_tmstatement(tmstm)
        self.textmodel.save()
        show_info_dialog(None, "Add successful")
        self.overview_component.clean_and_populate_model()

    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        tmstm = TmstatementDAO(model.get(tree_iter, 0)[0])
        tmstm.delete()
        model.remove(tree_iter)
        self.textmodel.load()
        show_info_dialog(None, "Delete successful")


class TextmodelStatementOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns = [TreeviewColumn("textmodel_statement_uuid", 0, True),
                   TreeviewColumn("textmodel_uuid", 1, True),
                   TreeviewColumn("State PIT begin", 2, False),
                   TreeviewColumn("State PIT end", 3, False),
                   TreeviewColumn("Statement", 4, False)]

    def __init__(self, textmodel):
        self.textmodel = textmodel
        super(TextmodelStatementOverviewComponent, self).__init__(TextmodelStatementOverviewComponent.treecolumns)

    def create_layout(self, parent_layout_grid, row):
        row += 1
        
        self.treeview.set_size_request(200, 150)
        parent_layout_grid.attach(self.treeview, 0, row, 4, 1)
                
        return row

    def populate_model(self):
        self.treemodel.clear()
        for tm in self.textmodel.TextmodelToTmstatement:
            tmstm = TmstatementDAO(tm.secDAO_uuid)
            tmstm.load()
            self.treemodel.append(["%s" % tmstm.uuid, "%s" % self.textmodel.uuid, "%s" % tmstm.tmbegin, "%s" % tmstm.tmend, tmstm.text])

