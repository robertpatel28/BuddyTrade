#
# Author: Robert Patel
# This class handles all authentication operations within the application.
#

import bcrypt
from models.user import User
from services.db_service import DatabaseService

class AuthService:

    # Contructor used for AuthService class.
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    # Hashes the password using bcrypt
    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Verifies a raw password against a hashed one
    def verify_password(self, input_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

    # Logs in a user by checking email and password
    def login_user(self, email: str, password: str) -> User | None:
        user = self.db_service.get_user_by_email(email)
        if user and self.verify_password(password, user.get_hashed_password()):
            user.set_authenticated_status(True)
            return user
        return None

    # Logs out the current user
    def logout_user(self, user: User) -> None:
        user.set_authenticated_status(False)

