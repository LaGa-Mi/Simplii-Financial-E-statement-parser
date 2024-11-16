import os
import sys

from model.Transaction import Transaction
from importing.importTransactions import getTransactions
from exporting.exportTransactions import exportTransactions

def checkArguments(argc: int, argv: list) -> tuple[str, str]:
    if argc != 3:
        print("Usage: python main.py <folderpath> <output_filepath>")
        sys.exit(1)

    statementsFolderPath = argv[1]
    outputFilePath = argv[2]

    if not os.path.isdir(statementsFolderPath):
        print(f"Error: The folder '{statementsFolderPath}' does not exist.")
        sys.exit(1)

    output_folder = os.path.dirname(outputFilePath)
    if not os.path.isdir(output_folder):
        print(f"Error: The folder for the output file '{output_folder}' does not exist.")
        sys.exit(1)

    return statementsFolderPath, outputFilePath

def main():
    statementsFolderPath, outputFilePath = checkArguments(len(sys.argv), sys.argv)

    transactions: list[Transaction] = getTransactions(statementsFolderPath)

    exportTransactions(transactions, outputFilePath)

    return 0

if __name__ == "__main__":
    main()