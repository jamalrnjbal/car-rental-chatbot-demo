# CarRent AI Chatbot Demo

A WhatsApp-style web chatbot that helps customers find the perfect rental car through natural, conversational AI interactions.

## Features

- **AI-Powered Conversations**: Uses OpenAI GPT-4 to provide natural, friendly, and persuasive customer interactions
- **Smart Car Recommendations**: Intelligently matches customers with vehicles based on their needs, budget, and preferences
- **WhatsApp-Style Interface**: Familiar, mobile-responsive chat interface that mimics WhatsApp
- **Real-Time Availability**: Checks car availability and provides pricing information
- **19 Vehicle Inventory**: Includes economy cars, SUVs, luxury vehicles, electric cars, trucks, and more

## Demo Purpose

This demo is designed to showcase the potential of an AI-powered customer support chatbot for a car rental company. It demonstrates how AI can:

- Engage customers in natural conversation
- Understand customer needs and preferences
- Make personalized vehicle recommendations
- Provide pricing and availability information
- Guide customers toward rental decisions

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download this repository**

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

5. **Initialize the database**:
   ```bash
   python database.py
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Demo Scenarios

Try these conversation flows to showcase the chatbot's capabilities:

### Scenario 1: Budget-Conscious Family
```
User: "I need a car for a family trip next week. We're 4 people with lots of luggage."
Bot: [Will ask about budget and recommend appropriate vehicles]
User: "Looking to spend around $50-60 per day"
Bot: [Will suggest compact SUVs or minivans]
```

### Scenario 2: Luxury Experience
```
User: "I want something luxurious for a business meeting"
Bot: [Will recommend luxury sedans with premium features]
User: "What's the nicest car you have?"
Bot: [Will showcase BMW, Mercedes-Benz, or Audi options]
```

### Scenario 3: Eco-Friendly Customer
```
User: "Do you have any electric or hybrid vehicles?"
Bot: [Will show Tesla Model 3, Nissan Leaf, and hybrid options]
```

### Scenario 4: Group Transportation
```
User: "I need to transport 8 people"
Bot: [Will recommend minivans or full-size SUVs]
```

## Project Structure

```
car-rental-chatbot-demo/
├── app.py                 # Flask application and API routes
├── chatbot.py            # AI chatbot logic and OpenAI integration
├── database.py           # SQLite database setup and queries
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── README.md            # This file
├── templates/
│   └── index.html       # WhatsApp-style chat interface
└── static/
    ├── style.css        # Styling for the chat UI
    └── script.js        # Frontend JavaScript for chat functionality
```

## Technical Details

### Backend
- **Framework**: Flask (Python web framework)
- **AI**: OpenAI GPT-4 with function calling
- **Database**: SQLite (lightweight, file-based)

### Frontend
- **UI**: Vanilla HTML/CSS/JavaScript
- **Design**: WhatsApp-inspired responsive interface
- **Features**: Real-time messaging, typing indicators, smooth animations

### AI Capabilities
The chatbot uses OpenAI's function calling to:
- Access the complete car inventory
- Search cars by price, category, fuel type, and capacity
- Provide personalized recommendations
- Answer questions about specific vehicles

## Car Inventory

The demo includes 19 vehicles across multiple categories:

- **Economy**: Toyota Corolla, Honda Civic, Hyundai Elantra
- **Compact SUVs**: Mazda CX-5, Honda CR-V, Toyota RAV4
- **Full-Size SUVs**: Chevrolet Tahoe, Ford Explorer
- **Luxury**: BMW 3 Series, Mercedes-Benz C-Class, Audi A4
- **Minivans**: Chrysler Pacifica, Honda Odyssey
- **Electric**: Tesla Model 3, Nissan Leaf
- **Trucks**: Ford F-150, Chevrolet Silverado
- **Sports**: Ford Mustang, Chevrolet Camaro

Each vehicle includes:
- Make, model, and year
- Daily rental price
- Passenger and luggage capacity
- Transmission type
- Fuel type (Gasoline, Hybrid, or Electric)
- Key features

## Future Enhancements

For a production deployment, consider adding:

1. **WhatsApp Integration**: Connect to Meta's WhatsApp Business API
2. **Booking System**: Complete reservation and payment processing
3. **Car Images**: Visual gallery of available vehicles
4. **Multi-language Support**: Serve international customers
5. **Analytics Dashboard**: Track conversations and conversion rates
6. **User Authentication**: Customer accounts and rental history
7. **Email Notifications**: Booking confirmations and reminders
8. **Admin Panel**: Manage inventory and pricing

## Troubleshooting

### Database Error
If you see database errors, run:
```bash
python database.py
```

### API Key Error
Make sure your `.env` file exists and contains a valid OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key
```

### Port Already in Use
If port 5000 is busy, modify the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
```

### Module Not Found
Ensure you've activated your virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

## Notes for Demo

- The chatbot maintains conversation context throughout the session
- Responses are generated in real-time by GPT-4
- The interface is fully responsive and works on mobile devices
- All data is stored locally in SQLite (no external database required)
- The typing indicator provides natural conversation pacing

## API Costs

This demo uses OpenAI's GPT-4 API, which has usage costs:
- Typical conversation: ~$0.02-0.05 per exchange
- For the demo, budget ~$5-10 for testing
- Consider using GPT-3.5-turbo for lower costs (change in `chatbot.py`)

## License

This is a demo project for showcasing AI chatbot capabilities.

## Support

For questions or issues, please refer to:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/)

---

**Built for CEO Demo - Ready to showcase AI-powered customer engagement!** 🚗💬