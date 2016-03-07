from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog
from predictor.model.DAO import DAOList
from predictor.model.predictor_model import OriginatorDAO, PersonDAO, OrganisationDAO
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.originator.exttreeview import PredictionOriginatorExtTreeview


class OriginatorAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Originator Dialog",
                            None,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.prediction = prediction
        self.set_default_size(400, 400)
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

        row = 0

        originator_label = Gtk.Label("Originator")
        originator_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(originator_label,0,row,1,1)

        row+=1

        person_originator_label = Gtk.Label("Person")
        person_originator_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(person_originator_label,0,row,1,1)


        self.person_combobox_model = self.populate_person_combobox_model()
        self.person_combobox=Gtk.ComboBox.new_with_model_and_entry(self.person_combobox_model)
        self.person_combobox.set_entry_text_column(1)
        layout_grid.attach(self.person_combobox,1,row,1,1)

        self.add_person_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        layout_grid.attach(self.add_person_button,2,row,1,1)
        self.add_person_button.connect("clicked", self.add_person_action)

        row += 1

        organisation_originator_label = Gtk.Label("Organisation")
        organisation_originator_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(organisation_originator_label,0,row,1,1)


        self.organisation_combobox_model = self.populate_organisation_combobox_model()
        self.organisation_combobox=Gtk.ComboBox.new_with_model_and_entry(self.organisation_combobox_model)
        self.organisation_combobox.set_entry_text_column(1)
        layout_grid.attach(self.organisation_combobox,1,row,1,1)

        self.add_organisation_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        layout_grid.attach(self.add_organisation_button,2,row,1,1)
        self.add_organisation_button.connect("clicked", self.add_organisation_action)

        row += 1
        """
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)
        layout_grid.attach(self.delete_button,0,row,1,1)

        row += 1
        """

        layout_grid.attach(self.overview_component, 0, row, 2, 1)


    def populate_person_combobox_model(self):
        combobox_model = Gtk.ListStore(str,str)
        person_list = DAOList(PersonDAO)
        person_list.load()
        for p in person_list:
            combobox_model.append(["%s" % p.uuid, p.common_name])
        return combobox_model

    def populate_organisation_combobox_model(self):
        combobox_model = Gtk.ListStore(str,str)
        organisation_list = DAOList(OrganisationDAO)
        organisation_list.load()
        for p in organisation_list:
            combobox_model.append(["%s" % p.uuid, p.commonname])
        return combobox_model

    def get_active_person(self):
        tree_iter = self.person_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.person_combobox.get_model()
            person_uuid = model[tree_iter][0]
            return person_uuid
        else:
            show_info_dialog(None, "please choose a person!")

    def get_active_organisation(self):
        tree_iter = self.organisation_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.organisation_combobox.get_model()
            organisation_uuid = model[tree_iter][0]
            return organisation_uuid
        else:
            show_info_dialog(None, "please choose a organisation!")

    def noop(self, widget=None):
        pass

    @transactional
    def add_person_action(self, widget=None):
        # load person
        person = PersonDAO(self.get_active_person())
        person.load()
        # insert new originator
        originator = OriginatorDAO(None, {"short_description":None})
        originator.save()
        originator.load()
        # add person to originator
        originator.add_person(person)
        originator.save()
        # add originator to the prediction
        self.prediction.add_originator(originator)
        self.prediction.save()
        self.overview_component.fill_treeview(0)

    @transactional
    def add_organisation_action(self, widget=None):
        # load organisation
        organisation = OrganisationDAO(self.get_active_organisation())
        organisation.load()
        # insert new originator
        originator = OriginatorDAO(None, {"short_description":None})
        originator.save()
        originator.load()
        # add organisation to originator
        originator.add_organisation(organisation)
        originator.save()
        # add originator to the prediction
        self.prediction.add_originator(originator)
        self.prediction.save()
        self.overview_component.fill_treeview(0)

    def delete_action(self, widget=None):
        print("in delete_action")