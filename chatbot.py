import os
from openai import OpenAI
from database import get_all_cars, search_cars
import json

class CarRentalChatbot:
    def __init__(self):
        """Initialize the chatbot with OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"

        # System prompt for the chatbot
        self.system_prompt = """You're a helpful car rental assistant. Keep it casual and natural - talk like a real person, not a robot.

How to help customers:

If they ask about a SPECIFIC car:
- Ask when they need it
- Check if it's available and tell them the price
- If available: highlight 1-2 cool features
- If not available: show similar options right away

If they ask GENERALLY about cars:
- Ask when they need it
- Show 2-3 nice options (mix of prices)
- Ask if they want something different

When customer decides to book a car:
- Say "Awesome! It's booked!" or "Perfect, you're all set!"
- Ask for their email: "What's your email so I can send you the booking confirmation?"
- After they give email, confirm: "Great! I've sent the confirmation to [email]. You're all set!"

Keep messages SHORT - 1-2 sentences max. Don't list a bunch of questions.

When showing cars, format like this:

**2024 Toyota Corolla** - $35/day
Great for city driving, seats 5, has AC and Bluetooth

---

**2024 BMW 3 Series** - $95/day
Luxury sedan with leather seats and premium sound

---

Chat naturally. Be helpful but chill. Don't overthink it.

You can search the inventory using get_car_inventory (all cars) or search_cars (filter by price, passengers, category, fuel type)."""

    def get_response(self, user_message, conversation_history=None):
        """Get a response from the chatbot"""
        if conversation_history is None:
            conversation_history = []

        # Build messages for OpenAI
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        for msg in conversation_history:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Define functions for the AI to use
        functions = [
            {
                "name": "get_car_inventory",
                "description": "Get the complete list of available rental cars with all details including make, model, price, capacity, and features",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "search_cars",
                "description": "Search for cars that match specific criteria like budget, passenger count, category, or fuel type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "max_price": {
                            "type": "number",
                            "description": "Maximum daily price in dollars"
                        },
                        "min_passengers": {
                            "type": "integer",
                            "description": "Minimum number of passengers the car should accommodate"
                        },
                        "category": {
                            "type": "string",
                            "description": "Car category",
                            "enum": ["Economy", "Compact SUV", "Mid-Size SUV", "Full-Size SUV", "Luxury", "Minivan", "Electric", "Pickup Truck", "Sports"]
                        },
                        "fuel_type": {
                            "type": "string",
                            "description": "Type of fuel",
                            "enum": ["Gasoline", "Hybrid", "Electric"]
                        }
                    }
                }
            }
        ]

        try:
            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=functions,
                function_call="auto",
                temperature=0.7,
                max_tokens=1500
            )

            response_message = response.choices[0].message

            # Check if the model wants to call a function
            if response_message.function_call:
                # Execute the function
                function_name = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)

                if function_name == "get_car_inventory":
                    function_response = get_all_cars()
                elif function_name == "search_cars":
                    function_response = search_cars(function_args)
                else:
                    function_response = {"error": "Unknown function"}

                # Add function call and response to messages
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": function_name,
                        "arguments": response_message.function_call.arguments
                    }
                })
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })

                # Get final response from the model
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )

                return second_response.choices[0].message.content

            else:
                # No function call, return direct response
                return response_message.content

        except Exception as e:
            print(f"Error getting response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Could you please try again?"

    def format_car_info(self, car):
        """Format car information for display"""
        features = ", ".join(car['features'][:3])  # Show top 3 features
        return f"{car['year']} {car['make']} {car['model']} - ${car['daily_price']:.2f}/day ({car['passengers']} passengers, {features})"
