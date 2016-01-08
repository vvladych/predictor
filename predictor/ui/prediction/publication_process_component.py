"""
Created on 20.05.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent

from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog

from predictor.model.predictor_model import PublicationDAO
from predictor.model.predictor_model import PredictiontoPublication


class PublicationProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(PublicationProcessComponent, self).__init__(PublicationManipulationComponent(forecast, PublicationOverviewComponent(forecast)))
        
        
class PublicationManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(PublicationManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label,0,row,1,1)
        
        row+=1

        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label,0,row,1,1)

        self.publication_model=self.populate_publication_combobox_model()
        self.publication_combobox=Gtk.ComboBox.new_with_model_and_entry(self.publication_model)
        self.publication_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.publication_combobox,1,row,1,1)
        
        
        row+=1
        
        self.add_publication_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_publication_button,2,row,1,1)
        self.add_publication_button.connect("clicked", self.add_publication_action)
        
        row+=1
        
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,0,row,1,1)
        
        row+=1
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
        row+=2
        
        return row
        
    def populate_publication_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        publication_list=Publication().get_all()
        for p in publication_list:
            combobox_model.append(["%s" % p.sid, "%s %s %s" % (p.publisher.common_name, p.publishing_date.strftime('%d.%m.%Y'), p.title)])
        return combobox_model
    
    
    def add_publication_action(self, widget):
        (publication_sid,publication_info)=self.get_active_publication()
        forecast_publication = ForecastPublication(forecast_sid=self.forecast.sid, publication_sid=publication_sid)
        forecast_publication.insert()
        

        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
        

    def get_active_publication(self):
        tree_iter = self.publication_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.publication_combobox.get_model()
            publication_sid = model[tree_iter][:2]
            return publication_sid
        else:
            print("please choose a publication!")

    
    
    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        ForecastPublication(model[tree_iter][5]).delete()
        model.remove(tree_iter)
        show_info_dialog("Delete successful")   
        
    
        

class PublicationOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("publication_sid", 0, True), 
                 TreeviewColumn("Publisher", 1, False), TreeviewColumn("Title", 2, False, True),
                 TreeviewColumn("Date", 3, False), TreeviewColumn("URL", 4, False),
                 TreeviewColumn("forecast_publication_sid", 5, True),
                 ]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(PublicationOverviewComponent, self).__init__(PublicationOverviewComponent.treecolumns)
        

    def populate_model(self):
        self.treemodel.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,)
        cur.execute("""SELECT 
                        fc_publication.sid as publication_sid, 
                        fc_publisher.publisher_common_name, fc_publication.title, fc_publication.publishing_date,
                         fc_publication.publication_url, fc_forecast_publication.sid  as forecast_publication_sid  
                        FROM 
                        fc_forecast_publication, fc_publication, fc_publisher 
                        WHERE
                        fc_forecast_publication.forecast_sid=%s AND
                        fc_forecast_publication.publication_sid=fc_publication.sid AND  
                        fc_publication.publisher_sid=fc_publisher.sid 
                        """,data)
        for p in cur.fetchall():
            self.treemodel.append([ "%s" % p.publication_sid, p.publisher_common_name, p.title, p.publishing_date.strftime('%d.%m.%Y'),p.publication_url, "%s" % p.forecast_publication_sid])
        cur.close()
        
        

        
        
        