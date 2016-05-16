
from gi.repository import Gtk
from predictor.model.DAO import DAOList


class TreeviewColumn(object):
    
    def __init__(self, column_name, order_number, hidden=True, fixed_size=False):
        self.column_name = column_name
        self.ordernum = order_number
        self.hidden = hidden
        self.fixed_size = fixed_size


def add_column_to_treeview(columnname, counter, hidden, fixed_size=False):
    column = Gtk.TreeViewColumn(columnname)
    if hidden:
        column.set_visible(False)
    renderer = Gtk.CellRendererText()
    column.pack_start(renderer, True)
    column.add_attribute(renderer, "text", counter)
    if fixed_size:
        column.set_fixed_width(50)
    return column


def show_info_dialog(main_window, message):
    info_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
    info_dialog.run()
    info_dialog.destroy()


def show_error_dialog(main_window, message):
    error_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
    error_dialog.run()
    error_dialog.destroy()




def toolbutton_factory(stock_item=None, tooltip_text="", clicked_action=None, data=None) -> Gtk.ToolButton:
    toolbutton = Gtk.ToolButton(stock_item)
    toolbutton.set_tooltip_text(tooltip_text)
    toolbutton.connect("clicked", clicked_action, data)
    return toolbutton
