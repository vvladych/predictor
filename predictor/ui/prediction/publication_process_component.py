"""
Created on 20.05.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent

from predictor.ui.ui_tools import TreeviewColumn, show_info_dialog

from predictor.model.predictor_model import PublicationDAO, PredictionDAO, PredictionPublisherV
from predictor.model.predictor_model import PredictiontoPublication
from predictor.model.DAO import DAOList


class PublicationProcessComponent(AbstractDataProcessComponent):

    def __init__(self, prediction):
        super(PublicationProcessComponent, self).__init__(PublicationManipulationComponent(prediction, PublicationOverviewComponent(prediction)))


class PublicationManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, prediction, overview_component):
        super(PublicationManipulationComponent, self).__init__(overview_component)
        self.prediction = prediction
        
    def create_layout(self, parent_layout_grid, row):
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label, 0, row, 1, 1)
        
        row += 1

        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label, 0, row, 1, 1)

        self.publication_model = self.populate_publication_combobox_model()
        self.publication_combobox = Gtk.ComboBox.new_with_model_and_entry(self.publication_model)
        self.publication_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.publication_combobox, 1, row, 1, 1)

        row += 1
        
        add_publication_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(add_publication_button, 2, row, 1, 1)
        add_publication_button.connect("clicked", self.add_publication_action)
        
        row += 1
        
        delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        delete_button.connect("clicked", self.delete_action)
        parent_layout_grid.attach(delete_button, 0, row, 1, 1)
        
        row += 1
        
        row = self.overview_component.create_layout(parent_layout_grid, row)
        
        row += 2
        
        return row
        
    def populate_publication_combobox_model(self):
        combobox_model = Gtk.ListStore(str, str)
        publications = DAOList(PublicationDAO)
        publications.load()
        for p in publications:
            combobox_model.append(["%s" % p.uuid, "%s %s %s" % ("Publisher", p.date, p.title)])
        return combobox_model

    def add_publication_action(self, widget):
        publication = PublicationDAO(self.get_active_publication())
        self.prediction.add_publication(publication)
        self.prediction.save()
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()

    def get_active_publication(self):
        tree_iter = self.publication_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.publication_combobox.get_model()
            publication_uuid = model[tree_iter][0]
            return publication_uuid
        else:
            print("please choose a publication!")

    def delete_action(self, widget):
        (model, tree_iter) = self.overview_component.treeview.get_selection().get_selected()
        prediction = PredictionDAO(model[tree_iter][0])
        prediction.load()
        prediction.remove_publication(PublicationDAO(model[tree_iter][5]))
        prediction.save()
        model.remove(tree_iter)
        show_info_dialog("Delete successful")   


class PublicationOverviewComponent(AbstractDataOverviewComponent):
    
    def on_row_select(self, widget, path, data):
        pass

    treecolumns = [TreeviewColumn("prediction_uuid", 0, True),
                   TreeviewColumn("Publisher", 1, False),
                   TreeviewColumn("Title", 2, False, True),
                   TreeviewColumn("Date", 3, False),
                   TreeviewColumn("URL", 4, False),
                   TreeviewColumn("publication_uuid", 5, False),
                   ]
    
    def __init__(self, prediction):
        self.prediction = prediction
        super(PublicationOverviewComponent, self).__init__(PublicationOverviewComponent.treecolumns)

    def populate_model(self):
        self.treemodel.clear()
        prediction_publications = DAOList(PredictionPublisherV)
        prediction_publications.load()
        for p in prediction_publications:
            self.treemodel.append(["%s" % p.uuid, p.commonname, p.title, p.date.strftime('%d.%m.%Y'),p.url, "%s" % p.publication_uuid])
