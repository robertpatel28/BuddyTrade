#
# Author: Robert Patel
# This class represents the controller which connects the UI for the user registration window
# and the backend logic for registering a user.
#
# registration_controller.py
from PyQt6.QtWidgets import QMessageBox
from controllers.user_controller import UserController
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from PyQt6.QtWidgets import QMainWindow
from controllers.screen_manager import ScreenManager
from controllers.portfolio_controller import PortfolioController
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import yfinance as yf

class AnalysisController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager, portfolio_controller: PortfolioController):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager
        self.portfolio_controller = portfolio_controller

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.btnDashboard.clicked.connect(self.handle_dashboard)
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnGitHub.clicked.connect(self.handle_github)
        self.ui.btnLinkedIn.clicked.connect(self.handle_linkedin)

    # Opens the home window (guest version)
    def handle_home(self):
        if self.app_state.get_current_user() is None:
            self.screen_manager.show_home_logged_out()
        else:
            self.screen_manager.show_home_logged_in()

    # Method that opens the dashboard. Throws an error when called in this window as user is not logged in.
    def handle_dashboard(self):
        if self.app_state.is_user_authenticated():
            self.screen_manager.show_dashboard()
        else:
            self.show_error("Invalid User", "Please log in or register to access the dashboard tab.")
            self.screen_manager.show_login()
    
    def load_analysis(self, ticker: str):
        stock = yf.Ticker(ticker)
        try:
            info = stock.fast_info  # faster than .info
        except Exception:
            raise ValueError("Ticker does not exist.")
        price_data = self.portfolio_controller.get_price_data(ticker)

        self.ui.txtEma10.setText(f"${self.portfolio_controller.get_ema(price_data, 10):.2f}")
        self.ui.txtEma34.setText(f"${self.portfolio_controller.get_ema(price_data, 34):.2f}")
        self.ui.txtEma50.setText(f"${self.portfolio_controller.get_ema(price_data, 50):.2f}")
        self.ui.txtSma20.setText(f"${self.portfolio_controller.get_sma(price_data, 20):.2f}")
        self.ui.txtSma50.setText(f"${self.portfolio_controller.get_sma(price_data, 50):.2f}")
        self.ui.txtSma100.setText(f"${self.portfolio_controller.get_sma(price_data, 100):.2f}")
        self.ui.txtSma200.setText(f"${self.portfolio_controller.get_sma(price_data, 200):.2f}")
        self.ui.txtAdx.setText(f"{self.portfolio_controller.get_adx(price_data):.2f}")
        self.ui.txtRsi.setText(f"{self.portfolio_controller.get_rsi(price_data):.2f}")
        self.ui.txtRsiVolume.setText(f"{self.portfolio_controller.get_rsi_volume(price_data):.2f}")

        market_cap = self.portfolio_controller.get_market_cap(ticker)
        self.ui.txtMarketCap.setText(self.format_large_number(market_cap) if market_cap else "N/A")

        pe_ratio = self.portfolio_controller.get_pe_ratio(ticker)
        self.ui.txtPriceToEarningsRatio.setText(f"{pe_ratio:.2f}" if isinstance(pe_ratio, (float, int)) else "N/A")

        eps = self.portfolio_controller.get_eps(ticker)
        self.ui.txtEps.setText(f"{eps:.2f}" if isinstance(eps, (float, int)) else "N/A")

        dividend_yield = self.portfolio_controller.get_dividend_yield(ticker)
        self.ui.txtDividendYield.setText(dividend_yield if isinstance(dividend_yield, str) else "N/A")

    # Opens the login window for user to log into application.
    def handle_login(self):
        self.screen_manager.show_login()

    # Method that opens register window.
    def handle_register(self):
        self.screen_manager.show_register()

    def handle_faqs(self):
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
    def handle_support(self):
        None
        # IN PROGRESS

    # Helper method that shows error box with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    # Helper method that shows information box with given title and message.
    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)

    # Helper method for market cap.
    def format_large_number(self, n: float) -> str:
        if n is None:
            return "N/A"
        elif n >= 1_000_000_000_000:
            return f"${n / 1_000_000_000_000:.1f}T"
        elif n >= 1_000_000_000:
            return f"${n / 1_000_000_000:.1f}B"
        elif n >= 1_000_000:
            return f"${n / 1_000_000:.1f}M"
        elif n >= 1_000:
            return f"${n / 1_000:.1f}K"
        return f"${n:.2f}"


