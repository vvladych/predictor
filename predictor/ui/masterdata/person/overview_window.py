

from gi.repository import Gtk
from predictor.ui.ui_tools import show_info_dialog, show_error_dialog, DateWidget, TextViewWidget, TextEntryWidget, add_column_to_treeview
from predictor.helpers.db_connection import enum_retrieve_valid_values
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PersonDAO, PersonnameDAO, PersonnamepartDAO



class PersonOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, person=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.person = person
        self.create_layout()
        if person is not None:
            self.person.load()
            self.load_person()
        self.parent_callback = callback

    def create_layout(self):

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: person uuid
        self.uuid_text_entry = TextEntryWidget("UUID", None, False)
        self.attach(self.uuid_text_entry, 0, row, 2, 1)

        row += 1
        # Row 1: common name
        self.common_name_text_entry = TextEntryWidget("Common name", None, True)
        self.attach(self.common_name_text_entry, 0, row, 2, 1)

        row += 1
        # Row: birth date
        birth_date_label = Gtk.Label("Birth Date")
        self.attach(birth_date_label, 0, row, 1, 1)

        self.birth_date_widget = DateWidget()
        self.attach(self.birth_date_widget, 1, row, 1, 1)

        row += 1

        # Row: birth place
        ##self.birth_place_text_entry = TextEntryWidget("Birth place", None, False)
        ##self.attach(self.birth_place_text_entry, 0, row, 2, 1)

        row += 1

        # name
        name_label = Gtk.Label("Name")
        self.attach(name_label, 0, row, 1, 1)

        self.name_roles_model = self.populate_name_roles_model()
        self.name_role_combobox = Gtk.ComboBox.new_with_model_and_entry(self.name_roles_model)
        self.name_role_combobox.set_entry_text_column(1)
        self.name_role_combobox.set_active(0)
        self.attach(self.name_role_combobox, 1, row, 1, 1)

        name_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        name_add_button.connect("clicked", self.add_name)
        self.attach(name_add_button, 2, row, 1, 1)

        row += 1
        # name part role
        namepart_label = Gtk.Label("Name part")
        self.attach(namepart_label, 0, row, 1, 1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part)
        self.attach(namepart_add_button, 2, row, 1, 1)

        namepart_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_delete_button.connect("clicked", self.delete_name_part)
        self.attach(namepart_delete_button, 3, row, 1, 1)

        self.namepart_roles_model = self.populate_namepart_roles_model()
        self.namepart_role_combobox = Gtk.ComboBox.new_with_model_and_entry(self.namepart_roles_model)
        self.namepart_role_combobox.set_entry_text_column(1)
        self.namepart_role_combobox.set_active(0)

        self.attach(self.namepart_role_combobox, 1, row, 1, 1)

        row += 1
        # Row 3: name part value
        self.namepart_role_value_entry = Gtk.Entry()
        self.attach(self.namepart_role_value_entry, 1, row, 1, 1)

        row += 1
        # Row 4: treeview
        self.create_namepart_treeview()
        self.attach(self.nameparts_treeview, 0, row, 4, 1)

        row += 1
        # Row 5
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_person_action)
        self.attach(save_button, 1, row, 1, 1)

    def load_person(self):
        self.uuid_text_entry.set_entry_value(self.person.uuid)
        self.common_name_text_entry.set_entry_value(self.person.common_name)
        ##self.birth_place_text_entry.set_entry_value(self.person.birth_place)
        if self.person.birth_date is not None:
            self.birth_date_widget.set_date_from_string("%s-%s-%s" % (self.person.birth_date.year,
                                                                      self.person.birth_date.month,
                                                                      self.person.birth_date.day))
        self.namepart_treestore.clear()

        for name in self.person.PersontoPersonname:
            personname = PersonnameDAO(name.secDAO_uuid)
            personname.load()
            tree_iter = self.namepart_treestore.append(None, ["%s" % personname.uuid, personname.personname_role, None])
            for namepart in personname.PersonnametoPersonnamepart:
                np = PersonnamepartDAO(namepart.secDAO_uuid)
                np.load()
                self.namepart_treestore.append(tree_iter,["%s" % np.uuid, np.namepart_role, np.namepart_value])


    def populate_namepart_roles_model(self):
        namepart_roles_model = Gtk.ListStore(int, str)
        namepart_roles_list = enum_retrieve_valid_values("t_person_name_part_role")
        counter = 0
        for namepart_role in namepart_roles_list:
            namepart_roles_model.append([counter,namepart_role])
            counter += 1
        return namepart_roles_model

    def populate_name_roles_model(self):
        name_roles_model = Gtk.ListStore(int, str)
        nameroles_list = enum_retrieve_valid_values("t_person_name_role")
        counter = 0
        for namerole in nameroles_list:
            name_roles_model.append([counter,namerole])
            counter += 1
        return name_roles_model

    @transactional
    def save_person_action(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        person_uuid = None
        if self.person is not None:
            person_uuid = self.person.uuid

        person = PersonDAO(person_uuid,
                           {"common_name": common_name,
                            "birth_date": self.birth_date_widget.get_date()})
        name_iter = self.namepart_treestore.get_iter_first()
        while name_iter:
            (person_name_uuid, person_name_role) = self.namepart_treestore.get(name_iter, 0, 1)
            personname = PersonnameDAO(person_name_uuid, {"personname_role":person_name_role})
            personname.save()
            person.add_personname(personname)

            # children of name a nameparts
            if self.namepart_treestore.iter_has_child(name_iter):
                child_iter = self.namepart_treestore.iter_children(name_iter)
                while child_iter:
                    (namepart_uuid, namepart_role, namepart_value) = self.namepart_treestore.get(child_iter, 0, 1, 2)
                    namepart = PersonnamepartDAO(namepart_uuid, {"namepart_role":namepart_role, "namepart_value":namepart_value})
                    namepart.save()
                    personname.add_personnamepart(namepart)
                    personname.save()
                    child_iter = self.namepart_treestore.iter_next(child_iter)

            person.add_personname(personname)
            person.save()
            name_iter = self.namepart_treestore.iter_next(name_iter)

        show_info_dialog(None, "Person inserted")
        self.person = person
        self.person.load()
        self.parent_callback()

    def get_active_name_role(self):
        name_combobox_iter = self.name_role_combobox.get_active_iter()
        if name_combobox_iter is not None:
            model = self.name_roles_model
            name = model[name_combobox_iter][:2]
        else:
            name = self.name_role_combobox.get_child()
        return name

    def get_active_name_treestore(self):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        return tree_iter

    def add_name(self, widget):
        name_role_id, name_role_value = self.get_active_name_role()
        self.namepart_treestore.append(None, [None, name_role_value, None])

    def add_name_part(self,widget):
        (namepart_role_id, namepart_role_value) = self.get_active_namepart_role()
        tree_iter = self.get_active_name_treestore()

        if tree_iter is None:
            show_error_dialog(self.main_window, "Error: name part cannot be added as root element")
            return

        if self.namepart_treestore.iter_depth(tree_iter) != 0:
            show_error_dialog(self.main_window, "Error: name part can be added to a root element only")
            return

        self.namepart_treestore.append(tree_iter,
                                       [None, namepart_role_value,
                                        self.namepart_role_value_entry.get_text()])
        self.namepart_role_value_entry.set_text('')

    # NamePart
    def delete_name_part(self, widget):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        model.remove(tree_iter)

    def get_active_namepart_role(self):
        tree_iter = self.namepart_role_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.namepart_role_combobox.get_model()
            name = model[tree_iter][:2]
        else:
            name = self.namepart_role_combobox.get_child()
        return name

    def create_namepart_treeview(self):
        self.namepart_treestore = Gtk.TreeStore(str, str, str)
        self.nameparts_treeview = Gtk.TreeView(self.namepart_treestore)
        self.nameparts_treeview.append_column(add_column_to_treeview("UUID", 0, True))
        self.nameparts_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.nameparts_treeview.append_column(add_column_to_treeview("Value", 2, False))
        self.nameparts_treeview.set_size_request(200, 300)
        self.nameparts_treeview.connect("row-activated", self.on_row_selection)

    def on_row_selection(self, treeview, path,column):
        model, treeiter = self.nameparts_treeview.get_selection().get_selected()
        self.namepart_role_combobox.set_active(model[treeiter][0])
        self.namepart_role_value_entry.set_text(model[treeiter][2])
