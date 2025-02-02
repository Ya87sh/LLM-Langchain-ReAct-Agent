#importing libraries

import sqlite3
import re
from langchain.tools import tool # type: ignore

# Initialize SQLite Database
def setup_database():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

# Check if the customer exists in the database by email
@tool
def check_existing_customer_email(email: str) -> str:

    """
    Checks if a customer exists in the database by email.
    """
    
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    customer = cursor.fetchone()
    conn.close()
    
    if customer:
        # Return customer details if found
        return f"Customer exists: Name={customer[1]}, Email={customer[2]}, Phone={customer[3]}"
    else:
        # Return a clear message if not found
        return "No customer found with the provided email address."

# Check if the customer exists in the database by name
@tool
def check_existing_customer_name(name: str) -> str:

    """
    Checks if a customer exists in the database by name.
    """
    
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE name = ?", (name,))
    customer = cursor.fetchone()
    conn.close()
    
    if customer:
        # Return customer details if found
        return f"Customer exists: Name={customer[1]}, Email={customer[2]}, Phone={customer[3]}"
    else:
        # Return a clear message if not found
        return "No customer found with the given name."

# Check if the customer exists in the database by phone number
@tool
def check_existing_customer_phone(phone: str) -> str:

    """
    Checks if a customer exists in the database by phone number.
    """
    
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE phone = ?", (phone,))
    customer = cursor.fetchone()
    conn.close()
    
    if customer:
        # Return customer details if found
        return f"Customer exists: Name={customer[1]}, Email={customer[2]}, Phone={customer[3]}"
    else:
        # Return a clear message if not found
        return "No customer found with the given name."

# Add a new customer to the database
@tool
def add_new_customer(input_data: str) -> str:
    """
    Adds a new customer to the database. Accepts natural language input like:
    'Hi, I am Yash, my email is "abc@example.com" and my phone number is 8456258965.'
    """

    # Extract name, email, and phone using regex
    name_match = re.search(r"(?:I am|My name is|Hi, this is)\s([A-Za-z\s]+)", input_data, re.IGNORECASE)
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", input_data)
    phone_match = re.search(r"\b\d{10}\b", input_data)

    if not (name_match and email_match and phone_match):
        return "Error: Could not extract name, email, or phone from the input. Please provide complete information."

    name = name_match.group(1).strip()
    email = email_match.group(0).strip()
    phone = phone_match.group(0).strip()

    try:
        # Insert into database
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        return f"Customer {name} added successfully!"
    except sqlite3.IntegrityError:
        return "Error: Duplicate email found."
    finally:
        conn.close()

# Preprocess and Validate Email Address
@tool
def validate_email(email: str) -> str:
    
    """
    Validates the format of the phone number
    """

    # Preprocess text
    email = email.lower()  # Convert to lowercase
    email = email.replace(" at ", "@")  # Replace 'at' with '@'
    email = email.replace(" dot ", ".")  # Replace 'dot' with '.'
    email = email.replace(" ", "")  # Remove unnecessary spaces

    # Validate email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Validate Phone Number
@tool
def validate_phone(phone: str) -> str:

    """
    Validates the format of the phone number.
    """

    # Preprocess phone number to remove spaces, dashes, and parentheses
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Regex to validate exactly 10 digits
    phone_regex = r'^[0-9]{10}$'
    return re.match(phone_regex, phone) is not None