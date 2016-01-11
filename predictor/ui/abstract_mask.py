"""
Created on 17.08.2015

@author: vvladych
"""

from gi.repository import Gtk


class AbstractMask(Gtk.Grid):
    
    def __init__(self, main_window):
        Gtk.Grid.__init__(self)

        self.main_window = main_window

        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_working_pane.set_size_request(500, 600)
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                       
        self.main_working_pane.add1(self.main_left_pane)
        self.main_working_pane.add2(self.main_middle_pane)
        
        self.create_main_left_pane()
        
    def create_main_left_pane(self):
        self.create_overview_treeview()
        self.add_context_menu_overview_treeview()
        
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(self.overview_treeview)
        scrolledwindow.set_size_request(200, 600)
        
        self.main_left_pane.pack_start(scrolledwindow, False, False, 0)  
        
    def clear_main_middle_pane(self):
        for child in self.main_middle_pane.get_children():
            self.main_middle_pane.remove(child)        

    def create_overview_treeview(self):
        raise NotImplementedError("create_overview_treeview still not implemented")
    
    def add_context_menu_overview_treeview(self):
        raise NotImplementedError("add_context_menu_overview_treeview still not implemented")
