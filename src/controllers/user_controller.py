#
# Author: Robert Patel
# This class is utilized as a controller in an MVC pattern
# for the User class.
#

import tkinter as tk
from tkinter import messagebox
from models.user import User
from services.db_service import DatabaseService
from services.auth_service import AuthService
from command import Command, CommandValue
from services.app_state import AppState

# Handles interactions regarding the User's information in the database.
class UserController:

    # Constructor for user_controller class.
    def __init__(self, current_user: User, auth_service: AuthService, db_service: DatabaseService, app_state: AppState):
        self.current_user = current_user
        self.auth_service = auth_service
        self.db_service = db_service
        self.app_state = app_state

    # Logins user into the application.
    def login_user(self, email: str, password: str) -> bool:
        conn = self.db_service.connect()
        # Validates the connection.
        if conn is None:
            return None

        # Retrieves the user email.
        user = self.db_service.get_user_by_email(email)

        if not user:
            self.msg_box("User Not Found", "User does not exist under given email.")
            raise ValueError("User not found in database.")
        if user.get_hashed_password() != password:
            self.msg_box("Password Incorrect", "Password does not match password for account under given email.")
            raise ValueError("Incorrect Password.")
        
        # User login successful, transitions to dashboard.
        command = Command(CommandValue.DASHBOARD)
        self.app_state.execute(command)
        return True
        





    # Registers a new user into the database.
    def register_user(self, password: str, first_name: str, last_name: str, email: str) -> bool:
        conn = self.db_service.connect()
        # Validates the connection.
        if conn is None:
            return None
        
        # Validates passed in variables prior to pushing new user information to database.
        if not password:
            self.msg_box("Password Error", "Password is required for user registration.")
            return False
        if not first_name:
            self.msg_box("First Name Error", "First Name is required for user registration.")
            return False
        if not last_name:
            self.msg_box("Last Name Error", "Last Name is required for user registration.")
            return False
        if not email:
            self.msg_box("Email Error", "Email is required for user registration.")
            return False
        # Hashes the password passed in for secure storage in the database.
        hashed_password = self.auth_service.hash_password(password)

        # Verifies that there is not already an account under the same email provided.
        if self.db_service.get_user_by_email(email).lower() == email.lower():
            self.msg_box("Account Already Exists", "An account with this email already exists. Please use a different email.")
            return False
        
        # Pushes the new user information to the database.
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (?, ?, ?, ?)", (first_name, last_name, email, hashed_password))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            # Closes database connection and returns True for a successful user registration.
            conn.close()
            return True


    # Removes a user from the database.
    def remove_user(self, first_name: str, last_name: str, email: str) -> bool:
        pass

    # Helper method for displaying messagebox for errors.
    def msg_box(self, title: str, body: str):
        messagebox.showinfo(title, body)