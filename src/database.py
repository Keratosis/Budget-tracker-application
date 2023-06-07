from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base

# Define the database connection URL
DATABASE_URL = 'sqlite:///budget_tracker.db'

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Function to initialize the database
def initialize_database():
    Base.metadata.create_all(engine)
    print("Database initialized.")

# Function to get a new database session
def get_session():
    return Session()

# Function to add an object to the database
def add_object(obj):
    session = get_session()
    session.add(obj)
    session.commit()

# Function to query objects from the database
def query_objects(model):
    session = get_session()
    return session.query(model).all()

# Function to update an object in the database
def update_object(obj):
    session = get_session()
    session.commit()

# Function to delete an object from the database
def delete_object(obj):
    session = get_session()
    session.delete(obj)
    session.commit()

# Function to create tables in the database
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created.")

# Check if this file is executed directly
if __name__ == "__main__":
    create_tables()
