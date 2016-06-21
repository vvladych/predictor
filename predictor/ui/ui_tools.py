from gi.repository import Gtk


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


def attach_next_to_bottom_position(grid, widget_to_attach, widget_next_to):
    grid.attach_next_to(widget_to_attach, widget_next_to, Gtk.PositionType.BOTTOM, 1, 1)


def attach_next_to_bottom_position_expander(grid, widget_to_attach, widget_next_to, expander_label=None):
    expander = Gtk.Expander()
    expander.set_label(expander_label)
    expander.add(widget_to_attach)
    attach_next_to_bottom_position(grid, expander, widget_next_to)