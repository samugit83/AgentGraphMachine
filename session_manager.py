# session_manager.py
import redis
import pickle
import threading
from transitions.extensions import GraphMachine


from data_model import DataModel
from state_machine import StateMachineModel, states, transitions

        
class SessionManager:
    def __init__(self, redis_host='redis', redis_port=6379, db=0):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=db)
        self.lock = threading.Lock()

    def get_session_key(self, session_id):
        return f"session:{session_id}"

    def load_session(self, session_id, session_chat_history, user_id=None):
        """
        Load (unpickle) the user's DataModel from Redis,
        create a fresh StateMachineModel from it,
        and then attach transitions.
        """
        with self.lock:
            serialized_data = self.redis.get(self.get_session_key(session_id))
            if serialized_data:
                # Unpickle the data
                data_model = pickle.loads(serialized_data)
                # Update chat history
                data_model.session_chat_history = session_chat_history

                # Rebuild the StateMachineModel using the data
                model = StateMachineModel(data_model)

                # Re-bind transitions to the model
                machine = GraphMachine(
                    model=model,
                    states=states,
                    transitions=transitions,
                    initial=model.state,  # resume from stored state
                    auto_transitions=False,
                    queued=True,
                    title="My State Machine Diagram",
                    show_conditions=True,
                    graph_engine="graphviz"
                )
            else:
                # Create a new DataModel and a new StateMachineModel
                data_model = DataModel(
                    name="MySanibotCoreMachine",
                    session_id=session_id,
                    user_id=user_id,
                    session_chat_history=session_chat_history
                )
                model = StateMachineModel(data_model)

                # Initialize the state machine
                machine = GraphMachine(
                    model=model,
                    states=states,
                    transitions=transitions,
                    initial='idle',
                    auto_transitions=False,
                    queued=True,
                    title="My State Machine Diagram",
                    show_conditions=True,
                    graph_engine="graphviz"
                )

            model.get_graph().draw('newstate.png', prog='dot')
            return model

    def save_session(self, model: StateMachineModel):
        """
        Serialize (pickle) ONLY the data model and store it in Redis.
        """
        with self.lock:
            serialized_data = pickle.dumps(model.data)
            self.redis.set(self.get_session_key(model.data.session_id), serialized_data)
