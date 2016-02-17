
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent
from predictor.ui.ui_tools import show_info_dialog
from predictor.model.DAO import DAOList
from predictor.model.predictor_model import PublicationDAO, PredictionPublisherV
from predictor.ui.base.exttreeview import TreeviewColumn
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview



class PublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            None,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 400)
        self.layout_grid = Gtk.Grid()
        # (self, main_window, start_row, rows_per_page, on_row_select_callback, on_new_callback, on_edit_callback, concrete_dao):

        self.overview_component = PredictionPublicationExtTreeview(parent,
                                                              0,
                                                              20,
                                                              None,#self.on_row_select,
                                                              None,#self.new_callback,
                                                              None,#self.edit_callback,
                                                              prediction)

        self.process_component = AbstractDataProcessComponent(PublicationManipulationComponent(prediction,
                                                                                               self.overview_component))
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

        self.overview_component.set_size_request(100, 300)
        self.layout_grid.attach(self.overview_component, 0, row, 1, 1)

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

        publication_model = self.populate_publication_combobox_model()
        self.publication_combobox = Gtk.ComboBox.new_with_model_and_entry(publication_model)
        self.publication_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.publication_combobox, 1, row, 1, 1)

        row += 1

        add_publication_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(add_publication_button, 1, row, 1, 1)
        add_publication_button.connect("clicked", self.add_publication_action)

        row += 1

        #row = self.overview_component.create_layout(parent_layout_grid, row)

        return row

    def populate_publication_combobox_model(self):
        combobox_model = Gtk.ListStore(str, str)
        publications = DAOList(PublicationDAO)
        publications.load()
        for p in publications:
            combobox_model.append(["%s" % p.uuid, "%s %s %s" % ("Publisher", p.date, p.title)])
        return combobox_model

    @transactional
    def add_publication_action(self, widget):
        publication = PublicationDAO(self.get_active_publication())
        publication.load()
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
            show_info_dialog(None, "please choose a publication!")


class PublicationOverviewComponent(AbstractDataOverviewComponent):

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

    def on_row_select(self, widget, path, data):
        pass
