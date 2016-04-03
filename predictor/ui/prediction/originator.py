from . import *


class PersonOriginatorComboBoxWidget(DAOComboBoxWidget):
    dao = PersonDAO

    def add_entry(self, p):
        self.model.append(["%s" % p.uuid, p.commonname])


class OrganisationOriginatorComboBoxWidget(DAOComboBoxWidget):
    dao = OrganisationDAO

    def add_entry(self, p):
        self.model.append(["%s" % p.uuid, p.commonname])


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


class OriginatorAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Originator Dialog",
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.prediction = prediction
        self.set_default_size(400, 400)
        self.main_window = parent
        self.overview_component = PredictionOriginatorExtTreeview(self,
                                                                  0,
                                                                  20,
                                                                  self.noop,
                                                                  self.noop,
                                                                  self.noop,
                                                                  self.prediction)

        self.create_layout()
        self.show_all()

    def create_layout(self):

        box = self.get_content_area()
        layout_grid = Gtk.Grid()
        box.add(layout_grid)

        originator_label = LabelWidget("Originator")
        layout_grid.attach(originator_label, 0, 0, 1, 1)

        self.person_originator_combobox = PersonOriginatorComboBoxWidget("Person")
        layout_grid.attach_next_to(self.person_originator_combobox, originator_label, Gtk.PositionType.BOTTOM, 1, 1)

        add_person_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_person_button.connect("clicked", self.add_originator, "person")
        layout_grid.attach_next_to(add_person_button, self.person_originator_combobox, Gtk.PositionType.RIGHT, 1, 1)

        self.organisation_originator_combobox = OrganisationOriginatorComboBoxWidget("Organisation")
        layout_grid.attach_next_to(self.organisation_originator_combobox, self.person_originator_combobox, Gtk.PositionType.BOTTOM, 1, 1)

        add_organisation_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_organisation_button.connect("clicked", self.add_originator, "organisation")
        layout_grid.attach_next_to(add_organisation_button, self.organisation_originator_combobox, Gtk.PositionType.RIGHT, 1, 1)

        layout_grid.attach_next_to(self.overview_component, self.organisation_originator_combobox, Gtk.PositionType.BOTTOM, 2, 1)

    def noop(self, widget=None):
        pass

    @transactional
    def add_originator(self, widget, originator_type):
        originator = OriginatorDAO(None, {"short_description":None})
        originator.save()
        originator.load()
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
