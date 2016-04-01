
from gi.repository import Gtk

from predictor.ui.prediction.publication.exttreeview import PredictionPublicationExtTreeview
from predictor.ui.prediction.textmodel.exttreeview import PredictionTextmodelExtTreeview
from predictor.ui.prediction.publication.add_dialog import PublicationAddDialog
from predictor.ui.prediction.originator.add_dialog import OriginatorAddDialog
#from predictor.ui.prediction.textmodel.add_dialog import TextModelAddDialog
from predictor.ui.prediction.textmodel.tmstatement import TextmodelStatementAddDialog, TextmodelStatementExtTreeview
from predictor.ui.ui_tools import TextViewWidget, TextEntryWidget, LabelWidget
from predictor.ui.prediction.originator.exttreeview import PredictionOriginatorExtTreeview

from predictor.model.predictor_model import PredictionDAO, PredictionPublicationPublisherV
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.prediction.add_dialog import PredictionNewDialog
from predictor.ui.ui_tools import show_info_dialog