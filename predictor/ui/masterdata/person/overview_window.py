

from gi.repository import Gtk
from predictor.ui.ui_tools import show_info_dialog, show_error_dialog, DateWidget, TextViewWidget, TextEntryWidget
from predictor.helpers.db_connection import enum_retrieve_valid_values


class PersonOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, person=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.person = person
        self.create_layout()
        if person is not None:
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
        self.common_name_text_entry = TextEntryWidget("Common name", None, False)
        self.attach(self.common_name_text_entry, 0, row, 2, 1)

        row += 1
        # Row: birth date
        birth_date_label = Gtk.Label("Birth Date")
        self.attach(birth_date_label, 0, row, 1, 1)

        self.birth_date_day_text_entry = Gtk.Entry()
        self.birth_date_month_text_entry = Gtk.Entry()
        self.birth_date_year_text_entry = Gtk.Entry()
        self.attach(DateWidget(self.birth_date_day_text_entry,
                               self.birth_date_month_text_entry,
                               self.birth_date_year_text_entry), 1, row, 1, 1)
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
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button, 1, row, 1, 1)

    def load_person(self):
        self.uuid_text_entry.set_entry_value(self.person.uuid)
        self.common_name_text_entry.set_entry_value(self.person.common_name)
        ##self.birth_place_text_entry.set_entry_value(self.person.birth_place)
        if self.person.birth_date is not None:
            self.birth_date_year_text_entry.set_text("%s" % self.person.birth_date.year)
            self.birth_date_month_text_entry.set_text("%s" % self.person.birth_date.month)
            self.birth_date_day_text_entry.set_text("%s" % self.person.birth_date.day)
        self.namepart_treestore.clear()
        """
        for name in self.person.names:
            tree_iter=self.namepart_treestore.append(None,[name.sid, name.name_role, None])
            for namepart in name.nameparts:
                self.namepart_treestore.append(tree_iter,[namepart.sid, namepart.namepart_role, namepart.namepart_value])
        """

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

    def add_name(self, widget):
        print("in add_name")

    def add_name_part(self, widget):
        print("in add_name_part")

    def delete_name_part(self, widget):
        print("in delete_name_part")

    def save_current_object(self, widget):
        print("in save")

    def create_namepart_treeview(self):
        self.namepart_treestore = Gtk.TreeStore(int, str, str)
        self.nameparts_treeview = Gtk.TreeView(self.namepart_treestore)
        self.nameparts_treeview.set_size_request(200, 300)
