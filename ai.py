import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_ai_response(user_input):
    """Send free-form user input to Gemini and get text response."""
    convo = model.start_chat(history=[
        {"role": "system", "parts": "You are an HR assistant helping employees with leave management."}
    ])
    response = convo.send_message(user_input)
    return response.text

def extract_intent_and_entities(user_input):
    """Prompt Gemini to extract structured intent and entities in JSON format."""
    prompt = f"""
You are an AI assistant helping with employee leave management.
Classify the following request into:
- intent: one of (check_balance, request_leave, cancel_leave, view_history)
- leave_type: (if applicable)
- number_of_days: (if applicable)
- start_date: (if applicable)

Reply strictly in JSON format. Avoid markdown or extra formatting.

User input: "{user_input}"
"""
    convo = model.start_chat()
    response = convo.send_message(prompt)
    return response.text
