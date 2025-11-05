from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chatbot import CarRentalChatbot
from database import init_db, get_all_cars, get_user_conversation, save_user_conversation
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import requests
import tempfile

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

def transcribe_voice_message(media_url):
    """
    Download and transcribe a voice message from Twilio using OpenAI Whisper.

    Args:
        media_url: URL to the audio file from Twilio

    Returns:
        Transcribed text string, or None if transcription fails
    """
    try:
        # Get Twilio credentials for authenticated download
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        print(f"Downloading voice message from: {media_url}")

        # Download the audio file from Twilio (requires authentication)
        response = requests.get(
            media_url,
            auth=(twilio_account_sid, twilio_auth_token),
            timeout=30
        )
        response.raise_for_status()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_audio:
            temp_audio.write(response.content)
            temp_audio_path = temp_audio.name

        print(f"Audio file downloaded to: {temp_audio_path}")

        # Transcribe using OpenAI Whisper
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        with open(temp_audio_path, 'rb') as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"  # Can be removed to auto-detect language
            )

        # Clean up temporary file
        os.unlink(temp_audio_path)

        transcribed_text = transcript.text
        print(f"Transcription successful: {transcribed_text}")

        return transcribed_text

    except Exception as e:
        print(f"Error transcribing voice message: {e}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages (text and voice) from Twilio"""
    try:
        # Get incoming message details from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')  # Format: whatsapp:+1234567890
        num_media = int(request.values.get('NumMedia', 0))

        # Debug logging
        print(f"Received message from {sender_number}")
        print(f"Text: {incoming_msg}")
        print(f"Number of media attachments: {num_media}")

        # Check if this is a voice message
        if num_media > 0:
            media_content_type = request.values.get('MediaContentType0', '')
            media_url = request.values.get('MediaUrl0', '')

            print(f"Media type: {media_content_type}")
            print(f"Media URL: {media_url}")

            # Handle voice messages (audio files)
            if 'audio' in media_content_type.lower():
                print("Voice message detected, transcribing...")

                transcribed_text = transcribe_voice_message(media_url)

                if transcribed_text:
                    incoming_msg = transcribed_text
                    print(f"Transcribed voice message: {incoming_msg}")
                else:
                    # Transcription failed
                    resp = MessagingResponse()
                    resp.message("I'm sorry, I couldn't understand your voice message. Could you please try again or send a text message?")
                    return str(resp)
            else:
                # Non-audio media (ignore images, videos, etc.)
                print(f"Non-audio media received, ignoring")
                resp = MessagingResponse()
                resp.message("I can only process voice messages and text. Please send a voice message or text.")
                return str(resp)

        # Check if we have a message to process (text or transcribed voice)
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
