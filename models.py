from datetime import datetime, date

from data_io import (
    load_books, save_books,
    load_members, save_members,
    load_loans, save_loans,
    load_passwords,
)


class BookNotFoundError(Exception):
    #Raised when a book ISBN doesn't exist in books.txt." 
    pass


class DuplicateBookError(Exception):
    #Raised when trying to add a book whose ISBN already exists.
    pass


class MemberNotFoundError(Exception):
    #Raised when a username doesn't exist in members.txt.
    pass


class AuthenticationError(Exception):
    #Raised when a login attempt fails (bad username or password).  
    pass


class User:
    
    #Base class for anyone using the system. Librarian and Student both inherit from this.
 

    def __init__(self, username, full_name, role):
        self.username = username
        self.full_name = full_name
        self.role = role

    def __str__(self):
        return f"{self.full_name} ({self.role}, username: {self.username})"

    @classmethod
    def authenticate(cls, username, password):
    
     # Check the given username/password against passwords. 

        try:
            passwords = load_passwords()
            members = load_members()
        except Exception as e:
            # any unexpected file problem should surface as a clear error,
            # not a raw traceback
            raise AuthenticationError(f"Could not read login data: {e}")

        if username not in passwords:
            raise AuthenticationError("Username not found.")

        if passwords[username] != password:
            raise AuthenticationError("Incorrect password.")

        member_record = next((m for m in members if m["username"] == username), None)
        if member_record is None:
            raise AuthenticationError("Username has no matching member record.")

        role = member_record["role"]
        full_name = member_record["full_name"]

        if role == "Librarian":
            return Librarian(username, full_name, role)
        elif role == "Student":
            return Student(username, full_name, role)
        else:
            raise AuthenticationError(f"Unknown role '{role}' for user '{username}'.")


class Librarian(User):
   
    def add_book(self, isbn, title, author):
        #Add a new book. Raises DuplicateBookError if the ISBN already exists.  
        books = load_books()
        if any(b["isbn"] == isbn for b in books):
            raise DuplicateBookError(f"A book with ISBN {isbn} already exists.")
        books.append({
            "isbn": isbn,
            "title": title,
            "author": author,
            "available": "Yes",
        })
        save_books(books)
        return f"Added '{title}' by {author} (ISBN {isbn})."


    def remove_book(self, isbn):
    #Remove a book by ISBN. Raises BookNotFoundError if it doesn't exist.
        books = load_books()
        matching = [b for b in books if b["isbn"] == isbn]
        if not matching:
            raise BookNotFoundError(f"No book found with ISBN {isbn}.")
        books = [b for b in books if b["isbn"] != isbn]
        save_books(books)
        return f"Removed '{matching[0]['title']}' (ISBN {isbn})."

    def update_member(self, username, **fields):
    
    #   Update a member's record.  
        members = load_members()
        member = next((m for m in members if m["username"] == username), None)
        if member is None:
            raise MemberNotFoundError(f"No member found with username '{username}'.")

        for key, value in fields.items():
            if key not in ("full_name", "role"):
                raise ValueError(f"Cannot update unknown field '{key}'.")
            member[key] = value

        save_members(members)
        return f"Updated member '{username}': {fields}"

    def generate_overdue_report(self):
       
        #Return a list of overdue loans
        loans = load_loans()
        today = date.today()
        overdue = []

        for loan in loans:
            if loan["returned"] == "Yes":
                continue
            try:
                due = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()
            except ValueError:
                # a malformed date shouldn't crash the whole report
                print(f"Skipping loan with bad due_date: {loan}")
                continue

            if due < today:
                days_overdue = (today - due).days
                overdue.append({**loan, "days_overdue": days_overdue})

        return overdue


class Student(User):
     
    def search_books(self, keyword):
        
       # Return books whose title or author contains `keyword`.
         
        
        books = load_books()
        keyword = keyword.strip().lower()
        return [
            b for b in books
            if keyword in b["title"].lower() or keyword in b["author"].lower()
        ]

    def view_my_loans(self):
        #Return only the loans that belong to this student.
        loans = load_loans()
        return [l for l in loans if l["username"] == self.username]

    def update_profile(self, **fields):
        
       # Update this student's own record. 
        
        allowed_fields = ("full_name",)
        for key in fields:
            if key not in allowed_fields:
                raise ValueError(
                    f"Students cannot update '{key}'. Allowed fields: {allowed_fields}"
                )

        members = load_members()
        member = next((m for m in members if m["username"] == self.username), None)
        if member is None:
            raise MemberNotFoundError(
                f"No member record found for username '{self.username}'."
            )

        member.update(fields)
        save_members(members)

        if "full_name" in fields:
            self.full_name = fields["full_name"]

        return f"Profile updated: {fields}"