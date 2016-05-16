from . import *
from .textentry_widget import TextEntryWidget


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
