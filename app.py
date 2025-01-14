
from flask import Flask, request, jsonify, render_template
import os
from state_machine import run_machine
from session_manager import SessionManager
from interactive_multiagent.planner import AgentPlanner
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

app = Flask(__name__, static_folder='static', template_folder='templates')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

session_manager = SessionManager(redis_host=REDIS_HOST, redis_port=REDIS_PORT, db=REDIS_DB)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-ai-agent', methods=['POST'])
def run_ai_agent():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is empty"}), 400

        required_fields = ['session_id', 'session_chat_history']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        session_id = data['session_id']
        session_chat_history = data['session_chat_history']
        user_id = data.get('user_id')
        
        # Retrieve or create the session state machine
        model = session_manager.load_session(session_id, session_chat_history, user_id)

        # Start or continue the state machine
        response = run_machine(model)

        # Save the updated session
        session_manager.save_session(model)

        if 'error' in response:
            return jsonify({"error": response["error"]}), 400
        return jsonify({"assistant": response["answer_message"]}), 200

    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        logging.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=True
    )
