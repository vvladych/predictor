"""
Created on 17.08.2015

@author: vvladych
"""

from gi.repository import Gtk


class AbstractMask(Gtk.Paned):

    dao_type = None
    overview_window = None
    exttreeview = None
    treecolumns = []
    default_height = 300
    default_width = 200
    
    def __init__(self, main_window, dao=None):
        Gtk.Paned.__init__(self)

        self.main_window = main_window

        self.dao = dao

        self.overview_treeview = self.__class__.exttreeview(self.main_window,
                                                            0,
                                                            20,
                                                            self.on_row_select,
                                                            self.new_callback,
                                                            self.edit_callback,
                                                            self.dao)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.overview_treeview.set_size_request(self.__class__.default_width / 3, -1)
        self.main_middle_pane.set_size_request(self.__class__.default_width / 3 * 2, -1)
                       
        self.pack1(self.overview_treeview, True, True)
        self.pack2(self.main_middle_pane, True, True)
        
    def clear_main_middle_pane(self):
        for child in self.main_middle_pane.get_children():
            self.main_middle_pane.remove(child)        

    def new_callback(self):
        pass

    def edit_callback(self):
        pass

    def on_row_select(self, uuid):
        self.clear_main_middle_pane()
        dao = self.__class__.dao_type(uuid)
        dao.load()
        if self.__class__.overview_window is not None:
            self.main_middle_pane.pack_start(self.__class__.overview_window(self.main_window,
                                                                            dao,
                                                                            self.overview_treeview.reset_treemodel),
                                             False,
                                             False,
                                             0)
            self.main_middle_pane.show_all()
