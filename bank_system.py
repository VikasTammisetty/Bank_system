# This class represents a regular bank account.
# It has the basic features: deposit, withdraw, check balance, and view transactions.
class MoneyHolder:
    def __init__(self, person_name, id_number, starting_cash):
        # Initializes the account with owner's name, ID number, and starting balance
        self._person = person_name
        self._id = id_number
        self._cash_stack = starting_cash  # Current balance
        self._money_moves = [] # List to store transaction history

    # Adds money to the account and logs the transaction
    def put_money_in(self, amount):
        if amount <= 0:
            print("You can't add zero or negative money.") # Validate input
            return
        self._cash_stack += amount   # Add amount to current balance
        note = f"Added €{amount} to account."
        self._money_moves.append(note)
        print(note) # Show confirmation

    # Withdraws money from the account after checking balance
    def pull_money_out(self, amount):
        if amount <= 0:
            print("Taking out zero or negative money? Not allowed.")
            return
        if amount > self._cash_stack:
            print("Not enough funds to make this withdrawal.")  # Prevent overdraft
            return
        self._cash_stack -= amount  # Subtract amount from balance
        note = f"Took out €{amount} from account."
        self._money_moves.append(note)
        print(note)

    # Displays the current balance
    def check_wallet(self):
        print(f"Current balance: €{self._cash_stack}")
        return self._cash_stack
    # Shows all transactions made in the account
    def show_money_moves(self):
        print("\n Transaction History:")
        if not self._money_moves:
            print("No activity yet. This account's clean as a whistle.")   # No transactions
        else:
            for i, move in enumerate(self._money_moves, 1):  # Loop through each transaction
                print(f"{i}. {move}")
        print("") 

# Savings account that gives a bonus interest on each deposit    
class SaverAccount(MoneyHolder):
    def __init__(self, person_name, id_number, starting_cash):
        super().__init__(person_name, id_number, starting_cash)  # Call parent constructor
        self._interest_rate = 0.02 
    # Overrides deposit to include 2% interest bonus
    def put_money_in(self, amount):
        if amount <= 0:
            print("You can't add zero or negative money.")
            return

        bonus = amount * self._interest_rate  # Calculate interest bonus
        total = amount + bonus
        self._cash_stack += total

        note = f"Added €{amount} with €{bonus:.2f} interest bonus. Total added: €{total:.2f}"
        self._money_moves.append(note)
        print(note)
        
# Checking account that charges a fixed fee on withdrawals
class SpenderAccount(MoneyHolder):
    def __init__(self, person_name, id_number, starting_cash):
        super().__init__(person_name, id_number, starting_cash)
        self._withdrawal_fee = 1.50 
    # Overrides withdrawal to include a €1.50 fee 
    def pull_money_out(self, amount):
        total_cost = amount + self._withdrawal_fee

        if amount <= 0:
            print("Nope, can't withdraw zero or negative money.")
            return

        if total_cost > self._cash_stack:
            print(f"Not enough money. You need €{total_cost:.2f} including the fee.")  # Check for sufficient funds
            return

        self._cash_stack -= total_cost
        note = f"Withdrew €{amount} with €{self._withdrawal_fee:.2f} fee. Total deducted: €{total_cost:.2f}"
        self._money_moves.append(note)
        print(note)

