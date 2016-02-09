"""
Created on 17.08.2015

@author: vvladych
"""

from gi.repository import Gtk


class AbstractMask(Gtk.Grid):

    dao_type = None
    overview_window = None
    exttreeview = None
    treecolumns = []
    
    def __init__(self, main_window, dao=None):
        Gtk.Grid.__init__(self)

        self.main_window = main_window

        self.dao = dao

        self.overview_treeview = self.__class__.exttreeview(self.main_window, self.__class__.treecolumns, 0, 20, self.on_row_select, self.new_callback, self.dao)
        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_working_pane.set_size_request(300, 300)
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                       
        self.main_working_pane.add1(self.main_left_pane)
        self.main_working_pane.add2(self.main_middle_pane)
        
        self.create_main_left_pane()
        
    def create_main_left_pane(self):

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(self.overview_treeview)
        scrolledwindow.set_size_request(300, 300)
        
        self.main_left_pane.pack_start(scrolledwindow, False, False, 0)  
        
    def clear_main_middle_pane(self):
        for child in self.main_middle_pane.get_children():
            self.main_middle_pane.remove(child)        

    def new_callback(self):
        pass

    def on_row_select(self, uuid):
        self.clear_main_middle_pane()
        dao = self.__class__.dao_type(uuid)
        dao.load()
        self.main_middle_pane.pack_start(self.__class__.overview_window(self,
                                                                        dao,
                                                                        self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()

