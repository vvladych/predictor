from . import *


class PredictionOriginatorExtTreeview(ExtendedTreeView):

    dao_type = PredictionOriginatorV
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("originator_uuid", 1, True),
               TreeviewColumn("concrete_uuid", 2, True),
               TreeviewColumn("common_name", 3, False, True),
               TreeviewColumn("person", 4, False),
               TreeviewColumn("organisation", 5, False)
               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid,
                                        "%s" % row.originator_uuid,
                                        "%s" % row.concrete_uuid,
                                        "%s" % row.common_name,
                                        "%s" % row.is_person,
                                        "%s" % row.is_organisation
                                        ])

    def on_row_select_callback(self, dao_uuid):
        pass

    @transactional
    def on_menu_item_delete(self, widget):
        row = super(PredictionOriginatorExtTreeview, self).get_selected_row()
        if row is not None:
            prediction = PredictionDAO(row[0])
            prediction.load()
            originator = OriginatorDAO(row[1])
            originator.load()
            prediction.remove_originator(originator)
            originator.delete()
            prediction.save()
            self.fill_treeview(0)
            
    def on_menu_item_new(self, widget):
        pass


class OriginatorAddDialog(BaseAddDialog):

    def set_overview_component(self):
        self.overview_component = PredictionOriginatorExtTreeview(self,
                                                                  0,
                                                                  20,
                                                                  self.noop,
                                                                  self.noop,
                                                                  self.noop,
                                                                  self.prediction)

    def create_layout(self):
        layout_grid = Gtk.Grid()

        originator_label = LabelWidget("Originator")
        layout_grid.attach(originator_label, 0, 0, 1, 1)

        self.person_originator_combobox = ComboBoxWidget("Person",
                                                         DAOList(PersonDAO, True),
                                                         lambda x: ["%s" % x.uuid, "%s" % x.commonname])
        layout_grid.attach_next_to(self.person_originator_combobox, originator_label, Gtk.PositionType.BOTTOM, 1, 1)

        add_person_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_person_button.connect("clicked", self.add_originator, "person")
        layout_grid.attach_next_to(add_person_button, self.person_originator_combobox, Gtk.PositionType.RIGHT, 1, 1)

        self.organisation_originator_combobox = ComboBoxWidget("Organisation",
                                                               DAOList(OrganisationDAO, True),
                                                               lambda x: ["%s" % x.uuid, "%s" % x.commonname])
        layout_grid.attach_next_to(self.organisation_originator_combobox, self.person_originator_combobox, Gtk.PositionType.BOTTOM, 1, 1)

        add_organisation_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_organisation_button.connect("clicked", self.add_originator, "organisation")
        layout_grid.attach_next_to(add_organisation_button, self.organisation_originator_combobox, Gtk.PositionType.RIGHT, 1, 1)

        layout_grid.attach_next_to(self.overview_component, self.organisation_originator_combobox, Gtk.PositionType.BOTTOM, 2, 1)

        return layout_grid

    @transactional
    def add_originator(self, widget, originator_type):
        originator = OriginatorDAO(None, {'short_description':None})
        originator.save()
            
        if originator_type == "person":
            person = PersonDAO(self.person_originator_combobox.get_active_entry())
            person.load()
            originator.add_person(person)
        elif originator_type == "organisation":
            organisation = OrganisationDAO(self.organisation_originator_combobox.get_active_entry())
            organisation.load()
            originator.add_organisation(organisation)
        originator.save()
        self.prediction.add_originator(originator)
        self.prediction.save()
        self.overview_component.fill_treeview(0)

    def delete_action(self, widget=None):
        print("in delete_action")
