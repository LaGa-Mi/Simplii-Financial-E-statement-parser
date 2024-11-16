import csv
from model.Transaction import Transaction
import os

def exportTransactions(transactions: list[Transaction], CSVPath: str) -> None:
    os.makedirs(os.path.dirname(CSVPath), exist_ok=True)

    # Define the headers based on the transaction object structure
    headers = Transaction.getHeaders()

    with open(CSVPath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()

        # Write the transaction data
        for transaction in transactions:
            writer.writerow(transaction.getHeaderToFieldMapper())