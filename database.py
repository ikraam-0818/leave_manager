import json
from config import DATA_FILE, DEFAULT_LEAVE_BALANCE
from datetime import datetime

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def reset_leave_balances_if_needed(name):
    data = load_data()
    employee = data.get(name)
    if not employee:
        return

    current_year = datetime.today().year
    last_reset_year = employee.get("last_reset_year", 0)

    if current_year > last_reset_year:
        # Reset balances
        employee["leave_balance"] = DEFAULT_LEAVE_BALANCE.copy()
        employee["last_reset_year"] = current_year
        save_data(data)

def get_employee(name):
    data = load_data()
    return data.get(name)


def update_employee(name, employee_data):
    data = load_data()
    data[name] = employee_data
    save_data(data)


def add_employee(name, leave_balance):
    data = load_data()
    if name in data:
        return False 

    new_employee = {
        "leave_balance": leave_balance,
        "leave_history": []
    }
    data[name] = new_employee
    save_data(data)
    return True


def list_employees():
    data = load_data()
    return list(data.keys())


def remove_employee(name):
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
        return True
    return False
