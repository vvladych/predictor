from . import *


class TextEntryWidget(Gtk.Grid):

    def __init__(self, title, text_entry_value=None, editable=True, width=300, height=-1):
        Gtk.Grid.__init__(self)
        label = Gtk.Label(title)
        label.set_alignment(xalign=0, yalign=0.5)
        self.textentry = Gtk.Entry()
        self.set_entry_value(text_entry_value)
        self.textentry.set_editable(editable)

        self.textentry.set_size_request(width, height)
        label.set_size_request(200, -1)
        self.attach(label, 0, 0, 1, 1)
        self.attach_next_to(self.textentry, label, Gtk.PositionType.RIGHT, 1, 1)

    def get_entry_value(self):
        return self.textentry.get_text()

    def set_entry_value(self, text_entry_value):
        if text_entry_value is not None:
            self.textentry.set_text("%s" % text_entry_value)
