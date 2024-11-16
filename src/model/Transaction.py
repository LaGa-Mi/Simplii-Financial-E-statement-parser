from typing import Self

from model.enums.TransactionTypes import TransactionTypes

class Transaction:
    headers = ["Transaction Date", "Effective Date", "Transaction Name", "Difference", "Final Amount", "Transaction Type"]

    def __init__(self, transactionDate, effectiveDate, transactionName, difference, finalAmount, transactionType):
        self.transactionDate = transactionDate
        self.effectiveDate = effectiveDate
        self.transactionName = transactionName
        self.difference = difference
        self.finalAmount = finalAmount
        self.transactionType = transactionType

    def setTransactionTypeFromPreviousTransaction(self, previousTransaction: Self):
        if self.finalAmount == previousTransaction.finalAmount:
            raise Exception("Final amount is the same as previous transaction")
        elif self.finalAmount > previousTransaction.finalAmount:
            self.transactionType = TransactionTypes.FUNDS_IN
        else:
            self.transactionType = TransactionTypes.FUNDS_OUT

    def correctDifference(self):
        if self.transactionType == TransactionTypes.FUNDS_OUT and self.difference > 0:
            self.difference *= -1

    def getHeaders() -> list[str]:
        return Transaction.headers
    
    def getHeaderToFieldMapper(self) -> dict[str, str]:
        return {"Transaction Date": self.transactionDate, "Effective Date": self.effectiveDate, "Transaction Name": self.transactionName, "Difference": self.difference, "Final Amount": self.finalAmount, "Transaction Type": self.transactionType.name}

    def __repr__(self) -> str:
        return f"{self.transactionDate.strftime("%b %d %Y")} - {self.effectiveDate.strftime("%b %d %Y")} - {self.transactionName} - {self.difference} - {self.finalAmount} - {self.transactionType.name}"