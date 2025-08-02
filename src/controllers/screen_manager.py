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
from views.buy_page import Ui_PurchaseWindow
from views.sell_page import Ui_SellWindow
from controllers.dashboard_controller import DashboardController
from PyQt6.QtWidgets import QMainWindow

class ScreenManager:

    # Constructor used for the ScreenManager class.
    def __init__(self, login_window: QMainWindow, register_window: QMainWindow, dashboard_window: QMainWindow, home_logged_out:
                QMainWindow, home_logged_in: QMainWindow, analysis: QMainWindow, sell_page: QMainWindow, buy_page: QMainWindow):
        self.login_window = login_window
        self.register_window = register_window
        self.dashboard_window = dashboard_window
        self.home_logged_out = home_logged_out
        self.home_logged_in = home_logged_in
        self.analysis = analysis
        self.sell_page = sell_page
        self.buy_page = buy_page

    # Opens the login page.
    def show_login(self):
        self.hide_all()
        self.login_window.show()

    # Opens the register page.
    def show_register(self):
        self.hide_all()
        self.register_window.show()

    # Opens the dashboard for the user.
    def show_dashboard(self):
        self.hide_all()
        self.dashboard_window.show()

    # Opens the analysis page.
    def show_analysis(self):
        self.hide_all()
        self.analysis.show()

    # Opens the logged-in home page for user.
    def show_home_logged_in(self):
        self.hide_all()
        self.home_logged_in.show()

    # Opens the guest home page.
    def show_home_logged_out(self):
        self.hide_all()
        self.home_logged_out.show()

    # Opens the user / settings page.
    def show_user_settings(self):
        self.hide_all()

    # Opens the window for purchasing a stock.
    def show_buy_window(self):
        self.hide_all()
        self.buy_page.show()

    # Opens the window for selling a stock.
    def show_sell_window(self):
        self.hide_all()
        self.sell_page.show()

    # Helper method for closing previous windows to maintain efficiency.
    def hide_all(self):
        self.login_window.hide()
        self.register_window.hide()
        self.dashboard_window.hide()
        self.analysis.hide()
        self.home_logged_in.hide()
        self.home_logged_out.hide()