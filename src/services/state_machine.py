#
# Author: Robert Patel
# This class handles transitions between enum states in the application.
#

from models.command import Command, CommandValue
from app_state import AppState

class StateMachine:

    # Initializes with the given state
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self.last_command = None
        self.current_state = CommandValue.INIT

    # Processes a command and performs state transitions
    def process_command(self, command: Command):
        self.last_command = command
        command_value = command.get_command_value()


        if command_value == CommandValue.INIT:
            self.transition_to(CommandValue.INIT)
            self.app_state.set_current_portfolio(None)
            self.app_state.set_current_user(None)
            self.app_state.is_authenticated = False

        elif command_value == CommandValue.LOGIN:
            self.transition_to(CommandValue.DASHBOARD)

        elif command_value == CommandValue.LOGOUT:
            self.app_state.set_current_user(None)
            self.transition_to(CommandValue.LOGIN)

        elif command_value == CommandValue.EXIT:
            self.transition_to(CommandValue.EXIT)

        elif command_value == CommandValue.DASHBOARD:
            self.transition_to(CommandValue.DASHBOARD)

        elif command_value == CommandValue.PORTFOLIO_VIEW:
            self.transition_to(CommandValue.PORTFOLIO_VIEW)
            
        elif command_value == CommandValue.ANALYSIS:
            self.transition_to(CommandValue.ANALYSIS)

        
        else:
            raise ValueError("Unsupported command.")

    # Returns the current state
    def get_current_state(self):
        return self.current_state

    # Transitions to the new state
    def transition_to(self, new_state):
        self.current_state = new_state
