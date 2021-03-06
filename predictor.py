import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


#from predictor.ui.masterdata.masterdata_mask import MasterdataMask
from predictor.ui.masterdata.main_mask import MDMask
from predictor.ui.prediction.prediction import PredictionMask
from predictor.ui.publication.publication import PublicationMask
from predictor.ui.formmodel.concept import ConceptMask
from predictor.ui.ui_tools import toolbutton_factory


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Predictor")
        self.set_default_size(1200, 800)

        # The main area, grid
        self.main_grid = Gtk.Grid()
        self.main_grid.set_orientation(Gtk.Orientation.VERTICAL)

        self.add(self.main_grid)

        menubar = self.create_menubar()
        self.main_grid.attach(menubar, 0, 0, 1, 1)

        toolbar = self.create_toolbar()
        self.main_grid.attach_next_to(toolbar, menubar, Gtk.PositionType.BOTTOM, 1, 1)

        self.working_area=Gtk.Grid()
        self.working_area.set_orientation(Gtk.Orientation.VERTICAL)
        self.main_grid.attach_next_to(self.working_area, toolbar, Gtk.PositionType.BOTTOM, 1, 1)
        self.set_working_area(action="publication")

        self.statusbar = Gtk.Statusbar()
        self.main_grid.attach_next_to(self.statusbar, self.working_area, Gtk.PositionType.BOTTOM, 1, 1)

    def create_toolbar(self) -> Gtk.Toolbar:
        toolbar = Gtk.Toolbar()
        toolbar.add(toolbutton_factory(Gtk.STOCK_ABOUT, "predictions", self.set_working_area, "prediction"))
        toolbar.add(toolbutton_factory(Gtk.STOCK_EDIT, "publications", self.set_working_area, "publication"))
        toolbar.add(toolbutton_factory(Gtk.STOCK_EXECUTE, "master data", self.set_working_area, "masterdata"))
        toolbar.add(toolbutton_factory(Gtk.STOCK_CONNECT, "concepts", self.set_working_area, "concept"))
        toolbar.add(toolbutton_factory(Gtk.STOCK_QUIT, "quit", self.on_menu_file_quit, None))
        return toolbar

    def create_menubar(self) -> Gtk.MenuBar:
        menubar = Gtk.MenuBar()
        file_menu_entry = Gtk.MenuItem("File")
        menu = Gtk.Menu()
        mitem_quit = Gtk.MenuItem("Quit")
        mitem_quit.connect("activate", self.on_menu_file_quit)
        menu.insert(mitem_quit, 0)
        file_menu_entry.set_submenu(menu)
        menubar.append(file_menu_entry)
        return menubar

    def clean_working_area(self):
        for child in self.working_area.get_children():
            self.working_area.remove(child)

    def set_working_area(self, widget=None, action="publication"):
        self.clean_working_area()
        if action == "masterdata":
            self.working_area.attach(MDMask(self), 0, 0, 1, 1)
        elif action == "prediction":
            self.working_area.attach(PredictionMask(self), 0, 0, 1, 1)
        elif action == "publication":
            self.working_area.attach(PublicationMask(self), 0, 0, 1, 1)
        elif action == "concept":
            self.working_area.attach(ConceptMask(self), 0, 0, 1, 1)
        else:
            print("unimplemented")

        self.working_area.show_all()

    def on_menu_file_quit(self, widget, data=None):
        Gtk.main_quit()


win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
