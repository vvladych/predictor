
from gi.repository import Gtk
from predictor.ui.masterdata.person.main_mask import PersonMask
from predictor.ui.masterdata.organisation.main_mask import OrganisationMask


class MDMask(Gtk.Grid):

    def __init__(self, main_window):
        Gtk.Grid.__init__(self)

        self.main_window = main_window

        self.attach(self.mask_chooser(), 0, 0, 1, 1)
        self.working_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.attach(self.working_area, 0, 1, 1, 1)
        self.mask_combo.set_active(0)

    def mask_chooser(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # add empty Label
        vbox.pack_start(Gtk.Label(" "), False, False, 0)

        # add mask chooser
        mask_store = Gtk.ListStore(int, str)
        mask_store.append([1, "Person"])
        mask_store.append([2, "Organisation"])
        mask_store.append([3, "Publisher"])
        mask_store.append([4, "Object catalog"])

        self.mask_combo = Gtk.ComboBox.new_with_model_and_entry(mask_store)
        self.mask_combo.set_entry_text_column(1)
        self.mask_combo.connect("changed", self.mask_combo_changed)
        vbox.pack_start(self.mask_combo, False, False, 0)
        return vbox

    def mask_combo_changed(self, mask_combo):
        if self.mask_combo.get_active() == 0:
            self.set_working_area("person")
        elif self.mask_combo.get_active() == 1:
            self.set_working_area("organisation")
        else:
            print("unimplemented")

    def clean_working_area(self):
        for child in self.working_area.get_children():
            self.working_area.remove(child)

    def set_working_area(self, action="person"):
        self.clean_working_area()
        if action == "person":
            self.working_area.pack_start(PersonMask(self.main_window), True, True, 0)
        elif action == "organisation":
            self.working_area.pack_start(OrganisationMask(self.main_window), True, True, 0)
        else:
            print("unimplemented")
        self.working_area.show_all()