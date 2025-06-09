# Simple Accounting System

This project provides a lightweight CLI tool to keep track of business and personal spending. It stores data in a local SQLite database and supports importing transaction history from an XLSX file.

## Features

- Import transactions from an XLSX file (`Date`, `Description`, and `Amount` columns required)
- Categorise transactions based on editable description rules
- Manually add transactions
- View a pivot report of monthly spend by category

## Usage

```bash
# Initialise the database and load default categories and rules
python accounting/main.py initdb

# Upload a transaction history spreadsheet
python accounting/main.py upload path/to/transactions.xlsx

# Add a manual transaction
python accounting/main.py add-transaction 2025-06-01 "Coffee Shop" 35.50

# See uncategorised descriptions to help create new rules
python accounting/main.py list-uncategorised

# Add a rule (pattern is matched against the transaction description)
python accounting/main.py add-rule "COFFEE" 57

# Generate a spend report by category and month
python accounting/main.py report
```

The default categories and rules are stored in the `accounting/categories.csv` and `accounting/rules.csv` files. The database is located at `accounting/data.db`.
