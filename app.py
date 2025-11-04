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

        # Debug logging
        print(f"Received message from {sender_number}: {incoming_msg}")

        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("I didn't receive a message. Please try again!")
            return str(resp)

        # Retrieve conversation history for this user
        conversation_history = get_user_conversation(sender_number)
        print(f"Retrieved conversation history: {len(conversation_history)} messages")

        # Get chatbot response (reuse existing chatbot logic)
        bot_response = chatbot.get_response(incoming_msg, conversation_history)
        print(f"Generated response: {bot_response[:100]}...")

        # Save conversation state
        save_user_conversation(sender_number, incoming_msg, bot_response)

        # Create Twilio response
        resp = MessagingResponse()

        # Check if bot response mentions specific cars and try to send images
        image_urls = extract_car_images_from_response(incoming_msg, conversation_history)

        if image_urls:
            # Send images with the response
            msg = resp.message(bot_response)
            for url in image_urls[:3]:  # Limit to 3 images to avoid spam
                msg.media(url)
            print(f"Sending {len(image_urls)} images")
        else:
            # No images, just send text
            resp.message(bot_response)

        twiml_response = str(resp)
        print(f"TwiML Response: {twiml_response[:200]}...")

        return twiml_response

    except Exception as e:
        print(f"Error in WhatsApp webhook: {e}")
        import traceback
        traceback.print_exc()
        resp = MessagingResponse()
        resp.message("Sorry, I'm having trouble right now. Please try again in a moment!")
        return str(resp)

def extract_car_images_from_response(user_msg, conversation_history):
    """
    Extract car image URLs when the bot recommends cars.
    This checks if the conversation involves car recommendations and fetches images.
    """
    from database import search_cars, get_all_cars

    # Keywords that suggest user is looking for cars
    car_keywords = ['car', 'vehicle', 'rental', 'need', 'looking', 'trip', 'family', 'luxury', 'suv', 'sedan']

    if not any(keyword in user_msg.lower() for keyword in car_keywords):
        return []

    # Try to get relevant cars based on recent conversation
    try:
        # Simple heuristic: get a few cars from popular categories
        cars = get_all_cars()

        # Return up to 3 car images
        images = []
        for car in cars[:3]:
            if car.get('image_url'):
                images.append(car['image_url'])

        return images
    except Exception as e:
        print(f"Error extracting car images: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
