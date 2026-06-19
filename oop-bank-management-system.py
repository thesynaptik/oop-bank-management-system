class Customer:
    def __init__(self,customer_name,customer_id,customer_phone,customer_address):
        self.__customer_name=customer_name
        self.__customer_id=customer_id
        self.__customer_phone=customer_phone
        self.__customer_address=customer_address

    #getters

    def get_name(self):
        return self.__customer_name

    def get_id(self):
        return self.__customer_id

    def get_phone(self):
        return self.__customer_phone

    def get_address(self):
        return self.__customer_address

    #setters

    def update_phone_number(self,new_number):
        self.__customer_phone=new_number

    def update_address(self,new_address):
        self.__customer_address=new_address

    #method
    def show_info(self):
        print(f"name: {self.__customer_name}")
        print(f"ID: {self.__customer_id}")
        print(f"phone number{self.__customer_phone}")
        print(f"address: {self.__customer_address}")

    
class Account:
    def __init__(self,account_number,balance,customer):
        self.__account_number=account_number
        self.__balance=balance
        self.__customer=customer

    #getters
    def get_balance(self):
        return self.__balance

    def get_customer_name(self):
        return self.__customer.get_name()

    def get_account_number(self):
        return self.__account_number

    #setters
    def deposit(self,amount):
        try:
            
            if(amount>0):
                self.__balance+=amount
                print("Deposit successful")
            else:
                print("Invalid amount")
        except ValueError as e:
            print(e)

    def withdraw(self,amount):
        try:
            if(amount<=0):
                print("Invalid amount")
            elif(amount<=self.__balance):
                self.__balance-=amount
                print("Withdraw successful")
            elif(amount>self.__balance):
                print("Insufficient balance")
            else:
                print("Invalid amount")
        except ValueError as e:
            print(e)

    def set_balance(self,new_balance):
        self.__balance=new_balance

    def show_info(self):
        print(f"Account number: {self.__account_number} ")
        print(f"Balance: {self.__balance}")
        print(f"Customer:{self.__customer.get_name()}")
            

class Saving_account(Account):
    def __init__(self,account_number,balance,customer,interest_rate):
        super().__init__(account_number,balance,customer)
        self.__interest_rate=interest_rate

    def apply_interest(self):
        interest=self.get_balance()*self.__interest_rate
        self.deposit(interest)

    def show_info(self):
        super().show_info()
        print(f"intrest rate: {self.__interest_rate}")
        
        
class Current_account(Account):
    def __init__(self,account_number,balance,customer,overdraft_limit):
        super().__init__(account_number,balance,customer)
        self.__overdraft_limit=overdraft_limit

    def withdraw(self,amount):
        if(amount<=0):
            print("Invalid amount")
        elif(amount<=self.get_balance()+self.__overdraft_limit):
            self.set_balance(self.get_balance()-amount)
            print("Withdraw successful")
        else:
            print("Insufficient balance")

    def show_info(self):
        super().show_info()
        print(f"overdraft limit: {self.__overdraft_limit}")



class Bank:
    def __init__(self):
        self.__customers=[]
        self.__accounts=[]

    
    def add_customer(self,customer):
        if(self.find_customer(customer.get_id()) is None):
            self.__customers.append(customer)
            print("Customer added successfully")
        else:
            print("customer is alredy exist")
    def create_account(self,account):
        try:
            if(self.find_account(account.get_account_number()) is None):
                self.__accounts.append(account)
                print("Account created successfully")
            else:
                print('account is alredy exist')
        except ValueError as e:
            print(e)
    def find_customer(self,customer_id):
            
        for customer in self.__customers:
            if(customer_id==customer.get_id()):
                return customer


    def find_account(self,account_number):
        for account in self.__accounts:
            if(account.get_account_number()==account_number):
                return account
    def transfer_money(self,from_account_number,to_account_number,amount):
        try:
            from_account_number=self.find_account(from_account_number)
            to_account_number=self.find_account(to_account_number)
            if(from_account_number is None or to_account_number is None ):
                print("Account not found")
            elif(amount<=0):
                print("Invalid amount")
            elif(from_account_number.get_balance()>=amount):
                from_account_number.withdraw(amount)
                to_account_number.deposit(amount)
                print("transfer successful")
            else:
                print("Insufficient balance")
        except ValueError as e:
            print(e)
    def remove_account(self,account_number):
        try:
            account=self.find_account(account_number)
            if(account  is not None):
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
    

print("\n===== TEST PROJECT =====")

bank = Bank()

c1 = Customer("Ahmed", 11, "01022", "Cairo")
c2 = Customer("Ali", 12, "01111", "Alex")
c3 = Customer("Mona", 13, "01233", "Giza")

bank.add_customer(c1)
bank.add_customer(c2)
bank.add_customer(c3)

bank.add_customer(c1)

acc1 = Account("ACC1001", 5000, c1)
acc2 = Saving_account("ACC1002", 3000, c2, 0.10)
acc3 = Current_account("ACC1003", 1000, c3, 500)

bank.create_account(acc1)
bank.create_account(acc2)
bank.create_account(acc3)

bank.create_account(acc1)

print("\n===== DEPOSIT / WITHDRAW =====")
acc1.deposit(1000)
acc1.withdraw(2000)
acc1.withdraw(10000)
acc1.withdraw(-50)

print("\n===== SAVING ACCOUNT INTEREST =====")
acc2.show_info()
acc2.apply_interest()
acc2.show_info()

print("\n===== CURRENT ACCOUNT OVERDRAFT =====")
acc3.show_info()
acc3.withdraw(1200)   
acc3.show_info()
acc3.withdraw(1000)   
acc3.show_info()

print("\n===== TRANSFER MONEY =====")
bank.transfer_money("ACC1001", "ACC1002", 1000)
bank.transfer_money("ACC1001", "ACC9999", 500)
bank.transfer_money("ACC1001", "ACC1002", -100)
bank.transfer_money("ACC1001", "ACC1002", 999999)

print("\n===== SHOW ALL CUSTOMERS =====")
bank.show_all_customers()

print("\n===== SHOW ALL ACCOUNTS =====")
bank.show_all_accounts()

print("\n===== REMOVE ACCOUNT =====")
bank.remove_account("ACC1002")
bank.remove_account("ACC9999")

print("\n===== SHOW ACCOUNTS AFTER REMOVE =====")
bank.show_all_accounts()





