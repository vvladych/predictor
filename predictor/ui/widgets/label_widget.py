from . import *


class LabelWidget(Gtk.Grid):

    def __init__(self, title):
        Gtk.Grid.__init__(self)
        label = Gtk.Label(title)
        label.set_size_request(200, -1)
        label.set_alignment(xalign=0, yalign=0.5)
        self.attach(label, 0, 0, 1, 1)
