import random
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

# Mock database
database = {
    "users": {},
    "events": {},
    "bets": []
}

# Helper functions
def register_user(username, balance):
    if username in database["users"]:
        return False, "User already exists."
    if not username or balance <= 0:
        return False, "Invalid username or balance."
    database["users"][username] = balance
    return True, "User registered successfully."

def create_event(event_name, odds):
    if not event_name or odds <= 0:
        return False, "Invalid event name or odds."
    event_id = len(database["events"]) + 1
    database["events"][event_id] = {"name": event_name, "odds": odds}
    return True, f"Event created with ID {event_id}."

def place_bet(username, event_id, amount):
    if username not in database["users"]:
        return False, "User does not exist."
    if event_id not in database["events"]:
        return False, "Event does not exist."
    if amount <= 0 or database["users"][username] < amount:
        return False, "Insufficient balance or invalid amount."

    database["users"][username] -= amount
    database["bets"].append({"user": username, "event": event_id, "amount": amount})
    return True, "Bet placed successfully."

# GUI Class
class BettingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Betting App")
        self.root.geometry("700x500")
        self.style = ttk.Style()

        # Apply a macOS-like theme
        self.style.theme_use("clam")
        self.root.configure(bg="#F8F9FA")

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.notebook, style="TFrame")
        self.tab2 = ttk.Frame(self.notebook, style="TFrame")
        self.tab3 = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab1, text="Users")
        self.notebook.add(self.tab2, text="Events")
        self.notebook.add(self.tab3, text="Bets")
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        # Styling
        self.style.configure("TNotebook.Tab", padding=(10, 10), font=("Helvetica", 12))
        self.style.configure("TFrame", background="#F8F9FA")
        self.style.configure("TButton", font=("Helvetica", 10), padding=5)
        self.style.configure("TLabel", font=("Helvetica", 11))

        # Tab 1: User Management
        self.user_label = ttk.Label(self.tab1, text="Username:", background="#F8F9FA")
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.user_entry = ttk.Entry(self.tab1)
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)

        self.balance_label = ttk.Label(self.tab1, text="Balance:", background="#F8F9FA")
        self.balance_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.balance_entry = ttk.Entry(self.tab1)
        self.balance_entry.grid(row=1, column=1, padx=10, pady=10)

        self.register_button = ttk.Button(self.tab1, text="Register User", command=self.handle_register_user)
        self.register_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.user_status = ttk.Label(self.tab1, text="", foreground="blue", background="#F8F9FA")
        self.user_status.grid(row=3, column=0, columnspan=2)

        # Tab 2: Event Management
        self.event_label = ttk.Label(self.tab2, text="Event Name:", background="#F8F9FA")
        self.event_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.event_entry = ttk.Entry(self.tab2)
        self.event_entry.grid(row=0, column=1, padx=10, pady=10)

        self.odds_label = ttk.Label(self.tab2, text="Odds:", background="#F8F9FA")
        self.odds_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.odds_entry = ttk.Entry(self.tab2)
        self.odds_entry.grid(row=1, column=1, padx=10, pady=10)

        self.create_event_button = ttk.Button(self.tab2, text="Create Event", command=self.handle_create_event)
        self.create_event_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.event_status = ttk.Label(self.tab2, text="", foreground="blue", background="#F8F9FA")
        self.event_status.grid(row=3, column=0, columnspan=2)

        # Tab 3: Bets
        self.bet_user_label = ttk.Label(self.tab3, text="Username:", background="#F8F9FA")
        self.bet_user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.bet_user_entry = ttk.Entry(self.tab3)
        self.bet_user_entry.grid(row=0, column=1, padx=10, pady=10)

        self.bet_event_label = ttk.Label(self.tab3, text="Event ID:", background="#F8F9FA")
        self.bet_event_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.bet_event_entry = ttk.Entry(self.tab3)
        self.bet_event_entry.grid(row=1, column=1, padx=10, pady=10)

        self.bet_amount_label = ttk.Label(self.tab3, text="Amount:", background="#F8F9FA")
        self.bet_amount_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.bet_amount_entry = ttk.Entry(self.tab3)
        self.bet_amount_entry.grid(row=2, column=1, padx=10, pady=10)

        self.place_bet_button = ttk.Button(self.tab3, text="Place Bet", command=self.handle_place_bet)
        self.place_bet_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.bet_status = ttk.Label(self.tab3, text="", foreground="blue", background="#F8F9FA")
        self.bet_status.grid(row=4, column=0, columnspan=2)

    # Handlers
    def handle_register_user(self):
        username = self.user_entry.get()
        try:
            balance = float(self.balance_entry.get())
        except ValueError:
            self.user_status.config(text="Invalid balance.")
            return

        success, message = register_user(username, balance)
        self.user_status.config(text=message, foreground="green" if success else "red")

    def handle_create_event(self):
        event_name = self.event_entry.get()
        try:
            odds = float(self.odds_entry.get())
        except ValueError:
            self.event_status.config(text="Invalid odds.")
            return

        success, message = create_event(event_name, odds)
        self.event_status.config(text=message, foreground="green" if success else "red")

    def handle_place_bet(self):
        username = self.bet_user_entry.get()
        try:
            event_id = int(self.bet_event_entry.get())
            amount = float(self.bet_amount_entry.get())
        except ValueError:
            self.bet_status.config(text="Invalid input.")
            return

        success, message = place_bet(username, event_id, amount)
        self.bet_status.config(text=message, foreground="green" if success else "red")

# Run the app
if __name__ == "__main__":
    root = ThemedTk(theme="breeze")
    app = BettingApp(root)
    root.mainloop()
