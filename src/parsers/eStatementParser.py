import pdfplumber
import re
from datetime import datetime

from model.Transaction import Transaction
from model.enums.TransactionTypes import TransactionTypes
from model.enums.Months import MonthNames, MonthIndices

def extract(path: str) -> list[Transaction]:
    data: list[Transaction] = []
    transactionCount: int = 0
    year: int = 0

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            table_started = False

            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                if not table_started:
                    if "date date" in line:
                        table_started = True
                        continue
                    elif "statement period:" in line:
                        year = int(re.search(r"\b\d{4}\b", line).group())
                    else:
                        continue
                if "transactions continue in the next page" in line:
                    break
                if "end of transactions" in line:
                    return data
                
                if table_started:
                    isBalanceForward = "BALANCE FORWARD" in line
                    if (isValidTransactionLine(line, isBalanceForward)):
                        transaction = parseLineToTransaction(line, year, isBalanceForward)
                        if (transaction is not None):
                            data.append(transaction)
                            transactionCount += 1
                        else:
                            raise ValueError("Could not parse transaction")
                    else:
                        data[transactionCount - 1].transactionName += " " + line

    return data

def parseLineToTransaction(line, year, isBalanceForward):
    i = 0
    columnIndex = 0
    incValue = 0
    try:
        while i < len(line):
            if line[i] == " ":
                i = i + 1
                continue
            match columnIndex:
                case 0: # First column is a date in the format "<3 character month name> ##"
                    transactionDate, incValue = getDate(line[i:i+6], year)
                case 1: # Second column is a date in the format "<3 character month name> ##"
                    effectiveDate, incValue = getDate(line[i:i+6], year)
                case 2: # Third column has a transaction name
                    transactionName, incValue = getTransactionName(line[i:])
                case 3: # Fourth column name has a monetary value
                    if (isBalanceForward):
                        difference = 0
                        incValue = 0
                        transactionType = TransactionTypes.BALANCE_FORWARD
                    else:
                        difference, incValue = getMonetaryValue(line[i:])
                        transactionType = TransactionTypes.UNKNOWN
                case 4: # Fifth column name has a monetary value, but does not need to be parsed
                    finalAmount, incValue = getMonetaryValue(line[i:])
                case _:
                    break
            i += incValue
            columnIndex += 1
    except:
        return None

    return Transaction(transactionDate, effectiveDate, transactionName, difference, finalAmount, transactionType)

def getDate(string, year):
    if not len(string) != 6:
        date = string[0:6].lower()

        if date[0:3] in (MonthNames.set()):
            if (date[4].isdigit() and date[5].isdigit()):
                return (datetime(year, MonthIndices[date[0:3]].value, int(date[4:6])), 6)
    
    raise ValueError("Could not get date")

def getTransactionName(string):
    i = 0
    while(not isMonetary(string[i:])):
        i += 1
    i -= 1
    
    return (string[:i], i) # Remove trailing space

def isMonetary(string):
    return not (re.match(r"^\d{1,3}(,\d{3})*(\.\d{2}).*$", string) is None)

def getMonetaryValue(string):
    i = 0

    while(i < len(string) and (string[i].isdigit() or string[i] == '.' or string[i] == ',')):
        i += 1

    if (i < len(string) and string[i] == '-'):
        return (-1 * float(string[:i].replace(",", "")), i) # Remove trailing space and replace commas with nothing

    return (float(string[:i].replace(",", "")), i) # Remove trailing space and replace commas with nothing

def isValidTransactionLine(transactionLine, isBalanceForward):
    if (isBalanceForward):
        pattern = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} .+\d{1,3}(,\d{3})*(\.\d{2}).*$"
    else:
        pattern = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} .+\d{1,3}(,\d{3})*(\.\d{2}) \d{1,3}(,\d{3})*(\.\d{2}).*$"
    return re.match(pattern, transactionLine) is not None