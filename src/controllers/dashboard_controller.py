#
# Author: Robert Patel
# This class represents the controller for the dashboard GUI.
#
from PyQt6.QtWidgets import QMessageBox
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTableWidgetItem
from controllers.portfolio_controller import PortfolioController
from datetime import datetime


class DashboardController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, screen_manager, user_controller, portfolio_controller):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.screen_manager = screen_manager
        self.user_controller = user_controller
        self.portfolio_controller = portfolio_controller

        self.setup_connections()

    # Sets up the connections used within the class.
    def setup_connections(self):
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnDashboard.clicked.connect(self.load_portfolio)
        self.ui.btnLogin.clicked.connect(self.handle_usersettings)
        self.ui.btnAddHolding.clicked.connect(self.handle_add_stock)
        self.ui.btnSellHolding.clicked.connect(self.handle_sell_stock)
        self.ui.btnAnalyze.clicked.connect(
            lambda: self.load_recommendations(self.ui.txtTickerAnalyzer.text())
            )

    # Loads the users portfolio from the class.
    def load_portfolio(self):
        user = self.app_state.get_current_user()
        if not user:
            return
        
        user_email = user.get_email()
        user_id = self.db_service.get_user_id(user_email)  # get user ID
        portfolio_id = self.db_service.get_portfolio_id(user_id)
        portfolio_data = self.db_service.get_user_portfolio(portfolio_id)

        table = self.ui.tblPortfolio
        table.setRowCount(len(portfolio_data))
        for row_index, row in enumerate(portfolio_data):
            gain_or_loss = 0
            values = list(row.values())  # Retrieves the data for each row of data; The purchase information per stock.
            ticker = values[0]
            current_price = self.portfolio_controller.get_current_price(ticker)
            values.append(current_price)
            shares = int(values[2])
            buy_price = float(values[1])
            gain_or_loss = (shares * (current_price - buy_price))
            gain_or_loss_formatted = f"${float(gain_or_loss):.2f}"
            current_price_formatted = f"${float(current_price):.2f}"
            buy_price_formatted = f"${float(buy_price):.2f}"
            values.append(gain_or_loss_formatted)
            values_formatted = [values[0], buy_price_formatted, values[2], current_price_formatted, values[5], values[3]]
            #golden_cross = self.portfolio_controller.get_golden_cross(ticker)
            #values.append(golden_cross)
            for col_index, value in enumerate(values_formatted):
                table.setItem(row_index, col_index, self.make_table_item(str(value)))

    # Loads the recommendations into the corresponding table.
    def load_recommendations(self, ticker: str):
        print(ticker)
        # Retrieves the price data.
        price_data = self.portfolio_controller.get_price_data(ticker)
        
        ema_10 = self.portfolio_controller.get_ema(price_data, 10)
        ema_34 = self.portfolio_controller.get_ema(price_data, 34)
        ema_50 = self.portfolio_controller.get_ema(price_data, 50)
        sma_20 = self.portfolio_controller.get_sma(price_data, 20)
        sma_50 = self.portfolio_controller.get_sma(price_data, 50)
        sma_100 = self.portfolio_controller.get_sma(price_data, 100)
        sma_200 = self.portfolio_controller.get_sma(price_data, 200)
        adx = self.portfolio_controller.get_adx(price_data)
        rsi = self.portfolio_controller.get_rsi(price_data)
        rsi_volume = self.portfolio_controller.get_rsi_volume(price_data)
        values = [ema_10, ema_34, ema_50, sma_20, sma_50, sma_100, sma_200, adx, rsi, rsi_volume]
        # Step 1: Get current row count
        for row, value in enumerate(values):
            try:
                display_value = f"{float(value):.2f}"
            except (ValueError, TypeError):
                display_value = str(value)  # fallback if value is not a number
            self.ui.tblIndicators.setItem(row, 0, QTableWidgetItem(display_value))


    # Opens the analysis window.
    def analyze_ticker(self):
        self.screen_manager.show_analysis()

    # Opens the home window for a logged-in user.
    def handle_home(self):
        self.screen_manager.show_home_logged_in()

    # Opens the window to prompt the user to buy/add a stock to their portfolio.
    def handle_add_stock(self):
        self.screen_manager.show_buy_window()

    # Opens the window to prompt the user to sell a stock.
    def handle_sell_stock(self):
        self.screen_manager.show_sell_window()

    # Opens the user / settings window.
    def handle_usersettings(self):
        None
        # IN PROGRESS
    
    def make_table_item(self, value: str) -> QTableWidgetItem:
        return QTableWidgetItem(value)
