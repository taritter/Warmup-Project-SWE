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
    #needs to be double nested for loop because the input array is a 2-d array. like this kind of idk we'll fix it later 
    for and_array in range(len(arr)):
        for statement in and_array:
            books_ref = books_ref.where(filter=FieldFilter(arr[and_array][0], arr[and_array][1], arr[and_array][2]))

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
    book_set = set()
    i = 0
    for i in range(len(arr)):
        book = books_ref.where(filter=FieldFilter(arr[i][0], arr[i][1], arr[i][2])).stream()
        for b in book:
        # Prints our book title
            book_set.add(b.id)


    if not books_ref:
        print(f"There are no books where {arr[i][0]} {arr[i][1]} {arr[i][2]}")


    for bs in book_set:
        # Prints our book title
        print(bs)


def filter_fields_and(arr, db) -> dict:
    """
    field = "genrez"
    operator = "=="
    value = "fantasy"
    """

    # filters out all books with genre as fantasy

    books_ref = db.collection("Books")
    #needs to be double nested for loop because the input array is a 2-d array. like this kind of idk we'll fix it later 
    for and_array in range(len(arr)):
        for statement in and_array:
            books_ref = books_ref.where(filter=FieldFilter(arr[and_array][0], arr[and_array][1], arr[and_array][2]))

    book_dict = books_ref.stream()

    if not books_ref:
        print(f"There are no books where {arr[i][0]} {arr[i][1]} {arr[i][2]}")


    for b in book_dict:
        # Prints our book title
        book_data = b.id
        print(book_data)
    return book_dict


# input validation - Paul
def book_title(title, db):
    # gets information about a specific book
    field = db.collection("Books").document(title).get()
    # print(field.to_dict())
    if field.to_dict() == None:
        print("This book does not exist in the database")
    return field.to_dict()


def main():
    db = Utilities.connect_to_firestore()
    # print(filter_fields([["g", "==", "fantasy"]]))
    #print("cost > 10")
    #filter_fields_and([["cost", ">", 10]], db)
    #print("genre is fantasy and cost > 10")
    #filter_fields_and([["genre", "==", "Fantasy"], ["cost", ">", 10]], db)
    # print(filter_fields([["genre", "==", "fantasy"], ["cost", ">", 10]]))
    # filter_fields_or([["genre", "==", "Fantasy"], ["cost", ">", 10]], db)
    # filter_fields([[['genre', '=', '"Type of Genre"'], ['author', '=', '"Hibbeler"']], [['cost', '>', '"4"'], ['author', '=', '"5"']], [['title', '=', '"bob"']]])

    book_title("The Dark Tower", db)


if __name__ == "__main__":
    main()
