from . import *


class PredictionNewDialog(BaseAddDialog):

    def create_layout(self):
        layout_grid = Gtk.Grid()

        new_label = LabelWidget("Create new prediction")
        layout_grid.attach(new_label, 0, 0, 1, 1)

        self.prediction_name_entry_widget = TextEntryWidget("Prediction name")
        layout_grid.attach_next_to(self.prediction_name_entry_widget, new_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.desc_textview = TextViewWidget(None, None, "Short description")
        layout_grid.attach_next_to(self.desc_textview, self.prediction_name_entry_widget, Gtk.PositionType.BOTTOM, 1, 1)

        return layout_grid

    @transactional
    def perform_insert(self):
        prediction = PredictionDAO(None, {'commonname':self.prediction_name_entry_widget.get_entry_value(),
                                          'short_description':self.desc_textview.get_textview_text()})
        prediction.save()

    def set_overview_component(self):
        pass


class PredictionOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, prediction=None, callback=None):
        Gtk.Grid.__init__(self)
        self.main_window = main_window
        self.publication_overview_component = PredictionPublicationExtTreeview(main_window, 0, 20, None, None, self.show_publication_dialog, prediction)
        self.tmstatement_overview_component = TextmodelStatementExtTreeview(main_window, 0, 20, None, None, self.show_tmstatement_dialog, prediction)
        self.originator_overview_component = PredictionOriginatorExtTreeview(main_window, 0, 20, None, None, self.show_originator_dialog, prediction)
        self.prediction = prediction
        self.create_layout()
        self.load_prediction()

    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        self.attach(placeholder_label, 0, 0, 1, 1)

        self.prediction_uuid_text_entry = TextEntryWidget("prediction UUID", None, False)
        self.attach_next_to(self.prediction_uuid_text_entry, placeholder_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.common_name_text_entry = TextEntryWidget("Common name", None, False)
        self.attach_next_to(self.common_name_text_entry, self.prediction_uuid_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.desc_textview_widget = TextViewWidget(None, None, "Description")
        self.attach_next_to(self.desc_textview_widget, self.common_name_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        # originators
        originators_label = LabelWidget("Originators")
        self.attach_next_to(originators_label, self.desc_textview_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.originator_overview_component, originators_label, Gtk.PositionType.BOTTOM, 1, 1)

        publications_label = LabelWidget("Publications")
        self.attach_next_to(publications_label, self.originator_overview_component, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.publication_overview_component, publications_label, Gtk.PositionType.BOTTOM, 1, 1)

        statements_label = LabelWidget("Statements")
        self.attach_next_to(statements_label, self.publication_overview_component, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.tmstatement_overview_component, statements_label, Gtk.PositionType.BOTTOM, 1, 1)

    def load_prediction(self):
        if self.prediction is not None:
            self.prediction_uuid_text_entry.set_entry_value(self.prediction.uuid)
            self.common_name_text_entry.set_entry_value(self.prediction.commonname)
            self.desc_textview_widget.set_text(self.prediction.short_description)

    def show_publication_dialog(self):
        dialog = PredictionPublicationAddDialog(self.main_window, self.prediction, "Publication Dialog")
        dialog.run()
        dialog.destroy()
        self.publication_overview_component.fill_treeview(0)

    def show_originator_dialog(self):
        dialog = OriginatorAddDialog(self.main_window, self.prediction, "Originator Dialog")
        dialog.run()
        dialog.destroy()
        self.originator_overview_component.fill_treeview(0)

    def show_tmstatement_dialog(self):
        dialog = TextmodelStatementAddDialog(self.main_window, self.prediction, "Model Dialog")
        dialog.run()
        dialog.destroy()
        self.tmstatement_overview_component.fill_treeview(0)


class PredictionExtTreeview(ExtendedTreeView):

    dao_type = PredictionPublicationPublisherV

    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("Date", 2, False),
               TreeviewColumn("Publication", 3, False),
               TreeviewColumn("Publisher", 4, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.created_date, "%s" % row.publication_title, "%s" % row.publisher_commonname])

    def on_menu_item_new(self, widget):
        new_prediction_dialog = PredictionNewDialog(self.main_window, None, "New Prediction")
        response = new_prediction_dialog.run()

        if response == Gtk.ResponseType.OK:
            new_prediction_dialog.perform_insert()
        elif response == Gtk.ResponseType.CANCEL:
            show_info_dialog(self.main_window, "Canceled")
        else:
            show_info_dialog(self.main_window, "Unknown action")

        new_prediction_dialog.destroy()
        self.reset_treemodel()


class PredictionMask(AbstractMask):

    dao_type = PredictionDAO
    overview_window = PredictionOverviewWindow
    exttreeview = PredictionExtTreeview
