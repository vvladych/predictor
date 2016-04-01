from . import *


class ConceptOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, concept=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.concept = concept
        self.create_layout()

        if concept is not None:
            self.load_concept()

        self.parent_callback = callback

    def create_layout(self):

        row = 0

        self.attach(LabelWidget("Concept"), 0, row, 1, 1)

        row +=1

        self.concept_uuid_entry_widget = TextEntryWidget("concept UUID", None, True)
        self.attach(self.concept_uuid_entry_widget, 0, row, 1, 1)

        row += 1

        self.commonname_entry_widget = TextEntryWidget("common name", None, True)
        self.attach(self.commonname_entry_widget, 0, row, 1, 1)

        row += 1

        self.uri_entry_widget = TextEntryWidget("URI", None, True)
        self.attach(self.uri_entry_widget, 0, row, 1, 1)

        row += 1

        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.set_size_request(100, -1)
        self.attach(save_button, 0, row, 1, 1)
        save_button.connect("clicked", self.save_concept_action)

    def load_concept(self):
        self.concept_uuid_entry_widget.set_entry_value("%s" % self.concept.uuid)
        self.commonname_entry_widget.set_entry_value("%s" % self.concept.commonname)
        self.uri_entry_widget.set_entry_value("%s" % self.concept.uri)

    @transactional
    def save_concept_action(self, widget):
        concept_uri = self.uri_entry_widget.get_entry_value()
        concept_commonname = self.commonname_entry_widget.get_entry_value()

        concept_uuid = None
        if self.concept is not None:
            concept_uuid = self.concept.uuid

        concept = ConceptDAO(concept_uuid,
                             {"commonname": concept_commonname,
                              "url": concept_uri})
        concept.save()
        show_info_dialog(self.main_window, "Concept inserted")
        self.concept = concept
        self.concept.load()
        self.load_concept()
        self.parent_callback()


class ConceptExtTreeview(ExtendedTreeView):

    dao_type = ConceptDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("common name", 1, False),
               TreeviewColumn("URI", 2, False)
               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.uri])


class ConceptMask(AbstractMask):

    dao_type = ConceptDAO
    exttreeview = ConceptExtTreeview
    overview_window = ConceptOverviewWindow

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(ConceptOverviewWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()
