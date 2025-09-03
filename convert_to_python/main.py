# main_program.py - Equivalent to COBOL MainProgram
from operations import Operations

class MainProgram:
    """Main program - handles menu display and user interaction"""

    def __init__(self):
        self.continue_flag = 'YES'
        self.operations = Operations()

    def run(self):
        """Main logic - equivalent to COBOL MAIN-LOGIC paragraph"""
        while self.continue_flag == 'YES':
            self._display_menu()
            user_choice = self._get_user_choice()

            try:
                if user_choice == 1:  # View balance
                    balance = self.operations.call_program('TOTAL')
                    print(f"Current balance: {balance:.2f}")

                elif user_choice == 2:  # Credit
                    amount = self._get_amount("Enter credit amount: ")
                    balance = self.operations.call_program('CREDIT', amount)
                    print(f"Amount credited. New balance: {balance:.2f}")

                elif user_choice == 3:  # Debit
                    amount = self._get_amount("Enter debit amount: ")
                    balance = self.operations.call_program('DEBIT', amount)
                    print(f"Amount debited. New balance: {balance:.2f}")

                elif user_choice == 4:  # Exit
                    self.continue_flag = 'NO'

                else:
                    print("Invalid choice, please select 1-4.")

            except ValueError as e:
                print(e)

        print("Exiting the program. Goodbye!")

    def _display_menu(self):
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")

    def _get_user_choice(self):
        while True:
            try:
                return int(input("Enter your choice (1-4): ").strip())
            except ValueError:
                print("Invalid input, please enter a number between 1 and 4.")

    def _get_amount(self, prompt):
        while True:
            try:
                amount = float(input(prompt).strip())
                if amount < 0:
                    print("Amount must be zero or positive.")
                else:
                    return amount
            except ValueError:
                print("Invalid amount, please enter a valid number.")

def main():
    program = MainProgram()
    program.run()

if __name__ == "__main__":
    main()
