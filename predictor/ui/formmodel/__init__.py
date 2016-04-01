from gi.repository import Gtk

from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.ui_tools import show_info_dialog, TextViewWidget, DAOComboBoxWidget, LabelWidget, TextEntryWidget, ComboBoxWidget, TextEntryFileChooserWidget

from predictor.model.predictor_model import ConceptDAO
from predictor.helpers.transaction_broker import transactional