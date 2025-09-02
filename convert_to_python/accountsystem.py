# Python implementation of the COBOL Account Management System
# Replicates EXACTLY the COBOL logic, menu, validation, and error handling

class AccountSystem:
    def __init__(self):
        self.balance = 1000.00
        self.running = True

    def display_menu(self):
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")

    def get_choice(self):
        while True:
            try:
                choice = int(input("Enter your choice (1-4): ").strip())
                if choice in [1, 2, 3, 4]:
                    return choice
                else:
                    print("Invalid choice, please select 1-4.")
            except ValueError:
                print("Invalid input, please enter a number between 1 and 4.")

    def view_balance(self):
        print(f"Current balance: {self.balance:.2f}")

    def credit_account(self):
        amount = self.get_amount("Enter credit amount: ")
        self.balance += amount
        print(f"Amount credited. New balance: {self.balance:.2f}")

    def debit_account(self):
        amount = self.get_amount("Enter debit amount: ")
        if self.balance >= amount:
            self.balance -= amount
            print(f"Amount debited. New balance: {self.balance:.2f}")
        else:
            print("Insufficient funds for this debit.")

    def get_amount(self, prompt):
        while True:
            try:
                raw = input(prompt).strip()
                amount = float(raw)
                if amount < 0:
                    print("Amount must be zero or positive.")
                else:
                    return amount
            except ValueError:
                print("Invalid amount, please enter a valid number.")

    def run(self):
        while self.running:
            self.display_menu()
            choice = self.get_choice()
            if choice == 1:
                self.view_balance()
            elif choice == 2:
                self.credit_account()
            elif choice == 3:
                self.debit_account()
            elif choice == 4:
                self.running = False
                print("Exiting the program. Goodbye!")

if __name__ == "__main__":
    AccountSystem().run()
