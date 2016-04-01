from . import *


class PredictionPublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.prediction = prediction
        self.set_default_size(400, 400)
        self.overview_component = PredictionPublicationExtTreeview(self,
                                                                   0,
                                                                   20,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.prediction)

        self.create_layout()
        self.show_all()

    def create_layout(self):
        box = self.get_content_area()

        layout_grid = Gtk.Grid()

        box.add(layout_grid)

        row = 0
        layout_grid.attach(Gtk.Label("Prediction's predpublication(s)"), 0, row, 1, 1)

        row += 1

        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(publication_label, 0, row, 1, 1)

        row += 1

        publisher_label = Gtk.Label("Publisher")
        publisher_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(publisher_label, 0, row, 1, 1)

        publication_model = self.populate_publication_combobox_model()
        self.publication_combobox = Gtk.ComboBox.new_with_model_and_entry(publication_model)
        self.publication_combobox.set_entry_text_column(1)
        layout_grid.attach(self.publication_combobox, 1, row, 1, 1)

        row += 1

        add_publication_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        layout_grid.attach(add_publication_button, 1, row, 1, 1)
        add_publication_button.connect("clicked", self.add_publication_action)

        row += 1

        layout_grid.attach(self.overview_component, 0, row, 2, 1)

    def populate_publication_combobox_model(self):
        combobox_model = Gtk.ListStore(str, str)
        publications = DAOList(PublicationPublisherV)
        publications.load()
        for p in publications:
            combobox_model.append(["%s" % p.uuid, "%s %s %s" % (p.publisher_commonname, p.publication_date, p.publication_title)])
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

    def noop(self, widget=None):
        pass


class PredictionPublicationExtTreeview(ExtendedTreeView):

    dao_type = PredictionPublisherV
    columns = [TreeviewColumn("prediction_uuid", 0, True),
               TreeviewColumn("Publisher", 1, False),
               TreeviewColumn("Title", 2, False, True),
               TreeviewColumn("Date", 3, False),
               TreeviewColumn("URL", 4, False),
               TreeviewColumn("publication_uuid", 5, True),
               ]

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

    default_height = 80
    default_width = 400

    def __init__(self, main_window, prediction):
        super(PredictionPublicationMask, self).__init__(main_window, prediction)
        self.prediction = prediction

    def new_callback(self):
        dialog = PredictionPublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)