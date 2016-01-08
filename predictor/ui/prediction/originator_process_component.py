"""
Created on 19.05.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent

from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog

#from forecastmgmt.model.person import Person
#from forecastmgmt.model.organisation import Organisation
#from forecastmgmt.model.originator import Originator
#from forecastmgmt.model.forecast_originator import ForecastOriginator
#from forecastmgmt.model.originator_person import OriginatorPerson
#from forecastmgmt.model.originator_organisation import OriginatorOrganisation
#from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class OriginatorProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(OriginatorProcessComponent, self).__init__(OriginatorManipulationComponent(forecast, OriginatorOverviewComponent(forecast)))
        
        
class OriginatorManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(OriginatorManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        
        originator_label = Gtk.Label("Originator")
        originator_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(originator_label,0,row,1,1)
        
        row+=1

        person_originator_label = Gtk.Label("Person")
        person_originator_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(person_originator_label,0,row,1,1)

        
        self.person_combobox_model=self.populate_person_combobox_model()
        self.person_combobox=Gtk.ComboBox.new_with_model_and_entry(self.person_combobox_model)
        self.person_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.person_combobox,1,row,1,1)
        
        self.add_person_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_person_button,2,row,1,1)
        self.add_person_button.connect("clicked", self.add_person_action)

        row += 1

        organisation_originator_label = Gtk.Label("Organisation")
        organisation_originator_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(organisation_originator_label,0,row,1,1)

        
        self.organisation_combobox_model=self.populate_organisation_combobox_model()
        self.organisation_combobox=Gtk.ComboBox.new_with_model_and_entry(self.organisation_combobox_model)
        self.organisation_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.organisation_combobox,1,row,1,1)
        
        self.add_organisation_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_organisation_button,2,row,1,1)
        self.add_organisation_button.connect("clicked", self.add_organisation_action)

        row += 1
        
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,0,row,1,1)

        row += 1
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
        row += 1
        
        return row


    def populate_person_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        person_list=Person().get_all()
        for p in person_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model

    def populate_organisation_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        organisation_list=Organisation().get_all()
        for p in organisation_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model

    
    def add_person_action(self, widget):
        # get person sid
        (current_person_sid,current_person_common_name)=self.get_active_person()
        # insert originator
        originator=Originator(common_name=current_person_common_name)
        originator.insert()
        # insert forecast_originator
        forecast_originator = ForecastOriginator(forecast_sid=self.forecast.sid, originator_sid=originator.sid)
        forecast_originator.insert()
        # insert originator_person
        originator_person=OriginatorPerson(originator_sid=originator.sid,person_sid=current_person_sid)
        originator_person.insert()
        
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
        
        
    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        (originator_sid)=model.get(tree_iter, 0)
        Originator(originator_sid).delete()
        model.remove(tree_iter)   
        show_info_dialog("Delete successful")   
        
        
    def get_active_person(self):
        tree_iter = self.person_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.person_combobox.get_model()
            person_sid = model[tree_iter][:2]
            return person_sid
        else:
            print("please choose a person!")



    def add_organisation_action(self, widget):
        # get organisation sid
        (current_organisation_sid,current_organisation_common_name)=self.get_active_organisation()
        # insert originator
        originator=Originator(common_name=current_organisation_common_name)
        originator.insert()
        # insert forecast_originator
        forecast_originator = ForecastOriginator(forecast_sid=self.forecast.sid, originator_sid=originator.sid)
        forecast_originator.insert()
        # insert originator_person
        originator_organisation=OriginatorOrganisation(originator_sid=originator.sid,organisation_sid=current_organisation_sid)
        originator_organisation.insert()
        
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
    
        
    def get_active_organisation(self):
        tree_iter = self.organisation_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.organisation_combobox.get_model()
            organisation_sid = model[tree_iter][:2]
            return organisation_sid
        else:
            print("please choose an organisation!")


        
        
class OriginatorOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("originator_sid", 0, True), TreeviewColumn("person_sid", 1, True), 
                TreeviewColumn("organisation_sid", 2, True), TreeviewColumn("Typ", 3, False),
                TreeviewColumn("Common name", 4, False)]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(OriginatorOverviewComponent, self).__init__(OriginatorOverviewComponent.treecolumns)
        


    
    
    def populate_model(self):
        self.treemodel.clear()                        
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,self.forecast.sid,)
        cur.execute("""SELECT 
                        fc_person.sid as sid, fc_person.common_name, fc_originator_person.originator_sid,'person' as origin_type 
                        FROM 
                        fc_forecast_originator, fc_originator_person, fc_person 
                        WHERE
                        fc_forecast_originator.forecast_sid=%s AND 
                        fc_forecast_originator.originator_sid=fc_originator_person.originator_sid AND
                        fc_originator_person.person_sid=fc_person.sid
                        UNION
                        SELECT 
                        fc_organization.sid as sid, fc_organization.common_name, fc_originator_organisation.originator_sid,'organisation'  as origin_type  
                        FROM 
                        fc_forecast_originator, fc_originator_organisation, fc_organization
                        WHERE
                        fc_forecast_originator.forecast_sid=%s AND 
                        fc_forecast_originator.originator_sid=fc_originator_organisation.originator_sid AND
                        fc_originator_organisation.organisation_sid=fc_organization.sid
                        """,data)
        for p in cur.fetchall():
            if p.origin_type=='person':
                self.treemodel.append([ "%s" % p.originator_sid, "%s" % p.sid, None, p.origin_type, p.common_name])
            elif p.origin_type=='organisation':
                self.treemodel.append([ "%s" % p.originator_sid, None,"%s" % p.sid, p.origin_type, p.common_name])
            else:
                raise Exception("unknown type: %s, expected person or organisation" % p.origin_type)
        cur.close()
        
  
        
