import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('budget_tracker.db')
cursor = conn.cursor()

# Create the necessary table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        category TEXT,
        amount REAL,
        date TEXT
    )
''')
conn.commit()


def add_transaction():
    print("Add a new transaction:")
    transaction_type = input("Type (income/expense): ")
    category = input("Category: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")

    # Insert the transaction into the database
    cursor.execute('''
        INSERT INTO transactions (type, category, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (transaction_type, category, amount, date))
    conn.commit()
    print("Transaction added successfully!")


def view_transactions():
    print("Viewing all transactions:")

    # Retrieve all transactions from the database
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(f"ID: {transaction[0]}")
        print(f"Type: {transaction[1]}")
        print(f"Category: {transaction[2]}")
        print(f"Amount: {transaction[3]}")
        print(f"Date: {transaction[4]}")
        print("------------------------")

def main():
    print("Welcome to the Budget Tracker CLI!")
    print("----------------------------------")

    while True:
        print("\nSelect an option:")
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Thank you for using the Budget Tracker CLI!")

# Run the application
if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
