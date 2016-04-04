from . import *


class PredictionPublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.main_window = parent
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

        predpub_label = LabelWidget("Prediction's predpublication(s)")
        layout_grid.attach(predpub_label, 0, 0, 1, 1)

        publication_label = LabelWidget("Publication")
        layout_grid.attach_next_to(publication_label, predpub_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.publications_combobox = ComboBoxWidget("Publisher",
                                                    DAOList(PublicationPublisherV, True),
                                                    lambda x: ["%s" % x.uuid, "%s %s %s" % (x.publisher_commonname, x.publication_date, x.publication_title)])
        layout_grid.attach_next_to(self.publications_combobox, publication_label, Gtk.PositionType.BOTTOM, 1, 1)

        add_publication_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_publication_button.connect("clicked", self.add_publication_action)
        layout_grid.attach_next_to(add_publication_button, self.publications_combobox, Gtk.PositionType.BOTTOM, 1, 1)

        layout_grid.attach_next_to(self.overview_component, add_publication_button, Gtk.PositionType.BOTTOM, 1, 1)

    @transactional
    def add_publication_action(self, widget):
        publication = PublicationDAO(self.get_active_publication())
        publication.load()
        self.prediction.add_publication(publication)
        self.prediction.save()
        show_info_dialog(self.main_window, "Add successful")
        self.overview_component.fill_treeview(0)

    def get_active_publication(self):
        return self.publications_combobox.get_active_entry()

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