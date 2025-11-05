"""
Test script for the Instructor-based chatbot
"""
from chatbot import CarRentalChatbot
from dotenv import load_dotenv

load_dotenv()

def test_chatbot():
    """Test the chatbot with various queries"""

    print("=== Testing Instructor-based Chatbot ===\n")

    chatbot = CarRentalChatbot()

    test_queries = [
        "Hi, I need a car",
        "Show me cars under $50 per day",
        "I need something for 7 passengers",
    ]

    for query in test_queries:
        print(f"User: {query}")
        try:
            response = chatbot.get_response(query)
            print(f"Bot: {response}\n")
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"ERROR: {e}\n")
            import traceback
            traceback.print_exc()
            break

    print("=== Test Complete ===")

if __name__ == "__main__":
    test_chatbot()
