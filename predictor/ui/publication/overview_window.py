"""
Created on 20.08.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog, DateWidget, TextViewWidget, DAOComboBoxWidget, LabelWidget, TextEntryWidget, ComboBoxWidget, TextEntryFileChooserWidget
from predictor.model.predictor_model import PublisherDAO, PublicationDAO, PublicationtextDAO, BinaryfileDAO, LanguageDAO
from predictor.helpers.transaction_broker import transactional
import tempfile
import subprocess
from predictor.helpers import config
import os


class PublisherComboBoxWidget(DAOComboBoxWidget):
    dao = PublisherDAO

    def add_entry(self, publisher):
        self.model.append(["%s" % publisher.uuid, "%s" % publisher.commonname])


class LanguageComboBoxWidget(DAOComboBoxWidget):
    dao = LanguageDAO

    def add_entry(self, language):
        self.model.append(["%s" % language.uuid, "%s" % language.commonname])


class PublicationOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, publication=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.publication = publication
        self.create_layout()

        if publication is not None:
            self.load_publication()

        self.parent_callback = callback
        
    def create_layout(self):
        
        row = 0
        
        self.attach(LabelWidget("Publication"), 0, row, 2, 1)

        row += 1

        self.publisher_combobox_widget = PublisherComboBoxWidget("Publisher")
        self.attach(self.publisher_combobox_widget, 0, row, 1, 1)

        row += 1

        self.publication_date_widget = DateWidget("Date")
        self.attach(self.publication_date_widget, 0, row, 1, 1)

        row += 1

        self.language_combobox_widget = LanguageComboBoxWidget("Language")
        self.attach(self.language_combobox_widget, 0, row, 1, 1)

        row += 1

        self.publication_title_entry_widget = TextEntryWidget("Title")
        self.attach(self.publication_title_entry_widget, 0, row, 1, 1)

        row += 1

        self.publication_url_entry_widget = TextEntryWidget("URL")
        self.attach(self.publication_url_entry_widget, 0, row, 1, 1)

        row += 1

        self.attach(LabelWidget("Publication File"), 0, row, 2, 1)

        row += 1

        self.publication_file_entry_widget = TextEntryFileChooserWidget("File")
        self.attach(self.publication_file_entry_widget, 0, row, 1, 1)

        row += 1

        self.binaryfile_uuid_entry_widget = TextEntryWidget("File UUID", None, False)
        self.attach(self.binaryfile_uuid_entry_widget, 0, row, 1, 1)

        row += 1

        choose_file_grid = Gtk.Grid()

        self.filetype_combobox_widget = ComboBoxWidget("", ["application/pdf", "text/html"], lambda x: [None, "%s" % x])
        choose_file_grid.attach(self.filetype_combobox_widget, 1, 0, 1, 1)

        preview_file_button = Gtk.Button("Preview")
        preview_file_button.set_size_request(100, -1)
        preview_file_button.connect("clicked", self.preview_file)
        choose_file_grid.attach(preview_file_button, 2, 0, 1, 1)

        self.attach(choose_file_grid, 0, row, 1, 1)

        row += 1

        self.attach(LabelWidget("Content"), 0, row, 2, 1)

        row += 1

        self.textview_widget = TextViewWidget(None, None, "Text")
        self.attach(self.textview_widget, 0, row, 2, 1)

        row += 1
        
        save_publication_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        self.attach(save_publication_button, 1, row, 1, 1)
        save_publication_button.connect("clicked", self.save_publication_action)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(400, 400)
        placeholder_label.set_vexpand(True)
        placeholder_label.set_hexpand(True)
        self.attach(placeholder_label, 2, 0, 1, 12)

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

        language = self.publication.get_language()
        if language is not None:
            self.language_combobox_widget.set_active_entry(language.uuid)

        binaryfile = self.publication.get_binaryfile()
        if binaryfile is not None:
            self.publication_file_entry_widget.set_entry_value(binaryfile.filename)
            self.binaryfile_uuid_entry_widget.set_entry_value(binaryfile.uuid)
            self.filetype_combobox_widget.set_active_entry(self.filetype_combobox_widget.get_entry_key_for_value(binaryfile.filetype))

    @transactional
    def save_publication_action(self, widget):
        publication_title = self.publication_title_entry_widget.get_entry_value()
        publication_text = self.textview_widget.get_textview_text()
        publication_url = self.publication_url_entry_widget.get_entry_value()
        publication_binaryfile_name = self.publication_file_entry_widget.get_entry_value()
        publication_binaryfile_type = self.filetype_combobox_widget.get_active_entry_visible()
                
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

        language_uuid = self.language_combobox_widget.get_active_entry()
        language = LanguageDAO(language_uuid)
        publication.add_language(language)

        if publication_binaryfile_name is not None and len(publication_binaryfile_name)>0 and os.path.isfile(publication_binaryfile_name):
            binaryfile_DAO = BinaryfileDAO()
            binaryfile_DAO.filecontent = open(publication_binaryfile_name, mode='rb').read()
            binaryfile_DAO.filetype = publication_binaryfile_type
            binaryfile_DAO.filename = publication_binaryfile_name
            binaryfile_DAO.save()
            publication.add_binaryfile(binaryfile_DAO)

        publication.save()

        show_info_dialog(None, "Publication inserted")
        self.publication = publication
        self.publication.load()
        self.load_publication()
        self.parent_callback()

    def preview_file(self, widget):
        if self.publication is not None:
            binaryfile = self.publication.get_binaryfile()
            if binaryfile is not None:
                if binaryfile.filetype == "application/pdf":
                    tmpfile = tempfile.NamedTemporaryFile()
                    tmpfile.write(binaryfile.filecontent)
                    subprocess.call([config.get('binaryfileviewer', 'application/pdf'), tmpfile.name])
                    tmpfile.close()
