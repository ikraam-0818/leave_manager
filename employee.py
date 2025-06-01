class LeaveRequest:

    VALID_STATUSES = ["Pending", "Approved", "Rejected", "Cancelled"]

    def __init__(self, leave_type, start_date, number_of_days, status="Pending"):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self.leave_type = leave_type
        self.start_date = start_date
        self.number_of_days = number_of_days
        self.status = status

    def update_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

    def to_dict(self):
        return {
            "leave_type": self.leave_type,
            "start_date": self.start_date,
            "number_of_days": self.number_of_days,
            "status": self.status
        }


class Employee:
    def __init__(self, name, leave_balance, leave_history=None):
        self.name = name
        self.leave_balance = leave_balance
        self.leave_history = leave_history if leave_history else []

    def add_leave_request(self, leave_request):
        self.leave_history.append(leave_request.to_dict())


# Admin
class Admin:
    def __init__(self):
        pass

    def add_employee(self, name, leave_balance):
        from database import add_employee
        return add_employee(name, leave_balance)

    def list_employees(self):
        from database import list_employees
        return list_employees()

    def remove_employee(self, name):
        from database import remove_employee
        return remove_employee(name)

    def update_employee_balance(self, name, leave_type, new_balance):
        from database import get_employee, update_employee

        employee = get_employee(name)
        if not employee:
            return False, "Employee not found."

        if leave_type not in employee["leave_balance"]:
            return False, "Invalid leave type."

        employee["leave_balance"][leave_type] = new_balance
        update_employee(name, employee)
        return True, f"{leave_type} balance updated to {new_balance} for {name}."
    
    def update_leave_status(self, employee_name, leave_type, start_date, new_status):
        from database import get_employee, update_employee
        emp = get_employee(employee_name)
        if not emp:
            return False, "Employee not found."

        found = False
        for req in emp["leave_history"]:
            if req["leave_type"] == leave_type and req["start_date"] == start_date:
                req["status"] = new_status
                found = True
                break

        if found:
            update_employee(employee_name, emp)
            return True, f"Updated to {new_status}"
        else:
            return False, "Leave request not found."

    def view_employee_history(self, name):
        from database import get_employee

        employee = get_employee(name)
        if not employee:
            return None, "Employee not found."

        history = employee.get("leave_history", [])
        return history, None
