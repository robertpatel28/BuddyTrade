#
# Author: Robert Patel
# This class represents the controller for the dashboard GUI.
#
from PyQt6.QtWidgets import QMessageBox
from controllers.user_controller import UserController
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from PyQt6.QtWidgets import QMainWindow
from controllers.screen_manager import ScreenManager

class DashboardController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager

    # Sets up the connections used within the class.
    def setup_connections(self):
        self.ui.btnAnalyze.clicked.connect(self.analyze_ticker)
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnDashboard.clicked.connect(self.load_portfolio)
        self.ui.btnLogin.clicked.connect(self.handle_usersettings)
        self.ui.btnAddHolding.clicked.connect(self.handle_add_stock)
        self.ui.btnSellHolding.clicked.connect(self.handle_sell_stock)

    # Loads the users portfolio from the class.
    def load_portfolio(self):
        user = self.app_state.get_current_user()
        user_email = user.get_email()
        portfolio_data = self.db_service.get_user_portfolio(user_email)

        table = self.ui.tblPortfolio
        table.setRowCount(len(portfolio_data))
        for row_index, row in enumerate(portfolio_data):
            for col_index, value in enumerate(row):
                table.setItem(row_index, col_index, self.make_table_item(str(value)))

    # Opens the analysis window.
    def analyze_ticker(self):
        self.screen_manager.show_analysis()

    # Opens the home window for a logged-in user.
    def handle_home(self):
        self.screen_manager.show_home_logged_in()

    # Opens the window to prompt the user to buy/add a stock to their portfolio.
    def handle_add_stock(self):
        self.screen_manager.show_add_stock()

    # Opens the window to prompt the user to sell a stock.
    def handle_sell_stock(self):
        self.screen_manager.show_sell_stock()

    # Opens the user / settings window.
    def handle_usersettings(self):
        None
        # IN PROGRESS
