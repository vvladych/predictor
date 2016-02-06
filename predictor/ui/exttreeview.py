from gi.repository import Gtk

from predictor.model.DAO import DAOListl
from predictor.ui.ui_tools import show_info_dialog


class TreedataContainer(object):

    def __init__(self, dao_type):
        self.data = DAOListl(dao_type)

    def get_length(self):
        return len(self.data)

    def load(self):
        self.data.load()


class ExtendedTreeView(Gtk.Grid):

    def __init__(self, columns, start_row=0, rows_per_page=0, on_row_select_callback=None):
        super(ExtendedTreeView, self).__init__()
        self.treedata = TreedataContainer(self.__class__.dao_type)
        self.rows_per_page = rows_per_page
        self.on_row_select_callback = on_row_select_callback
        self.columns = columns

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.treeview = self.create_treeview()

        self.scrolled_window.add(self.treeview)
        self.scrolled_window.set_size_request(600, 600)

        self.total_counter = self.treedata.get_length()

        self.add(self.scrolled_window)
        self.paginator = TreemodelPaginator(self.rows_per_page, self.total_counter)
        self.attach_next_to(self.paginator, self.scrolled_window, Gtk.PositionType.BOTTOM, 1, 1)
        self.fill_treeview(start_row)

    def create_treeview(self):
        return CustomTreeview(self.columns, self.rows_per_page, self.fill_treeview, self.on_row_select_callback, self.on_menu_item_new, self.on_menu_item_delete)

    def fill_treeview(self, start_row):
        self.treeview.treemodel.clear()
        self.treedata.load()
        for row in self.treedata.data[start_row:(self.rows_per_page+start_row)]:
            self.append_treedata_row(row)
        self.paginator.create_pagination_buttons(start_row, self.fill_treeview)

    def append_treedata_row(self, row):
        raise NotImplementedError("append_treedata_row still not implemented")

    def on_menu_item_new(self, widget):
        raise NotImplementedError("on_menu_item_new still not implemented")

    def on_menu_item_delete(self, widget):
        (model, tree_iter) = self.treeview.get_selection().get_selected()
        uuid = model.get_value(tree_iter, 0)
        nd = Gtk.Dialog("Really delete?",
                        None,
                        0,
                        ("OK", Gtk.ResponseType.OK, "CANCEL", Gtk.ResponseType.CANCEL))
        ret = nd.run()
        nd.destroy()
        if ret == Gtk.ResponseType.OK:
            dao = self.__class__.dao_type(uuid)
            dao.delete()
            self.reset_treemodel()
        else:
            show_info_dialog(None, "Canceled")

    def reset_treemodel(self):
        self.treeview = self.create_treeview()
        self.fill_treeview(0)
        for c in self.scrolled_window.get_children():
            self.scrolled_window.remove(c)
        self.scrolled_window.add(self.treeview)
        self.show_all()


