# 📝 AI-Powered Leave Management System

A terminal-based leave management system enhanced with AI-powered natural language interaction (via Google Gemini API). Employees can request leaves, check balances, view history, and admins can manage employee records and leave approvals.

---

## 📦 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/ikraam-1808/leave-management-ai.git
cd leave-management-ai
```

2. **Create and Activate a Virtual Environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up API Key**

Open config.py and replace:
```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```
with your actual Google Gemini API key.

## ▶️ How to Run the Application

```bash
python main.py
```

You’ll be prompted to select either:

- user — to request/check/cancel leaves
- admin — to add/list employees or manage leave approvals

## 🔧 API Key Configuration

The application uses Google’s Gemini API via google-generativeai.
Ensure your API key is set correctly in config.py:

```python
GEMINI_API_KEY = "your_actual_api_key"
MODEL_NAME = "models/gemini-2.0-flash"
```

## 📖 Assumptions Made

- Leave Types are fixed as per config.py:
```python
  LEAVE_TYPES = ["Sick Leave", "Annual Leave", "Maternity Leave", "Paternity Leave"]
```

- Leave Balances are initialized by the admin when adding an employee.
- Natural Language Queries are parsed using AI (Gemini) and expected to return a specific JSON structure.
- Date Handling supports:
  - today
  - tomorrow
  - Specific dates in YYYY-MM-DD or natural language formats like "next Monday" (powered by dateparser).
- Leave Reset:
  - Annual leave balances can be reset every January 1st (auto-reset logic can be triggered on app run).
- Data Persistence:
  - Data is stored in a local data/data.json file.
  - Logs are recorded in logs/actions.log.
- No concurrency control — not designed for simultaneous multi-user access.

## ✅ Features

- Natural language leave management
- Admin-only employee management
- Leave request approval/rejection (planned extension)
- Leave cancellation
- Leave history tracking
- AI-assisted intent recognition
- Flexible date parsing
