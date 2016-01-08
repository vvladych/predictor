"""
Created on 19.05.2015

@author: vvladych
"""

from gi.repository import Gtk

from predictor.ui.ui_tools import add_column_to_treeview


class AbstractDataProcessComponent(object):

    def __init__(self, data_manipulation_component):        
        self.data_manipulation_component=data_manipulation_component

    def create_layout(self, parent_layout_grid, row):
        return self.data_manipulation_component.create_layout(parent_layout_grid, row)


class AbstractDataManipulationComponent(object):

    def __init__(self, overview_component):
        self.overview_component=overview_component

    def create_layout(self, parent_layout_grid, row):
        raise NotImplementedError("create_layout still not implemented")


class AbstractDataOverviewComponent(object):

    def __init__(self, columns):
        self.treemodel=Gtk.ListStore(*([str]*len(columns)))
        self.clean_and_populate_model()
        self.treeview=Gtk.TreeView(self.treemodel)
        for column in columns:
            self.treeview.append_column(add_column_to_treeview(column.column_name, column.ordernum, column.hidden, column.fixed_size))
        self.treeview.connect("row-activated", self.on_row_select)
        #self.treeview.set_size_request(200,150)

    def create_layout(self, parent_layout_grid, row):
        row += 1
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        scrolled_window.set_size_request(600, 200)
        parent_layout_grid.attach(scrolled_window, 0, row, 4, 1)

        return row

    def clean_and_populate_model(self):
        self.treemodel.clear()
        self.populate_model()

    def populate_model(self):
        raise NotImplementedError("populate_model still not implemented!")

    def on_row_select(self, widget, path, data):
        raise NotImplementedError("on_row_select still not implemented!")
