import argparse
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

DB_PATH = Path('accounting/data.db')
CATEGORIES_CSV = Path(__file__).with_name('categories.csv')
RULES_CSV = Path(__file__).with_name('rules.csv')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Create tables
    cur.execute(
        """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            vat_able BOOLEAN NOT NULL,
            type TEXT NOT NULL
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description_pattern TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )"""
    )
    conn.commit()

    # Load default categories if table empty
    cur.execute('SELECT COUNT(*) FROM categories')
    if cur.fetchone()[0] == 0:
        with open(CATEGORIES_CSV, newline='') as f:
            reader = csv.DictReader(f)
            cur.executemany(
                'INSERT INTO categories (id, name, vat_able, type) VALUES (:id, :name, :vat_able, :type)',
                list(reader)
            )
            conn.commit()

    # Load default rules if table empty
    cur.execute('SELECT COUNT(*) FROM rules')
    if cur.fetchone()[0] == 0:
        with open(RULES_CSV, newline='') as f:
            reader = csv.DictReader(f)
            rows = [
                {
                    'description_pattern': r['description_pattern'],
                    'category_id': r['category_id'],
                    'created_at': r['created_at']
                }
                for r in reader
            ]
            cur.executemany(
                'INSERT INTO rules (description_pattern, category_id, created_at) VALUES (:description_pattern, :category_id, :created_at)',
                rows
            )
            conn.commit()
    conn.close()


def load_rules(cur):
    cur.execute('SELECT id, description_pattern, category_id FROM rules')
    return [dict(row) for row in cur.fetchall()]


def categorise_description(desc, rules):
    desc_upper = desc.upper()
    for rule in rules:
        if rule['description_pattern'] in desc_upper:
            return rule['category_id']
    return None


def upload_xlsx(path):
    conn = get_connection()
    df = pd.read_excel(path)
    expected = {'Date', 'Description', 'Amount'}
    if not expected.issubset(df.columns):
        raise ValueError(f"Input XLSX must contain columns: {expected}")
    cur = conn.cursor()
    rules = load_rules(cur)
    for _, row in df.iterrows():
        category_id = categorise_description(str(row['Description']), rules)
        cur.execute(
            'INSERT INTO transactions (date, description, amount, category_id) VALUES (?, ?, ?, ?)',
            (pd.to_datetime(row['Date']).date().isoformat(), row['Description'], row['Amount'], category_id)
        )
    conn.commit()
    conn.close()


def add_transaction(args):
    conn = get_connection()
    cur = conn.cursor()
    date = pd.to_datetime(args.date).date().isoformat()
    rules = load_rules(cur)
    category_id = categorise_description(args.description.upper(), rules)
    if args.category:
        category_id = args.category
    cur.execute(
        'INSERT INTO transactions (date, description, amount, category_id) VALUES (?, ?, ?, ?)',
        (date, args.description, args.amount, category_id)
    )
    conn.commit()
    conn.close()


def list_uncategorised():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT description, COUNT(*) as cnt FROM transactions WHERE category_id IS NULL GROUP BY description ORDER BY cnt DESC'
    )
    rows = cur.fetchall()
    for r in rows:
        print(r['cnt'], r['description'])
    conn.close()


def add_rule(args):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO rules (description_pattern, category_id, created_at) VALUES (?, ?, ?)',
        (args.pattern.upper(), args.category, datetime.utcnow().isoformat())
    )
    # Apply to existing transactions
    cur.execute('SELECT id, description FROM transactions WHERE category_id IS NULL')
    rules = load_rules(cur)
    for row in cur.fetchall():
        cat = categorise_description(row['description'], rules)
        if cat:
            cur.execute('UPDATE transactions SET category_id=? WHERE id=?', (cat, row['id']))
    conn.commit()
    conn.close()


def report():
    conn = get_connection()
    df = pd.read_sql_query(
        'SELECT t.date, c.name as category, t.amount FROM transactions t LEFT JOIN categories c ON t.category_id = c.id',
        conn
    )
    if df.empty:
        print('No transactions loaded.')
        return
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    pivot = df.pivot_table(index='category', columns='month', values='amount', aggfunc='sum', fill_value=0)
    print(pivot)
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Simple accounting system')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('initdb', help='Initialise the database with default categories and rules')

    upload = sub.add_parser('upload', help='Upload transactions from XLSX file')
    upload.add_argument('path')

    add_t = sub.add_parser('add-transaction', help='Add a manual transaction')
    add_t.add_argument('date', help='Transaction date YYYY-MM-DD')
    add_t.add_argument('description')
    add_t.add_argument('amount', type=float)
    add_t.add_argument('--category', type=int, help='Category id override')

    sub.add_parser('list-uncategorised', help='List uncategorised transaction descriptions')

    add_r = sub.add_parser('add-rule', help='Add a new description rule')
    add_r.add_argument('pattern')
    add_r.add_argument('category', type=int)

    sub.add_parser('report', help='Show spend report by category/month')

    args = parser.parse_args()
    if args.command == 'initdb':
        init_db()
    elif args.command == 'upload':
        upload_xlsx(args.path)
    elif args.command == 'add-transaction':
        add_transaction(args)
    elif args.command == 'list-uncategorised':
        list_uncategorised()
    elif args.command == 'add-rule':
        add_rule(args)
    elif args.command == 'report':
        report()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
