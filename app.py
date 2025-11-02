from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chatbot import CarRentalChatbot
from database import init_db, get_all_cars
from email_report import send_conversation_report

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
init_db()

# Initialize chatbot
chatbot = CarRentalChatbot()

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Get response from chatbot
        bot_response = chatbot.get_response(user_message, conversation_history)

        # Send email report to company
        send_conversation_report(user_message, bot_response, conversation_history)

        return jsonify({
            'response': bot_response,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Get all available cars (for debugging/admin)"""
    try:
        cars = get_all_cars()
        return jsonify({
            'cars': cars,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
