#
# Author: Robert Patel
# This class is used as a controller in a MVC pattern for
# the sell_page window, which prompts in the dashboard when
# a user wishes to sell a recent stock purchase.
#

from PyQt6.QtWidgets import QMessageBox
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from controllers.screen_manager import ScreenManager
from PyQt6.QtWidgets import QMainWindow

