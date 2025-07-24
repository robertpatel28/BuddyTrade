#
# Author: Robert Patel
# This class is used as a controller in a MVC pattern for
# the buy_page window, which prompts in the dashboard when
# a user wishes to add a recent stock purchase.
#

from PyQt6.QtWidgets import QMessageBox
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from controllers.screen_manager import ScreenManager
from PyQt6.QtWidgets import QMainWindow

class BuyPageController:

    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, screen_manager: ScreenManager):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.screen_manager = screen_manager

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnPurchase.clicked.connect(self.purchase_stock)

    # Helper method to ensure data is entered into fields prior to button-call.
    def validate_input(self):
        ticker_input = self.ui.txtTicker.text()
        purchase_price_input = self.ui.txtPurchasePrice.text()
        quantity_input = self.ui.txtQuantity.text()

        if not ticker_input:
            raise ValueError("Missing ticker input.")
        if not purchase_price_input:
            raise ValueError("Missing purchase price.")
        if not quantity_input:
            raise ValueError("Missing quantity.")

        try:
            purchase_price = float(purchase_price_input)
            quantity = int(quantity_input)

            if len(ticker_input) > 5 and not ticker_input.is_alpha():
                raise ValueError("Invalid stock ticker.")

            if purchase_price <= 0:
                raise ValueError("Invalid purchase price.")

            if quantity <= 0:
                raise ValueError("Invalid quantity.")

        except ValueError:
            raise ValueError("Invalid inputs.")

    def purchase_holding(self):
        self.db_service.
