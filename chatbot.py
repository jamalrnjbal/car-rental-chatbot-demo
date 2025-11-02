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
        self.system_prompt = """You are a friendly, helpful, and persuasive car rental assistant for a car rental company.
Your goal is to help customers find the perfect rental car for their needs through natural conversation.

Your personality:
- Warm and welcoming
- Professional but conversational
- Enthusiastic about helping customers
- Patient and attentive to details
- Persuasive but not pushy

Your process:
1. Greet customers warmly
2. Ask about their rental needs ONE question at a time (dates, location, number of passengers, luggage, budget, preferences)
3. Recommend suitable vehicles based on their requirements
4. Provide clear pricing information
5. Highlight key features and benefits
6. Check availability when requested
7. Guide them toward making a decision

When recommending cars:
- Always mention the daily price
- Highlight 2-3 key features that match their needs
- Compare options if they're unsure
- Be specific about capacity (passengers and luggage)
- Suggest upgrades when appropriate
- IMPORTANT: When you receive car data from the database, each car has an "image_url" field
- When showing a specific car, you MUST include the image by writing: [IMAGE:] followed by the actual image_url value from that car's data
- Example: If a car's image_url is "https://example.com/car.jpg", write: [IMAGE:https://example.com/car.jpg]
- Do NOT write "url_here" or any placeholder - use the ACTUAL image_url from the car data

CRITICAL RULES:
- **Ask ONLY ONE question per response** - never ask multiple questions at once
- Keep responses conversational and natural (2-4 sentences typically)
- Don't overwhelm with too many options at once (show 2-3 cars max)
- Gather information gradually through the conversation
- Be enthusiastic about the vehicles you recommend
- Use emojis sparingly and naturally
- Let the conversation flow naturally - don't rush to gather all information at once

You have access to the following car information through function calls. Use the get_car_inventory function to see all available cars, or search_cars to find specific vehicles based on criteria.

Remember: Your main goal is to help customers find the perfect car and feel confident about their choice! Take your time and build rapport by asking one question at a time."""

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
                max_tokens=500
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
                    max_tokens=500
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
