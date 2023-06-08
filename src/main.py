import click
from getpass import getpass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,func
from models import User, Transaction, Budget
from utils import clear_screen
import matplotlib.pyplot as plt
import datetime
import bcrypt

# Global variable to track the authenticated user
authenticated_user = None

Session = sessionmaker(bind=create_engine("sqlite:///budget_tracker.db"))

  

@click.command()
def register_user():
    """User registration functionality."""
    username = click.prompt("Enter your username")
    password = getpass("Enter your password")
    email = click.prompt("Enter your email")

    session = Session()
    existing_user = session.query(User).filter_by(username=username).first()

    if existing_user is not None:
        click.echo("Username already exists. Please log in or choose a different username.")
        session.close()
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password, email=email)
    session.add(new_user)
    session.commit()
    session.close()

    click.echo("Registration successful.")
    login()  # Redirect to the login functionality after successful registration


@click.command()
def login():
    """Login functionality."""
    username = click.prompt("Enter your username")
    password = getpass("Enter your password")

    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user is None:
        click.echo("User not found. Please register first.")
        return

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        click.echo("Incorrect password. Please try again.")
        return 

    # Store the authenticated user's information in the session or as a global variable
    global authenticated_user
    authenticated_user = user

    click.echo("Login successful.")
    show_user_menu()  # Show the user menu directly after successful login


#user and login interface

def print_menu():
    print("Budget Tracker CLI")
    print("-------------------")
    print("1. Register")
    print("2. Login")

def print_user_menu():
    click.echo(click.style(f"Welcome, {authenticated_user.username}!", fg="cyan", bold=True))
    session = Session()
    total_income = session.query(func.sum(Transaction.amount)).filter_by(user_id=authenticated_user.id, transaction_type='income').scalar() or 0
    total_expenses = session.query(func.sum(Transaction.amount)).filter_by(user_id=authenticated_user.id, transaction_type='expense').scalar() or 0
    balance = total_income - total_expenses
    session.close()
    click.echo(click.style(f"Available Balance: {balance}", fg="green", bold=True))
    click.echo("-----------------------------")
    print("1. Add a transaction")
    print("2. View all transactions")
    print("3. Delete a transaction")
    print("4. Generate report")
    print("5. Set budget")
    print("6. Logout")
    print("7. Exit")

def show_user_menu():
    clear_screen()

    while True:
        print_user_menu()
        choice = click.prompt("Enter your choice (1-7): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            delete_transaction()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            generate_report()
        elif choice == "6":
            logout()
            break  # Exit the user menu and return to the main menu
        elif choice == "7":
            exit_program()
        else:
            click.echo("Invalid choice. Please try again.")


def add_transaction():
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    click.echo("Add a new transaction:")
    transaction_type = click.prompt("Type (income/expense): ")
    category = click.prompt("Category: ")
    amount_str = click.prompt("Amount: ")
    amount = float(amount_str.replace(",", ""))
    date_str = click.prompt("Date (YYYY-MM-DD): ")
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    transaction = Transaction(transaction_type=transaction_type, category=category, amount=amount, date=date, user_id=authenticated_user.id)
    session = Session()
    session.add(transaction)
    session.commit()
    session.close()

    click.echo("Transaction added successfully!")

def view_transactions():
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    click.echo("Viewing all transactions:")
    click.echo("*********************  ")
    click.echo("Viewing all transactions:")
    session = Session()
    transactions = session.query(Transaction).filter_by(user_id=authenticated_user.id).all()
    session.close()

    if not transactions:
        click.echo("No transactions found.")
        return

    for transaction in transactions:
        click.echo(f"ID: {transaction.id}")
        click.echo(f"Type: {transaction.transaction_type}")
        click.echo(f"Category: {transaction.category}")
        click.echo(f"Amount: {transaction.amount}")
        click.echo(f"Date: {transaction.date}")
        click.echo("------------------------")
        
        

def delete_transaction():
    """Delete a transaction from the database."""
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    transaction_id = click.prompt("Enter the transaction ID")
    session = Session()
    transaction = session.query(Transaction).get(transaction_id)
    if transaction:
        session.delete(transaction)
        session.commit()
        click.echo("Transaction deleted successfully.")
    else:
        click.echo("Transaction not found.")
        
    session.close()

def set_budget():
    """Set the budget for the authenticated user."""
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    click.echo("Set Budget:")
    category = click.prompt("Enter the budget category: ")
    amount_str = click.prompt("Enter the budget amount: ")
    amount = float(amount_str.replace(",", ""))

    session = Session()
    existing_budget = session.query(Budget).filter_by(user_id=authenticated_user.id, category=category).first()

    if existing_budget:
        existing_budget.amount = amount
        click.echo("Budget updated successfully.")
    else:
        new_budget = Budget(user_id=authenticated_user.id, category=category, amount=amount)
        session.add(new_budget)
        click.echo("Budget set successfully.")

    session.commit()
    session.close()

@click.option("--user-id", type=int, help="User ID for generating the report")
def generate_report(user_id=None):
    """Generate a report of transactions for a specific user."""
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    if user_id is not None and user_id != authenticated_user.id:
        click.echo("You are not authorized to access this report.")
        return

    session = Session()
    if user_id is None:
        transactions = session.query(Transaction).filter_by(user_id=authenticated_user.id).all()
        click.echo(f"Report for User ID: {authenticated_user.id}")
    else:
        transactions = session.query(Transaction).filter_by(user_id=user_id).all()
        click.echo(f"Report for User ID: {user_id}")
    session.close()

    if not transactions:
        click.echo("No transactions found.")
        return

    click.echo("Transactions:")
    for transaction in transactions:
        click.echo(f"ID: {transaction.id}")
        click.echo(f"Type: {transaction.transaction_type}")
        click.echo(f"Category: {transaction.category}")
        click.echo(f"Amount: {transaction.amount}")
        click.echo(f"Date: {transaction.date}")
        click.echo("------------------------")


def logout():
    """Logout the authenticated user."""
    global authenticated_user
    authenticated_user = None
    click.echo("Logged out successfully.")
    
    main()
     

def exit_program():
    """Exit the program."""
    click.echo("Exiting the program. Goodbye!")
    raise SystemExit



def main():
    clear_screen()

    while True:
        print_menu()
        choice = click.prompt("Enter your choice (1-2): ")

        if choice == "1":
            register_user()
            break  # Exit the main loop after successful registration
        elif choice == "2":
            login()
            if authenticated_user is not None:
                show_user_menu()  # Show the user menu if login is successful
            break  # Exit the main loop after successful login
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
