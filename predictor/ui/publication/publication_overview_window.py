"""
Created on 20.08.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog, DateWidget, TextViewWidget
from predictor.model.predictor_model import PublisherDAO
from predictor.model.predictor_model import PublicationDAO
from predictor.model.predictor_model import PublicationtextDAO
from predictor.model.DAO import DAOList
from predictor.helpers.transaction_broker import transactional
import datetime


class PublicationOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, publication=None, callback=None):
        Gtk.Grid.__init__(self)
        self.main_window = main_window
        self.publication = publication
        self.create_layout()
        if publication is not None:
            self.load_publication()
        self.parent_callback=callback
        
    def create_layout(self):
        
        row = 1
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_label, 0, row, 1, 1)
        
        row += 1

        publisher_label = Gtk.Label("Publisher")
        publisher_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publisher_label, 0, row, 1 ,1)

        self.publisher_model = self.populate_publisher_combobox_model()
        self.publisher_combobox = Gtk.ComboBox.new_with_model_and_entry(self.publisher_model)
        self.publisher_combobox.set_entry_text_column(1)
        self.attach(self.publisher_combobox, 1, row, 1, 1)
        
        row += 1

        publication_date_label = Gtk.Label("Publication Date")
        publication_date_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_date_label, 0, row, 1, 1)
        
        self.publication_date_day_textentry = Gtk.Entry()
        self.publication_date_month_textentry = Gtk.Entry()
        self.publication_date_year_textentry = Gtk.Entry()
        
        self.publication_date_widget = DateWidget(self.publication_date_day_textentry, self.publication_date_month_textentry, self.publication_date_year_textentry)
        
        self.attach(self.publication_date_widget, 1, row, 1, 1)

        row += 1

        publication_title_label = Gtk.Label("Publication Title")
        publication_title_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_title_label, 0, row, 1, 1)
        
        self.publication_title_textentry = Gtk.Entry()
        self.attach(self.publication_title_textentry, 1, row, 2, 1)

        row += 1

        publication_file_label = Gtk.Label("Publication file")
        publication_file_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_file_label, 0, row, 1, 1)

        self.publication_file_textentry = Gtk.Entry()
        self.attach(self.publication_file_textentry, 1, row, 2, 1)

        row += 1

        publication_url_label = Gtk.Label("Publication URL")
        publication_url_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_url_label, 0, row, 1, 1)

        self.publication_url_textentry = Gtk.Entry()
        self.attach(self.publication_url_textentry, 1, row, 2, 1)

        row += 1
        
        publication_text_label = Gtk.Label("Publication text")
        publication_text_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_text_label, 0, row, 1, 1)
        
        self.textview = Gtk.TextView()
        self.textview_widget = TextViewWidget(self.textview)
        self.attach(self.textview_widget, 1, row, 2, 1)

        row += 1
        
        self.save_publication_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        self.attach(self.save_publication_button, 1, row, 1, 1)
        self.save_publication_button.connect("clicked", self.save_publication_action)
        
        row += 1
        
    def populate_publisher_combobox_model(self):
        combobox_model = Gtk.ListStore(str, str)
        publishers = DAOList(PublisherDAO)
        publishers.load()
        for p in publishers:
            combobox_model.append(["%s" % p.uuid, p.commonname])
        return combobox_model

    def set_active_publisher(self, publisher_uuid):
        model_iter = self.publisher_model.get_iter_first()

        while model_iter is not None and self.publisher_model.iter_is_valid(model_iter):
            if publisher_uuid == self.publisher_model.get_value(model_iter,0):
                self.publisher_combobox.set_active_iter(model_iter)
            model_iter = self.publisher_model.iter_next(model_iter)
    
    def load_publication(self):
        self.publication_title_textentry.set_text(self.publication.title)
        self.publication_url_textentry.set_text("%s" % self.publication.url)
        publicationtext = self.publication.get_publicationtext()
        if publicationtext is not None:
            self.textview_widget.set_text(publicationtext.text)

        self.publication_date_widget.set_date_from_string("%s" % self.publication.date)
        publisher = self.publication.get_publisher()
        if publisher is not None:
            #self.publisher_combobox.set_active_id("%s" % publisher.uuid)
            self.set_active_publisher(publisher.uuid)
    
    def save_publication_action(self, widget):
        if self.publication is not None:
            print("update")
        else:
            self.insert_new_publication_from_mask()

    @transactional
    def insert_new_publication_from_mask(self):
        publisher_uuid = self.get_active_publisher()
        publication_title = self.publication_title_textentry.get_text()
        publication_text = self.textview_widget.get_textview_text()
        publication_url = self.publication_url_textentry.get_text()
                
        # insert publication
        publication = PublicationDAO(None,
                                     datetime.date(int(self.publication_date_year_textentry.get_text()),
                                                   int(self.publication_date_month_textentry.get_text()),
                                                   int(self.publication_date_day_textentry.get_text())),
                                     publication_title,
                                     publication_url)

        publication_text_DAO = PublicationtextDAO()
        publication_text_DAO.text = publication_text
        publication_text_DAO.save()
        publication.add_publicationtext(publication_text_DAO)

        publication.save()
        show_info_dialog("Publication inserted")
        self.publication = publication
        self.parent_callback()

    def get_active_publisher(self):
        tree_iter = self.publisher_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.publisher_combobox.get_model()
            publisher_sid = model[tree_iter][:2]
            return publisher_sid[0]
        else:
            print("please choose a publisher!")

    def delete_action(self, widget):
        print("not implemented")
