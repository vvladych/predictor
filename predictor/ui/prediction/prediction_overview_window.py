"""
Created on 14.03.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.prediction.publication.main_mask import PredictionPublicationMask
from predictor.ui.prediction.textmodel.main_mask import PredictionTextmodelMask
#from forecastmgmt.ui.forecast.originator_add_dialog import OriginatorAddDialog
####from predictor.ui.prediction.originator_process_component import OriginatorOverviewComponent
#from forecastmgmt.ui.forecast.rawtext_add_dialog import RawTextAddDialog
#from forecastmgmt.ui.forecast.model_add_dialog import ModelAddDialog
from predictor.ui.prediction.textmodel.add_dialog import TextModelAddDialog
from predictor.ui.ui_tools import TextViewWidget



class PredictionOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, prediction=None, callback=None):
        Gtk.Grid.__init__(self)
        ###self.originator_overview_component=OriginatorOverviewComponent(forecast)
        self.publication_overview_component = PredictionPublicationMask(main_window, prediction)
        self.textmodel_overview_component = PredictionTextmodelMask(main_window, prediction)
        self.main_window = main_window
        self.prediction = prediction
        self.create_layout()

    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: prediction uuid
        uuid_label = Gtk.Label("prediction UUID")
        uuid_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(uuid_label, 0, row, 1, 1)
        prediction_uuid_text_entry = Gtk.Entry()
        prediction_uuid_text_entry.set_editable(False)
        self.attach(prediction_uuid_text_entry, 1, row, 1, 1)
        
        if self.prediction is not None:
            prediction_uuid_text_entry.set_text("%s" % self.prediction.uuid)

        row += 1

        common_name_label = Gtk.Label("Common name")
        common_name_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(common_name_label, 0, row, 1, 1)
        common_name_text_entry = Gtk.Entry()
        self.attach(common_name_text_entry, 1, row, 1, 1)

        if self.prediction is not None:
            common_name_text_entry.set_text("%s" % self.prediction.commonname)

        row += 1
        
        description_label = Gtk.Label("Description")
        description_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(description_label, 0, row, 1, 1)
        
        short_desc_text = None
        if self.prediction is not None:
            short_desc_text = self.prediction.short_description

        self.desc_textview = Gtk.TextView()
        desc_textview_widget = TextViewWidget(self.desc_textview, short_desc_text)

        self.attach(desc_textview_widget, 1, row, 1, 1)
        
        row += 3
        # forecast originators
        originators_label = Gtk.Label("Originators")
        originators_label.set_justify(Gtk.Justification.LEFT)
        self.attach(originators_label, 0, row, 2, 1)
        
        row += 1

        ####self.originator_overview_component.clean_and_populate_model()
        ####row = self.originator_overview_component.create_layout(self, row)
        """
        row += 1

        button_add_originator_dialog = Gtk.Button("Edit originator(s)")
        button_add_originator_dialog.connect("clicked", self.show_originator_dialog)
        self.attach(button_add_originator_dialog, 0, row, 1, 1)
        
        row += 2
        """

        publications_label = Gtk.Label("Publications")
        publications_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publications_label, 0, row, 2, 1)

        row += 1
        
        # project publications
        self.attach(self.publication_overview_component, 0, row, 2, 1)

        row += 3
        # prediction model
        model_label = Gtk.Label("Model")
        model_label.set_justify(Gtk.Justification.LEFT)
        self.attach(model_label, 0, row, 3, 1)
        
        row += 1

        #buttonGrid = Gtk.Grid()
        
        #button_rawtext_dialog=Gtk.Button("Raw text")
        #button_rawtext_dialog.connect("clicked", self.show_rawtext_dialog)
        #buttonGrid.attach(button_rawtext_dialog, 0, row, 1, 1)

        #button_edit_textmodel_dialog = Gtk.Button("Text model(s)")
        #button_edit_textmodel_dialog.connect("clicked", self.show_textmodel_dialog)
        #buttonGrid.attach(button_edit_textmodel_dialog, 1, row, 1, 1)

        row += 1
        # project textmodel
        self.attach(self.textmodel_overview_component, 0, row, 2, 1)

        #button_edit_model_dialog = Gtk.Button("Formal model(s)")
        #button_edit_model_dialog.connect("clicked", self.show_model_dialog)
        #buttonGrid.attach(button_edit_model_dialog, 2, row, 1, 1)
        
        #self.attach(buttonGrid, 0, row, 2, 1)

    def show_originator_dialog(self, widget):
        #dialog=OriginatorAddDialog(self, self.prediction)
        #dialog.run()
        #dialog.destroy()
        #self.originator_overview_component.clean_and_populate_model()
        pass


    def show_rawtext_dialog(self, widget):
        #dialog=RawTextAddDialog(self, self.forecast)
        #dialog.run()
        #dialog.destroy()
        pass

    def show_model_dialog(self, widget):
        #dialog=ModelAddDialog(self, self.forecast)
        #dialog.run()
        #dialog.destroy()
        pass
    
    def show_textmodel_dialog(self, widget):
        dialog = TextModelAddDialog(self, self.prediction)
        dialog.run()
        dialog.destroy()
