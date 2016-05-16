from . import *


class TextViewWidget(Gtk.Grid):

    def __init__(self, textview=None, model_text=None, title="", width=600, height=100, vexpand=False):
        Gtk.Grid.__init__(self)

        self.width = width
        self.height = height
        self.vexpand = vexpand

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
        scrolledwindow.set_size_request(self.width, self.height)
        #scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(self.vexpand)

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
