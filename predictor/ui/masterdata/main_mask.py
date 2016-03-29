from gi.repository import Gtk

from predictor.ui.masterdata.organisation import OrganisationMask
from predictor.ui.masterdata.person import PersonMask
from predictor.ui.masterdata.publisher import PublisherMask
from predictor.ui.masterdata.country import CountryMask
from predictor.ui.masterdata.language import LanguageMask



class MDMask(Gtk.Grid):

    def __init__(self, main_window):
        Gtk.Grid.__init__(self)

        self.set_column_spacing(5)
        self.set_row_spacing(3)

        self.main_window = main_window

        self.attach(self.mask_chooser(), 0, 0, 1, 1)
        self.working_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.attach(self.working_area, 0, 1, 1, 1)
        self.mask_combo.set_active(0)

    def mask_chooser(self):
        grid = Gtk.Grid()
        grid.attach(Gtk.Label(""), 0, 0, 1, 1)

        mask_store = Gtk.ListStore(int, str)
        mask_store.append([1, "Person"])
        mask_store.append([2, "Organisation"])
        mask_store.append([3, "Publisher"])
        mask_store.append([4, "Country"])
        mask_store.append([5, "Language"])

        self.mask_combo = Gtk.ComboBox.new_with_model_and_entry(mask_store)
        self.mask_combo.set_size_request(200, -1)

        self.mask_combo.set_entry_text_column(1)
        self.mask_combo.connect("changed", self.mask_combo_changed)
        grid.attach(self.mask_combo, 1, 0, 1, 1)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(200, -1)
        placeholder_label.set_hexpand(True)

        grid.attach(placeholder_label, 2, 0, 1, 1)

        return grid

    def mask_combo_changed(self, mask_combo):
        if self.mask_combo.get_active() == 0:
            self.set_working_area("person")
        elif self.mask_combo.get_active() == 1:
            self.set_working_area("organisation")
        elif self.mask_combo.get_active() == 2:
            self.set_working_area("publisher")
        elif self.mask_combo.get_active() == 3:
            self.set_working_area("country")
        elif self.mask_combo.get_active() == 4:
            self.set_working_area("language")
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
        elif action == "publisher":
            self.working_area.pack_start(PublisherMask(self.main_window), True, True, 0)
        elif action == "country":
            self.working_area.pack_start(CountryMask(self.main_window), True, True, 0)
        elif action == "language":
            self.working_area.pack_start(LanguageMask(self.main_window), True, True, 0)
        else:
            print("unimplemented")
        self.working_area.show_all()
