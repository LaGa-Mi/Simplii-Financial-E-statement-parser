import os

from model.Transaction import Transaction
from parsers.eStatementParser import extract

def getTransactions(statementsFolderPath: str) -> list[Transaction]:
    transactions: list[Transaction] = []

    for root, dirs, files in os.walk(statementsFolderPath):
        for file in files:
            if (file.endswith(".pdf")):
                transactions.extend(extract(os.path.join(root, file)))
    
    cleanTransactions(transactions)
    sortTransactionsByDate(transactions)

    return transactions

def cleanTransactions(transactions: list[Transaction]):
    for i in range(1, len(transactions) - 1):
        transactions[i].setTransactionTypeFromPreviousTransaction(transactions[i - 1])
        transactions[i].correctDifference()

def sortTransactionsByDate(transactions: list[Transaction]):
    transactions.sort(key=lambda x: x.transactionDate)