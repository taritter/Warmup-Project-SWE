import Utilities
import json


def pull_from_firestore(filename):
    db = Utilities.connect_to_firestore()

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
