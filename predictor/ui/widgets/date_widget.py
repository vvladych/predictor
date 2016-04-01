from gi.repository import Gtk
import time
import datetime


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
