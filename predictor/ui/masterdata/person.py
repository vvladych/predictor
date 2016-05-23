from . import *
from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PersonDAO, PersonnameDAO, PersonnamepartDAO
from predictor.helpers.db_connection import enum_retrieve_valid_values


class PersonExtTreeview(ExtendedTreeView):

    dao_type = PersonDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("Common name", 1, False),
               TreeviewColumn("Birth date", 2, False)]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.birth_date])


class PersonWindow(MDOWindow):

    def create_additional_widgets(self, additional_widgets_grid):

        self.birth_date_widget = DateWidget("Birth date")
        additional_widgets_grid.attach(self.birth_date_widget, 0, 0, 1, 1)

        name_label = LabelWidget("Name")
        additional_widgets_grid.attach_next_to(name_label, self.birth_date_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.name_role_combobox_widget = ComboBoxWidget("Name role",
                                                        enum_retrieve_valid_values("t_person_name_role"),
                                                        lambda x: ["%s" % x[0], "%s" % x[1]])
        additional_widgets_grid.attach_next_to(self.name_role_combobox_widget, name_label, Gtk.PositionType.BOTTOM, 1, 1)

        name_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        name_add_button.connect("clicked", self.add_name)
        additional_widgets_grid.attach_next_to(name_add_button, self.name_role_combobox_widget, Gtk.PositionType.RIGHT, 1, 1)

        self.name_part_combobox_widget = ComboBoxWidget("Namepart",
                                                        enum_retrieve_valid_values("t_person_name_part_role"),
                                                        lambda x: ["%s" % x[0], "%s" % x[1]])
        additional_widgets_grid.attach_next_to(self.name_part_combobox_widget, self.name_role_combobox_widget, Gtk.PositionType.BOTTOM, 1, 1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part)
        additional_widgets_grid.attach_next_to(namepart_add_button, self.name_part_combobox_widget, Gtk.PositionType.RIGHT, 1, 1)

        namepart_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_delete_button.connect("clicked", self.delete_name_part)
        additional_widgets_grid.attach_next_to(namepart_delete_button, namepart_add_button, Gtk.PositionType.RIGHT, 1, 1)

        self.namepart_role_value_entry = TextEntryWidget(" ")
        additional_widgets_grid.attach_next_to(self.namepart_role_value_entry, self.name_part_combobox_widget, Gtk.PositionType.BOTTOM, 2, 1)

        self.create_namepart_treeview()
        additional_widgets_grid.attach_next_to(self.nameparts_treeview, self.namepart_role_value_entry, Gtk.PositionType.BOTTOM, 4, 1)

    def load_dao(self):
        self.uuid_text_entry.set_entry_value(self.dao.uuid)
        self.common_name_text_entry.set_entry_value(self.dao.commonname)
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
                           {"commonname": common_name,
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

    def add_name(self, widget):
        self.namepart_treestore.append(None, [None, self.name_role_combobox_widget.get_active_entry_visible(), None])

    def add_name_part(self,widget):
        namepart_role_value = self.name_part_combobox_widget.get_active_entry_visible()
        model, tree_iter = self.nameparts_treeview.get_selection().get_selected()

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

    def __init__(self, main_window, dao=None):
        super(PersonMask, self).__init__(main_window, dao, PersonExtTreeview, PersonWindow, PersonDAO)

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PersonWindow(self.main_window, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()