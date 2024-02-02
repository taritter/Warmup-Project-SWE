import Admin
import json
from google.cloud.firestore_v1 import FieldFilter


def pull_from_firestore(filename):
    db = Admin.connect_to_firestore()

    with open(filename) as json_file:
        json_data = json.load(json_file)

        # iterate through json file and add to firestore
        for book_data in json_data:
            title = book_data.get("title")

            book_dict = {
                "author": book_data.get("author"),
                "genre": book_data.get("genre"),
                "goodreads_rating": book_data.get("goodreads rating"),
                "date_published": book_data.get("date published"),
                # "series": book_data.get("series?"),
                "cost": book_data.get("cost (paperback)"),
                "our_rating": book_data.get("our rating (out of 5)"),
            }
            db.collection("Books").document(title).set(book_dict)


# input validation - Tess
def filter_fields(field, operator, value):
    field = "genre"
    operator = "=="
    value = "fantasy"
    db = Admin.connect_to_firestore()
    # filters out all books with genre as fantasy
    book_dict = db.collection("Books").where(filter=FieldFilter(field, operator, value)).stream()

    for b in book_dict:
        print(f"{b.id} => {b.to_dict()}")

    return book_dict


# input validation - Paul
def book_title(title, get_field):
    db = Admin.connect_to_firestore()
    # gets information about a specific book
    title = "Crime and Punishment"
    get_field = "cost"
    field = db.collection("Books").document(title).get()
    print(field.to_dict())
    print(field.get(get_field))

    return field.get(get_field)

