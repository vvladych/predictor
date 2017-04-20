from . import *


class PredictionPublicationAddDialog(BaseAddDialog):

    def set_overview_component(self):
        self.overview_component = PredictionPublicationExtTreeview(self,
                                                                   0,
                                                                   20,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.prediction)

    def create_layout(self):

        layout_grid = Gtk.Grid()

        predpub_label = LabelWidget("Prediction's predpublication(s)")
        layout_grid.attach(predpub_label, 0, 0, 1, 1)

        publication_label = LabelWidget("Publication")
        layout_grid.attach_next_to(publication_label, predpub_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.publications_combobox = ComboBoxWidget("Publisher",
                                                    DAOList(PublicationPublisherV, True),
                                                    lambda x: ["%s" % x.uuid, "%s %s %s" % (x.publisher_commonname, x.publication_date, x.publication_title), "%s" % x.publication_date],
                                                    sorted=True)

        layout_grid.attach_next_to(self.publications_combobox, publication_label, Gtk.PositionType.BOTTOM, 1, 1)

        add_publication_button = ButtonWidget("Add", Gtk.STOCK_ADD, self.add_publication_action)
        layout_grid.attach_next_to(add_publication_button, self.publications_combobox, Gtk.PositionType.BOTTOM, 1, 1)

        layout_grid.attach_next_to(self.overview_component, add_publication_button, Gtk.PositionType.BOTTOM, 1, 1)

        return layout_grid

    @transactional
    def add_publication_action(self, widget):
        publication = PublicationDAO(self.publications_combobox.get_active_entry())
        publication.load()
        self.prediction.add_publication(publication)
        self.prediction.save()
        show_info_dialog(self.main_window, "Add successful")
        self.overview_component.fill_treeview(0)



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
            
    def on_menu_item_new(self, widget):
        pass
            


class PredictionPublicationMask(AbstractMask):

    def __init__(self, main_window, prediction, dao=None):
        super(PredictionPublicationMask, self).__init__(main_window, dao, PredictionPublicationExtTreeview, None, PredictionPublisherV)
        self.prediction = prediction

    def new_callback(self):
        dialog = PredictionPublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.overview_treeview.fill_treeview(0)
