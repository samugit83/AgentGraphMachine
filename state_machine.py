# state_machine.py
import logging
import json
from models.models import call_model
from tools.tools import select_tool
from data_model import DataModel
from tools.prompts import ANSWER_WITH_PARAMS_PROMPT


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StateMachineModel:
    """
    This class wraps a DataModel instance and exposes a 'state' property
    so that the transitions library can manage state changes.
    """

    def __init__(self, data_model: DataModel):
        self.data = data_model

    @property
    def state(self):
        """
        The transitions library uses model.state to get/set the current state.
        We store that in self.data.state so it's preserved when pickled.
        """
        return self.data.state

    @state.setter
    def state(self, value):
        self.data.state = value
    
    def reset_initial_data(self):
        self.data.active_tool = None
        self.data.active_tool_params = None
        self.data.error_message = None

    def on_enter_idle(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: idle")
        self.reset_initial_data()

    def on_enter_tool_selection(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: tool_selection")
        self.data.counters['tool_selection'] += 1

        tool_list = [
            {
                'tool_name': 'out_of_scope_question',
                'tool_description': 'Any question that is not about medicine, health, and pharmacy.'
            },
            {
                "tool_name": "user_diagnosis",
                "tool_description": "This tool assists in diagnosing a user's condition based on their reported symptoms, age, gender, and medical history.",
                "tool_params": [
                    {
                        "param_name": "symptoms",
                        "param_type": "string",
                        "param_description": "A detailed list of the symptoms the user is currently experiencing.",
                        "param_value": None
                    },
                    {
                        "param_name": "age",
                        "param_type": "string",
                        "param_description": "The age of the user.",
                        "param_value": None
                    },
                    {
                        "param_name": "history",
                        "param_type": "string",
                        "param_description": "The user's relevant medical history and past conditions.",
                        "param_value": None
                    }
                ]
            },
            {
                "tool_name": "state_selection",
                "tool_description": "This is a tool for demonstration purposes only to transition from one state to another in the state machine. The user simply asks to switch to a specific state in the state machine.",
                "tool_params": [
                    {
                        "param_name": "state_name",
                        "param_type": "string",
                        "param_description": "Il nome dello stato da cui passare",
                        "enums": ["state_a", "state_b", "state_c", "state_d", "state_e"],
                        "param_value": None
                    }
                ]
            }
        ]

        tool_response = select_tool(self, self.data.session_chat_history, tool_list, self.data.active_tool_params)

        logger.info(f"\n[Session {self.data.session_id}] 🟣 Tool response:\n{json.dumps(tool_response, indent=4)}\n")
        if self.data.state == 'waiting_user_params':
            return

        match self.data.active_tool:
            case 'out_of_scope_question':
                self.exec_out_of_scope_question()
            case 'user_diagnosis':
                self.exec_user_diagnosis()
            case 'no_tool_selected':
                self.exec_general_answer()
            case 'state_selection':
                self.exec_state_selection()
            case _:
                self.error_occurred()
                self.data.error_message = "Invalid tool selected"
        
    def on_enter_out_of_scope_question(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: out_of_scope_question")
        self.data.answer_message = "I'm sorry, but I cannot answer this question."

    def on_enter_user_diagnosis(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: user_diagnosis")
        GENERATED_PROMPT = ANSWER_WITH_PARAMS_PROMPT.format(
            active_tool_params=self.data.active_tool_params,
            session_chat_history=self.data.session_chat_history
        )
        response = call_model(chat_history=[{"role": "user", "content": GENERATED_PROMPT}], model="gpt-4o") 
        self.data.answer_message = response
        self.complete()

    def on_enter_state_selection(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: state_selection")
        response = call_model(chat_history=self.data.session_chat_history, model="gpt-4o") 
        self.data.state = self.data.active_tool_params[0]['param_value']
        logger.info(f"🟡🟡🟡 You switch to state {self.data.state}!")
        self.data.answer_message = f"🟡🟡🟡 You switch to state {self.data.state}!"
        self.complete()

    def on_enter_general_answer(self):
        logger.info(f"[Session {self.data.session_id}] 🟡 Entered state: general_answer")
        response = call_model(chat_history=self.data.session_chat_history, model="gpt-4o") 
        self.data.answer_message = response
        self.complete()

    def on_enter_error(self):
        logger.error(
            f"[Session {self.data.session_id}] 🔴 Entered state: error. "
            f"Error message: {self.data.error_message}"
        )
        self.data.counters['error'] += 1
        self.reset()

    def on_enter_completed(self):
        logger.info(
            f"[Session {self.data.session_id}] 🟢 Entered state: completed at {self.data.completed_time}"
        )
        self.data.counters['completed'] += 1
        self.reset()



# Define states and hierarchical transitions
states = [
    'idle',
    'tool_selection',
    'out_of_scope_question',
    'user_diagnosis',
    'waiting_user_params',
    'general_answer',
    'error',
    'completed',
    'state_selection',
    'state_a',
    'state_b',
    'state_c',
    'state_d',
    'state_e'
]

transitions = [

    {
        'trigger': 'initiate',
        'source': ['idle', 'waiting_user_params'],
        'dest': 'tool_selection'
    },
    {
        'trigger': 'exec_out_of_scope_question',
        'source': 'tool_selection',
        'dest': 'out_of_scope_question' 
    },
    {
        'trigger': 'exec_user_diagnosis',
        'source': 'tool_selection',
        'dest': 'user_diagnosis'
    },
    {
        'trigger': 'exec_general_answer',
        'source': 'tool_selection',
        'dest': 'general_answer'
    },
    {
        'trigger': 'exec_state_selection',
        'source': 'tool_selection',
        'dest': 'state_selection'
    },
    {
        'trigger': 'complete',
        'source': '*',
        'dest': 'completed'
    },
    {
        'trigger': 'error_occurred',
        'source': '*',
        'dest': 'error'
    },
    {
        'trigger': 'reset',
        'source': '*',
        'dest': 'idle'
    }
]


def run_machine(model: StateMachineModel):

    logger.info(f"[Session {model.data.session_id}] 🔵 Running state machine")

    try:
        if model.state == 'idle' or model.state == 'waiting_user_params':
            model.initiate()
        else:
            # If none of the above states match, we trigger an error
            model.error_occurred()

        logger.info(f"[Session {model.data.session_id}] 🟢 Running state machine complete. Final answer message: {model.data.answer_message}")

        return {"answer_message": model.data.answer_message}

    except Exception as e:
        model.data.error_message = str(e)   
        model.error_occurred()
        return {"error": model.data.error_message}
