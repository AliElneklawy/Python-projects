from Bank import *
from pyinputplus import inputMenu

oBank = Bank("9AM to 4PM", "123 Main St., Egypt", "(065) 620-80-32")

while True:
    choice = inputMenu(["Get balance",
                        "Make a deposit",
                        "Open a new account",
                        "Withdraw",
                        "Get info",], numbered=True)
    try:
        if choice == "Get balance":
            oBank.getBalance()
        elif choice == "Make a deposit":
            oBank.deposite()
        elif choice == "Withdraw":
            oBank.withdraw()
        elif choice == "Open a new account":
            oBank.openAcc()
        elif choice == "Get info":
            oBank.getInfo()

    except AbortTransaction as error:
        print(error)