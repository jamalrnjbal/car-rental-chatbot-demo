"""
Test WhatsApp webhook locally to diagnose issues
"""
from database import get_user_conversation, save_user_conversation
from chatbot import CarRentalChatbot
from dotenv import load_dotenv

load_dotenv()

def test_conversation():
    """Test the conversation flow that happens in WhatsApp webhook"""

    # Simulate a WhatsApp user
    test_phone = "whatsapp:+1234567890"

    print("=== Testing WhatsApp Conversation Flow ===\n")

    # Initialize chatbot
    chatbot = CarRentalChatbot()

    # Test messages
    test_messages = [
        "Hi, I need a car",
        "I need it for a family trip",
        "What do you have?",
    ]

    for user_msg in test_messages:
        print(f"User: {user_msg}")

        try:
            # Get conversation history (same as webhook does)
            conversation_history = get_user_conversation(test_phone)
            print(f"History length: {len(conversation_history)} messages")

            # Get chatbot response
            bot_response = chatbot.get_response(user_msg, conversation_history)
            print(f"Bot: {bot_response}\n")

            # Save conversation (same as webhook does)
            save_user_conversation(test_phone, user_msg, bot_response)

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            break

    print("\n=== Test Complete ===")

    # Show final conversation history
    final_history = get_user_conversation(test_phone)
    print(f"\nFinal history has {len(final_history)} messages")

if __name__ == "__main__":
    test_conversation()
