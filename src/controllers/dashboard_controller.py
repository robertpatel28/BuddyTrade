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
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QInputDialog
from datetime import datetime
import yfinance as yf


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
        self.ui.btnAddHolding.clicked.connect(self.handle_add_stock)
        self.ui.btnSellHolding.clicked.connect(self.handle_sell_stock)
        self.ui.btnAbout.clicked.connect(self.handle_about)
        self.ui.btnGitHub.clicked.connect(self.handle_github)
        self.ui.btnLinkedIn.clicked.connect(self.handle_linkedin)
        self.ui.btnAddWatchlist.clicked.connect(self.handle_add_watchlist_ticker)

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
        
        try:
            # Retrieves the price data.
            price_data = self.portfolio_controller.get_price_data(ticker)
            
            # Assigns the values for the indicators table and places into a list.
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

            # Loads values into indicators table.
            for row, value in enumerate(values):
                try:
                    display_value = f"{float(value):.2f}"
                except (ValueError, TypeError):
                    display_value = str(value)  # fallback if value is not a number
                self.ui.tblIndicators.setItem(row, 0, QTableWidgetItem(display_value))

            # Assigns values for the recommendations table and places into a list.
            time = self.portfolio_controller.get_datetime()
            golden_cross = self.portfolio_controller.is_golden_cross(ticker, price_data)
            short_momentum = self.portfolio_controller.get_short_momentum(price_data)
            price_over_200_ema = self.portfolio_controller.is_price_over_200_ema(price_data)
            is_rsi_overbought = self.portfolio_controller.get_rsi_strength(price_data)
            is_rsi_oversold = self.portfolio_controller.is_rsi_oversold(price_data)
            is_adx_strong = self.portfolio_controller.is_adx_strong(price_data)
            pullback_opportunity = self.portfolio_controller.pullback_opportunity(ticker, price_data)
            volume_spike = self.portfolio_controller.volume_spike(price_data)
            high_volume = self.portfolio_controller.high_volume(price_data)
            recommendations = [time, golden_cross, short_momentum, price_over_200_ema, is_rsi_overbought, is_rsi_oversold, is_adx_strong,
                            pullback_opportunity, volume_spike, high_volume]
            
            # Loads recommendations into recommendations table.
            table = self.ui.tblTechnicalAnalysis
            row_idx = table.rowCount()
            table.insertRow(row_idx)
            # Fill columns
            for col_idx, value in enumerate(recommendations):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except ValueError as e:
            # handled gracefully by your error helper
            raise ValueError("Ticker not valid.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while analyzing '{ticker}': {str(e)}")

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

    # Opens the github profile.
    def handle_github(self):
        url = "https://github.com/robertpatel28"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    # Opens the linkedin profile.
    def handle_linkedin(self):
        url = "https://www.linkedin.com/in/robertpatel/"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    def handle_about(self):
        url = "https://github.com/robertpatel28/BuddyTrade"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)
    def handle_add_watchlist_ticker(self):

        # Prompt user for input
        ticker, ok = QInputDialog.getText(self.main_window, "Add to Watchlist", "Enter ticker symbol:")
        
        if not ok or not ticker.strip():
            return  # Cancelled or empty

        ticker = ticker.strip().upper()

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Validate shortName and currentPrice
            name = info.get("shortName")
            price = info.get("currentPrice") or info.get("regularMarketPrice")

            if not name or price is None:
                raise ValueError("Invalid ticker")

            # Add to watchlist table
            row_idx = self.ui.tblWatchlist.rowCount()
            self.ui.tblWatchlist.insertRow(row_idx)
            self.ui.tblWatchlist.setItem(row_idx, 0, QTableWidgetItem(ticker))
            self.ui.tblWatchlist.setItem(row_idx, 1, QTableWidgetItem(name))
            self.ui.tblWatchlist.setItem(row_idx, 2, QTableWidgetItem(f"${float(price):.2f}"))

        except Exception:
            QMessageBox.critical(self.main_window, "Invalid Ticker", f"'{ticker}' is not a valid stock ticker.")

    
    def make_table_item(self, value: str) -> QTableWidgetItem:
        return QTableWidgetItem(value)