# This class manages all user accounts and handles account creation and searching
class MoneyVault:
    def __init__(self): 
        self._all_accounts = {} # Dictionary to store account objects by account number
    # Allows the user to create a new account and choose its type
    def make_new_account(self):
        print("\n Let’s get a fresh account made.")

        # Validate name input: only letters, not empty
        while True:
            name = input("Enter your name (letters only): ").strip()
            if not name.replace(" ", "").isalpha():  # Validate name
                print("Name should contain only letters. Try again.")
            elif len(name) < 2:
                print("Name too short. Try again.")
            else:
                break

        # Validate account number: exactly 8 digits
        while True:
            acc_number = input("Pick a new account number (8 digits, unique): ").strip()
            if not acc_number.isdigit() or len(acc_number) != 8:
                print("Account number must be exactly 8 digits.")
            elif acc_number in self._all_accounts:  # Check uniqueness
                print("This account number is already taken. Try a different one.")
            else:
                break

        # Validate starting balance
        try:
            start_cash = float(input("Starting balance (minimum €1): €"))
            if start_cash < 1:
                print("Starting balance must be at least €1.")   # Minimum balance
                return
        except ValueError:
            print("That wasn’t a number. Try again.")  # Validate numeric input
            return

        # Account type choice
        print("\nChoose account type:")
        print("1. Normal Account")
        print("2. Saver Account (earns 2% bonus on each deposit)")
        print("3. Spender Account (charges €1.50 fee per withdrawal)")

        acc_type = input("Enter 1, 2, or 3: ").strip()
        if acc_type == "1":
            new_acc = MoneyHolder(name, acc_number, start_cash)
        elif acc_type == "2":
            new_acc = SaverAccount(name, acc_number, start_cash)
        elif acc_type == "3":
            new_acc = SpenderAccount(name, acc_number, start_cash)
        else:
            print("Invalid option. Account not created.")
            return

        self._all_accounts[acc_number] = new_acc
        print(f" New {type(new_acc).__name__} created for {name} with number [{acc_number}] and €{start_cash}.")


    # Shows all accounts registered under a user's name
    def show_accounts_for_person(self, person_name):
        print(f"\nAccounts for {person_name}:")
        found = False
        for acc_num, acc in self._all_accounts.items():
            if acc._person.lower() == person_name.lower():  # Loop through stored accounts
                if isinstance(acc, SaverAccount):
                    acc_type = "Saver"
                elif isinstance(acc, SpenderAccount):
                    acc_type = "Spender"
                else:
                    acc_type = "Normal"

                print(f"- [{acc_type}] Account #: {acc_num} | Balance: €{acc._cash_stack}")
                found = True
        if not found:
            print("No accounts found under that name.")
    # Searches for an account by account number
    def find_account(self, acc_number):
        return self._all_accounts.get(acc_number, None)

# This function runs the main menu and handles user choices
def run_vault_terminal():
    vault = MoneyVault()   # Create a vault to manage accounts
    print("===================================")
    print("     Welcome to Money Bank     ")
    print("===================================")

    while True:
        # Display menu options
        print("\nMain Menu:")
        print("1. Make a new account")
        print("2. Use an existing account")
        print("3. View all my accounts by name")
        print("4. Leave the bank (Exit)")

        pick = input("Choose an option (1/2/3/4): ").strip()
        if not pick.isdigit() or pick not in {"1", "2", "3", "4"}:
            print("Invalid input. Please enter 1, 2, 3, or 4.")
            continue
        if pick == "1":
            vault.make_new_account()  # Create account

        elif pick == "2":
            user_id = input("Enter your account number: ")  # Ask for account number
            current_user = vault.find_account(user_id)
            if current_user:
                use_account_options(current_user)
            else:
                print("Hmm, that account doesn't exist. Check the number and try again.")
        elif pick == "3":
            name_check = input("Enter your name to see all your accounts: ")  # List user accounts
            vault.show_accounts_for_person(name_check)
        elif pick == "4":
            print("Thanks for using Simple Bank. Have a great day!")
            break   
        else:
            print("That wasn’t a valid choice. Please pick 1, 2, 3, or 4.")

# Lets the user perform actions inside a specific account
def use_account_options(account_obj):
    print(f"\n Welcome, {account_obj._person}!")
    while True:
         # Display account action menu
        print("\nWhat would you like to do?")
        print("1. Add money")
        print("2. Take money out")
        print("3. See balance")
        print("4. View money move history")
        print("5. Go back to main menu")

        choice = input("Pick an action (1-5): ")

        if choice == "1":
            try:
                amount = float(input("Enter amount to add: €"))
                account_obj.put_money_in(amount)
            except ValueError:
                print("That wasn’t a valid number.")

        elif choice == "2":
            try:
                amount = float(input("Enter amount to take out: €"))
                account_obj.pull_money_out(amount)
            except ValueError:
                print("That wasn’t a valid number.")

        elif choice == "3":
            account_obj.check_wallet()

        elif choice == "4":
            account_obj.show_money_moves()

        elif choice == "5":
            print("Returning to main menu...")
            break

        else:
            print("Pick something between 1 and 5.")

# Starts the program
if __name__ == "__main__":
    run_vault_terminal()
