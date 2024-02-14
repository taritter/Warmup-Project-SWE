from pyparsing import one_of, OneOrMore, ZeroOrMore, Word, Opt, Suppress, originalTextFor

import Utilities

from google.cloud.firestore_v1 import FieldFilter

#pip install --upgrade firebase-admin

# Example Strings
ex_string1 = 'genre == "Fantasy" and author == "Samantha Shannon"'
ex_string2 = 'genre == "Fantasy" and author == "Samantha Shannon" or cost < "4.4"'
# cost == 23.99 or author == "Samantha Shannon"
     

# Pyparsing forms
alphanums = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.'
field = one_of("title cost author date_published genre goodreads_rating our_rating")
value = Suppress(Opt('\"')) + OneOrMore(Word(alphanums)) + Suppress(Opt('\"'))
operators = one_of("== < > of")
concat = one_of("and or")
query_form = field + operators + originalTextFor(value)
combined_query = query_form + ZeroOrMore(concat + query_form)


# Parse function
def parse(s: str, db):
    # Remove leading + trailing whitespace
    s.strip()
    query_array = []

    # Detect type of query
    try:
        if s[0] == '\"':
            # title query bc first char is beginning of quotes
            return book_title(s.strip('\"'), db)

        else:
            # Figure out if its 'of query' or 'regular query'
            result = combined_query.parseString(s).as_list()

            # Read through query and separate different or queries
            temp_and_list = []
            temp_or_list = []

            for i in result:
                if i == "or":
                    if temp_and_list:  #check if there are values separated by and
                        temp_or_list.append(temp_and_list)  #add values separated by and to or list
                    query_array.append(temp_or_list)  #add or list to the main query array
                    temp_and_list = []  #reset lists
                    temp_or_list = []
                elif i == "and":
                    if temp_and_list:  #check if there are values separated by "and"
                        temp_or_list.append(temp_and_list)  #add values separated by and to or list
                    temp_and_list = []  #reset and list
                else:
                    temp_and_list.append(i)

            if temp_and_list:  #check if there are values in and list
                temp_or_list.append(temp_and_list)  #add values to or list
            query_array.append(temp_or_list)  #add or list to the main query array

            return filter_fields_and(query_array, db)
    except:
        #
        print()
        print("[ERROR: Please check formatting or enter help for a help message]")
        print()


def book_title(title, db):
    # gets information about a specific book
    fields = db.collection("Books").document(title).get()
    # print(field.to_dict())
    if len(fields.to_dict()) == 0:
        print("This book does not exist in the database")
    return fields.to_dict()


def filter_fields_and(or_arr, db) -> set:
    """
    field = "genrez"
    operator = "=="
    value = "fantasy"
    """
    books_ref = db.collection("Books")
    book_set = set()
    # test = db.collection("Books").where(filter=FieldFilter("genre", "==", "Fantasy")).stream()
    # for bt in test:
    #     print(bt.id)
    books_or = {}

    for and_array in or_arr:
        # print(and_array)
        books_ref = db.collection("Books")
        for statement in and_array:

            #print(type(statement[2]))

            try:
                query_value = float(statement[2].strip('\"'))
            except:
                query_value = str(statement[2]).strip("\"")

            #print(type(query_value))
            #print(query_value)

            books_ref = books_ref.where(filter=FieldFilter(statement[0], statement[1], query_value))

        book_add(books_ref, book_set)

    return book_set


def book_add(books_ref, book_set):
    book = books_ref.stream()

    for b in book:
        book_set.add(b.id)


def main():
    # Admin.pull_from_firestore("Books.json")
    # print(parse(ex_string2))

    print("Welcome to ... \nfor help type 'help'")

    done_querying = False
    db = Utilities.connect_to_firestore()
    while not done_querying:

        query_prompt = input("Enter your search: ")

        if query_prompt.casefold() == 'help':
            print(f"\nFormat your query with either of the following notations:\n",
                    "1: [field] [operator] [\"value\"] (and/or) ...\nExample: genre == \"Fantasty\" \nExample: cost == \"23.99\" or date_published == \"1996\"\n\n", 
                    "Fields: title, cost, author, date_published, genre, goodreads_rating, our_rating \n", 
                    "Value: This is the area to put in the genre of a book or the numerical rating to be queried",
                    "Operators: ==, <, > \n\n",
                    "2: [\"title of book\"]\nExample: \"The Hobbit\"\n\n",
                    "Misc: help\n")
            continue
        print()
        print(parse(query_prompt, db))
        print()
        # filter_fields_and(parse(query_prompt, db), db)

        done = input("Would you like to make another query? (y/n)")

        if done.casefold() == 'n':
            done_querying = True

    return 0


if __name__ == "__main__":
    main()
#uhfghdruhbdgrurdgb