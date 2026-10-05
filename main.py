from models import (
    User,
    AuthenticationError,
    BookNotFoundError,
    DuplicateBookError,
    MemberNotFoundError,
)


def login():
    #Ask for username/password up to 3 times, return a User.
    for attempt in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        try:
            user = User.authenticate(username, password)
            print(f"\nWelcome, {user.full_name}! Logged in as {user.role}.\n")
            return user
        except AuthenticationError as e:
            print(f"Login failed: {e}")
            print(f"Attempts remaining: {2 - attempt}\n")
    print("Too many failed attempts. Exiting.")
    return None


def librarian_menu(librarian):
    while True:
        print("\n--- Librarian Menu ---")
        print("1. Add book")
        print("2. Remove book")
        print("3. Update member record")
        print("4. Generate overdue report")
        print("5. Logout")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                isbn = input("ISBN: ").strip()
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                print(librarian.add_book(isbn, title, author))

            elif choice == "2":
                isbn = input("ISBN to remove: ").strip()
                print(librarian.remove_book(isbn))

            elif choice == "3":
                username = input("Username to update: ").strip()
                new_name = input("New full name (leave blank to skip): ").strip()
                fields = {}
                if new_name:
                    fields["full_name"] = new_name
                if fields:
                    print(librarian.update_member(username, **fields))
                else:
                    print("Nothing to update.")

            elif choice == "4":
                overdue = librarian.generate_overdue_report()
                if not overdue:
                    print("No overdue books. Nice.")
                else:
                    print(f"\n{len(overdue)} overdue loan(s):")
                    for loan in overdue:
                        print(
                            f"  ISBN {loan['isbn']} | borrower: {loan['username']} "
                            f"| due: {loan['due_date']} | {loan['days_overdue']} day(s) overdue"
                        )

            elif choice == "5":
                print("Logged out.")
                break

            else:
                print("Not a valid option, try again.")

        except (BookNotFoundError, DuplicateBookError, MemberNotFoundError) as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")


def student_menu(student):
    while True:
        print("\n--- Student Menu ---")
        print("1. Search books")
        print("2. View my loans")
        print("3. Update my profile")
        print("4. Logout")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                keyword = input("Search keyword (title or author): ").strip()
                results = student.search_books(keyword)
                if not results:
                    print("No books matched.")
                else:
                    for b in results:
                        print(f"  {b['title']} by {b['author']} \u2014 {b['available']}")

            elif choice == "2":
                loans = student.view_my_loans()
                if not loans:
                    print("You have no loans on record.")
                else:
                    for l in loans:
                        status = "Returned" if l["returned"] == "Yes" else "Not returned"
                        print(f"  ISBN {l['isbn']} | due {l['due_date']} | {status}")

            elif choice == "3":
                new_name = input("New full name: ").strip()
                if new_name:
                    print(student.update_profile(full_name=new_name))
                else:
                    print("Nothing entered, no changes made.")

            elif choice == "4":
                print("Logged out.")
                break

            else:
                print("Not a valid option, try again.")

        except MemberNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")


def main():
    print("=== Library Resource Management System ===\n")
    user = login()
    if user is None:
        return

    if user.role == "Librarian":
        librarian_menu(user)
    else:
        student_menu(user)


if __name__ == "__main__":
    main()