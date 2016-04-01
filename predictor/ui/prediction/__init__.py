
from gi.repository import Gtk

from predictor.ui.prediction.textmodel.tmstatement import TextmodelStatementAddDialog, TextmodelStatementExtTreeview
from predictor.ui.prediction.predpublication.predpublication import PredictionPublicationExtTreeview, PredictionPublicationAddDialog
from predictor.ui.ui_tools import TextViewWidget, TextEntryWidget, LabelWidget, show_info_dialog
from predictor.ui.prediction.originator.originator import PredictionOriginatorExtTreeview, OriginatorAddDialog

from predictor.model.predictor_model import PredictionDAO, PredictionPublicationPublisherV
from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
