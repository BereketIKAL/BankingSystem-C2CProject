import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import random
import decimal

# Import db functions
import db

class BankingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Bank")
        self.root.geometry("400x500")
        self.current_user = None
        self.show_login_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    #Login screen
    def show_login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Tiger Bank 🐯", font=('Arial', 16)).pack(pady=20)
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Label(frame, text="Account Number:").grid(row=0, column=0, pady=5)
        self.account_entry = tk.Entry(frame)
        self.account_entry.grid(row=0, column=1, pady=5)
        tk.Label(frame, text="PIN:").grid(row=1, column=0, pady=5)
        self.pin_entry = tk.Entry(frame, show="*")
        self.pin_entry.grid(row=1, column=1, pady=5)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Create Account", 
                 command=self.show_create_account_screen).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Log in", 
                 command=lambda: self.login(self.account_entry.get(), self.pin_entry.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", 
                 command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    #Creating the account screen
    def show_create_account_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Create a new account", font=('Arial', 16)).pack(pady=20)
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Label(frame, text="Name:").grid(row=0, column=0, pady=5)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=0, column=1, pady=5)
        tk.Label(frame, text="Date of birth:").grid(row=1, column=0, pady=5)
        dob_entry = tk.Entry(frame)
        dob_entry.grid(row=1, column=1, pady=5)
        tk.Label(frame, text="PIN:").grid(row=2, column=0, pady=5)
        pin_entry = tk.Entry(frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Create", 
                 command=lambda: self.create_account(name_entry.get(), dob_entry.get(), pin_entry.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", 
                 command=self.show_login_screen).pack(side=tk.LEFT, padx=5)
    
    def show_main_menu(self):
        self.clear_window()
        # Get account name and balance from db
        name = db.get_account_name(self.current_user)
        balance = db.get_balance(self.current_user)
        tk.Label(self.root, text=f"Welcome {name}!", font=('Arial', 16)).pack(pady=10)
        tk.Label(self.root, text=f"Current Balance: ${balance:,.2f}", font=('Arial', 14), fg='green').pack(pady=10)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Check Balance", 
                 command=self.check_balance).pack(pady=5)
        tk.Button(button_frame, text="Deposit Money", 
                 command=lambda: self.show_transaction_screen("deposit")).pack(pady=5)
        tk.Button(button_frame, text="Withdraw", 
                 command=lambda: self.show_transaction_screen("withdraw")).pack(pady=5)
        tk.Button(button_frame, text="Edit Account", 
                 command=self.show_edit_account_screen).pack(pady=5)
        tk.Button(button_frame, text="Exit", 
                 command=self.show_login_screen).pack(pady=5)
    
    #Transaction screen
    def show_transaction_screen(self, transaction_type):
        self.clear_window()
        title = "Deposit Money" if transaction_type == "deposit" else "Withdraw Money"
        tk.Label(self.root, text=title, font=('Arial', 16)).pack(pady=10)
        balance = db.get_balance(self.current_user)
        tk.Label(self.root, text=f"Current Balance: ${balance:,.2f}", font=('Arial', 14), fg='green').pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Label(frame, text="Amount:").pack()
        amount_entry = tk.Entry(frame)
        amount_entry.pack(pady=5)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Submit", 
                 command=lambda: self.process_transaction(transaction_type, amount_entry.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", 
                 command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
    
    #Creating the account
    def create_account(self, name, dob, pin):
        if not all([name, dob, pin]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if len(str(pin)) > 4:
            messagebox.showerror("Error", "PIN must be at most 4 digits!")
            return
        # Validate date format (expecting YYYY-MM-DD)
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date of birth must be in YYYY-MM-DD format!")
            return
        try:
            # Generate a random 8-digit account number
            account_number = str(random.randint(10**7, 10**8 - 1))
            # Pass account_number to db.create_account
            db.create_account(account_number=account_number, name=name, date_of_birth=dob, pin=pin)
            messagebox.showinfo("Success", f"Account created! Your account number is: {account_number}")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")
    
    def login(self, account_number, pin):
        try:
            # Strip whitespace from inputs
            account_number = account_number.strip()
            pin = pin.strip()
            if len(str(pin)) > 4:
                messagebox.showerror("Error", "PIN must be at most 4 digits!")
                return
            # Use db.check_credentials (must be implemented in db.py)
            if db.check_credentials(account_number, pin):
                self.current_user = account_number
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Invalid account number or PIN!")
        except Exception as e:
            import json
            if isinstance(e, json.decoder.JSONDecodeError):
                messagebox.showerror("Error", "Database file is empty or corrupted. Please create an account first.")
            else:
                messagebox.showerror("Error", f"Login failed: {e}")
            print(f"Login error: {e}")
    
    def check_balance(self):
        balance = db.get_balance(self.current_user)
        messagebox.showinfo("Balance", f"Your balance is: ${balance:,.2f}")
        self.show_main_menu()
    
    def process_transaction(self, transaction_type, amount):
        try:
            amount = decimal.Decimal(amount)
            if amount <= 0:
                raise ValueError
            balance = db.get_balance(self.current_user)
            # Ensure balance is Decimal
            if not isinstance(balance, decimal.Decimal):
                balance = decimal.Decimal(str(balance))
            if transaction_type == "withdraw":
                if amount > balance:
                    messagebox.showerror("Error", "Insufficient funds!")
                    return
                new_balance = balance - amount
                db.update_balance(self.current_user, new_balance)
                message = f"You withdrew ${amount:,.2f}"
            else:
                new_balance = balance + amount
                db.update_balance(self.current_user, new_balance)
                message = f"You deposited ${amount:,.2f}"
            messagebox.showinfo("Success", f"{message}. New balance: ${new_balance:,.2f}")
            self.show_main_menu()
        except (ValueError, decimal.InvalidOperation):
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Transaction failed: {e}")
    
    def show_edit_account_screen(self):
        # Placeholder implementation
        messagebox.showinfo("Edit Account", "Edit Account feature is not implemented yet.")
        self.show_main_menu()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BankingSystem()
    app.run()