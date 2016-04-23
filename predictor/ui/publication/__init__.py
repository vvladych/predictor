__author__ = "vvladych"
__date__ = "30.12.2015 23:56:50$"

from gi.repository import Gtk

from predictor.ui.base.abstract_mask import AbstractMask
from predictor.ui.base.exttreeview import ExtendedTreeView, TreeviewColumn
from predictor.ui.ui_tools import show_info_dialog, TextViewWidget, LabelWidget, TextEntryWidget, ComboBoxWidget, TextEntryFileChooserWidget
from predictor.ui.widgets.date_widget import DateWidget
from predictor.model.predictor_model import PublisherDAO, PublicationDAO, PublicationtextDAO, BinaryfileDAO, LanguageDAO, PublicationUnassignedV
from predictor.helpers.transaction_broker import transactional
from predictor.model.DAO import DAOList
import tempfile
import subprocess
from predictor.helpers import config
import os
