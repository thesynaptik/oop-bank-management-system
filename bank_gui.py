import io
import contextlib
import tkinter as tk
from tkinter import ttk, messagebox


class Customer:
    def __init__(self, customer_name, customer_id, customer_phone, customer_address):
        self.__customer_name = customer_name
        self.__customer_id = customer_id
        self.__customer_phone = customer_phone
        self.__customer_address = customer_address

    def get_name(self):
        return self.__customer_name

    def get_id(self):
        return self.__customer_id

    def get_phone(self):
        return self.__customer_phone

    def get_address(self):
        return self.__customer_address

    def update_phone_number(self, new_number):
        self.__customer_phone = new_number

    def update_address(self, new_address):
        self.__customer_address = new_address

    def show_info(self):
        print(f"name: {self.__customer_name}")
        print(f"ID: {self.__customer_id}")
        print(f"phone number{self.__customer_phone}")
        print(f"address: {self.__customer_address}")


class Account:
    def __init__(self, account_number, balance, customer):
        self.__account_number = account_number
        self.__balance = balance
        self.__customer = customer

    def get_balance(self):
        return self.__balance

    def get_customer_name(self):
        return self.__customer.get_name()

    def get_account_number(self):
        return self.__account_number

    def deposit(self, amount):
        try:
            if (amount > 0):
                self.__balance += amount
                print("Deposit successful")
            else:
                print("Invalid amount")
        except ValueError as e:
            print(e)

    def withdraw(self, amount):
        try:
            if (amount <= 0):
                print("Invalid amount")
            elif (amount <= self.__balance):
                self.__balance -= amount
                print("Withdraw successful")
            elif (amount > self.__balance):
                print("Insufficient balance")
            else:
                print("Invalid amount")
        except ValueError as e:
            print(e)

    def set_balance(self, new_balance):
        self.__balance = new_balance

    def show_info(self):
        print(f"Account number: {self.__account_number} ")
        print(f"Balance: {self.__balance}")
        print(f"Customer:{self.__customer.get_name()}")


class Saving_account(Account):
    def __init__(self, account_number, balance, customer, interest_rate):
        super().__init__(account_number, balance, customer)
        self.__interest_rate = interest_rate

    def apply_interest(self):
        interest = self.get_balance() * self.__interest_rate
        self.deposit(interest)

    def show_info(self):
        super().show_info()
        print(f"intrest rate: {self.__interest_rate}")


class Current_account(Account):
    def __init__(self, account_number, balance, customer, overdraft_limit):
        super().__init__(account_number, balance, customer)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if (amount <= 0):
            print("Invalid amount")
        elif (amount <= self.get_balance() + self.__overdraft_limit):
            self.set_balance(self.get_balance() - amount)
            print("Withdraw successful")
        else:
            print("Insufficient balance")

    def show_info(self):
        super().show_info()
        print(f"overdraft limit: {self.__overdraft_limit}")


class Bank:
    def __init__(self):
        self.__customers = []
        self.__accounts = []

    def add_customer(self, customer):
        if (self.find_customer(customer.get_id()) is None):
            self.__customers.append(customer)
            print("Customer added successfully")
        else:
            print("customer is alredy exist")

    def create_account(self, account):
        try:
            if (self.find_account(account.get_account_number()) is None):
                self.__accounts.append(account)
                print("Account created successfully")
            else:
                print('account is alredy exist')
        except ValueError as e:
            print(e)

    def find_customer(self, customer_id):
        for customer in self.__customers:
            if (customer_id == customer.get_id()):
                return customer

    def find_account(self, account_number):
        for account in self.__accounts:
            if (account.get_account_number() == account_number):
                return account

    def transfer_money(self, from_account_number, to_account_number, amount):
        try:
            from_account_number = self.find_account(from_account_number)
            to_account_number = self.find_account(to_account_number)
            if (from_account_number is None or to_account_number is None):
                print("Account not found")
            elif (amount <= 0):
                print("Invalid amount")
            elif (from_account_number.get_balance() >= amount):
                from_account_number.withdraw(amount)
                to_account_number.deposit(amount)
                print("transfer successful")
            else:
                print("Insufficient balance")
        except ValueError as e:
            print(e)

    def remove_account(self, account_number):
        try:
            account = self.find_account(account_number)
            if (account is not None):
                self.__accounts.remove(account)
                print("Account removed successfully")
            else:
                print("Account not found")
        except ValueError as e:
            print(e)

    def show_all_accounts(self):
        for account in self.__accounts:
            account.show_info()
            print("----------------------------")

    def show_all_customers(self):
        for customer in self.__customers:
            customer.show_info()
            print("----------------------------")

    @property
    def customers(self):
        return self.__customers

    @property
    def accounts(self):
        return self.__accounts


