"""
Created on 20.05.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent

from predictor.ui.ui_tools import show_info_dialog

from predictor.model.predictor_model import PublicationDAO, PredictionPublisherV, PredictionDAO
from predictor.model.DAO import DAOList
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.helpers.transaction_broker import transactional


class PredictionPublicationExtTreeview(ExtendedTreeView):

    dao_type = PredictionPublisherV

    def __init__(self, main_window, columns, start_row=0, rows_per_page=0, on_row_select_callback=None, on_new_callback=None, concrete_dao=None):
        super(PredictionPublicationExtTreeview, self).__init__(main_window, columns, start_row, rows_per_page, self.on_row_select_callback, on_new_callback, concrete_dao)

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.commonname,
                                        "%s" % row.title,
                                        "%s" % row.date,
                                        "%s" % row.url,
                                        "%s" % row.publication_uuid])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionPublicationExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            publication = PublicationDAO(row[5])
            prediction.remove_publication(publication)
            prediction.save()
            self.fill_treeview(0)


class PredictionPublicationMask(AbstractMask):

    dao_type = PredictionPublisherV
    exttreeview = PredictionPublicationExtTreeview

    treecolumns = [TreeviewColumn("prediction_uuid", 0, True),
                   TreeviewColumn("Publisher", 1, False),
                   TreeviewColumn("Title", 2, False, True),
                   TreeviewColumn("Date", 3, False),
                   TreeviewColumn("URL", 4, False),
                   TreeviewColumn("publication_uuid", 5, False),
                   ]

    def __init__(self, main_window, prediction):
        super(PredictionPublicationMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = PublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)


class PublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            None,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 400)
        self.layout_grid = Gtk.Grid()

        self.process_component = AbstractDataProcessComponent(PublicationManipulationComponent(prediction, PublicationOverviewComponent(prediction)))

        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()

        box.add(self.layout_grid)

        row = 0
        label = Gtk.Label("Prediction's publication(s)")
        self.layout_grid.attach(label, 0, row, 1, 1)

        row += 1
        row = self.process_component.create_layout(self.layout_grid, row)

        return row


class PublicationManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, prediction, overview_component):
        super(PublicationManipulationComponent, self).__init__(overview_component)
        self.prediction = prediction
        
    def create_layout(self, parent_layout_grid, row):
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label, 0, row, 1, 1)
        
        row += 1

        publisher_label = Gtk.Label("Publisher")
        publisher_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publisher_label, 0, row, 1, 1)

        self.publication_model = self.populate_publication_combobox_model()
        self.publication_combobox = Gtk.ComboBox.new_with_model_and_entry(self.publication_model)
        self.publication_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.publication_combobox, 1, row, 1, 1)

        row += 1
        
        add_publication_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(add_publication_button, 1, row, 1, 1)
        add_publication_button.connect("clicked", self.add_publication_action)
        
        delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        delete_button.connect("clicked", self.delete_action)
        parent_layout_grid.attach(delete_button, 2, row, 1, 1)
        
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
        show_info_dialog(None, "Add successful")
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
        publication = PublicationDAO(model[tree_iter][5])
        publication.load()
        self.prediction.remove_publication(publication)
        self.prediction.save()
        self.prediction.load()
        model.remove(tree_iter)
        show_info_dialog(None, "Delete successful")


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
        prediction_publications.load("uuid='%s'" % self.prediction.uuid)
        for p in prediction_publications:
            self.treemodel.append(["%s" % p.uuid, p.commonname, p.title, p.date.strftime('%d.%m.%Y'),p.url, "%s" % p.publication_uuid])
