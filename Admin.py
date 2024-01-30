import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

with open("Books.json") as json_file:
    json_data = json.load(json_file)

    #iterate through json file and add to firestore
    for book_data in json_data:
        title = book_data.get("title")

        book_dict = {
            "author": book_data.get("author"),
            "genre": book_data.get("genre"),
            "goodreads rating": book_data.get("goodreads rating"),
            "date published": book_data.get("date published"),
            "series": book_data.get("series?"),
            "cost": book_data.get("cost (paperback)"),
            "our rating": book_data.get("our rating (out of 5)"),
        }
        db.collection("Books").document(title).set(book_dict)
