"""
Test the improved chatbot with better UX
"""
from chatbot import CarRentalChatbot
from dotenv import load_dotenv

load_dotenv()

def test_improved_ux():
    """Test the improved user experience"""

    print("=== Testing Improved Chatbot UX ===\n")

    chatbot = CarRentalChatbot()

    # Test professional greeting
    print("TEST 1: Professional greeting")
    print("User: Hello")
    response = chatbot.get_response("Hello")
    print(f"Bot: {response}\n")
    print("-" * 80 + "\n")

    # Test AED pricing
    print("TEST 2: Prices in AED")
    print("User: Show me some economy cars")
    response = chatbot.get_response("Show me some economy cars")
    print(f"Bot: {response}\n")
    print("-" * 80 + "\n")

    # Test booking flow - should not book immediately
    print("TEST 3: Booking flow (should ask for details first)")
    conversation = [
        {"role": "user", "content": "I need a car"},
        {"role": "assistant", "content": response}
    ]
    print("User: I'll take the Toyota Corolla")
    response = chatbot.get_response("I'll take the Toyota Corolla", conversation)
    print(f"Bot: {response}")
    print("\nExpected: Should ask for dates, not book immediately\n")

    print("=== Test Complete ===")

if __name__ == "__main__":
    test_improved_ux()
