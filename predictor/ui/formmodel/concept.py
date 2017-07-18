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
        main_label = LabelWidget("Concept")
        self.attach(main_label, 0, 0, 1, 1)

        self.concept_uuid_entry_widget = TextEntryWidget("concept UUID", None, True)
        self.attach_next_to(self.concept_uuid_entry_widget, main_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.commonname_entry_widget = TextEntryWidget("common name", None, True)
        self.attach_next_to(self.commonname_entry_widget, self.concept_uuid_entry_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.uri_entry_widget = TextEntryWidget("URI", None, True)
        self.attach_next_to(self.uri_entry_widget, self.commonname_entry_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.concept_datatype_widget = ComboBoxWidget("Concept datatype",
                                                      enum_retrieve_valid_values("t_concept_type"),
                                                      lambda x: ["%s" % x[0], "%s" % x[1]])
        self.attach_next_to(self.concept_datatype_widget, self.uri_entry_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.concept_dimension_widget = ComboBoxWidget("Concept dimension",
                                                       enum_retrieve_valid_values("t_concept_dimension"),
                                                       lambda x: ["%s" % x[0], "%s" % x[1]])
        self.attach_next_to(self.concept_dimension_widget, self.concept_datatype_widget, Gtk.PositionType.BOTTOM, 1, 1)

        save_button = ButtonWidget("Save", Gtk.STOCK_SAVE, self.save_concept_action)
        self.attach_next_to(save_button, self.concept_dimension_widget, Gtk.PositionType.BOTTOM, 1, 1)

    def load_concept(self):
        self.concept_uuid_entry_widget.set_entry_value("%s" % self.concept.uuid)
        self.commonname_entry_widget.set_entry_value("%s" % self.concept.commonname)
        self.uri_entry_widget.set_entry_value("%s" % self.concept.uri)
        self.concept_datatype_widget.set_active_entry(self.concept_datatype_widget.get_entry_key_for_value(self.concept.datatype))
        self.concept_dimension_widget.set_active_entry(self.concept_dimension_widget.get_entry_key_for_value(self.concept.dimension))

    @transactional
    def save_concept_action(self, widget):
        concept_uri = self.uri_entry_widget.get_entry_value()
        concept_commonname = self.commonname_entry_widget.get_entry_value()

        concept_uuid = None
        if self.concept is not None:
            concept_uuid = self.concept.uuid

        concept = ConceptDAO(concept_uuid,
                             {"commonname": concept_commonname,
                              "url": concept_uri,
                              "datatype": self.concept_datatype_widget.get_active_entry_visible(),
                              "dimension": self.concept_dimension_widget.get_active_entry_visible()})
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
               TreeviewColumn("URI", 2, False),
               TreeviewColumn("Datatype", 3, False),
               TreeviewColumn("Dimension", 4, False)
               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.uri, "%s" % row.datatype, "%s" % row.dimension])


class ConceptMask(AbstractMask):

    def __init__(self, main_window, dao=None):
        super(ConceptMask, self).__init__(main_window, dao, ConceptExtTreeview, ConceptOverviewWindow, ConceptDAO)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(ConceptOverviewWindow(self.main_window, None, self.overview_treeview.reset_treemodel),0, 0, 1, 1)
        self.main_middle_pane.show_all()
