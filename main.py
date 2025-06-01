import json
from datetime import datetime
from ai import extract_intent_and_entities
from database import get_employee, update_employee, add_employee, list_employees, remove_employee, reset_leave_balances_if_needed
from employee import Employee, LeaveRequest
from config import LEAVE_TYPES, LEAVE_TYPE_ALIASES
from utils import is_valid_date, parse_natural_date
from logger import log_action

def parse_ai_response(response_text):
    """Clean and parse AI response JSON."""
    if response_text.startswith("```"):
        response_text = response_text.strip("`")
        if response_text.lower().startswith("json"):
            response_text = response_text[4:].strip()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None

def handle_check_balance(employee, leave_type=None):
    if leave_type:
        balance = employee["leave_balance"].get(leave_type, "N/A")
        print(f"You have {balance} {leave_type} remaining.")
        log_action("User", "Checked Leave Balance", f"{leave_type}: {balance}")
    else:
        print("Your leave balances:")
        for lt, bal in employee["leave_balance"].items():
            print(f"- {lt}: {bal}")
        log_action("User", "Checked All Leave Balances")

def handle_request_leave(employee_name, employee, leave_type, num_days, start_date):
    if leave_type not in LEAVE_TYPES:
        print("Invalid leave type.")
        log_action(employee_name, "Invalid Leave Type", leave_type)
        return

    if not is_valid_date(start_date):
        print("Invalid start date.")
        log_action(employee_name, "Invalid Start Date", start_date)
        return

    balance = employee["leave_balance"].get(leave_type, 0)
    if balance < num_days:
        print(f"Sorry, you only have {balance} {leave_type} remaining.")
        log_action(employee_name, "Insufficient Balance", f"{leave_type}: {balance}, Requested: {num_days}")
        return

    new_request = LeaveRequest(leave_type, start_date, num_days)
    employee_obj = Employee(employee_name, employee["leave_balance"], employee["leave_history"])
    employee_obj.add_leave_request(new_request)
    employee["leave_balance"][leave_type] -= num_days
    employee["leave_history"] = employee_obj.leave_history

    update_employee(employee_name, employee)
    print(f"Leave request for {num_days} {leave_type} starting {start_date} submitted successfully.")
    log_action(employee_name, "Requested Leave", f"{leave_type}, {num_days} days from {start_date}")

def handle_cancel_leave(employee_name, employee, leave_type, start_date):
    found = False
    for req in employee["leave_history"]:
        if req["leave_type"] == leave_type and req["start_date"] == start_date and req["status"] == "Pending":
            req["status"] = "Cancelled"
            found = True
            break

    if found:
        update_employee(employee_name, employee)
        print(f"Leave on {start_date} for {leave_type} cancelled.")
        log_action(employee_name, "Cancelled Leave", f"{leave_type} on {start_date}")
    else:
        print("No matching pending leave request found.")
        log_action(employee_name, "Cancel Leave Failed", f"{leave_type} on {start_date} not found")

def handle_view_history(employee):
    if not employee["leave_history"]:
        print("No leave history found.")
        log_action("User", "Viewed Leave History", "No history found")
    else:
        print("Your leave history:")
        for req in employee["leave_history"]:
            print(f"- {req['leave_type']} from {req['start_date']} for {req['number_of_days']} days (Status: {req['status']})")
        log_action("User", "Viewed Leave History")

def admin_mode():
    print("Entering Admin Mode")
    while True:
        print("\n[1] Add Employee\n[2] List Employees\n[3] Remove Employee\n[4] Exit Admin Mode")
        choice = input("Select option: ").strip()

        if choice == "1":
            name = input("Employee Name: ").strip()
            leave_balance = {}
            for lt in LEAVE_TYPES:
                bal = int(input(f"Initial {lt} balance: "))
                leave_balance[lt] = bal
            if add_employee(name, leave_balance):
                print(f"Employee {name} added successfully.")
            else:
                print(f"Employee {name} already exists.")

        elif choice == "2":
            employees = list_employees()
            print("Employees:")
            for emp in employees:
                print(f"- {emp}")

        elif choice == "3":
            name = input("Employee Name to Remove: ").strip()
            if remove_employee(name):
                print(f"Employee {name} removed.")
            else:
                print(f"No employee named {name} found.")

        elif choice == "4":
            print("Exiting Admin Mode.")
            break
        else:
            print("Invalid option.")


def run():
    mode = input("Select mode (user/admin): ").strip().lower()

    if mode == "admin":
        admin_mode()
        return

    employee_name = input("Enter your name: ").strip()
    employee = get_employee(employee_name)
    if not employee:
        print(f"No record found for {employee_name}. Please contact admin.")
        return

    print(f"Welcome {employee_name}! How can I assist you today?")

    reset_leave_balances_if_needed(employee_name)
    employee = get_employee(employee_name)

    while True:
        user_input = input(">> ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        try:
            ai_response = extract_intent_and_entities(user_input)
            print(f"[AI Response]: {ai_response}")

            parsed = parse_ai_response(ai_response)
            if not parsed:
                print("Could not parse AI response. Please try phrasing your request differently.")
                log_action(employee_name, "AI Parse Error", user_input)
                continue

            intent = parsed.get("intent")
            leave_type = parsed.get("leave_type")
            num_days = parsed.get("number_of_days")
            start_date = parsed.get("start_date")

            # Map AI's leave_type to config LEAVE_TYPES if alias exists
            if leave_type in LEAVE_TYPE_ALIASES:
                leave_type = LEAVE_TYPE_ALIASES[leave_type]

            # Convert natural language dates to actual date string
            if start_date:
                start_date = parse_natural_date(start_date)
                if not start_date:
                    print("Could not recognize the start date. Please rephrase.")
                    continue

            if intent == "check_balance":
                handle_check_balance(employee, leave_type)
            elif intent == "request_leave":
                handle_request_leave(employee_name, employee, leave_type, num_days, start_date)
            elif intent == "cancel_leave":
                handle_cancel_leave(employee_name, employee, leave_type, start_date)
            elif intent == "view_history":
                handle_view_history(employee)
            else:
                print("Sorry, I couldn't understand that request.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            log_action(employee_name, "Unhandled Error", str(e))

if __name__ == "__main__":
    run()
