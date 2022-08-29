class AbortTransaction(Exception):  # create custom exception
    pass

class Account():
    def __init__(self, userName, userPassword, balance) -> None:
        self.userName = userName
        self.userPassword = userPassword
        self.balance = balance

    def checkPass(self, userPassword) -> None:
        if userPassword != self.userPassword:
            raise AbortTransaction('Wrong passowrd')

    def validateAmount(self, Amount) -> None:
        try:
            int(Amount)
        except ValueError:
            raise AbortTransaction('Amount must be an integer.')
        if Amount <= 0:
            raise AbortTransaction('Amount must be positive')

    def deposite(self, userPassword, deposAmount) -> int:
        self.checkPass(userPassword)
        self.validateAmount(deposAmount)
        self.balance += deposAmount
        return self.balance

    def withdraw(self, userPassword, withdrawalAmount) -> int:
        self.checkPass(userPassword)
        self.validateAmount(withdrawalAmount)
        if withdrawalAmount > self.balance:
            raise AbortTransaction("No enough balance.")
        self.balance -= withdrawalAmount
        return self.balance

    def getBalance(self, userPassword) -> int:
        self.checkPass(userPassword)
        return self.balance