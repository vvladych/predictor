"""
Created on 20.08.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog, DateWidget, TextViewWidget, DAOComboBoxWidget, LabelWidget, TextEntryWidget
from predictor.model.predictor_model import PublisherDAO, PublicationDAO, PublicationtextDAO
from predictor.helpers.transaction_broker import transactional


class PublisherComboBoxWidget(DAOComboBoxWidget):
    dao = PublisherDAO

    def add_entry(self, publisher):
        self.model.append(["%s" % publisher.uuid, "%s" % publisher.commonname])


class PublicationOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, publication=None, callback=None):
        Gtk.Grid.__init__(self)
        #self.set_row_spacing(3)
        #self.set_column_spacing(3)

        self.main_window = main_window
        self.publication = publication
        self.create_layout()
        """
        if publication is not None:
            self.load_publication()
        """
        self.parent_callback = callback
        
    def create_layout(self):
        
        row = 1
        
        self.attach(LabelWidget("Publication"), 0, row, 2, 1)

        row += 1

        self.publisher_combobox_widget = PublisherComboBoxWidget("Publisher")
        self.attach(self.publisher_combobox_widget, 0, row, 1, 1)

        row += 1

        self.publication_date_widget = DateWidget("Date")
        self.attach(self.publication_date_widget, 0, row, 1, 1)

        row += 1

        self.publication_title_entry_widget = TextEntryWidget("Title")
        self.attach(self.publication_title_entry_widget, 0, row, 1, 1)

        row += 1

        self.publication_file_entry_widget = TextEntryWidget("File")
        self.attach(self.publication_file_entry_widget, 0, row, 1, 1)

        row += 1

        self.publication_url_entry_widget = TextEntryWidget("URL")
        self.attach(self.publication_url_entry_widget, 0, row, 1, 1)

        row += 1

        self.textview_widget = TextViewWidget(None, None, "Text")
        self.attach(self.textview_widget, 0, row, 2, 1)

        row += 1
        
        save_publication_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        self.attach(save_publication_button, 1, row, 1, 1)
        save_publication_button.connect("clicked", self.save_publication_action)

    def load_publication(self):
        self.publication_title_entry_widget.set_entry_value(self.publication.title)
        self.publication_url_entry_widget.set_entry_value("%s" % self.publication.url)
        publicationtext = self.publication.get_publicationtext()
        if publicationtext is not None:
            self.textview_widget.set_text(publicationtext.text)

        self.publication_date_widget.set_date_from_string("%s" % self.publication.date)
        publisher = self.publication.get_publisher()
        if publisher is not None:
            self.publisher_combobox_widget.set_active_entry(publisher.uuid)

    @transactional
    def save_publication_action(self, widget):
        publication_title = self.publication_title_entry_widget.get_entry_value()
        publication_text = self.textview_widget.get_textview_text()
        publication_url = self.publication_url_entry_widget.get_text()
                
        # insert publication
        publication_uuid = None
        if self.publication is not None:
            publication_uuid = self.publication.uuid

        publication = PublicationDAO(publication_uuid,
                                     {"date": self.publication_date_widget.get_date(),
                                      "title": publication_title,
                                      "url": publication_url})

        publication_text_DAO = PublicationtextDAO()
        publication_text_DAO.text = publication_text
        publication_text_DAO.save()
        publication.add_publicationtext(publication_text_DAO)

        publisher_uuid = self.publisher_combobox_widget.get_active_entry()
        publisher = PublisherDAO(publisher_uuid)
        publication.add_publisher(publisher)

        publication.save()

        show_info_dialog(None, "Publication inserted")
        self.publication = publication
        self.publication.load()
        self.load_publication()
        self.parent_callback()
