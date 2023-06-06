import sqlite3
import click
import getpass
import hashlib
import time
from datetime import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect('budget.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE,
                  password_hash TEXT NOT NULL, email TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS income
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
                  amount FLOAT NOT NULL, date DATE NOT NULL, user_id INTEGER NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
                  amount FLOAT NOT NULL, date DATE NOT NULL, user_id INTEGER NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
                  amount FLOAT NOT NULL, user_id INTEGER NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS savings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, savings_goal FLOAT NOT NULL,
                  current_savings FLOAT NOT NULL, user_id INTEGER NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@click.command()
def register():
    """Register a new user."""
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    password_hash = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", (username, password_hash, email))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username or email already exists.")
        conn.rollback()

@click.command()
def login():
    """Log in to the budget tracker."""
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_hash = hash_password(password)
    c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password_hash))
    user = c.fetchone()
    if user:
        print(f"Welcome back, {user[1]}!")
    else:
        print("Invalid username or password.")

@click.command()
def logout():
    """Log out of the budget tracker."""
    print("Goodbye!")
    conn.close()

@click.group()
def cli():
    pass

cli.add_command(register)
cli.add_command(login)
cli.add_command(logout)

if __name__ == '__main__':
    create_tables()
    cli()