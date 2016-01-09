'''
Created on 29.07.2015

@author: vvladych
'''
from gi.repository import Gtk
from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent
from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog, DateWidget, TextViewWidget
import datetime
from forecastmgmt.model.fc_textmodel_statement import FCTextmodelStatement


class TextmodelStatementProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, textmodel):
        super(TextmodelStatementProcessComponent, self).__init__(TextmodelStatementManipulationComponent(textmodel, TextmodelStatementOverviewComponent(textmodel)))
        
        
class TextmodelStatementManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, textmodel, overview_component):
        super(TextmodelStatementManipulationComponent, self).__init__(overview_component)
        self.textmodel=textmodel
        
    def create_layout(self, parent_layout_grid, row):
        self.parent_layout_grid=parent_layout_grid
        row+=1
        
        statement_label=Gtk.Label("Statement")
        parent_layout_grid.attach(statement_label,0,row,1,1)
        
        self.forecast_model_textview=Gtk.TextView()
        self.forecast_model_textview_widget=TextViewWidget(self.forecast_model_textview)
        
        parent_layout_grid.attach(self.forecast_model_textview_widget,1,row,2,1)
        
        
        row+=2
                
        pit_label=Gtk.Label("Choose point-in-time")
        pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(pit_label,0,row,1,1)

        begin_pit_label=Gtk.Label("Begin")
        begin_pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(begin_pit_label,1,row,1,1)

        
        self.state_begin_date_day_textentry=Gtk.Entry()
        self.state_begin_date_month_textentry=Gtk.Entry()
        self.state_begin_date_year_textentry=Gtk.Entry()
        
        self.parent_layout_grid.attach(DateWidget(self.state_begin_date_day_textentry, self.state_begin_date_month_textentry, self.state_begin_date_year_textentry),2,row,1,1)

        row+=1
        
        end_pit_label=Gtk.Label("End")
        end_pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(end_pit_label,1,row,1,1)

        
        self.state_end_date_day_textentry=Gtk.Entry()
        self.state_end_date_month_textentry=Gtk.Entry()
        self.state_end_date_year_textentry=Gtk.Entry()
        
        self.parent_layout_grid.attach(DateWidget(self.state_end_date_day_textentry, self.state_end_date_month_textentry, self.state_end_date_year_textentry),2,row,1,1)

                
        row+=2
        
        self.add_statement_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_statement_button,0,row,1,1)
        self.add_statement_button.connect("clicked", self.add_statement_action)
                
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,1,row,1,1)

        row+=3
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
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
        return self.forecast_model_textview_widget.get_textview_text()
    
    def add_statement_action(self, widget):
        FCTextmodelStatement(None,None,self.get_textmodel_statement_text(),self.get_point_in_time_begin(),self.get_point_in_time_end(), self.textmodel).insert()
        # 
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
        
        
    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        (textmodel_statement_sid)=model.get(tree_iter, 0)
        FCTextmodelStatement(textmodel_statement_sid).delete()
        model.remove(tree_iter)   
        show_info_dialog("Delete successful")         
        
class TextmodelStatementOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("textmodel_statement_sid", 0, True), TreeviewColumn("textmodel_statement_uuid", 1, True), 
                TreeviewColumn("fc_textmodel_sid", 2, True), 
                TreeviewColumn("State PIT begin", 3, False),  TreeviewColumn("State PIT end", 4, False),
                TreeviewColumn("Statement",5,False)]

    
    def __init__(self, textmodel):
        self.textmodel=textmodel
        super(TextmodelStatementOverviewComponent, self).__init__(TextmodelStatementOverviewComponent.treecolumns)
        

    def create_layout(self, parent_layout_grid, row):
        row += 1
        
        self.treeview.set_size_request(200,150)
        parent_layout_grid.attach(self.treeview,0,row,4,1)
                
        return row

        
    def populate_model(self):
        self.treemodel.clear()
        textmodel_statements=FCTextmodelStatement().get_all_for_foreign_key(self.textmodel)
        for p in textmodel_statements:
            self.treemodel.append(["%s" % p.sid, "%s" % p.uuid, "%s" % self.textmodel, "%s" % p.point_in_time_begin, "%s" % p.point_in_time_end, p.statement_text])

        