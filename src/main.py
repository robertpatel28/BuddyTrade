from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

# Import all UI classes
from views.login import Ui_Login
from views.register import Ui_Register
from views.dashboard import Ui_dashboard
from views.analysis import Ui_Analysis
from views.home_logged_out import Ui_Home_Logged_Out
from views.home_logged_in import Ui_Home_Logged_In
from views.buy_page import Ui_PurchaseWindow
from views.sell_page import Ui_SellWindow

# Import controllers and services
from controllers.login_controller import LoginController
from controllers.registration_controller import RegistrationController
from controllers.screen_manager import ScreenManager
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from controllers.user_controller import UserController
from controllers.home_logged_out_controller import HomeLoggedOutController
from controllers.home_logged_in_controller import HomeLoggedInController
from controllers.analysis_controller import AnalysisController
from controllers.portfolio_controller import PortfolioController
from controllers.buy_page_controller import BuyPageController
from controllers.dashboard_controller import DashboardController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create all windows
    login_window = QMainWindow()
    register_window = QMainWindow()
    dashboard_window = QMainWindow()
    home_logged_out_window = QMainWindow()
    home_logged_in_window = QMainWindow()
    analysis_window = QMainWindow()
    buy_window = QMainWindow()
    sell_window = QMainWindow()

    # Set up all UIs
    login_ui = Ui_Login(); login_ui.setupUi(login_window)
    register_ui = Ui_Register(); register_ui.setupUi(register_window)
    dashboard_ui = Ui_dashboard(); dashboard_ui.setupUi(dashboard_window)
    home_logged_out_ui = Ui_Home_Logged_Out(); home_logged_out_ui.setupUi(home_logged_out_window)
    home_logged_in_ui = Ui_Home_Logged_In(); home_logged_in_ui.setupUi(home_logged_in_window)
    analysis_ui = Ui_Analysis(); analysis_ui.setupUi(analysis_window)
    buy_window_ui = Ui_PurchaseWindow(); buy_window_ui.setupUi(buy_window)
    sell_window_ui = Ui_SellWindow(); sell_window_ui.setupUi(sell_window)

    # Initialize core services and shared state
    db_service = DatabaseService()
    auth_service = AuthService(db_service)
    app_state = AppState()

    # Initialize screen manager
    screen_manager = ScreenManager(
        login_window, register_window, dashboard_window,
        home_logged_out_window, home_logged_in_window,
        analysis_window, sell_window, buy_window
    )

    # Initialize controllers
    portfolio_controller = PortfolioController(db_service)

    user_controller = UserController(
        None, auth_service, db_service, app_state, screen_manager, portfolio_controller
    )

    dashboard_controller = DashboardController(
        dashboard_ui, dashboard_window,
        db_service, auth_service, app_state, screen_manager, user_controller, portfolio_controller
    )

    screen_manager.dashboard_controller = dashboard_controller

    login_controller = LoginController(
        login_ui, login_window,
        db_service, auth_service, app_state,
        user_controller, screen_manager,
        portfolio_controller, dashboard_controller
    )

    registration_controller = RegistrationController(
        register_ui, register_window,
        db_service, auth_service, app_state, user_controller, screen_manager
    )

    analysis_controller = AnalysisController(
        analysis_ui, analysis_window,
        db_service, auth_service, app_state, user_controller, screen_manager, portfolio_controller
    )

    home_logged_in_controller = HomeLoggedInController(
        home_logged_in_ui, home_logged_in_window,
        db_service, auth_service, app_state, user_controller, screen_manager, analysis_controller
    )

    home_logged_out_controller = HomeLoggedOutController(
        home_logged_out_ui, home_logged_out_window,
        db_service, auth_service, app_state, user_controller, screen_manager, analysis_controller
    )

    buy_page_controller = BuyPageController(
        buy_window_ui, buy_window, db_service, screen_manager, app_state
    )

    # Start app at guest home
    home_logged_out_window.show()
    sys.exit(app.exec())
