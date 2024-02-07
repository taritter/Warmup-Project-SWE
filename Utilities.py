import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def connect_to_firestore():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db
