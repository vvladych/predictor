
from gi.repository import Gtk

from predictor.ui.prediction.abstract_data_process_component import AbstractDataManipulationComponent, AbstractDataProcessComponent
from predictor.ui.ui_tools import show_info_dialog
from predictor.model.DAO import DAOList
from predictor.model.predictor_model import PublicationDAO
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview


class PublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.prediction = prediction
        self.layout_grid = Gtk.Grid()

        self.set_default_size(400, 400)

        self.overview_component = PredictionPublicationExtTreeview(self,
                                                                   0,
                                                                   20,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.prediction)

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

        self.overview_component.window.set_size_request(400, 300)
        self.layout_grid.attach(self.overview_component, 0, row, 2, 1)

        return row

    def noop(self, widget=None):
        pass


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
        self.overview_component.fill_treeview(0)

    def get_active_publication(self):
        tree_iter = self.publication_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.publication_combobox.get_model()
            publication_uuid = model[tree_iter][0]
            return publication_uuid
        else:
            show_info_dialog(None, "please choose a publication!")
