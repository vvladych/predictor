"""
Created on 17.08.2015

@author: vvladych
"""

from . import *


class AbstractMask(Gtk.Paned):

    treecolumns = []
    default_height = 300
    default_width = 200

    def __init__(self, main_window, dao=None, exttreeview=None, overview_window=None, dao_type=None):
        Gtk.Paned.__init__(self)

        self.main_window = main_window
        self.dao = dao
        self.exttreeview = exttreeview
        self.overview_window = overview_window
        self.dao_type = dao_type

        # the middle pane: working area
        self.main_middle_pane = Gtk.Grid()
        #self.main_middle_pane.set_orientation(Gtk.Orientation.HORIZONTAL)
        main_window_width = self.main_window.get_size()[0]
        overview_width = main_window_width / 4
        self.left_pane = Gtk.Grid()
        #self.left_pane.set_orientation(Gtk.Orientation.VERTICAL)
        self.left_pane.set_size_request(overview_width, -1)
        self.populate_left_pane()

        self.main_middle_pane.set_size_request(main_window_width - overview_width , -1)
        self.pack1(self.left_pane, True, True)
        self.pack2(self.main_middle_pane, True, True)

    def replace_exttreeview(self, exttreeview_class):
        self.left_pane.remove(self.overview_treeview)
        self.overview_treeview = exttreeview_class(self.main_window,
                                                   0,
                                                   20,
                                                   self.on_row_select,
                                                   self.new_callback,
                                                   self.edit_callback,
                                                   self.dao)
        self.left_pane.add(self.overview_treeview)
        self.left_pane.show_all()

    def populate_left_pane(self):

        self.overview_treeview = self.exttreeview(self.main_window,
                                                  0,
                                                  20,
                                                  self.on_row_select,
                                                  self.new_callback,
                                                  self.edit_callback,
                                                  self.dao)
        self.left_pane.attach(self.overview_treeview, 0, 0, 1, 2)
        self.filter_combobox_widget = self.add_left_pane_filter()
        #self.left_pane.attach(self.filter_combobox_widget, 0, 1, 1, 1)
        if self.filter_combobox_widget is not None:
            self.left_pane.attach_next_to(self.filter_combobox_widget, self.overview_treeview, Gtk.PositionType.BOTTOM, 1, 1)

    def add_left_pane_filter(self):
        self.overview_treeview = self.exttreeview(self.main_window,
                                                    0,
                                                    20,
                                                    self.on_row_select,
                                                    self.new_callback,
                                                    self.edit_callback,
                                                    self.dao)

        self.overview_treeview.window.set_size_request(self.default_width, self.default_height)

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
        dao = self.dao_type(uuid)
        dao.load()
        if self.overview_window is not None:
            self.main_middle_pane.attach(self.overview_window(self.main_window,
                                                                  dao,
                                                                  self.overview_treeview.reset_treemodel),
                                         0, 0, 1, 1)
            self.main_middle_pane.show_all()
