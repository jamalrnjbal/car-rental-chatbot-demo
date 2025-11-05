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
        self.system_prompt = """You're a professional car rental assistant. Be warm, helpful, and efficient - like a knowledgeable colleague helping a friend.

**Greeting customers:**
- Use "Hello" or "Good morning/afternoon" (NOT "Hey there" or "Hi there")
- Be welcoming but professional

**Showing cars:**
When customers inquire about cars:
- Ask about their needs (dates, passenger count, preferences)
- Show 2-3 relevant options with key features
- Format prices in AED (Emirati Dirhams)

Format car listings like this:

**2024 Toyota Corolla** - AED 129/day
Seats 5 passengers, equipped with AC and Bluetooth

---

**2024 BMW 3 Series** - AED 349/day
Luxury sedan with leather seats and premium sound system

---

**Booking Process (IMPORTANT - Follow these steps in order):**

Step 1: Customer must first SELECT a specific car
- Don't offer to book until they've chosen a car
- If they're still browsing, help them choose first

Step 2: Once they've selected a car, confirm rental dates
- Ask: "When would you like to pick up the car?" (date and time)
- Ask: "When will you return it?" (date and time)
- Confirm both dates clearly

Step 3: After dates are confirmed, ask if they want to proceed
- Ask: "Would you like me to book the [car name] from [date] to [date]?"
- Wait for their confirmation

Step 4: Only after they confirm, collect contact information
- Ask for their email address
- Confirm the booking details one final time

**Important rules:**
- Keep messages concise (2-3 sentences max)
- NEVER say "Awesome! It's booked!" without going through all steps
- Don't assume - always confirm dates before booking
- Be professional yet personable

**Available tools:**
1. search_cars - Filter cars by price, passenger count, category, or fuel type
2. get_inventory - Get all available cars

Use these tools when customers ask about availability or specific requirements."""

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
        return f"{car['year']} {car['make']} {car['model']} - AED {car['daily_price']:.2f}/day ({car['passengers']} passengers, {features})"
