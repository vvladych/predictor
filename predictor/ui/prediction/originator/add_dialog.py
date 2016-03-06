from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog
from predictor.model.DAO import DAOList
from predictor.model.predictor_model import OriginatorDAO, PersonDAO, OrganisationDAO
from predictor.helpers.transaction_broker import transactional
from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview


class PublicationAddDialog(Gtk.Dialog):

    def __init__(self, parent, prediction):
        Gtk.Dialog.__init__(self,
                            "Publication Dialog",
                            parent,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.prediction = prediction
        self.set_default_size(400, 400)
        self.overview_component = PredictionPublicationExtTreeview(self,
                                                                   0,
                                                                   20,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.noop,
                                                                   self.prediction)

        self.create_layout()
        self.show_all()