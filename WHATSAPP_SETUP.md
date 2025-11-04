# WhatsApp Integration Setup Guide

Your chatbot now supports **both** web interface AND WhatsApp! This guide will help you set up WhatsApp integration using Twilio.

## Quick Start - Twilio Sandbox (Recommended for Demo)

The sandbox lets you test WhatsApp integration **immediately** without approval. Perfect for your CEO demo!

### Step 1: Create Twilio Account

1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free account
3. Verify your email and phone number
4. You'll get **$15 in free trial credits**

### Step 2: Access WhatsApp Sandbox

1. Log in to Twilio Console: https://console.twilio.com/
2. In the left sidebar, click **Messaging** → **Try it out** → **Send a WhatsApp message**
3. You'll see the sandbox page with a unique join code

### Step 3: Join the Sandbox from Your Phone

1. On your phone, open WhatsApp
2. Send a message to **+1 (415) 523-8886**
3. Message format: `join <your-code>` (e.g., `join steel-mountain`)
4. You'll receive a confirmation message

**That's it!** You can now chat with this number and it will connect to your chatbot.

### Step 4: Get Your Twilio Credentials

1. In Twilio Console, go to your Dashboard (home page)
2. Find your **Account SID** (starts with AC...)
3. Find your **Auth Token** (click "show" to reveal)
4. Copy both values

### Step 5: Configure Your Application

#### For Render (Production):

1. Go to your Render dashboard
2. Click on your service → **Environment**
3. Add these environment variables:
   ```
   TWILIO_ACCOUNT_SID = AC... (your value)
   TWILIO_AUTH_TOKEN = ... (your value)
   TWILIO_WHATSAPP_NUMBER = whatsapp:+15558251351
   ```
4. Click **Save Changes**

#### For Local Testing:

Update your `.env` file:
```env
TWILIO_ACCOUNT_SID=AC... (your value)
TWILIO_AUTH_TOKEN=... (your value)
TWILIO_WHATSAPP_NUMBER=whatsapp:+15558251351
```

**IMPORTANT:** Never commit `.env` to git - it contains secrets!

### Step 6: Configure the Webhook

This tells Twilio where to send incoming WhatsApp messages.

#### For Render (Production - Easiest):

1. Your webhook URL is: `https://car-rental-chatbot-demo.onrender.com/whatsapp`
2. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Scroll down to **Sandbox Configuration**
4. Under "WHEN A MESSAGE COMES IN", paste your webhook URL
5. Make sure method is set to **POST**
6. Click **Save**

#### For Local Testing (requires ngrok):

1. Install ngrok: https://ngrok.com/download
2. Run your Flask app locally: `python app.py`
3. In another terminal, run: `ngrok http 5000`
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
5. Your webhook URL is: `https://abc123.ngrok.io/whatsapp`
6. Configure in Twilio (same steps as above)

**Note:** ngrok URLs change every time you restart, so you'll need to update the webhook URL each time.

### Step 7: Test It!

1. Open WhatsApp on your phone
2. Send a message to **+1 (415) 523-8886**
3. Ask something like: "I need a car for a family trip"
4. The chatbot should respond!

**Demo tip:** Show the CEO both interfaces:
- Web: Open the Render URL in browser
- WhatsApp: Show it on your phone

---

## How It Works

### Message Flow:
```
User sends WhatsApp message
    ↓
Twilio receives it
    ↓
Twilio sends webhook to your app: POST /whatsapp
    ↓
Your app:
  1. Gets conversation history from database (by phone number)
  2. Sends message to ChatGPT
  3. Gets response
  4. Saves conversation history
  5. Returns TwiML response
    ↓
Twilio sends response back to WhatsApp
    ↓
User receives message
```

### Conversation Storage:

- Each user's conversation is stored in the `conversations` table
- Keyed by phone number (format: `whatsapp:+1234567890`)
- Keeps last 20 messages to avoid token limits
- Persists across app restarts

### Both Interfaces Work:

- **Web**: Uses existing `/api/chat` endpoint, state managed in browser
- **WhatsApp**: Uses new `/whatsapp` endpoint, state in database
- **Same chatbot logic** for both!

---

## Troubleshooting

### "I'm not getting responses in WhatsApp"

1. Check Twilio Console → Messaging → Logs for errors
2. Verify webhook URL is correct: `https://your-app.onrender.com/whatsapp`
3. Make sure you "joined" the sandbox (`join your-code`)
4. Check Render logs for errors
5. Verify environment variables are set in Render

### "Webhook returns 500 error"

1. Check Render logs for Python errors
2. Make sure database.py has the new functions
3. Verify twilio library is installed: check requirements.txt
4. Ensure database was reinitialized with conversations table

### "Conversation doesn't remember previous messages"

1. Check that conversation is being saved (look in Render logs)
2. Verify database has the `conversations` table
3. Phone number format should be `whatsapp:+1234567890`

### "Sandbox expired"

Sandbox expires after 3 days of inactivity. Just rejoin:
1. Send `join your-code` to +1 (415) 523-8886 again
2. You're back in!

---

## Sandbox Limitations

- Users must manually "join" your sandbox
- Shared Twilio number (+1 415-523-8886)
- Expires after 3 days of no activity
- Cannot customize the business name
- Free trial: 50 messages/day limit

**For production:** Apply for WhatsApp Business API approval (takes 2-15 days)

---

## Production Setup (Optional - After Demo)

For real customers, you'll need approved WhatsApp Business API access.

### Requirements:
- Facebook Business Manager account
- Dedicated phone number (not used for regular WhatsApp)
- Business verification
- 2-15 business days for approval

### Costs:
- Twilio: ~$0.005 per message
- Meta: Per-message pricing (varies by type)
- Free 24-hour window after customer initiates

### Apply:
1. Twilio Console → Messaging → WhatsApp → Get Started
2. Follow the approval process
3. Submit business verification documents
4. Wait for Meta approval

---

## Testing Checklist

Before the demo:
- [ ] Joined Twilio sandbox from your phone
- [ ] Configured webhook URL in Twilio
- [ ] Set Twilio credentials in Render environment variables
- [ ] Sent test message - got response
- [ ] Tested conversation memory (send multiple messages)
- [ ] Tested booking flow (say "I want to book")
- [ ] Verified web interface still works

---

## Demo Tips

### Show Both Interfaces:
1. **Web**: Open in browser, send a few messages
2. **WhatsApp**: Show on phone, send messages
3. Point out: "Same AI, multiple channels"

### Highlight Features:
- Natural conversation (not robotic)
- Remembers context across messages
- Quick car recommendations
- Booking confirmation with email collection
- Ready for real WhatsApp integration

### Address Concerns:
- **Cost**: ~$0.005/message, very affordable
- **Approval**: 2-15 days for production
- **Scale**: Handles multiple users simultaneously
- **Maintenance**: Fully automated, no manual responses needed

---

## Support

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- Twilio Console: https://console.twilio.com/
- Sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

Your chatbot is ready for WhatsApp! 🎉
