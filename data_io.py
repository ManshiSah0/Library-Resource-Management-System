import os

BOOKS_FILE = "books.txt"
MEMBERS_FILE = "members.txt"
LOANS_FILE = "loans.txt"
PASSWORDS_FILE = "passwords.txt"

# BOOKS
 
def load_books(filename=BOOKS_FILE):
    """Return a list of dicts: {isbn, title, author, available}"""
    books = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    # a malformed line shouldn't crash the whole program
                    print(f"Skipping malformed line in {filename}: {line}")
                    continue
                isbn, title, author, available = parts
                books.append({
                    "isbn": isbn,
                    "title": title,
                    "author": author,
                    "available": available,
                })
    except FileNotFoundError:
        # first run -- treat as an empty library rather than crashing
        print(f"{filename} not found, starting with an empty book list.")
    return books


def save_books(books, filename=BOOKS_FILE):
    """Write the full list of book dicts back to file, overwriting it."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for b in books:
                f.write(f"{b['isbn']},{b['title']},{b['author']},{b['available']}\n")
    except OSError as e:
        print(f"Error saving {filename}: {e}")


 
# MEMBERS 

def load_members(filename=MEMBERS_FILE):
    """Return a list of dicts: {username, full_name, role}"""
    members = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    print(f"Skipping malformed line in {filename}: {line}")
                    continue
                username, full_name, role = parts
                members.append({
                    "username": username,
                    "full_name": full_name,
                    "role": role,
                })
    except FileNotFoundError:
        print(f"{filename} not found, starting with an empty member list.")
    return members


def save_members(members, filename=MEMBERS_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for m in members:
                f.write(f"{m['username']},{m['full_name']},{m['role']}\n")
    except OSError as e:
        print(f"Error saving {filename}: {e}")


 
# LOANS
 
def load_loans(filename=LOANS_FILE):
    """Return a list of dicts: {isbn, username, borrow_date, due_date, returned}"""
    loans = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 5:
                    print(f"Skipping malformed line in {filename}: {line}")
                    continue
                isbn, username, borrow_date, due_date, returned = parts
                loans.append({
                    "isbn": isbn,
                    "username": username,
                    "borrow_date": borrow_date,
                    "due_date": due_date,
                    "returned": returned,
                })
    except FileNotFoundError:
        print(f"{filename} not found, starting with an empty loan list.")
    return loans


def save_loans(loans, filename=LOANS_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for l in loans:
                f.write(
                    f"{l['isbn']},{l['username']},{l['borrow_date']},"
                    f"{l['due_date']},{l['returned']}\n"
                )
    except OSError as e:
        print(f"Error saving {filename}: {e}")


 
# PASSWORDS
 

def load_passwords(filename=PASSWORDS_FILE):
    """Return a dict: {username: password}"""
    passwords = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 2:
                    print(f"Skipping malformed line in {filename}: {line}")
                    continue
                username, password = parts
                passwords[username] = password
    except FileNotFoundError:
        print(f"{filename} not found, starting with no registered users.")
    return passwords


def save_passwords(passwords, filename=PASSWORDS_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for username, password in passwords.items():
                f.write(f"{username},{password}\n")
    except OSError as e:
        print(f"Error saving {filename}: {e}")
    