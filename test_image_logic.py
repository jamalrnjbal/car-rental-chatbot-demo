"""
Test the improved image sending logic
"""
from app import extract_car_images_from_response

def test_image_logic():
    """Test when images should and shouldn't be sent"""

    print("=== Testing Image Sending Logic ===\n")

    # Test 1: Response with car listings (SHOULD send images)
    print("TEST 1: Response with car listings")
    bot_response = """Here are some economy cars:

**2024 Toyota Corolla** - AED 128.45/day
Seats 5 passengers, equipped with AC and Bluetooth

**2024 Honda Civic** - AED 139.46/day
Seats 5 passengers with AC, Bluetooth, and Lane Assist"""

    images = extract_car_images_from_response(bot_response, "Show me cars", [])
    print(f"Bot response includes car listings with AED pricing")
    print(f"Images to send: {len(images)}")
    print(f"URLs: {images}\n")
    print("-" * 80 + "\n")

    # Test 2: Greeting response (SHOULD NOT send images)
    print("TEST 2: Greeting response")
    bot_response = "Good afternoon! How can I assist you with your car rental needs today?"
    images = extract_car_images_from_response(bot_response, "Hello", [])
    print(f"Bot response: {bot_response}")
    print(f"Images to send: {len(images)} (should be 0)")
    print(f"Expected: No images\n")
    print("-" * 80 + "\n")

    # Test 3: Date question (SHOULD NOT send images)
    print("TEST 3: Date question response")
    bot_response = "Great choice! The 2024 Toyota Corolla is a reliable car. When would you like to pick it up?"
    images = extract_car_images_from_response(bot_response, "I'll take the Corolla", [])
    print(f"Bot response: {bot_response}")
    print(f"Images to send: {len(images)} (should be 0)")
    print(f"Expected: No images (no AED pricing in response)\n")
    print("-" * 80 + "\n")

    print("=== Test Complete ===")

if __name__ == "__main__":
    test_image_logic()
