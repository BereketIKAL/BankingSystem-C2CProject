from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    # Optionally, you can remove this if you no longer use the JSON file
    return {}

def check_credentials(account_number, pin):
    connection = connect_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            # Debug print
            print(f"Checking credentials for account_number={account_number}, pin={pin}")
            query = "SELECT account_number, pin FROM users WHERE account_number = %s"
            cursor.execute(query, (account_number,))
            result = cursor.fetchone()
            if result:
                db_account_number, db_pin = str(result[0]), str(result[1])
                print(f"DB returned: account_number={db_account_number}, pin={db_pin}")
                return db_account_number == str(account_number) and db_pin == str(pin)
            return False
    except Error as e:
        print(f"Error checking credentials: {e}")
        return False
    finally:
        connection.close()

def connect_db():
    try:
        connection = connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "Test"),
            password=os.getenv("DB_PASSWORD", "password!"),
            database=os.getenv("DB_NAME", "BankingSystem")
            # Remove auth_plugin argument
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_account(account_number, pin, name, date_of_birth, user_type="customer", initial_balance=0.00):
    # Ensure PIN is not longer than 4 characters
    if len(str(pin)) > 4:
        print("Error: PIN must be at most 4 digits.")
        return False
    connection = connect_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            user_query = """
            INSERT INTO users (account_number, pin, name, date_of_birth, user_type)
            VALUES (%s, %s, %s, %s, %s)
            """
            # Ensure pin is stored as string
            cursor.execute(user_query, (str(account_number), str(pin), name, date_of_birth, user_type))
            account_query = """
            INSERT INTO accounts (account_number, balance)
            VALUES (%s, %s)
            """
            cursor.execute(account_query, (str(account_number), initial_balance))
            connection.commit()
            print(f"Account created: {account_number}, PIN: {pin}")
            return True
    except Error as e:
        print(f"Error creating account: {e}")
        return False
    finally:
        connection.close()

def get_balance(account_number):
    connection = connect_db()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "SELECT balance FROM accounts WHERE account_number = %s"
            cursor.execute(query, (account_number,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return 0.0
    except Error as e:
        print(f"Error getting balance: {e}")
        return 0.0
    finally:
        connection.close()

def deposit(account_number, amount):
    if amount <= 0:
        print("Deposit amount must be positive.")
        return False
    connection = connect_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
            cursor.execute(query, (amount, account_number))
            if cursor.rowcount == 0:
                print("Account not found.")
                return False
            connection.commit()
            return True
    except Error as e:
        print(f"Error depositing: {e}")
        return False
    finally:
        connection.close()

def withdraw(account_number, amount):
    if amount <= 0:
        print("Withdrawal amount must be positive.")
        return False
    connection = connect_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            # Check balance first
            balance_query = "SELECT balance FROM accounts WHERE account_number = %s"
            cursor.execute(balance_query, (account_number,))
            result = cursor.fetchone()
            if not result or result[0] < amount:
                print("Insufficient funds.")
                return False
            # Deduct amount
            withdraw_query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
            cursor.execute(withdraw_query, (amount, account_number))
            connection.commit()
            return True
    except Error as e:
        print(f"Error withdrawing: {e}")
        return False
    finally:
        connection.close()

def get_account_name(account_number):
    connection = connect_db()
    if not connection:
        return ""
    try:
        with connection.cursor() as cursor:
            query = "SELECT name FROM users WHERE account_number = %s"
            cursor.execute(query, (account_number,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return ""
    except Error as e:
        print(f"Error getting account name: {e}")
        return ""
    finally:
        connection.close()

def update_balance(account_number, new_balance):
    connection = connect_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
            cursor.execute(query, (new_balance, account_number))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating balance: {e}")
        return False
    finally:
        connection.close()

# Add other functions like delete_account, modify_account, verify_user as needed

if __name__ == "__main__":
    # Test database connection
    connection = connect_db()
    if connection:
        print("Database connection successful!")
        connection.close()
    else:
        print("Database connection failed.")