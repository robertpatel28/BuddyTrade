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

class RegistrationController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, user_controller: UserController, screen_manager: ScreenManager):
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.user_controller = user_controller
        self.screen_manager = screen_manager

        self.connect_signals()

    def connect_signals(self):
        self.ui.btnRegister.clicked.connect(self.handle_register)

    def handle_register(self):
        email = self.ui.txtEmail.text().strip()
        verify_email = self.ui.txtVerifyEmail.text().strip()
        password = self.ui.txtPassword.text().strip()
        verify_password = self.ui.txtVerifyPassword.text().strip()
        first_name = self.ui.txtFirstName.text().strip()
        last_name = self.ui.txtLastName.text().strip()

        # Validation
        if email != verify_email:
            self.show_error("Email Mismatch", "Emails do not match.")
            return
        if password != verify_password:
            self.show_error("Password Mismatch", "Passwords do not match.")
            return

        try:
            success = self.user_controller.register_user(password, first_name, last_name, email)
            if success:
                self.show_info("Success", "Account successfully created!")
        except ValueError as e:
            self.show_error("Registration Error", str(e))
        except Exception as e:
            self.show_error("Unexpected Error", str(e))

    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)