class CustomTreeview(Gtk.TreeView):

    def __init__(self, columns, max_rows, parent_refresh_callback, on_row_select_callback, on_menu_new_callback, on_menu_delete_callback):
        self.columns = columns
        self.treemodel = Gtk.ListStore(*([str]*len(columns)))
        super(CustomTreeview, self).__init__(self.treemodel)
        self.add_context_menu_overview_treeview()
        i = 0
        for c in columns:
            self.add_column(c, i)
            i += 1
        self.on_row_select_callback = on_row_select_callback
        self.on_menu_new_callback = on_menu_new_callback
        self.on_menu_delete_callback = on_menu_delete_callback
        self.parent_refresh_callback = parent_refresh_callback

    def reset_treemodel(self):
        self.treemodel = Gtk.ListStore(*([str]*len(self.columns)))

    def add_column(self, c, counter):
        column = Gtk.TreeViewColumn(c.column_name)
        if c.hidden:
            column.set_visible(False)
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", counter)
        self.append_column(column)

    def add_context_menu_overview_treeview(self):
        menu = Gtk.Menu()
        menu_item_add = Gtk.MenuItem("Add...")
        menu_item_add.connect("activate", self.on_menu_item_add_click)
        menu.append(menu_item_add)
        menu_item_add.show()
        menu_item_delete = Gtk.MenuItem("Delete...")
        menu_item_delete.connect("activate", self.on_menu_item_delete_click)
        menu.append(menu_item_delete)
        menu_item_delete.show()
        self.connect("button_press_event", self.on_treeview_button_press_event,menu)

    def on_menu_item_add_click(self, widget):
        self.on_menu_new_callback(widget)

    def on_menu_item_delete_click(self, widget):
        self.on_menu_delete_callback(widget)

    def on_treeview_button_press_event(self, treeview, event, widget):
        x = int(event.x)
        y = int(event.y)
        pthinfo = treeview.get_path_at_pos(x, y)
        if pthinfo is not None:
            treeview.get_selection().select_path(pthinfo[0])

        if event.button == 1:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])
                dao_uuid = self.treemodel.get(self.treemodel.get_iter(pthinfo[0]), 0)[0]
                self.on_row_select_callback(dao_uuid)

        if event.button == 3:
            widget.popup(None, None, None, None, event.button, event.time)
        return True


class TreeviewColumn(object):

    def __init__(self, column_name, order_number, hidden=True, fixed_size=False):
        self.column_name = column_name
        self.ordernum = order_number
        self.hidden = hidden
        self.fixed_size = fixed_size


class TreemodelPaginator(Gtk.Grid):

    def __init__(self, rows_per_page=0, total=0):
        super(TreemodelPaginator, self).__init__()
        self.rows_per_page = rows_per_page
        self.total_buttons = 7
        self.total_counter = total
        self.buttonarray = []

    def create_pagination_buttons(self, current_position, parent_callback):
        for b in self.buttonarray:
            self.remove(b)
        self.buttonarray = []
        self.parent_callback = parent_callback
        self.current_position = current_position
        self.buttonarray = [PaginatorButton("1", 0, False, self.parent_callback)]
        total_pages = divmod(self.total_counter, self.rows_per_page)[0]+1
        if total_pages <= self.total_buttons:
            i = 2
            while i <= total_pages:
                self.buttonarray.append(PaginatorButton("%s" % i, (i-1) * self.rows_per_page, False, self.parent_callback))
                i += 1
        else:
            current_page = int(self.current_position / self.rows_per_page)+1
            self.create_prev_buttons(current_page)
            if current_page != 1:
                self.buttonarray.append(PaginatorButton("%s" % current_page, (current_page-1) * self.rows_per_page, False, self.parent_callback))
            self.create_next_buttons(current_page, total_pages)
        for button in self.buttonarray:
            self.add(button)
        self.show_all()

    def create_prev_buttons(self, current_page):
        if current_page - 1 > 2:
            self.buttonarray.append(PaginatorButton("...", self.rows_per_page * (current_page-3), False, self.parent_callback))
        if current_page > 2:
            p = current_page - 1
            self.buttonarray.append(PaginatorButton("%s" % p, self.rows_per_page * (p-1), False, self.parent_callback))

    def create_next_buttons(self, current_page, total_pages):
        p = current_page + 1
        if p-1 < total_pages:
            self.buttonarray.append(PaginatorButton("%s" % p, self.rows_per_page *(p-1), False, self.parent_callback))
            if total_pages - current_page > 2:
                self.buttonarray.append(PaginatorButton("...", self.rows_per_page * p, False, self.parent_callback))
        self.buttonarray.append(PaginatorButton("%s" % total_pages, self.rows_per_page * (total_pages-1), False, self.parent_callback))


class PaginatorButton(Gtk.Button):

    def __init__(self, caption, position, is_current=False, parent_callback=None):
        super(PaginatorButton, self).__init__(caption)
        self.connect("clicked", self.button_action, position)
        self.position = position
        self.parent_callback = parent_callback

    def button_action(self, widget, data):
        self.parent_callback(self.position)
