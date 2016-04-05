from gi.repository import Gtk

from predictor.ui.ui_tools import show_info_dialog, TextEntryWidget, TextViewWidget, LabelWidget, ComboBoxWidget
from predictor.ui.widgets.date_widget import DateWidget
from predictor.model.DAO import DAOList

from predictor.helpers.transaction_broker import transactional
from predictor.model.predictor_model import PredictionOriginatorV, PredictionDAO, OriginatorDAO, PersonDAO
from predictor.model.predictor_model import OrganisationDAO, PredictionPublicationPublisherV, PublicationDAO
from predictor.model.predictor_model import PublicationPublisherV, PredictionPublisherV, PredictionStatementV, TmstatementDAO
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.base.abstract_mask import AbstractMask

from predictor.ui.prediction.base_add_dialog import BaseAddDialog
from predictor.ui.prediction.tmstatement import TextmodelStatementAddDialog, TextmodelStatementExtTreeview
from predictor.ui.prediction.predpublication import PredictionPublicationAddDialog, PredictionPublicationExtTreeview
from predictor.ui.prediction.originator import PredictionOriginatorExtTreeview, OriginatorAddDialog