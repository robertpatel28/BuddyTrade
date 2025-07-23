#
# Author: Robert Patel
# This class is used for managing and navigating the screen transitions.
#
from views.login import Ui_Login
from views.register import Ui_Register
from views.dashboard import Ui_dashboard
from views.analysis import Ui_Analysis
from views.home_logged_out import Ui_Home_Logged_Out
from views.home_logged_in import Ui_Home_Logged_In
from PyQt6.QtWidgets import QMainWindow

class ScreenManager:

    def __init__(self, login_window: QMainWindow, register_window: QMainWindow, dashboard_window: QMainWindow, home_logged_out: QMainWindow, home_logged_in: QMainWindow, analysis: QMainWindow):
        self.login_window = login_window
        self.register_window = register_window
        self.dashboard_window = dashboard_window
        self.home_logged_out = home_logged_out
        self.home_logged_in = home_logged_in
        self.analysis = analysis

    def show_login(self):
        self.hide_all()
        self.login_window.show()

    def show_register(self):
        self.hide_all()
        self.register_window.show()

    def show_dashboard(self):
        self.hide_all()
        self.dashboard_window.show()

    def show_analysis(self):
        self.hide_all()
        self.analysis.show()

    def show_home_logged_in(self):
        self.hide_all()
        self.home_logged_in.show()

    def show_home_logged_out(self):
        self.hide_all()
        self.home_logged_out.show()

    def hide_all(self):
        self.login_window.hide()
        self.register_window.hide()
        self.dashboard_window.hide()
        self.analysis.hide()
        self.home_logged_in.hide()
        self.home_logged_out.hide()