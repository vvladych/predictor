from . import *

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
        placeholder_label.set_size_request(-1, -1)
        self.attach(placeholder_label, 0, -1, 1, 1)
        placeholder_label.set_hexpand(True)

        row = 0
        # Row 0: prediction uuid
        self.prediction_uuid_text_entry = TextEntryWidget("prediction UUID", None, False)
        self.attach(self.prediction_uuid_text_entry, 0, row, 2, 1)

        row += 1

        self.common_name_text_entry = TextEntryWidget("Common name", None, False)
        self.attach(self.common_name_text_entry, 0, row, 2, 1)

        row += 1

        desc_textview = Gtk.TextView()
        self.desc_textview_widget = TextViewWidget(desc_textview, None, "Description")

        self.attach(self.desc_textview_widget, 0, row, 1, 1)

        row += 3
        # originators
        self.attach(LabelWidget("Originators"), 0, row, 2, 1)

        row += 1
        self.attach(self.originator_overview_component, 0, row, 2, 1)

        row += 3

        # publications
        self.attach(LabelWidget("Publications"), 0, row, 2, 1)

        row += 1

        self.attach(self.publication_overview_component, 0, row, 2, 1)

        row += 3
        # prediction model
        self.attach(LabelWidget("Statements"), 0, row, 2, 1)

        row += 1

        self.attach(self.tmstatement_overview_component, 0, row, 2, 1)

        row += 1
        self.attach(Gtk.Label(""), 0, row, 3, 1)

    def load_prediction(self):
        if self.prediction is not None:
            self.prediction_uuid_text_entry.set_entry_value(self.prediction.uuid)
            self.common_name_text_entry.set_entry_value(self.prediction.commonname)
            self.desc_textview_widget.set_text(self.prediction.short_description)

    def show_publication_dialog(self):
        dialog = PublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.publication_overview_component.fill_treeview(0)

    def show_originator_dialog(self):
        dialog = OriginatorAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.originator_overview_component.fill_treeview(0)

    def show_tmstatement_dialog(self):
        dialog = TextmodelStatementAddDialog(self.main_window, self.prediction)
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
        new_prediction_dialog = PredictionNewDialog(self.main_window)
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
