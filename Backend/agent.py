import google.generativeai as genai
from calendar_utils import book_event, get_slots_for_date, check_availability
from datetime import datetime
import re
import os
from dotenv import load_dotenv
load_dotenv()


# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with os.getenv in deployment

# Initialize the model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print("❌ Error initializing Gemini model:", e)
    model = None

# Store conversation history
conversation_history = []

# State tracking
date_requested = None
pending_slots = []

# assistant context
instruction = {
    "role": "user",
    "parts": [
        "You are a helpful assistant for booking appointments. When the user wants to book, ask them for the date (in YYYY-MM-DD format). Then show the available time slots for that day. Respond politely and confirm booking clearly."
    ]
}
conversation_history.append(instruction)

def format_slots(slots, date_str):
    display = f"Here are available slots on {date_str}:"
    for i, slot in enumerate(slots, start=1):
        time = datetime.fromisoformat(slot["start"]).strftime("%I:%M %p")
        display += f"\n{i}. {time}"
    return display

def run_agent(user_input):
    global date_requested, pending_slots

    try:
        if not model:
            return "❌ Gemini model is not available."

        conversation_history.append({"role": "user", "parts": [user_input]})

        # 1. Ask for date
        if any(word in user_input.lower() for word in ["book", "appointment", "slot"]):
            date_requested = None
            pending_slots = []
            reply = "Sure! Please provide a date for the appointment (YYYY-MM-DD)."
            conversation_history.append({"role": "model", "parts": [reply]})
            return reply

        # 2. If input looks like a date
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", user_input)
        if date_match:
            date_requested = date_match.group()
            pending_slots = get_slots_for_date(date_requested)
            if not pending_slots:
                reply = f"❌ Sorry, no available slots on {date_requested}."
            else:
                reply = format_slots(pending_slots, date_requested)
            conversation_history.append({"role": "model", "parts": [reply]})
            return reply

        # 3. Slot selection by number or time
        for i, slot in enumerate(pending_slots, start=1):
            readable = datetime.fromisoformat(slot["start"]).strftime("%I:%M %p")
            if str(i) in user_input or readable.lower() in user_input.lower():
                if check_availability(slot["start"], slot["end"]):
                    book_event("Session with Dinesh", slot["start"], slot["end"])
                    confirmation = f"✅ Your session is booked on {date_requested} at {readable}."
                    conversation_history.append({"role": "model", "parts": [confirmation]})
                    # Reset state after booking
                    date_requested = None
                    pending_slots = []
                    return confirmation
                else:
                    conflict = f"❌ Sorry, the {readable} slot was just taken. Please pick another."
                    conversation_history.append({"role": "model", "parts": [conflict]})
                    return conflict

        # 4. Gemini chat
        response = model.generate_content(conversation_history)
        reply = response.text.strip() if hasattr(response, 'text') else str(response)
        conversation_history.append({"role": "model", "parts": [reply]})
        return reply

    except Exception as e:
        print("🔥 Gemini Error:", str(e))
        return "❌ Something went wrong: " + str(e)