def run_captured(func, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = func(*args, **kwargs)
    return result, buf.getvalue()


FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_MONO = ("Consolas", 9)


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Management System - Tkinter GUI")
        self.geometry("980x640")
        self.configure(bg="#0E1B22")

        self.bank = Bank()
        self._seed_data()

        self._build_style()
        self._build_layout()
        self._refresh_all()

    def _seed_data(self):
        c1 = Customer("Ahmed", 11, "01022", "Cairo")
        c2 = Customer("Ali", 12, "01111", "Alex")
        c3 = Customer("Mona", 13, "01233", "Giza")
        for c in (c1, c2, c3):
            self.bank.add_customer(c)
        self.bank.create_account(Account("ACC1001", 5000, c1))
        self.bank.create_account(Saving_account("ACC1002", 3000, c2, 0.10))
        self.bank.create_account(Current_account("ACC1003", 1000, c3, 500))

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg = "#0E1B22"
        surface = "#16262E"
        gold = "#CBA135"
        text = "#EDEFEF"
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=surface, foreground=text,
                         padding=(16, 8), font=FONT_BOLD)
        style.map("TNotebook.Tab", background=[("selected", gold)],
                   foreground=[("selected", "#1a1306")])
        style.configure("TFrame", background=bg)
        style.configure("Card.TFrame", background=surface)
        style.configure("TLabel", background=bg, foreground=text, font=FONT_NORMAL)
        style.configure("Card.TLabel", background=surface, foreground=text, font=FONT_NORMAL)
        style.configure("Title.TLabel", background=bg, foreground=text, font=FONT_TITLE)
        style.configure("TButton", font=FONT_BOLD, padding=6)
        style.configure("Gold.TButton", background=gold, foreground="#1a1306")
        style.map("Gold.TButton", background=[("active", "#dab64a")])
        style.configure("Treeview", background=surface, fieldbackground=surface,
                         foreground=text, rowheight=26, font=FONT_NORMAL)
        style.configure("Treeview.Heading", font=FONT_BOLD)
        style.configure("TCombobox", fieldbackground=surface, background=surface)

    def _build_layout(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        self.tab_overview = ttk.Frame(self.notebook)
        self.tab_customers = ttk.Frame(self.notebook)
        self.tab_accounts = ttk.Frame(self.notebook)
        self.tab_transfer = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_overview, text="Overview")
        self.notebook.add(self.tab_customers, text="Customers")
        self.notebook.add(self.tab_accounts, text="Accounts")
        self.notebook.add(self.tab_transfer, text="Transfer Money")

        self._build_overview_tab()
        self._build_customers_tab()
        self._build_accounts_tab()
        self._build_transfer_tab()

        console_frame = ttk.Frame(self)
        console_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Label(console_frame, text="Operation Output (original print messages):",
                   style="Title.TLabel").pack(anchor="w")
        self.console = tk.Text(console_frame, height=7, bg="#16262E", fg="#4CAF93",
                                insertbackground="#4CAF93", font=FONT_MONO, wrap="word")
        self.console.pack(fill="x", pady=(4, 0))
        self.console.configure(state="disabled")

    def log(self, text):
        if not text:
            return
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def _build_overview_tab(self):
        f = self.tab_overview
        stats_frame = ttk.Frame(f)
        stats_frame.pack(fill="x", padx=14, pady=14)
        self.stat_labels = {}
        for key, label in [("customers", "Customers"), ("accounts", "Accounts"),
                            ("balance", "Total Balance")]:
            box = ttk.Frame(stats_frame, style="Card.TFrame", padding=14)
            box.pack(side="left", padx=6, fill="x", expand=True)
            ttk.Label(box, text=label, style="Card.TLabel").pack(anchor="w")
            val = ttk.Label(box, text="0", style="Card.TLabel", font=FONT_TITLE)
            val.pack(anchor="w")
            self.stat_labels[key] = val

        ttk.Label(f, text="All Accounts", style="Title.TLabel").pack(anchor="w", padx=14, pady=(6, 4))
        cols = ("number", "customer", "type", "balance")
        self.tree_overview = ttk.Treeview(f, columns=cols, show="headings", height=10)
        for c, t in zip(cols, ["Account Number", "Customer", "Type", "Balance"]):
            self.tree_overview.heading(c, text=t)
            self.tree_overview.column(c, anchor="center")
        self.tree_overview.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def _build_customers_tab(self):
        f = self.tab_customers
        form = ttk.Frame(f, style="Card.TFrame", padding=14)
        form.pack(fill="x", padx=14, pady=14)

        self.c_name = self._labeled_entry(form, "Name", 0)
        self.c_id = self._labeled_entry(form, "ID", 1)
        self.c_phone = self._labeled_entry(form, "Phone", 2)
        self.c_address = self._labeled_entry(form, "Address", 3)

        ttk.Button(form, text="Add Customer", style="Gold.TButton",
                   command=self.on_add_customer).grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        ttk.Label(f, text="All Customers", style="Title.TLabel").pack(anchor="w", padx=14, pady=(6, 4))
        cols = ("id", "name", "phone", "address")
        self.tree_customers = ttk.Treeview(f, columns=cols, show="headings", height=10)
        for c, t in zip(cols, ["ID", "Name", "Phone", "Address"]):
            self.tree_customers.heading(c, text=t)
            self.tree_customers.column(c, anchor="center")
        self.tree_customers.pack(fill="both", expand=True, padx=14, pady=(0, 4))

        ttk.Button(f, text="Show Selected Customer Info (show_info)",
                   command=self.on_show_customer_info).pack(padx=14, pady=(0, 14), anchor="w")

    def on_show_customer_info(self):
        sel = self.tree_customers.selection()
        if not sel:
            messagebox.showinfo("Notice", "Select a customer from the table first")
            return
        cust_id = self.tree_customers.item(sel[0])["values"][0]
        customer = self.bank.find_customer(self._coerce_id(cust_id))
        if customer:
            _, out = run_captured(customer.show_info)
            self.log(out)

    def _coerce_id(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    def _build_accounts_tab(self):
        f = self.tab_accounts
        form = ttk.Frame(f, style="Card.TFrame", padding=14)
        form.pack(fill="x", padx=14, pady=14)

        ttk.Label(form, text="Customer", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.a_customer = ttk.Combobox(form, state="readonly", width=22)
        self.a_customer.grid(row=0, column=1, sticky="ew", padx=6, pady=4)

        ttk.Label(form, text="Account Type", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.a_type = ttk.Combobox(form, state="readonly", width=22,
                                    values=["Normal Account", "Saving Account", "Current Account"])
        self.a_type.current(0)
        self.a_type.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
        self.a_type.bind("<<ComboboxSelected>>", self._on_type_change)

        self.a_number = self._labeled_entry(form, "Account Number", 2)
        self.a_balance = self._labeled_entry(form, "Opening Balance", 3)
        self.a_extra_label = ttk.Label(form, text="", style="Card.TLabel")
        self.a_extra_label.grid(row=4, column=0, sticky="w", padx=6, pady=4)
        self.a_extra = ttk.Entry(form, width=24)
        self.a_extra.grid(row=4, column=1, sticky="ew", padx=6, pady=4)
        self._on_type_change()

        ttk.Button(form, text="Create Account", style="Gold.TButton",
                   command=self.on_create_account).grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        ttk.Label(f, text="All Accounts", style="Title.TLabel").pack(anchor="w", padx=14, pady=(6, 4))
        cols = ("number", "customer", "type", "balance")
        self.tree_accounts = ttk.Treeview(f, columns=cols, show="headings", height=8)
        for c, t in zip(cols, ["Account Number", "Customer", "Type", "Balance"]):
            self.tree_accounts.heading(c, text=t)
            self.tree_accounts.column(c, anchor="center")
        self.tree_accounts.pack(fill="both", expand=True, padx=14, pady=(0, 6))

        actions = ttk.Frame(f)
        actions.pack(fill="x", padx=14, pady=(0, 14))
        ttk.Label(actions, text="Amount:", style="TLabel").pack(side="left", padx=4)
        self.amount_entry = ttk.Entry(actions, width=12)
        self.amount_entry.pack(side="left", padx=4)
        ttk.Button(actions, text="Deposit", command=self.on_deposit).pack(side="left", padx=4)
        ttk.Button(actions, text="Withdraw", command=self.on_withdraw).pack(side="left", padx=4)
        ttk.Button(actions, text="Apply Interest", command=self.on_apply_interest).pack(side="left", padx=4)
        ttk.Button(actions, text="Show Info", command=self.on_show_account_info).pack(side="left", padx=4)
        ttk.Button(actions, text="Remove Account", command=self.on_remove_account).pack(side="right", padx=4)

    def _on_type_change(self, event=None):
        t = self.a_type.get()
        if t == "Saving Account":
            self.a_extra_label.config(text="Interest Rate (e.g. 0.1)")
            self.a_extra.grid()
        elif t == "Current Account":
            self.a_extra_label.config(text="Overdraft Limit")
            self.a_extra.grid()
        else:
            self.a_extra_label.config(text="")
            self.a_extra.delete(0, "end")

    def _labeled_entry(self, parent, label, row):
        ttk.Label(parent, text=label, style="Card.TLabel").grid(row=row, column=0, sticky="w", padx=6, pady=4)
        entry = ttk.Entry(parent, width=24)
        entry.grid(row=row, column=1, sticky="ew", padx=6, pady=4)
        return entry

    def _selected_account_number(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Notice", "Select an account from the table first")
            return None
        return tree.item(sel[0])["values"][0]

    def on_create_account(self):
        cust_label = self.a_customer.get()
        if not cust_label:
            messagebox.showwarning("Error", "Select a customer")
            return
        cust_id = self._customer_map.get(cust_label)
        customer = self.bank.find_customer(cust_id)
        number = self.a_number.get().strip()
        try:
            balance = float(self.a_balance.get())
        except ValueError:
            messagebox.showwarning("Error", "Balance must be a number")
            return
        if not number or customer is None:
            messagebox.showwarning("Error", "Fill in all fields")
            return

        t = self.a_type.get()
        if t == "Saving Account":
            try:
                rate = float(self.a_extra.get())
            except ValueError:
                messagebox.showwarning("Error", "Interest rate must be a number")
                return
            account = Saving_account(number, balance, customer, rate)
        elif t == "Current Account":
            try:
                limit = float(self.a_extra.get())
            except ValueError:
                messagebox.showwarning("Error", "Overdraft limit must be a number")
                return
            account = Current_account(number, balance, customer, limit)
        else:
            account = Account(number, balance, customer)

        _, out = run_captured(self.bank.create_account, account)
        self.log(out)
        self._refresh_all()

    def on_deposit(self):
        num = self._selected_account_number(self.tree_accounts)
        if num is None:
            return
        amount = self._read_amount()
        if amount is None:
            return
        account = self.bank.find_account(num)
        _, out = run_captured(account.deposit, amount)
        self.log(out)
        self._refresh_all()

    def on_withdraw(self):
        num = self._selected_account_number(self.tree_accounts)
        if num is None:
            return
        amount = self._read_amount()
        if amount is None:
            return
        account = self.bank.find_account(num)
        _, out = run_captured(account.withdraw, amount)
        self.log(out)
        self._refresh_all()

    def on_apply_interest(self):
        num = self._selected_account_number(self.tree_accounts)
        if num is None:
            return
        account = self.bank.find_account(num)
        if not isinstance(account, Saving_account):
            messagebox.showinfo("Notice", "Interest only applies to saving accounts")
            return
        _, out = run_captured(account.apply_interest)
        self.log(out)
        self._refresh_all()

    def on_show_account_info(self):
        num = self._selected_account_number(self.tree_accounts)
        if num is None:
            return
        account = self.bank.find_account(num)
        _, out = run_captured(account.show_info)
        self.log(out)

    def on_remove_account(self):
        num = self._selected_account_number(self.tree_accounts)
        if num is None:
            return
        _, out = run_captured(self.bank.remove_account, num)
        self.log(out)
        self._refresh_all()

    def _read_amount(self):
        try:
            return float(self.amount_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Enter a valid amount")
            return None

    def _build_transfer_tab(self):
        f = self.tab_transfer
        form = ttk.Frame(f, style="Card.TFrame", padding=14)
        form.pack(fill="x", padx=14, pady=14)

        ttk.Label(form, text="From Account", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.t_from = ttk.Combobox(form, state="readonly", width=20)
        self.t_from.grid(row=0, column=1, sticky="ew", padx=6, pady=4)

        ttk.Label(form, text="To Account", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.t_to = ttk.Combobox(form, state="readonly", width=20)
        self.t_to.grid(row=1, column=1, sticky="ew", padx=6, pady=4)

        ttk.Label(form, text="Amount", style="Card.TLabel").grid(row=2, column=0, sticky="w", padx=6, pady=4)
        self.t_amount = ttk.Entry(form, width=20)
        self.t_amount.grid(row=2, column=1, sticky="ew", padx=6, pady=4)

        ttk.Button(form, text="Transfer", style="Gold.TButton",
                   command=self.on_transfer).grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        ttk.Label(f, text="Current Accounts", style="Title.TLabel").pack(anchor="w", padx=14, pady=(6, 4))
        cols = ("number", "customer", "type", "balance")
        self.tree_transfer = ttk.Treeview(f, columns=cols, show="headings", height=10)
        for c, t in zip(cols, ["Account Number", "Customer", "Type", "Balance"]):
            self.tree_transfer.heading(c, text=t)
            self.tree_transfer.column(c, anchor="center")
        self.tree_transfer.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def on_transfer(self):
        from_num = self._account_map.get(self.t_from.get())
        to_num = self._account_map.get(self.t_to.get())
        if not from_num or not to_num:
            messagebox.showwarning("Error", "Select both accounts")
            return
        try:
            amount = float(self.t_amount.get())
        except ValueError:
            messagebox.showwarning("Error", "Enter a valid amount")
            return
        _, out = run_captured(self.bank.transfer_money, from_num, to_num, amount)
        self.log(out)
        self._refresh_all()

    def _account_type_label(self, account):
        if isinstance(account, Saving_account):
            return "Saving Account"
        if isinstance(account, Current_account):
            return "Current Account"
        return "Normal Account"

    def _refresh_all(self):
        self._customer_map = {f"{c.get_name()} (ID {c.get_id()})": c.get_id() for c in self.bank.customers}
        self._account_map = {f"{a.get_account_number()} - {a.get_customer_name()}": a.get_account_number()
                              for a in self.bank.accounts}

        self.a_customer["values"] = list(self._customer_map.keys())
        self.t_from["values"] = list(self._account_map.keys())
        self.t_to["values"] = list(self._account_map.keys())

        for row in self.tree_customers.get_children():
            self.tree_customers.delete(row)
        for c in self.bank.customers:
            self.tree_customers.insert("", "end", values=(c.get_id(), c.get_name(), c.get_phone(), c.get_address()))

        total_balance = 0
        for tree in (self.tree_overview, self.tree_accounts, self.tree_transfer):
            for row in tree.get_children():
                tree.delete(row)
        for a in self.bank.accounts:
            total_balance += a.get_balance()
            values = (a.get_account_number(), a.get_customer_name(), self._account_type_label(a), a.get_balance())
            self.tree_overview.insert("", "end", values=values)
            self.tree_accounts.insert("", "end", values=values)
            self.tree_transfer.insert("", "end", values=values)

        self.stat_labels["customers"].config(text=str(len(self.bank.customers)))
        self.stat_labels["accounts"].config(text=str(len(self.bank.accounts)))
        self.stat_labels["balance"].config(text=str(total_balance))

    def on_add_customer(self):
        name = self.c_name.get().strip()
        cust_id = self.c_id.get().strip()
        phone = self.c_phone.get().strip()
        address = self.c_address.get().strip()
        if not name or not cust_id:
            messagebox.showwarning("Error", "Fill in at least the name and ID")
            return
        customer = Customer(name, self._coerce_id(cust_id), phone, address)
        _, out = run_captured(self.bank.add_customer, customer)
        self.log(out)
        self._refresh_all()


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
