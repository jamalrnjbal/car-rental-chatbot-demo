import os
from openai import OpenAI
import instructor
from database import get_all_cars, search_cars
from models import ChatbotAction, CarSearchCriteria, GetCarInventory
import json

class CarRentalChatbot:
    def __init__(self):
        """Initialize the chatbot with Instructor-patched OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Keep both regular and Instructor-patched clients
        self.openai_client = OpenAI(api_key=api_key)
        self.client = instructor.from_openai(OpenAI(api_key=api_key))
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

You have access to two tools:
1. search_cars - Filter cars by price, passenger count, category, or fuel type
2. get_inventory - Get all available cars

Use search_cars when customers have specific requirements. Use get_inventory when they want to browse everything.
For simple questions or greetings, just respond directly without using tools."""

    def get_response(self, user_message, conversation_history=None):
        """Get a response from the chatbot using Instructor for structured outputs"""
        if conversation_history is None:
            conversation_history = []

        # Build messages for OpenAI
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        for msg in conversation_history:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Use Instructor to get structured output
            action: ChatbotAction = self.client.chat.completions.create(
                model=self.model,
                response_model=ChatbotAction,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )

            # Handle different action types
            if action.action_type == "search_cars" and action.search_criteria:
                # Convert Pydantic model to dict, excluding None values
                criteria = action.search_criteria.model_dump(exclude_none=True)
                cars = search_cars(criteria)

                # Format car results for the final response
                car_data = json.dumps(cars)

                # Get natural language response with the car data
                final_messages = messages + [
                    {"role": "assistant", "content": f"[Searching cars with criteria: {criteria}]"},
                    {"role": "user", "content": f"Here are the matching cars: {car_data}. Please present these to the customer naturally."}
                ]

                final_response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=final_messages,
                    temperature=0.7,
                    max_tokens=1500
                )

                return final_response.choices[0].message.content

            elif action.action_type == "get_inventory":
                # Get all cars
                cars = get_all_cars()
                car_data = json.dumps(cars)

                # Get natural language response with all cars
                final_messages = messages + [
                    {"role": "assistant", "content": "[Retrieving all available cars]"},
                    {"role": "user", "content": f"Here are all available cars: {car_data}. Please present 2-3 good options to the customer naturally."}
                ]

                final_response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=final_messages,
                    temperature=0.7,
                    max_tokens=1500
                )

                return final_response.choices[0].message.content

            elif action.action_type == "direct_response" and action.response:
                # Direct response without function calling
                return action.response

            else:
                # Fallback for unexpected cases
                return "I'm here to help you find a rental car! What kind of car are you looking for?"

        except Exception as e:
            print(f"Error getting response: {e}")
            import traceback
            traceback.print_exc()
            return "I apologize, but I'm having trouble processing your request right now. Could you please try again?"

    def format_car_info(self, car):
        """Format car information for display"""
        features = ", ".join(car['features'][:3])  # Show top 3 features
        return f"{car['year']} {car['make']} {car['model']} - ${car['daily_price']:.2f}/day ({car['passengers']} passengers, {features})"
