import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import mysql.connector
import os


class BankingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Bank")
        self.root.geometry("400x500")
        
        # Initialize data storage
        self.accounts_file = "accounts.json"
        self.accounts = self.load_accounts()
        self.current_user = None
        
        # Start with login screen
        self.show_login_screen()
        
    def load_accounts(self):
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_accounts(self):
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f)
    
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
        account_entry = tk.Entry(frame)
        account_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="PIN:").grid(row=1, column=0, pady=5)
        pin_entry = tk.Entry(frame, show="*")
        pin_entry.grid(row=1, column=1, pady=5)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Create Account", 
                 command=self.show_create_account_screen).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Log in", 
                 command=lambda: self.login(account_entry.get(), pin_entry.get())).pack(side=tk.LEFT, padx=5)
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
        
        tk.Label(self.root, text=f"Welcome {self.accounts[self.current_user]['name']}!", 
                font=('Arial', 16)).pack(pady=10)
        
        # Add balance display
        balance = self.accounts[self.current_user]["balance"]
        tk.Label(self.root, text=f"Current Balance: ${balance:,.2f}", 
                font=('Arial', 14), fg='green').pack(pady=10)
        
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
        
        # Add balance display
        balance = self.accounts[self.current_user]["balance"]
        tk.Label(self.root, text=f"Current Balance: ${balance:,.2f}", 
                font=('Arial', 14), fg='green').pack(pady=10)
        
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
            
        account_number = str(len(self.accounts) + 1000)
        self.accounts[account_number] = {
            "name": name,
            "dob": dob,
            "pin": pin,
            "balance": 0
        }
        self.save_accounts()
        messagebox.showinfo("Success", f"Account created! Your account number is: {account_number}")
        self.show_login_screen()
    
    def login(self, account_number, pin):
        if account_number in self.accounts and self.accounts[account_number]["pin"] == pin:
            self.current_user = account_number
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid account number or PIN!")
    
    def check_balance(self):
        balance = self.accounts[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your balance is: ${balance:,.2f}")
        self.show_main_menu()
    
    def process_transaction(self, transaction_type, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
                
            if transaction_type == "withdraw":
                if amount > self.accounts[self.current_user]["balance"]:
                    messagebox.showerror("Error", "Insufficient funds!")
                    return
                self.accounts[self.current_user]["balance"] -= amount
                message = f"You withdrew ${amount:,.2f}"
            else:
                self.accounts[self.current_user]["balance"] += amount
                message = f"You deposited ${amount:,.2f}"
                
            self.save_accounts()
            messagebox.showinfo("Success", f"{message}. New balance: ${self.accounts[self.current_user]['balance']:,.2f}")
            self.show_main_menu()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BankingSystem()
    app.run()