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
                "series": book_data.get("series?"),
                "cost": book_data.get("cost (paperback)"),
                "our_rating": book_data.get("our rating (out of 5)"),
            }
            db.collection("Books").document(title).set(book_dict)


def filter_fields(field, operator, value):
    field = "genre"
    operator = "=="
    value = "fantasy"
    db = Admin.connect_to_firestore()
    # filters out all books with genre as fantasy
    fantasy_books = db.collection("Books").where(filter=FieldFilter(field, operator, value)).stream()

    for f in fantasy_books:
        print(f"{f.id} => {f.to_dict()}")

def book_title(title):
    # gets information about a specific book
    title = "Crime and Punishment"
    crime = db.collection("Books").document(title).get()
    print(crime.to_dict())
    print(crime.get("cost"))