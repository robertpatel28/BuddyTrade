#
# Author: Robert Patel
# This class represents the controller for the dashboard GUI.
#

class DashboardController:
    def __init__(self, ui_dashboard, db_service, user_id):
        self.ui = ui_dashboard
        self.db_service = db_service
        self.user_id = user_id

        self.setup_connections()
        self.load_portfolio()

    # Sets up the connections used within the class.
    def setup_connections(self):
        self.ui.btnAnalyze.clicked.connect(self.analyze_ticker)
        self.ui.btnHome.clicked.connect(self.go_home)
        self.ui.btnDashboard.clicked.connect(self.load_portfolio)
        self.ui.btnLogin.clicked.connect(self.open_profile_settings)

    # Loads the users portfolio from the class.
    def load_portfolio(self):
        
        portfolio_data = self.db_service.get_user_portfolio(self.user_id)

        table = self.ui.tblPortfolio
        table.setRowCount(len(portfolio_data))
        for row_index, row in enumerate(portfolio_data):
            for col_index, value in enumerate(row):
                table.setItem(row_index, col_index, self.make_table_item(str(value)))

    def analyze_ticker(self):
        ticker = self.ui.txtTickerAnalyzer.text().strip()
        if ticker:
            # Call your analysis service here
            print(f"Analyzing {ticker}")
            # Optionally update analysis tables

    def go_home(self):
        # Logic to switch views or update app state
        print("Navigating to Home view")

    def open_profile_settings(self):
        # Logic to navigate to Profile/Settings
        print("Opening profile settings")

    @staticmethod
    def make_table_item(text):
        from PyQt6.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~0x2)  # Make it read-only
        return item
