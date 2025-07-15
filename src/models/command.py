#
# Author: Robert Patel
# Command class used to manage state transitions in the application.
#

from enum import Enum
from services.app_state import AppState

# Enum class defining possible commands that control application state transitions.
class CommandValue(Enum):
    INIT = "INIT"                      # Application initializes
    LOGIN = "LOGIN"                    # User logs into the system
    DASHBOARD = "DASHBOARD"            # Navigate to dashboard view
    PORTFOLIO_VIEW = "PORTFOLIO_VIEW"  # View user's portfolio
    ANALYSIS = "ANALYSIS"              # View stock analysis
    LOGOUT = "LOGOUT"                  # User logs out
    EXIT = "EXIT"                      # Exit the application

# Command class encapsulates a user action and optional data for state transitions.
class Command:

    # Constructor for Command
    # @param command: CommandValue enum that represents the type of action
    # @param command_data: Optional dictionary with additional data related to the command
    def __init__(self, command: CommandValue, command_data: dict = None):
        if command is None:
            raise ValueError("Command cannot be None.")
        self.command = command
        self.command_data = command_data or {}

    # Returns the command type
    def get_command(self) -> CommandValue:
        return self.command

    # Returns the optional data associated with the command
    def get_command_data(self) -> dict:
        return self.command_data
