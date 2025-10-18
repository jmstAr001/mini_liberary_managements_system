# Data structures
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Mystery", "Romance", "History")

books = {
    # Example: "978-1234567897": {"title": "Example", "author": "A Author", "genre": "Fiction",
    #                            "total_copies": 3, "available_copies": 3}
}

members = [
    # Example: {"member_id": "M001", "name": "John Doe", "email": "john@example.com", "borrowed_books": []}
]

def find_member_index(member_id):
    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            return i
    return None

# ---------- Core functions ----------
def add_book(isbn, title, author, genre, total_copies):
    if isbn in books:
        return False, f"ISBN {isbn} already exists."
    if genre not in GENRES:
        return False, f"Genre '{genre}' not valid. Valid genres: {GENRES}"
    try:
        total_copies = int(total_copies)
    except ValueError:
        return False, "total_copies must be an integer."
    if total_copies <= 0:
        return False, "total_copies must be at least 1."
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies
    }
    return True, f"Book '{title}' added with ISBN {isbn}."

def add_member(member_id, name, email):
    if find_member_index(member_id) is not None:
        return False, f"Member ID {member_id} already exists."
    members.append({"member_id": member_id, "name": name, "email": email, "borrowed_books": []})
    return True, f"Member {name} (ID {member_id}) added."

def search_books(query):
    """Search by title or author (case-insensitive). Returns list of (isbn, bookdict) matches."""
    q = query.strip().lower()
    results = []
    for isbn, info in books.items():
        if q in info["title"].lower() or q in info["author"].lower():
            results.append((isbn, info))
    return results

def update_book(isbn, **kwargs):
    if isbn not in books:
        return False, f"No book with ISBN {isbn}."
    book = books[isbn]
    # Allowed to update title, author, genre, total_copies
    if "genre" in kwargs:
        if kwargs["genre"] not in GENRES:
            return False, f"Genre '{kwargs['genre']}' not valid."
        book["genre"] = kwargs["genre"]
    if "title" in kwargs:
        book["title"] = kwargs["title"]
    if "author" in kwargs:
        book["author"] = kwargs["author"]
    if "total_copies" in kwargs:
        try:
            new_total = int(kwargs["total_copies"])
        except ValueError:
            return False, "total_copies must be an integer."
        if new_total < 0:
            return False, "total_copies cannot be negative."
        borrowed = book["total_copies"] - book["available_copies"]
        if new_total < borrowed:
            return False, f"Cannot set total_copies to {new_total}; currently {borrowed} copies are borrowed."
        # adjust available copies based on new total
        available_new = new_total - borrowed
        book["total_copies"] = new_total
        book["available_copies"] = available_new
    return True, f"Book {isbn} updated."

def update_member(member_id, **kwargs):
    idx = find_member_index(member_id)
    if idx is None:
        return False, f"No member with ID {member_id}."
    if "name" in kwargs:
        members[idx]["name"] = kwargs["name"]
    if "email" in kwargs:
        members[idx]["email"] = kwargs["email"]
    return True, f"Member {member_id} updated."

def delete_book(isbn):
    if isbn not in books:
        return False, f"No book with ISBN {isbn}."
    book = books[isbn]
    borrowed = book["total_copies"] - book["available_copies"]
    if borrowed > 0:
        return False, f"Cannot delete book {isbn}; {borrowed} copies are currently borrowed."
    del books[isbn]
    return True, f"Book {isbn} deleted."

def delete_member(member_id):
    idx = find_member_index(member_id)
    if idx is None:
        return False, f"No member with ID {member_id}."
    if members[idx]["borrowed_books"]:
        return False, f"Cannot delete member {member_id}; they have borrowed books."
    members.pop(idx)
    return True, f"Member {member_id} deleted."

def borrow_book(member_id, isbn):
    idx = find_member_index(member_id)
    if idx is None:
        return False, "Member not found."
    if isbn not in books:
        return False, "Book not found."
    member = members[idx]
    book = books[isbn]
    if len(member["borrowed_books"]) >= 3:
        return False, "Borrowing limit reached (3 books)."
    if book["available_copies"] <= 0:
        return False, "No available copies to borrow."
    # borrow
    member["borrowed_books"].append(isbn)
    book["available_copies"] -= 1
    return True, f"Member {member_id} borrowed book {isbn}."

def return_book(member_id, isbn):
    idx = find_member_index(member_id)
    if idx is None:
        return False, "Member not found."
    if isbn not in books:
        return False, "Book not found."
    member = members[idx]
    book = books[isbn]
    if isbn not in member["borrowed_books"]:
        return False, f"Member {member_id} did not borrow book {isbn}."
    member["borrowed_books"].remove(isbn)
    book["available_copies"] += 1
    # safety: available should not exceed total
    if book["available_copies"] > book["total_copies"]:
        book["available_copies"] = book["total_copies"]
    return True, f"Member {member_id} returned book {isbn}."

# ---------- Small demonstration ----------
def demo():
    print(add_book("978-1111111111", "The First Book", "Alice Smith", "Fiction", 2)[1])
    print(add_book("978-2222222222", "Science Today", "Bob Jones", "Non-Fiction", 1)[1])
    print(add_member("M001", "Jonathan Moriwah", "jonathan@example.com")[1])
    print(add_member("M002", "Mariama Kamara", "mariama@example.com")[1])
    print("Search 'first':", search_books("first"))
    print(borrow_book("M001", "978-1111111111")[1])
    print(borrow_book("M001", "978-1111111111")[1])  # second copy
    print(borrow_book("M001", "978-2222222222")[1])  # reaches limit of 3? this would be 3rd
    # Trying a 4th borrow (should fail)
    ok, msg = borrow_book("M001", "978-3333333333")
    print("Attempt borrow nonexisting:", msg)
    print(return_book("M001", "978-1111111111")[1])
    print(update_book("978-1111111111", title="The First Book - 2nd Ed", total_copies=3)[1])
    print(delete_member("M002")[1])
    print(delete_book("978-2222222222")[0], "- should fail if borrowed.")
    print("Books state:", books)
    print("Members state:", members)

# If run as script, run demo
if __name__ == "__main__":
    demo()


