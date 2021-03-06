from . import *
from predictor.ui.ui_tools import attach_next_to_bottom_position_expander


class PublicationOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, publication=None, callback=None):
        Gtk.Grid.__init__(self)

        self.main_layout_grid = Gtk.Grid()
        self.main_layout_grid.set_row_spacing(3)
        self.main_layout_grid.set_column_spacing(3)
        self.attach(self.main_layout_grid, 0, 0, 1, 1)

        self.main_window = main_window
        self.publication = publication

        self.create_layout()

        if publication is not None:
            self.load_publication()

        self.parent_callback = callback

    def create_layout(self):

        main_label = LabelWidget("Publication")
        self.main_layout_grid.attach(main_label, 0, 0, 1, 1)

        self.publisher_combobox_widget = ComboBoxWidget("Publisher",
                                                         DAOList(PublisherDAO, True),
                                                         lambda x: ["%s" % x.uuid, "%s" % x.commonname])
        self.main_layout_grid.attach_next_to(self.publisher_combobox_widget, main_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.publication_date_widget = DateWidget("Date")
        self.main_layout_grid.attach_next_to(self.publication_date_widget,
                                             self.publisher_combobox_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.language_combobox_widget = ComboBoxWidget("Language",
                                                        DAOList(LanguageDAO, True),
                                                        lambda x: ["%s" % x.uuid, "%s" % x.commonname])
        self.main_layout_grid.attach_next_to(self.language_combobox_widget,
                                             self.publication_date_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.publication_title_entry_widget = TextEntryWidget("Title")
        self.main_layout_grid.attach_next_to(self.publication_title_entry_widget,
                                             self.language_combobox_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.publication_url_entry_widget = TextEntryWidget("URL")
        self.main_layout_grid.attach_next_to(self.publication_url_entry_widget,
                                             self.publication_title_entry_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        pubfile_label = LabelWidget("Publication File")
        self.main_layout_grid.attach_next_to(pubfile_label,
                                             self.publication_url_entry_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.publication_file_entry_widget = TextEntryFileChooserWidget("File")
        self.main_layout_grid.attach_next_to(self.publication_file_entry_widget,
                                             pubfile_label,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.binaryfile_uuid_entry_widget = TextEntryWidget("File UUID", None, False)
        self.main_layout_grid.attach_next_to(self.binaryfile_uuid_entry_widget,
                                             self.publication_file_entry_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        choose_file_grid = Gtk.Grid()

        self.filetype_combobox_widget = ComboBoxWidget("", ["application/pdf", "text/html"], lambda x: [None, "%s" % x])
        choose_file_grid.attach(self.filetype_combobox_widget, 0, 0, 1, 1)

        preview_file_button = Gtk.Button("Preview")
        preview_file_button.set_size_request(100, -1)
        preview_file_button.connect("clicked", self.preview_file)
        choose_file_grid.attach(preview_file_button, 1, 0, 1, 1)

        self.main_layout_grid.attach_next_to(choose_file_grid,
                                             self.binaryfile_uuid_entry_widget,
                                             Gtk.PositionType.BOTTOM,
                                             1,
                                             1)

        self.textview_widget = TextViewWidget(None, None, "Text", 600, 200, True)
        exp_t_w = attach_next_to_bottom_position_expander(self.main_layout_grid,
                                                          self.textview_widget,
                                                          choose_file_grid,
                                                          "Content")

        save_publication_button = ButtonWidget("Save", Gtk.STOCK_SAVE, self.save_publication_action)
        self.main_layout_grid.attach_next_to(save_publication_button, exp_t_w, Gtk.PositionType.BOTTOM, 1, 1)

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

        # insert predpublication
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

        show_info_dialog(self.main_window, "Publication inserted")
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


class PublicationExtTreeview(ExtendedTreeView):

    dao_type = PublicationDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Title", 1, False),
               TreeviewColumn("Date", 2, False),
               TreeviewColumn("URL", 3, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.title, "%s" % row.date, "%s" % row.url])


class PublUnassignedExtTreeview(PublicationExtTreeview):
    dao_type = PublicationUnassignedV


class PublAssignedExtTreeview(PublicationExtTreeview):
    dao_type = PublicationAssignedV


class PublicationMask(AbstractMask):

    def __init__(self, main_window, dao=None):
        super(PublicationMask, self).__init__(main_window, dao, PublicationExtTreeview, PublicationOverviewWindow, PublicationDAO)
        self.filter_combobox_widget.set_active_entry("All")

    def add_left_pane_filter(self):
        self.filter_combobox_widget = ComboBoxWidget("Filter",
                                                     ["All", "Assigned", "Unassigned"],
                                                     lambda x: ["%s" % x, "%s" % x],
                                                     self.on_filter_combobox_change, 50, 50)
        return self.filter_combobox_widget


    def on_filter_combobox_change(self, widget=None):
        active_filter = self.filter_combobox_widget.get_active_entry()
        if active_filter == "Unassigned":
            self.replace_exttreeview(PublUnassignedExtTreeview)
        elif active_filter == "Assigned":
            self.replace_exttreeview(PublAssignedExtTreeview)
        else:
            self.replace_exttreeview(PublicationExtTreeview)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.attach(PublicationOverviewWindow(self.main_window, None, self.overview_treeview.reset_treemodel), 0, 0, 1, 1)
        self.main_middle_pane.show_all()
