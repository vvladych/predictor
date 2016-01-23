"""
Created on 04.05.2015

@author: vvladych
"""

from gi.repository import Gtk
from predictor.model.predictor_model import PersonDAO, PersonnamepartDAO
from predictor.model.DAO import DAOList
from predictor.ui.masterdata.masterdata_abstract_window import AbstractAddMask, AbstractListMask
from predictor.ui.ui_tools import DateWidget, add_column_to_treeview, show_info_dialog, show_error_dialog
import datetime


class PersonAddMask(AbstractAddMask):

    def __init__(self, main_window, reset_callback=None):
        self.common_name_text_entry = Gtk.Entry()
        super(PersonAddMask, self).__init__(main_window, reset_callback)
        self.create_layout()
        self.show_all()

    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1, 40)
        self.attach(placeholder_label, 0, -1, 1, 1)

        row = 0
        # Row 0: person uuid
        self.add_uuid_row("Person UUID", row)

        row += 1
        # Row 1: common name
        self.add_common_name_row("Common Name", row)

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
        birth_place_label = Gtk.Label("Birth Place")
        self.attach(birth_place_label, 0, row, 1, 1)
        self.birth_place_text_entry = Gtk.Entry()
        self.attach(self.birth_place_text_entry, 1, row, 1, 1)

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

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button, 2, row, 1, 1)

    def fill_mask_from_current_object(self):
        if self.current_object is not None:
            self.uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
            self.birth_place_text_entry.set_text(self.current_object.birth_place)
            if self.current_object.birth_date is not None:
                self.birth_date_year_text_entry.set_text("%s" % self.current_object.birth_date.year)
                self.birth_date_month_text_entry.set_text("%s" % self.current_object.birth_date.month)
                self.birth_date_day_text_entry.set_text("%s" % self.current_object.birth_date.day)
            self.namepart_treestore.clear()
            for name in self.current_object.names:
                tree_iter=self.namepart_treestore.append(None,[name.sid, name.name_role, None])
                for namepart in name.nameparts:
                    self.namepart_treestore.append(tree_iter,[namepart.sid, namepart.namepart_role, namepart.namepart_value])
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
            self.birth_place_text_entry.set_text("")
            self.birth_date_day_text_entry.set_text("")
            self.birth_date_month_text_entry.set_text("")
            self.birth_date_year_text_entry.set_text("")
            self.namepart_treestore.clear()

    def add_name(self, widget):
        name_role_id, name_role_value = self.get_active_name_role()
        self.namepart_treestore.append(None, [name_role_id, name_role_value, None])

    def get_active_name_role(self):
        name_combobox_iter = self.name_role_combobox.get_active_iter()
        if name_combobox_iter is not None:
            model = self.name_roles_model
            name = model[name_combobox_iter][:2]
        else:
            name = self.name_role_combobox.get_child()
        return name

    def __get_birth_date_from_mask(self):
        if self.birth_date_day_text_entry.get_text() != '' and \
           self.birth_date_month_text_entry.get_text() != '' and \
           self.birth_date_year_text_entry.get_text() != '':
            return datetime.date(int(self.birth_date_year_text_entry.get_text()),
                                 int(self.birth_date_month_text_entry.get_text()),
                                 int(self.birth_date_day_text_entry.get_text()))
        return None

    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if not common_name:
            show_error_dialog("Error: common name cannot be empty!")
            return

        person = PersonDAO(None,
                           self.common_name_text_entry.get_text(),
                           self.__get_birth_date_from_mask())

        # insert person names
        # iterate over names treestore
        name_iter = self.namepart_treestore.get_iter_first()
        while name_iter:
            (person_name_sid, person_name_role) = self.namepart_treestore.get(name_iter, 0, 1)

            namepart_list=[]
            # children of name a nameparts
            if self.namepart_treestore.iter_has_child(name_iter):
                child_iter = self.namepart_treestore.iter_children(name_iter)
                while child_iter:
                    (namepart_sid, namepart_role, namepart_value) = self.namepart_treestore.get(child_iter, 0, 1, 2)
                    namepart = PersonnamepartDAO(namepart_sid, namepart_role, namepart_value, person_name_sid)
                    namepart_list.append(namepart)
                    child_iter = self.namepart_treestore.iter_next(child_iter)

            person.addPersonnamepart(person_name_sid, person_name_role, self.current_object.sid, namepart_list)
            name_iter = self.namepart_treestore.iter_next(name_iter)

        return person

    def get_active_name_treestore(self):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        return tree_iter

    # NamePart
    def delete_name_part(self, widget):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        model.remove(tree_iter)

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
                                       [namepart_role_id,namepart_role_value,
                                        self.namepart_role_value_entry.get_text()])
        self.namepart_role_value_entry.set_text('')

    def get_active_namepart_role(self):
        tree_iter = self.namepart_role_combobox.get_active_iter()
        if tree_iter is not None:
            model = self.namepart_role_combobox.get_model()
            name = model[tree_iter][:2]
        else:
            name = self.namepart_role_combobox.get_child()
        return name

    def create_namepart_treeview(self):
        self.namepart_treestore = Gtk.TreeStore(int, str, str)
        self.nameparts_treeview = Gtk.TreeView(self.namepart_treestore)
        self.nameparts_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.nameparts_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.nameparts_treeview.append_column(add_column_to_treeview("Value", 2, False))
        self.nameparts_treeview.set_size_request(200, 300)
        self.nameparts_treeview.connect("row-activated", self.on_row_selection)

    def on_row_selection(self, treeview, path,column):
        model, treeiter = self.nameparts_treeview.get_selection().get_selected()
        self.namepart_role_combobox.set_active(model[treeiter][0])
        self.namepart_role_value_entry.set_text(model[treeiter][2])

    def populate_namepart_roles_model(self):
        namepart_roles_model = Gtk.ListStore(int, str)
        #namepart_roles_list = enum_retrieve_valid_values("t_person_name_part_role")
        #counter = 0
        #for namepart_role in namepart_roles_list:
        #    namepart_roles_model.append([counter,namepart_role])
        #    counter += 1
        namepart_roles_model.append([1, "a"])
        return namepart_roles_model

    def populate_name_roles_model(self):
        name_roles_model = Gtk.ListStore(int, str)
        #nameroles_list = enum_retrieve_valid_values("t_person_name_role")
        #counter = 0
        #for namerole in nameroles_list:
        #    name_roles_model.append([counter,namerole])
        #    counter += 1
        name_roles_model.append([1, "a"])
        return name_roles_model


class PersonListMask(AbstractListMask):

    treeview_columns=[{"column": "person uuid", "hide": True},
                      {"column": "common name", "hide": False},
                      {"column": "birth date", "hide": False}]

    def __init__(self, main_window, dao_class):
        super(PersonListMask, self).__init__(PersonListMask.treeview_columns,
                                             "person",
                                             main_window,
                                             dao_class,
                                             PersonAddMask)

    def populate_object_view_table(self):
        self.store.clear()
        persons = DAOList(PersonDAO)
        persons.load()
        for p in persons:
            self.store.append(["%s" % p.uuid, "%s" % p.common_name, "%s" % p.birth_date])
