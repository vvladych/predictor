from . import *


class ConceptOverviewWindow(Gtk.Grid):

    def __init__(self, main_window, concept=None, callback=None):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(3)
        self.set_column_spacing(3)

        self.main_window = main_window
        self.concept = concept
        self.create_layout()

        if concept is not None:
            self.load_concept()

        self.parent_callback = callback

    def create_layout(self):

        row = 0

        self.attach(LabelWidget("Concept"), 0, row, 1, 1)

    def load_concept(self):
        print("load concept")


class ConceptExtTreeview(ExtendedTreeView):

    dao_type = ConceptDAO
    columns = [TreeviewColumn("uuid", 0, True),
               TreeviewColumn("common name", 1, False),
               TreeviewColumn("URI", 2, False)
               ]

    def append_treedata_row(self, row):
        self.treeview.treemodel.append(["%s" % row.uuid, "%s" % row.commonname, "%s" % row.uri])


class ConceptMask(AbstractMask):

    dao_type = ConceptDAO
    exttreeview = ConceptExtTreeview
    overview_window = ConceptOverviewWindow

    def new_callback(self):
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(ConceptOverviewWindow(self, None, self.overview_treeview.reset_treemodel),
                                         False,
                                         False,
                                         0)
        self.main_middle_pane.show_all()
