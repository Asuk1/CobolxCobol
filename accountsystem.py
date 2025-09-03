# Simple Account Management System - COBOL logic replicated in Python
# Single class, single file, ready to run

class AccountSystem:
    def __init__(self):
        # Initial balance, matches COBOL default
        self.balance = 1000.00

    def display_menu(self):
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")

    def view_balance(self):
        print(f"Current balance: {self.balance:.2f}")

    def credit_account(self):
        try:
            amount = float(input("Enter credit amount: "))
            if amount < 0:
                print("Invalid amount. Please enter a positive value.")
                return
            # Read balance (simulated)
            self.balance += amount
            # Write balance (simulated)
            print(f"Amount credited. New balance: {self.balance:.2f}")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def debit_account(self):
        try:
            amount = float(input("Enter debit amount: "))
            if amount < 0:
                print("Invalid amount. Please enter a positive value.")
                return
            # Read balance (simulated)
            if self.balance >= amount:
                self.balance -= amount
                # Write balance (simulated)
                print(f"Amount debited. New balance: {self.balance:.2f}")
            else:
                print("Insufficient funds for this debit.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def run(self):
        continue_flag = 'YES'
        while continue_flag == 'YES':
            self.display_menu()
            choice = input("Enter your choice (1-4): ").strip()
            if choice == '1':
                self.view_balance()
            elif choice == '2':
                self.credit_account()
            elif choice == '3':
                self.debit_account()
            elif choice == '4':
                continue_flag = 'NO'
            else:
                print("Invalid choice, please select 1-4.")
        print("Exiting the program. Goodbye!")

if __name__ == "__main__":
    # Run the account management system
    account_system = AccountSystem()
    account_system.run()