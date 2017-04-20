from . import *


class ComboBoxWidget(Gtk.Grid):

    def __init__(self, title, list_to_load, append_func=None, on_changed=None, label_size=200, combobox_size=300, sorted=False):
        Gtk.Grid.__init__(self)
        title_label = Gtk.Label(title)
        title_label.set_size_request(label_size, -1)
        title_label.set_alignment(xalign=0, yalign=0.5)
        self.attach(title_label, 0, 0, 1, 1)
        if sorted==True:
            self.model = Gtk.ListStore(str, str, str)
            self.model.set_sort_column_id(2, Gtk.SortType.DESCENDING)
        else:
            self.model = Gtk.ListStore(str, str)
        self.append_func = append_func
        self.populate_model(list_to_load)
        self.combobox = Gtk.ComboBox.new_with_model_and_entry(self.model)
        self.combobox.set_entry_text_column(1)
        self.combobox.set_size_request(combobox_size, -1)
        self.attach(self.combobox, 1, 0, 1, 1)
        if on_changed is not None:
            self.combobox.connect("changed", on_changed)

    def populate_model(self, list_to_load):
        for p in list_to_load:
            self.add_entry(p)

    def add_entry(self, p):
        if self.append_func is not None:
            self.model.append(self.append_func(p))
        else:
            raise NotImplementedError("add_entry still not implemented!")

    def set_active_entry(self, entry_key):
        if entry_key is not None:
            model_iter = self.model.get_iter_first()

            found = False
            while model_iter is not None and self.model.iter_is_valid(model_iter):
                if entry_key == self.model.get_value(model_iter,0):
                    self.combobox.set_active_iter(model_iter)
                    found = True
                    break
                model_iter = self.model.iter_next(model_iter)
            if not found:
                print("entry_key %s not in model!" % entry_key)

    def get_active_entry(self):
        tree_iter = self.combobox.get_active_iter()
        if tree_iter is not None:
            model = self.combobox.get_model()
            (entry_key, entry_value) = model[tree_iter][:2]
            return entry_key
        return None

    def get_active_entry_visible(self):
        tree_iter = self.combobox.get_active_iter()
        if tree_iter is not None:
            model = self.combobox.get_model()
            entry_key = model[tree_iter][:2]
            return entry_key[1]
        return None

    def get_entry_key_for_value(self, entry_value):
        model_iter = self.model.get_iter_first()

        found = False
        entry_key = None
        while model_iter is not None and self.model.iter_is_valid(model_iter):
            if entry_value == self.model.get_value(model_iter, 1):
                entry_key = self.model.get_value(model_iter, 0)
                found = True
                break
            model_iter = self.model.iter_next(model_iter)
        return entry_key
