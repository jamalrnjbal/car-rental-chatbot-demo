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
        image_urls = extract_car_images_from_response(bot_response, incoming_msg, conversation_history)

        if image_urls:
            # Send images with the response
            msg = resp.message(bot_response)
            for url in image_urls[:3]:  # Limit to 3 images to avoid spam
                msg.media(url)
            print(f"Sending {len(image_urls)} images: {image_urls}")
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

def extract_car_images_from_response(bot_response, user_msg, conversation_history):
    """
    Extract car image URLs ONLY when the bot actually recommends specific cars.
    Parse the bot's response to find car names and return their images.
    """
    from database import get_all_cars
    import re

    # Only send images if the bot response contains car listings (has "AED" pricing)
    if "AED" not in bot_response or "/day" not in bot_response:
        print("No car listings detected in response (no AED pricing)")
        return []

    try:
        # Get all cars from database
        all_cars = get_all_cars()

        # Extract car names mentioned in the bot response
        # Look for patterns like "**2024 Toyota Corolla**" or "Toyota Corolla"
        mentioned_images = []

        for car in all_cars:
            car_name = f"{car['make']} {car['model']}"
            # Check if this car is mentioned in the response
            if car_name in bot_response:
                if car.get('image_url'):
                    mentioned_images.append(car['image_url'])
                    print(f"Adding image for {car_name}")

        # Limit to 3 images max
        return mentioned_images[:3]

    except Exception as e:
        print(f"Error extracting car images: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
