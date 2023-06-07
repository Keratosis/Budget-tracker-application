import click
from database import create_tables
from models import User, Transaction, Budget, create_tables
from utils import clear_screen
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

# Global variable to track the authenticated user
authenticated_user = None

Session = sessionmaker(bind=create_engine("sqlite:///budget_tracker.db"))

@click.command()
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

@click.command()
@click.option("--user-id", type=int, help="User ID for generating the report")
def generate_report(user_id):
    """Generate a report of transactions for a specific user."""
    if authenticated_user is None:
        click.echo("Please login first.")
        return

    if user_id != authenticated_user.id:
        click.echo("You are not authorized to access this report.")
        return

    session = Session()
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()
    session.close()

    click.echo(f"Report for User ID: {user_id}")
    click.echo("Transactions:")
    for transaction in transactions:
        click.echo(f"ID: {transaction.id}")
        click.echo(f"Type: {transaction.type}")
        click.echo(f"Category: {transaction.category}")
        click.echo(f"Amount: {transaction.amount}")
        click.echo(f"Date: {transaction.date}")
        click.echo("------------------------")

@click.command()
def register_user():
    """User registration functionality."""
    username = click.prompt("Enter your username")
    password = click.prompt("Enter your password")
    email = click.prompt("Enter your email")

    session = Session()
    existing_user = session.query(User).filter_by(username=username).first()

    if existing_user is not None:
        click.echo("Username already exists. Please log in or choose a different username.")
        session.close()
        return

    new_user = User(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    session.close()

    click.echo("Registration successful.")
    show_user_menu()  # Redirect to the user menu after successful registration

@click.command()
def login():
    """Login functionality."""
    username = click.prompt("Enter your username")
    password = click.prompt("Enter your password")

    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user is None:
        click.echo("User not found. Please register first.")
        return

    # Store the authenticated user's information in the session or as a global variable
    global authenticated_user
    authenticated_user = user

    click.echo("Login successful.")
    show_user_menu()  # Show the user menu directly after successful login

# Rest of the code remains the same

def print_menu():
    print("Budget Tracker CLI")
    print("-------------------")
    print("1. Register")
    print("2. Login")

def print_user_menu():
    print("1. Add a transaction")
    print("2. View all transactions")
    print("3. Delete a transaction")
    print("4. Generate report")
    print("5. Logout")
    print("6. Exit")

def show_user_menu():
    clear_screen()

    while True:
        print_user_menu()
        choice = click.prompt("Enter your choice (1-6): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            delete_transaction()
        elif choice == "4":
            generate_report(authenticated_user.id)
        elif choice == "5":
            logout()
            break  # Exit the user menu and return to the main menu
        elif choice == "6":
            exit_program()
        else:
            click.echo("Invalid choice. Please try again.")

def logout():
    """Logout the authenticated user."""
    global authenticated_user
    authenticated_user = None
    click.echo("Logged out successfully.")

def exit_program():
    """Exit the program."""
    click.echo("Exiting the program. Goodbye!")
    raise SystemExit

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

    transaction = Transaction(type=transaction_type, category=category, amount=amount, date=date, user_id=authenticated_user.id)
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
    session = Session()
    transactions = session.query(Transaction).filter_by(user_id=authenticated_user.id).all()
    session.close()

    if not transactions:
        click.echo("No transactions found.")
        return

    for transaction in transactions:
        click.echo(f"ID: {transaction.id}")
        click.echo(f"Type: {transaction.type}")
        click.echo(f"Category: {transaction.category}")
        click.echo(f"Amount: {transaction.amount}")
        click.echo(f"Date: {transaction.date}")
        click.echo("------------------------")

def plot_transaction_amounts(transactions):
    """Plot a bar chart of transaction amounts."""
    categories = [transaction.category for transaction in transactions]
    amounts = [transaction.amount for transaction in transactions]

    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Transaction Amounts")
    plt.show()

def main():
    create_tables()
    clear_screen()

    while True:
        print_menu()
        choice = click.prompt("Enter your choice (1-2): ")

        if choice == "1":
            register_user()
            break  # Exit the main loop after successful registration
        elif choice == "2":
            login()
            break  # Exit the main loop after successful login
        else:
            click.echo("Invalid choice. Please try again.")

    if authenticated_user is not None:
        show_user_menu()

if __name__ == "__main__":
    main()
