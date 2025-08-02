#
# Author: Robert Patel
# This class is used as a controller in a MVC pattern for
# the buy_page window, which prompts in the dashboard when
# a user wishes to add a recent stock purchase.
#

from PyQt6.QtWidgets import QMessageBox
from services.db_service import DatabaseService
from services.app_state import AppState
from controllers.screen_manager import ScreenManager
from PyQt6.QtWidgets import QMainWindow
from datetime import datetime

class BuyPageController:

    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, screen_manager: ScreenManager, app_state: AppState):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.screen_manager = screen_manager
        self.app_state = app_state

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnPurchase.clicked.connect(self.purchase_holding)

    # Helper method to ensure data is entered into fields prior to button-call.
    def validate_input(self):
        ticker_input = self.ui.txtTicker.text()
        purchase_price_input = self.ui.txtPurchasePrice.text()
        quantity_input = self.ui.txtQuantity.text()

        if not ticker_input:
            self.show_error("Error!", "Missing Ticker.")
        if not purchase_price_input:
            self.show_error("Error!", "Missing Purchase Price.")
        if not quantity_input:
            self.show_error("Error!", "Missing Quantity.")

        try:
            purchase_price = float(purchase_price_input)
            quantity = int(quantity_input)

            if len(ticker_input) > 5 or not ticker_input.isalpha():
                self.show_error("Error!", "Invalid Ticker.")

            if purchase_price <= 0:
                self.show_error("Error!", "Invalid Purchase Price.")

            if quantity <= 0:
                self.show_error("Error!", "Invalid Quantity.")

        except ValueError:
            self.show_error("Error!", "Invalid Inputs.")

    # Adds a holding to the db.
    def purchase_holding(self):
        try:
            self.validate_input()

            ticker = self.ui.txtTicker.text()
            purchase_price = float(self.ui.txtPurchasePrice.text())
            quantity = int(self.ui.txtQuantity.text())
            date_time = datetime.now()

            portfolio = self.app_state.get_current_portfolio()

            if portfolio is None:
                self.show_error("Error!", "Portfolio could not be loaded as it does not exist.")
            
            portfolio_tuple_id = portfolio.get_portfolio_id()
            portfolio_id = portfolio_tuple_id[0]
            
            success = self.db_service.add_holding(ticker, purchase_price, quantity, date_time, portfolio_id)

            if success:
                self.show_info("Success!", "Stock successfully purchased and added to portfolio.")
                self.screen_manager.show_dashboard()
            else:
                self.show_error("Database Error", "Failed to add holding to the database.")
        except Exception as e:
            self.show_error("Error!", "Could not add stock to database.")

    # Helper method that shows error box with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    # Helper method that shows information box with given title and message.
    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)


