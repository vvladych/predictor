"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview
from predictor.ui.prediction.textmodel.exttreeview import PredictionTextmodelExtTreeview
from predictor.ui.prediction.publication.add_dialog import PublicationAddDialog
#from forecastmgmt.ui.forecast.originator_add_dialog import OriginatorAddDialog
####from predictor.ui.prediction.originator_process_component import OriginatorOverviewComponent
from predictor.ui.prediction.textmodel.add_dialog import TextModelAddDialog
from predictor.ui.ui_tools import TextViewWidget, TextEntryWidget
from predictor.ui.prediction.originator.exttreeview import PredictionOriginatorExtTreeview



class PredictionOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, prediction=None, callback=None):
        Gtk.Grid.__init__(self)
        ###self.originator_overview_component=OriginatorOverviewComponent(forecast)

        self.publication_overview_component = PredictionPublicationExtTreeview(main_window, 0, 20, None, None, self.show_publication_dialog, prediction)
        self.textmodel_overview_component = PredictionTextmodelExtTreeview(main_window, 0, 20, None, None, self.show_textmodel_dialog, prediction)
        self.originator_overview_component = PredictionOriginatorExtTreeview(main_window, 0, 20, None, None, self.show_originator_dialog, prediction)
        self.main_window = main_window
        self.prediction = prediction
        self.create_layout()

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
        self.prediction_uuid_text_entry.set_size_request(500, -1)
        self.attach(self.prediction_uuid_text_entry, 0, row, 2, 1)

        row += 1

        self.common_name_text_entry = TextEntryWidget("Common name", None, False)
        self.attach(self.common_name_text_entry, 0, row, 2, 1)

        row += 1

        description_label = Gtk.Label("Description")
        description_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(description_label, 0, row, 1, 1)

        row += 1

        self.desc_textview = Gtk.TextView()
        desc_textview_widget = TextViewWidget(self.desc_textview)

        self.attach(desc_textview_widget, 0, row, 1, 1)

        if self.prediction is not None:
            self.prediction_uuid_text_entry.set_entry_value(self.prediction.uuid)
            self.common_name_text_entry.set_entry_value(self.prediction.commonname)
            desc_textview_widget.set_text(self.prediction.short_description)

        row += 3
        # originators
        originators_label = Gtk.Label("Originators")
        originators_label.set_justify(Gtk.Justification.LEFT)
        self.attach(originators_label, 0, row, 2, 1)
        
        row += 1
        self.attach(self.originator_overview_component, 0, row, 2, 1)

        row += 3

        # publications
        publications_label = Gtk.Label("Publications")
        publications_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publications_label, 0, row, 2, 1)

        row += 1

        self.attach(self.publication_overview_component, 0, row, 2, 1)

        row += 3
        # prediction model
        model_label = Gtk.Label("Model")
        model_label.set_justify(Gtk.Justification.LEFT)
        self.attach(model_label, 0, row, 2, 1)
        
        row += 1

        self.attach(self.textmodel_overview_component, 0, row, 2, 1)

        row += 1
        self.attach(Gtk.Label(""), 0, row, 3, 1)



    def show_publication_dialog(self):
        dialog = PublicationAddDialog(self.main_window, self.prediction)
        dialog.run()
        dialog.destroy()
        self.publication_overview_component.fill_treeview(0)

    def show_originator_dialog(self, widget):
        #dialog=OriginatorAddDialog(self, self.prediction)
        #dialog.run()
        #dialog.destroy()
        #self.originator_overview_component.clean_and_populate_model()
        print("in show_originator_dialog")
        pass


    def show_textmodel_dialog(self):
        dialog = TextModelAddDialog(self, self.prediction)
        dialog.run()
        dialog.destroy()
        self.textmodel_overview_component.fill_treeview(0)
