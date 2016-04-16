from . import *


class FormstatementExtTreeview(ExtendedTreeView):

    dao_type = PredictionFormstatementV
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("fstate_uuid", 1, True),
               TreeviewColumn("tmstatement_uuid", 2, True),
               TreeviewColumn("concept", 3, False),
               TreeviewColumn("datatype", 4, False),
               TreeviewColumn("fsvalue", 5, False),
               TreeviewColumn("fstatebegin", 6, False),
               TreeviewColumn("fstateend", 7, False),
               TreeviewColumn("PIT begin", 8, False),
               TreeviewColumn("PIT end", 9, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.fstate_uuid,
                                        "%s" % row.tmstatement_uuid,
                                        "%s" % row.concept_commonname,
                                        "%s" % row.concept_datatype,
                                        "%s" % row.fsvalue,
                                        "%s" % row.fstatebegin,
                                        "%s" % row.fstateend,
                                        "%s" % row.tmbegin,
                                        "%s" % row.tmend])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(FormstatementExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            fstate = FstateDAO(row[1])
            prediction.remove_fstate(fstate)
            prediction.save()
            self.fill_treeview(0)


class FormStatementAddDialog(BaseAddDialog):

    def set_overview_component(self):
        self.overview_component = FormstatementExtTreeview(self,
                                                           0,
                                                           20,
                                                           self.load_formstatement,
                                                           self.noop,
                                                           self.noop,
                                                           self.prediction)

    def create_layout(self):

        layout_grid = Gtk.Grid()

        stm_label = LabelWidget("Formstatement(s)")
        layout_grid.attach(stm_label, 0, 0, 1, 1)

        self.concept_combobox = ComboBoxWidget("Concept", DAOList(ConceptDAO, True), lambda x: ["%s" % x.uuid, "%s" % x.commonname], self.concept_combobox_on_changed)
        layout_grid.attach_next_to(self.concept_combobox, stm_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.concept_datatype_entry = TextEntryWidget("Datatype", False)
        layout_grid.attach_next_to(self.concept_datatype_entry, self.concept_combobox, Gtk.PositionType.BOTTOM, 1, 1)

        self.probability_entry = TextEntryWidget("Probability")
        layout_grid.attach_next_to(self.probability_entry, self.concept_datatype_entry, Gtk.PositionType.BOTTOM, 1, 1)

        pit_label = LabelWidget("Point-in-time")
        layout_grid.attach_next_to(pit_label, self.probability_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.state_begin_date_widget = DateWidget("Begin")
        layout_grid.attach_next_to(self.state_begin_date_widget, pit_label, Gtk.PositionType.BOTTOM, 1, 1)

        self.state_end_date_widget = DateWidget("End")
        layout_grid.attach_next_to(self.state_end_date_widget, self.state_begin_date_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.concept_workarea = Gtk.Grid()
        layout_grid.attach_next_to(self.concept_workarea, self.state_end_date_widget, Gtk.PositionType.BOTTOM, 1, 1)
        self.concept_workarea.attach(Gtk.Label(""), 0, 0, 1, 1)
        self.concept_workarea.attach(Gtk.Label(""), 0, 1, 1, 1)
        self.concept_workarea.attach(Gtk.Label(""), 0, 2, 1, 1)

        add_statement_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_statement_button.connect("clicked", self.add_statement_action)
        layout_grid.attach_next_to(add_statement_button, self.concept_workarea , Gtk.PositionType.BOTTOM, 1, 1)

        layout_grid.attach_next_to(self.overview_component, add_statement_button, Gtk.PositionType.BOTTOM, 1, 1)

        return layout_grid

    def get_selected_concept(self):
        concept = ConceptDAO(self.concept_combobox.get_active_entry())
        concept.load()
        return concept

    def concept_combobox_on_changed(self, widget=None):
        concept = self.get_selected_concept()
        self.concept_datatype_entry.set_entry_value(concept.datatype)
        self.clean_concept_workarea()
        if concept.datatype == "numeric":
            self.add_numeric_workarea()
        elif concept.datatype == "literal":
            self.add_literal_workarea()
        elif concept.datatype == "boolean":
            self.add_boolean_workarea()
        else:
            print("unknown concept.datatype %s" % concept.datatype)
        self.concept_workarea.show_all()

    def clean_concept_workarea(self):
        for child in self.concept_workarea.get_children():
            self.concept_workarea.remove(child)

    def add_numeric_workarea(self):
        lbl = LabelWidget("Numeric")
        self.concept_workarea.attach(lbl, 0, 0, 1, 1)
        self.numeric_start_widget = TextEntryWidget("Start value")
        self.concept_workarea.attach_next_to(self.numeric_start_widget, lbl, Gtk.PositionType.BOTTOM, 1, 1)

        self.numeric_end_widget = TextEntryWidget("End value")
        self.concept_workarea.attach_next_to(self.numeric_end_widget, self.numeric_start_widget, Gtk.PositionType.BOTTOM, 1, 1)

    def add_literal_workarea(self):
        lbl = LabelWidget("Literal")
        self.concept_workarea.attach(lbl, 0, 0, 1, 1)
        self.literal_value_widget = TextEntryWidget("Literal value")
        self.concept_workarea.attach_next_to(self.literal_value_widget, lbl, Gtk.PositionType.BOTTOM, 1, 1)

    def add_boolean_workarea(self):
        lbl = LabelWidget("Boolean")
        self.concept_workarea.attach(lbl, 0, 0, 1, 1)
        self.bool_combobox_widget = ComboBoxWidget("Value", ["True", "False"], lambda x: ["%s" % x, "%s" % x])
        self.concept_workarea.attach_next_to(self.bool_combobox_widget, lbl, Gtk.PositionType.BOTTOM, 1, 1)

    @transactional
    def add_statement_action(self, widget):
        # create and save fstate
        fstate = FstateDAO(None, {"fstatedate":"[2010-01-01 14:30, 2010-01-01 15:30]",
                                  "fstatebegin": self.state_begin_date_widget.get_date(),
                                  "fstateend": self.state_end_date_widget.get_date()})
        fstate.save()

        # add fstate to prediction
        self.prediction.add_fstate(fstate)
        self.prediction.save()

        # TODO: add tmstatement to fstate

        concept = self.get_selected_concept()
        if concept.datatype == "numeric":
            fsnumint = Fsnumint(None, {"value": "(%s,%s)" % (self.numeric_start_widget.get_entry_value(), self.numeric_end_widget.get_entry_value())})
            fsnumint.save()
            fstate.add_fsnumint(fsnumint)
        elif concept.datatype == "literal":
            print("literal")
        elif concept.datatype == "boolean":
            fsboolean = Fsboolean(None, {"value": self.bool_combobox_widget.get_active_entry_visible()})
            fsboolean.save()
            fstate.add_fsboolean(fsboolean)
        else:
            print("unknown concept.datatype %s" % concept.datatype)

        # add concept to fstate
        fstate.add_concept(self.get_selected_concept())
        fstate.save()
        show_info_dialog(self.main_window, "statement added")
        self.overview_component.reset_treemodel()

    def load_formstatement(self, widget):
        print("in load_statement")

