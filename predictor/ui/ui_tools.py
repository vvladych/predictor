
from gi.repository import Gtk
from predictor.model.DAO import DAOList


class TreeviewColumn(object):
    
    def __init__(self, column_name, order_number, hidden=True, fixed_size=False):
        self.column_name = column_name
        self.ordernum = order_number
        self.hidden = hidden
        self.fixed_size = fixed_size


def add_column_to_treeview(columnname, counter, hidden, fixed_size=False):
    column = Gtk.TreeViewColumn(columnname)
    if hidden:
        column.set_visible(False)
    renderer = Gtk.CellRendererText()
    column.pack_start(renderer, True)
    column.add_attribute(renderer, "text", counter)
    if fixed_size:
        column.set_fixed_width(50)
    return column


def show_info_dialog(main_window, message):
    info_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
    info_dialog.run()
    info_dialog.destroy()


def show_error_dialog(main_window, message):
    error_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
    error_dialog.run()
    error_dialog.destroy()


class TextViewWidget(Gtk.Grid):

    def __init__(self, textview=None, model_text=None, title=""):
        Gtk.Grid.__init__(self)

        label = Gtk.Label(title)
        label.set_alignment(xalign=0, yalign=0.5)
        label.set_size_request(200, -1)

        if textview is None:
            self.textview = Gtk.TextView()
        else:
            self.textview = textview

        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.model_text = model_text

        self.attach(label, 0, 0, 1, 1)
        self.attach_next_to(self.create_textview_widget(), label, Gtk.PositionType.RIGHT, 1, 1)

    def create_textview_widget(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_size_request(600, 100)
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        if self.model_text is not None:
            self.textview.get_buffer().set_text(self.model_text)
        scrolledwindow.add(self.textview)
        return scrolledwindow

    def get_textview_text(self):
        textbuffer = self.textview.get_buffer()
        return textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), True)
    
    def set_text(self, text):
        if text is not None:
            textbuffer = self.textview.get_buffer()
            textbuffer.set_text("%s" % text)


class TextEntryWidget(Gtk.Grid):

    def __init__(self, title, text_entry_value=None, editable=True):
        Gtk.Grid.__init__(self)
        label = Gtk.Label(title)
        label.set_alignment(xalign=0, yalign=0.5)
        self.textentry = Gtk.Entry()
        self.set_entry_value(text_entry_value)
        self.textentry.set_editable(editable)

        self.textentry.set_size_request(300, -1)
        label.set_size_request(200, -1)
        self.attach(label, 0, 0, 1, 1)
        self.attach_next_to(self.textentry, label, Gtk.PositionType.RIGHT, 1, 1)

    def get_entry_value(self):
        return self.textentry.get_text()

    def set_entry_value(self, text_entry_value):
        if text_entry_value is not None:
            self.textentry.set_text("%s" % text_entry_value)


class ComboBoxWidget(Gtk.Grid):

    def __init__(self, title, list_to_load, append_func=None):
        Gtk.Grid.__init__(self)
        title_label = Gtk.Label(title)
        title_label.set_size_request(200, -1)
        title_label.set_alignment(xalign=0, yalign=0.5)
        self.attach(title_label, 0, 0, 1 ,1)
        self.model = Gtk.ListStore(str, str)
        self.append_func = append_func
        self.populate_model(list_to_load)
        self.combobox = Gtk.ComboBox.new_with_model_and_entry(self.model)
        self.combobox.set_entry_text_column(1)
        self.combobox.set_size_request(300, -1)
        self.attach(self.combobox, 1, 0, 1, 1)

    def populate_model(self, list_to_load):
        for p in list_to_load:
            self.add_entry(p)

    def add_entry(self, p):
        if self.append_func is not None:
            self.model.append(self.append_func(p))
        else:
            raise NotImplementedError("add_entry still not implemented!")

    def set_active_entry(self, entry_key):
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


class TextEntryFileChooserWidget(TextEntryWidget):

    def __init__(self, title):
        TextEntryWidget.__init__(self, title)
        choose_file_button = Gtk.Button("Choose File")
        choose_file_button.connect("clicked", self.choose_file)
        self.attach(choose_file_button, 2, 0, 1, 1)

    def choose_file(self, widget):
        file_chooser_dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                                    Gtk.FileChooserAction.OPEN,
                                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                     "Select", Gtk.ResponseType.OK))
        file_chooser_dialog.set_default_size(400, 400)
        response = file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.set_entry_value(file_chooser_dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")
        else:
            print("undefined")
        file_chooser_dialog.destroy()


class LabelWidget(Gtk.Grid):

    def __init__(self, title):
        Gtk.Grid.__init__(self)
        label = Gtk.Label(title)
        label.set_size_request(200, -1)
        label.set_alignment(xalign=0, yalign=0.5)
        self.attach(label, 0, 0, 1, 1)


def toolbutton_factory(stock_item=None, tooltip_text="", clicked_action=None, data=None) -> Gtk.ToolButton:
    toolbutton = Gtk.ToolButton(stock_item)
    toolbutton.set_tooltip_text(tooltip_text)
    toolbutton.connect("clicked", clicked_action, data)
    return toolbutton
