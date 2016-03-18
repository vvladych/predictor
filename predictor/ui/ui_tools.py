
from gi.repository import Gtk
import time
import datetime
from predictor.model.DAO import DAOList
from predictor.helpers.db_connection import enum_retrieve_valid_values


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
    
    
class DateWidget(Gtk.Grid):
    
    def __init__(self, title=None):
        Gtk.Grid.__init__(self)
        if title is not None:
            self.title_label = Gtk.Label(title)
            self.title_label.set_size_request(200, -1)
            self.title_label.set_alignment(xalign=0, yalign=0.5)

        self.day_text_entry = Gtk.Entry()
        self.month_text_entry = Gtk.Entry()
        self.year_text_entry = Gtk.Entry()
        self.create_date_grid(True)

    def create_date_grid(self, show_calendar=False):
        self.set_column_spacing(1)
        self.day_text_entry.set_max_width_chars(2)
        self.day_text_entry.set_width_chars(2)
        self.month_text_entry.set_max_width_chars(2)
        self.month_text_entry.set_width_chars(2)
        self.year_text_entry.set_max_width_chars(4)
        self.year_text_entry.set_width_chars(4)

        column = 0

        if self.title_label is not None:
            self.attach(self.title_label, column, 0, 1, 1)
            column += 1

        self.attach(self.day_text_entry, column, 0, 1, 1)
        self.attach_next_to(Gtk.Label("DD"), self.day_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.month_text_entry, self.day_text_entry, Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(Gtk.Label("MM"), self.month_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.year_text_entry, self.month_text_entry, Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(Gtk.Label("YYYY"), self.year_text_entry, Gtk.PositionType.BOTTOM, 1, 1)

        if show_calendar:
            pick_date_button=Gtk.Button("Pick date")
            self.attach_next_to(pick_date_button, self.year_text_entry, Gtk.PositionType.RIGHT, 1, 1)
            pick_date_button.connect("clicked", self.show_calendar)


    def show_calendar(self, widget ):
        self.calendar_window = Gtk.Dialog()
        self.calendar_window.action_area.hide()
        self.calendar_window.set_decorated(False)
        self.calendar_window.set_property('skip-taskbar-hint', True)
        self.calendar_window.set_size_request(200,200)

        calendar = Gtk.Calendar()
        calendar.connect('day-selected-double-click', self.day_selected, None)
        self.calendar_window.vbox.pack_start(calendar, True, True, 0)
        calendar.show()
        self.calendar_window.run()

    def day_selected(self, calendar, event):
        (year,month,day) = calendar.get_date()
        month += 1
        self.day_text_entry.set_text("%s" % day)
        self.month_text_entry.set_text("%s" % month)
        self.year_text_entry.set_text("%s" % year)
        self.calendar_window.destroy() 

    def set_date_from_string(self, date_as_string):
        tm=time.strptime(date_as_string, "%Y-%m-%d")
        self.day_text_entry.set_text("%s" % tm.tm_mday)
        self.month_text_entry.set_text("%s" % tm.tm_mon)
        self.year_text_entry.set_text("%s" % tm.tm_year)

    def get_date(self):
        if self.day_text_entry.get_text() != '' and \
           self.month_text_entry.get_text() != '' and \
           self.year_text_entry.get_text() != '':
            return datetime.date(int(self.year_text_entry.get_text()),
                                 int(self.month_text_entry.get_text()),
                                 int(self.day_text_entry.get_text()))
        return None


class TextViewWidget(Gtk.Grid):

    def __init__(self, textview, model_text=None):
        Gtk.Grid.__init__(self)
        self.textview = textview
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.model_text = model_text
        self.create_textview_widget()

    def create_textview_widget(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        if self.model_text is not None:
            self.textview.get_buffer().set_text(self.model_text)
        scrolledwindow.add(self.textview)
        self.attach(scrolledwindow, 0, 1, 1, 1)

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

    def __init__(self, title, list_to_load):
        Gtk.Grid.__init__(self)
        title_label = Gtk.Label(title)
        title_label.set_size_request(200, -1)
        title_label.set_alignment(xalign=0, yalign=0.5)
        self.attach(title_label, 0, 0, 1 ,1)
        self.model = Gtk.ListStore(str, str)
        self.populate_model(list_to_load)
        self.combobox = Gtk.ComboBox.new_with_model_and_entry(self.model)
        self.combobox.set_entry_text_column(1)
        self.attach(self.combobox, 1, 0, 1, 1)

    def populate_model(self, list_to_load):
        for p in list_to_load:
            self.add_entry(p)

    def add_entry(self, p):
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


class DAOComboBoxWidget(ComboBoxWidget):
    dao = None
    def __init__(self, title):
        daos = DAOList(self.__class__.dao)
        daos.load()
        ComboBoxWidget.__init__(self, title, daos)


class DBEnumComboBoxWidget(ComboBoxWidget):
    enum_type = None
    def __init__(self, title):
        enumlist = enum_retrieve_valid_values(self.__class__.enum_type)
        ComboBoxWidget.__init__(self, title, enumlist)


def toolbutton_factory(stock_item=None, tooltip_text="", clicked_action=None) -> Gtk.ToolButton:
    toolbutton = Gtk.ToolButton(stock_item)
    toolbutton.set_tooltip_text(tooltip_text)
    toolbutton.connect("clicked", clicked_action)
    return toolbutton
