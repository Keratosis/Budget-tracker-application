import os
import datetime
import re


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")

def validate_date(date_str):
    """Validate a date string in the format 'YYYY-MM-DD'."""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_currency(amount):
    """Format an amount as currency."""
    return f"${amount:.2f}"

def calculate_total(transactions):
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return total

def format_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%B %d, %Y")

def display_progress_bar(progress):
    bar_length = 20
    filled_length = int(progress * bar_length)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    percentage = int(progress * 100)
    print(f"[{bar}] {percentage}% completed")

def validate_email(email):
    """Validate an email address."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def sanitize_input(user_input):
    """Sanitize user input by removing leading/trailing whitespace."""
    return user_input.strip()