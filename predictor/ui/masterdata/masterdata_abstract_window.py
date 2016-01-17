"""
Created on 27.04.2015

@author: vvladych
"""

from gi.repository import Gtk
from predictor.ui.ui_tools import add_column_to_treeview, show_info_dialog, show_error_dialog


class MasterdataAbstractWindow(Gtk.Box):

    def __init__(self, main_window, listmask, addmask):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window = main_window
        self.listmask = listmask
        self.addmask = addmask
        self.specific_name = "unspecified"
        
        self.action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(self.action_area, False, False, 0)

        self.working_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pack_start(self.working_area, False, False, 0)

        self.add_working_area()

    def reset_working_area(self):
        for child in self.working_area.get_children():
            self.working_area.remove(child)

    def add_working_area(self):
        self.reset_working_area()
        self.listmask.populate_object_view_table()
        self.working_area.pack_start(self.listmask, False, False, 0)
        self.working_area.show_all()   

    
class DeleteConfirmationDialog(Gtk.Dialog):
    
    def __init__(self, parent, object_name=None):
        Gtk.Dialog.__init__(self, "Confirm delete %s(s)" % object_name,
                            parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label("Delete chosen %s(s)?" % object_name)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class AbstractAddMask(Gtk.Grid):
    def __init__(self, main_window, reset_callback=None):
        Gtk.Grid.__init__(self)
        self.main_window = main_window
        self.reset_callback = reset_callback
        self.create_layout()
        self.current_object = None

    def add_uuid_row(self, label, row):
        uuid_label = Gtk.Label(label)
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.attach(uuid_label, 0, row, 1, 1)
        self.uuid_text_entry = Gtk.Entry()
        self.uuid_text_entry.set_editable(False)
        self.attach(self.uuid_text_entry, 1, row, 1, 1)

    def add_common_name_row(self, label, row):
        common_name_label = Gtk.Label(label)
        common_name_label.set_justify(Gtk.Justification.LEFT)
        self.attach(common_name_label, 0, row, 1, 1)
        self.attach(self.common_name_text_entry, 1, row, 1, 1)

    def set_masterdata_object(self, masterdata_object=None):
        self.masterdata_object = masterdata_object
        self.load_object(masterdata_object)

    def create_layout(self):
        raise NotImplementedError("create_layout not implemented!")
    
    def create_object_from_mask(self):    
        raise NotImplementedError("create_object_from_mask not implemented!")

    def parent_callback_func(self, widget, cb_func=None):
        self.reset_callback()
        
    def save_current_object(self, widget):
        new_object = self.create_object_from_mask()
        if self.current_object is None:
            new_object.save()
            show_info_dialog("Insert successful")
            self.current_object = new_object
            if self.reset_callback is not None:
                self.reset_callback()
        else:
            if self.current_object != new_object:
                self.current_object.update(new_object)
                self.loaded_organisation = new_object
                show_info_dialog("Update successful")
            else:
                show_info_dialog("Nothing has changed, nothing to update!")

    def load_object(self, object_to_load=None):
        self.current_object = object_to_load
        if object_to_load is not None:
            object_to_load.load()
        self.fill_mask_from_current_object()


class AbstractListMask(Gtk.Box):

    def __init__(self, columnlist, masterdataid):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.masterdataid = masterdataid
        self.store = Gtk.ListStore(*([str]*len(columnlist)))
        self.tree = Gtk.TreeView(self.store)          
        
        column_counter = 0
        for column in columnlist:
            self.tree.append_column(add_column_to_treeview(column["column"], column_counter, column["hide"]))
            column_counter += 1
                    
        self.tree.get_column(0).set_sort_order(Gtk.SortType.ASCENDING)
        self.tree.get_column(0).set_sort_column_id(0)

        self.tree.connect("row-activated", self.on_row_select)
        
        self.tree.set_size_request(200,300)
        self.pack_start(self.tree, False, False, 0)        
        self.add_context_menu_overview_treeview()
        self.populate_object_view_table()

    def add_context_menu_overview_treeview(self):
        menu = Gtk.Menu()
        menu_item_create_new_prediction = Gtk.MenuItem("Add new %s" % self.masterdataid)
        menu_item_create_new_prediction.connect("activate", self.on_menu_item_create_new_masterdataid_click)
        menu.append(menu_item_create_new_prediction)
        menu_item_create_new_prediction.show()
        menu_item_delete_prediction = Gtk.MenuItem("Delete %s" % self.masterdataid)
        menu_item_delete_prediction.connect("activate", self.on_menu_item_delete_masterdataid_click)
        menu.append(menu_item_delete_prediction)
        menu_item_delete_prediction.show()
        self.tree.connect("button_press_event", self.on_treeview_button_press_event, menu)

    def on_treeview_button_press_event(self, treeview, event, widget):
        x = int(event.x)
        y = int(event.y)
        pthinfo = treeview.get_path_at_pos(x, y)
        if event.button == 1:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])

        if event.button == 3:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])
            widget.popup(None, None, None, None, event.button, event.time)
        return True

    def on_menu_item_create_new_masterdataid_click(self, widget):
        raise NotImplementedError("new_masterdataid still not implemented")

    def on_menu_item_delete_masterdataid_click(self, widget):
        (current_object, tree_iter) = self.get_current_object()
        if current_object is not None:
            current_object.delete()
            self.store.remove(tree_iter)

    def populate_object_view_table(self):
        raise NotImplementedError("populate_object_view_table still unimplemented!")

    def delete_object(self):
        raise NotImplementedError("delete_object still unimplemented!")
    
    def get_current_object(self):
        raise NotImplementedError("get_current_object still unimplemented!")

    def on_row_select(self, widget, path, data):
        raise NotImplementedError("on_row_select still not implemented!")
