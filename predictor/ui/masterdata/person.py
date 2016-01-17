"""
Created on 04.05.2015

@author: vvladych
"""
from gi.repository import Gtk

from predictor.ui.masterdata.masterdata_abstract_window import MasterdataAbstractWindow, AbstractAddMask, AbstractListMask
from predictor.model.predictor_model import PersonDAO
from predictor.model.DAO import DAOList
from predictor.ui.ui_tools import show_info_dialog, show_error_dialog

