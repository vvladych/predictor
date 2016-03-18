from gi.repository import Gtk

from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PersonDAO, PersonnameDAO, PersonnamepartDAO
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.ui_tools import show_info_dialog, show_error_dialog, DateWidget, TextEntryWidget, add_column_to_treeview, DBEnumComboBoxWidget
from predictor.ui.masterdata.mdo_window import MDOWindow


class NamepartEnumComboBoxWidget(DBEnumComboBoxWidget):
    enum_type = "t_person_name_part_role"

    def add_entry(self, p):
        self.model.append(["%s" % p[0], p[1]])


class NameroleEnumComboBoxWidget(DBEnumComboBoxWidget):
    enum_type = "t_person_name_role"

    def add_entry(self, p):
        self.model.append(["%s" % p[0], p[1]])


class PersonExtTreeview(ExtendedTreeView):

    dao_type = PersonDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("Birth date", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.common_name, "%s" % row.birth_date])


class PersonWindow(MDOWindow):

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

        self.birth_date_widget = DateWidget("Birth date")
        self.attach(self.birth_date_widget, 0, row, 2, 1)

        row += 1

        # Row: birth place
        ##self.birth_place_text_entry = TextEntryWidget("Birth place", None, False)
        ##self.attach(self.birth_place_text_entry, 0, row, 2, 1)

        row += 1

        # name
        name_label = Gtk.Label("Name")
        name_label.set_size_request(200, -1)
        name_label.set_alignment(xalign=0, yalign=0.5)
        self.attach(name_label, 0, row, 1, 1)

        row += 1

        self.name_role_combobox_widget = NameroleEnumComboBoxWidget("Name role")
        self.attach(self.name_role_combobox_widget, 0, row, 1, 1)

        name_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        name_add_button.connect("clicked", self.add_name)
        self.attach(name_add_button, 1, row, 1, 1)

        row += 1

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part)
        self.attach(namepart_add_button, 1, row, 1, 1)

        namepart_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_delete_button.connect("clicked", self.delete_name_part)
        self.attach(namepart_delete_button, 2, row, 1, 1)

        self.name_part_combobox_widget = NamepartEnumComboBoxWidget("Namepart")
        self.attach(self.name_part_combobox_widget, 0, row, 1, 1)

        row += 1
        # Row 3: name part value
        self.namepart_role_value_entry = TextEntryWidget(" ")
        self.attach(self.namepart_role_value_entry, 0, row, 2, 1)

        row += 1
        # Row 4: treeview
        self.create_namepart_treeview()
        self.attach(self.nameparts_treeview, 0, row, 4, 1)

        row += 1
        # Row 5
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_dao)
        self.attach(save_button, 1, row, 1, 1)

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.common_name)
        ##self.birth_place_text_entry.set_entry_value(self.person.birth_place)
        if self.dao.birth_date is not None:
            self.birth_date_widget.set_date_from_string("%s-%s-%s" % (self.dao.birth_date.year,
                                                                      self.dao.birth_date.month,
                                                                      self.dao.birth_date.day))
        self.namepart_treestore.clear()

        for name in self.dao.PersontoPersonname:
            personname = PersonnameDAO(name.secDAO_uuid)
            personname.load()
            tree_iter = self.namepart_treestore.append(None, ["%s" % personname.uuid, personname.personname_role, None])
            for namepart in personname.PersonnametoPersonnamepart:
                np = PersonnamepartDAO(namepart.secDAO_uuid)
                np.load()
                self.namepart_treestore.append(tree_iter,["%s" % np.uuid, np.namepart_role, np.namepart_value])

    @transactional
    def save_dao(self, widget):
        common_name = self.common_name_text_entry.get_entry_value()

        person_uuid = None
        if self.dao is not None:
            person_uuid = self.dao.uuid

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

        show_info_dialog(self.main_window , "Person inserted")
        person.save()
        self.dao = person
        self.dao.load()
        self.parent_callback()

    def get_active_name_role(self):
        return self.name_role_combobox_widget.get_active_entry_visible()

    def get_active_namepart_role(self):
        return self.name_part_combobox_widget.get_active_entry_visible()

    def get_active_name_treestore(self):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        return tree_iter

    def add_name(self, widget):
        #name_role_id, name_role_value = self.get_active_name_role()
        name_role_value = self.get_active_name_role()
        self.namepart_treestore.append(None, [None, name_role_value, None])

    def add_name_part(self,widget):
        #(namepart_role_id, namepart_role_value) = self.get_active_namepart_role()
        namepart_role_value = self.get_active_namepart_role()
        tree_iter = self.get_active_name_treestore()

        if tree_iter is None:
            show_error_dialog(self.main_window, "Error: name part cannot be added as root element")
            return

        if self.namepart_treestore.iter_depth(tree_iter) != 0:
            show_error_dialog(self.main_window, "Error: name part can be added to a root element only")
            return

        if self.namepart_role_value_entry.get_entry_value() is None:
            show_error_dialog(self.main_window, "Error: name part cannot be empty!")
            return

        self.namepart_treestore.append(tree_iter,
                                       [None, namepart_role_value,
                                        self.namepart_role_value_entry.get_entry_value()])
        self.namepart_role_value_entry.set_entry_value('')

    # NamePart
    def delete_name_part(self, widget):
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()
        model.remove(tree_iter)

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


class PersonMask(AbstractMask):

    dao_type = PersonDAO
    exttreeview = PersonExtTreeview
    overview_window = PersonWindow

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PersonWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()