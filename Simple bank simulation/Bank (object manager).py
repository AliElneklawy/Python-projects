from Account import Account, AbortTransaction

class Bank():
    def __init__(self, hours: str, address: str, telephoneNum: str) -> None:
        self.hours = hours
        self.address = address
        self.telephoneNum = telephoneNum
        self.accountsDict = {}
        self.nextAccNum = 0

    def createAcc(self, userName: str, userPassword: int, startAmount: int) -> int:
        oAccount = Account(userName, userPassword, startAmount)
        self.accountsDict[self.nextAccNum] = oAccount
        self.nextAccNum += 1
        return self.nextAccNum - 1

    def openAcc(self) -> None:
        userName = input("What is your name? ")
        userPassword = int(input("Enter your PIN: "))
        startAmount = int(input("Enter the starting balance: "))
        userAccNum = self.createAcc(userName, userPassword, startAmount)
        print("Your accont number is: ", userAccNum)

    def checkAccExist(self) -> int:
        userAccNum = int(input("Enter your account number: "))
        if userAccNum not in self.accountsDict:
            raise AbortTransaction("Account number doesn't exist.")
        return userAccNum

    def deposite(self):
        userAccNum = self.checkAccExist()
        userPassword = int(input("Enter your PIN: "))
        deposAmount = int(input("Enter the amount of deposition: "))
        oAccount = self.accountsDict[userAccNum]
        Balance = oAccount.deposite(userPassword, deposAmount)
        print("Your new balance is: ", Balance)

    def withdraw(self):
        userAccNum = self.checkAccExist()
        userPassword = int(input("Enter your PIN: "))
        withdrawAmount = int(input("Enter the amount of withdrawal: "))
        oAccount = self.accountsDict[userAccNum]
        Balance = oAccount.withdraw(userPassword, withdrawAmount)
        print("Your new balance is: ", Balance)

    def getBalance(self) -> int:
        userAccNum = self.checkAccExist()
        userPassword = int(input("Enter your PIN: "))
        oAccount = self.accountsDict[userAccNum]
        Balance = oAccount.getBalance(userPassword)
        print("Current balance: ", Balance)
    
    def getInfo(self):
        print(f""" 
                Work hours: {self.hours}
                Address: {self.address}
                Phone number: {self.telephoneNum}
         """)
