from . import *


class ButtonWidget(Gtk.Grid):

    def __init__(self, title, clicked_action=None):
        Gtk.Grid.__init__(self)
        button = Gtk.Button(title)
        button.set_size_request(100, -1)
        button.connect("clicked", clicked_action)
        self.attach(button, 1, 0, 1, 1)
