# data_model.py
import datetime

class DataModel:
    """
    This class holds the essential data for the state machine.
    It does NOT include dynamic methods or triggers from transitions.
    """
    def __init__(self, name, session_id, user_id, session_chat_history=None):
        self.name = name
        self.session_id = session_id
        self.user_id = user_id
        self.session_chat_history = session_chat_history or []
        self.state = 'idle'  # The current state of the user session

        self.timestamp = datetime.datetime.now()
        self.answer_message = None

        self.active_tool = None
        self.active_tool_params = None

        self.counters = {
            'tool_selection': 0,
            'error': 0,
            'completed': 0
        }

        self.error_message = ""
        self.completed_time = None
