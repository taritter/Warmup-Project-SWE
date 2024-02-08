import Utilities
from google.cloud.firestore_v1 import FieldFilter


# input validation - Tess
# this is for and or regular args
def filter_fields_and(arr, db) -> dict:
    """
    field = "genrez"
    operator = "=="
    value = "fantasy"
    """

    # filters out all books with genre as fantasy

    books_ref = db.collection("Books")

    for i in range(len(arr)):
        books_ref = books_ref.where(filter=FieldFilter(arr[i][0], arr[i][1], arr[i][2]))

    book_dict = books_ref.stream()

    if not books_ref:
        print(f"There are no books where {arr[i][0]} {arr[i][1]} {arr[i][2]}")


    for b in book_dict:
        # Prints our book title
        book_data = b.id
        print(book_data)

    """
    book_dict = dict(books_ref.where(filter=FieldFilter(field, operator, value)).stream())
    if len(book_dict) == 0:
        # if field isn't found
        print(f"there is no data on {field} {operator} {value}")

    # if value is numeric no values that are greater than that
    if value.isnumeric():
        print(f"there are no books that are {operator} {value}")
        return {}
    for b in book_dict:
        print(f"{b.id} => {b.to_dict()}")
    """
    return book_dict


def filter_fields_or(arr, db) -> dict:
    books_ref = db.collection("Books")
    book = {}
    i = 0
    for i in range(len(arr)):
        book.update(books_ref.where(filter=FieldFilter(arr[i][0], arr[i][1], arr[i][2])).stream())


    if not books_ref:
        print(f"There are no books where {arr[i][0]} {arr[i][1]} {arr[i][2]}")

    for b in book:
        # Prints our book title
        book_data = b.id
        print(book_data)


# input validation - Paul
def book_title(title, get_field):
    db = Utilities.connect_to_firestore()
    # gets information about a specific book
    title = "Crime and Punishment"
    get_field = "cost"
    field = db.collection("Books").document(title).get()
    print(field.to_dict())
    print(field.get(get_field))

    return field.get(get_field)


def main():
    db = Utilities.connect_to_firestore()
    # print(filter_fields([["g", "==", "fantasy"]]))
    print("cost > 10")
    filter_fields_and([["cost", ">", 10]], db)
    print("genre is fantasy and cost > 10")
    filter_fields_and([["genre", "==", "Fantasy"], ["cost", ">", 10]], db)
    # print(filter_fields([["genre", "==", "fantasy"], ["cost", ">", 10]]))
    filter_fields_or([["genre", "==", "Fantasy"], ["cost", ">", 10]], db)


if __name__ == "__main__":
    main()