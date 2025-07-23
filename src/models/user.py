#
# Author: Robert Patel
# User class which contains getters/setters for User object.
#
class User:
    
    # Constructs a new User.
    def __init__(self, first_name: str, last_name: str, hashed_password: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.email = email
        self.is_authenticated = False
    
    # Gets first_name
    def get_first_name(self):
        return self.first_name
    
    # Sets first_name
    def set_first_name(self, first_name: str):
        self.first_name = first_name

    # Gets last_name
    def get_last_name(self):
        return self.last_name
    
    # Sets last_name
    def set_last_name(self, last_name: str):
        self.last_name = last_name

    # Gets email
    def get_email(self):
        return self.email
    
    # Sets email
    def set_email(self, email: str):
        self.email = email

    # Gets hashed_password
    def get_hashed_password(self):
        return self.hashed_password
    
    # Gets hashed_password
    def get_hashed_password(self) -> str:
        return self.hashed_password

    # Sets hashed_password
    def set_hashed_password(self, hashed_password: str):
        self.hashed_password = hashed_password
    
    # Sets authentication status
    def set_authenticated_status(self, status: bool):
        self.is_authenticated = status

    # Gets the authentication status
    def is_user_authenticated(self) -> bool:
        return self.is_authenticated
        