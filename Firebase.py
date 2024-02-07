import Utilities
from google.cloud.firestore_v1 import FieldFilter


# input validation - Tess
def filter_fields(arr, db) -> dict:
    """
    field = "genrez"
    operator = "=="
    value = "fantasy"
    """

    # filters out all books with genre as fantasy

    books_ref = db.collection("Books")


    """
    doc_ref = db.collection("Books").get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
    else:
        print("No such document!") """
    book_dict = {}
    where = "books_ref"
    for i in range(len(arr)):
        where += ".where(filter=FieldFilter(" + "\"" + str(arr[i][0]) + "\", " + "\"" + str(arr[i][1]) + "\", " + "\"" + str(arr[i][2]) + "\"" + "))"

    print(where)
    book_dict = exec(where)
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
    print(filter_fields([["cost", ">", 10]], db))
    print(filter_fields([["genre", "==", "Fantasy"], ["cost", ">", 10]], db))
    # print(filter_fields([["genre", "==", "fantasy"], ["cost", ">", 10]]))


if __name__ == "__main__":
    main()