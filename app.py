from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chatbot import CarRentalChatbot
from database import init_db, get_all_cars, get_user_conversation, save_user_conversation
from twilio.twiml.messaging_response import MessagingResponse

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

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get incoming WhatsApp message from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')  # Format: whatsapp:+1234567890

        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("I didn't receive a message. Please try again!")
            return str(resp)

        # Retrieve conversation history for this user
        conversation_history = get_user_conversation(sender_number)

        # Get chatbot response (reuse existing chatbot logic)
        bot_response = chatbot.get_response(incoming_msg, conversation_history)

        # Save conversation state
        save_user_conversation(sender_number, incoming_msg, bot_response)

        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_response)

        return str(resp)

    except Exception as e:
        print(f"Error in WhatsApp webhook: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, I'm having trouble right now. Please try again in a moment!")
        return str(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
