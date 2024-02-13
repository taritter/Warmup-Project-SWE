from pyparsing import one_of, OneOrMore, ZeroOrMore, Word, Opt, Suppress, alphanums, originalTextFor

import Utilities

from google.cloud.firestore_v1 import FieldFilter

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# Example Strings
ex_string1 = 'genre = "Type of Genre" and author = "Hibbeler" or cost > "4" and author = "5" or title = "bob"'
ex_string2 = '"If you give a mouse a cookie"'
ex_string3 = 'author of "Love Hypothesis"'
# ex_string4 = input("Show me:")


# Pyparsing forms
field = one_of("title cost author date_published genre goodreads_rating our_rating")
value = Suppress(Opt('\"')) + OneOrMore(Word(alphanums)) + Suppress(Opt('\"'))
operators = one_of("== < > of")
concat = one_of("and or")
query_form = field + operators + originalTextFor(value)
combined_query = query_form + ZeroOrMore(concat + query_form)


# Parse function
def parse(s: str):
    # Remove leading + trailing whitespace
    s.strip()

    # Detect type of query
    try:
        if s[0] == '\"':

            # title query bc first char is beginning of quotes
            title_query(s)

        else:
            # Figure out if its 'of query' or 'regular query'
            result = combined_query.parseString(s).as_list()

            # Read through query and separate different or queries
            query_array = []
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



    except:
        #
        print("failed")

    return query_array


def book_title(title, db):
    # gets information about a specific book
    field = db.collection("Books").document(title).get()
    # print(field.to_dict())
    if field.to_dict() == None:
        print("This book does not exist in the database")
    return field.to_dict()


def of_query(field: str, title: str):
    # make single call to query
    return NotImplementedError


def operator_query(fields: list, operators: list, values: list):
    # Each item[i] in each list corresponds to 1 query.
    # For single querys there will only be 1 item in each list
    # Concatenate queries together with for loop

    return NotImplementedError


#parse(ex_string1)
#parse(ex_string2)
#parse(ex_string3)


def filter_fields_and(arr, db) -> dict:
    """
    field = "genrez"
    operator = "=="
    value = "fantasy"
    """
    print(arr)
    # filters out all books with genre as fantasy
    books_ref = db.collection("Books")
    book_set = set()
    test = db.collection("Books").where(filter=FieldFilter("genre", "==", "Fantasy")).stream()
    for bt in test:
        print(bt.id)

    for and_array in arr:
        print(and_array)
        for statement in and_array:
            # try catch for int values
            print(type(statement[2]))
            books_ref = books_ref.where(filter=FieldFilter(statement[0], statement[1], statement[2].strip("\"")))

    book = books_ref.stream()
    print(book)

    for b in book:
        book_set.add(b.id)

        # book_dict = books_ref.stream()
    print(book_set)


    """
    if not books_ref:
        print(f"There are no books where {arr[i][0]} {arr[i][1]} {arr[i][2]}")

    for b in book_dict:
        # Prints our book title
        book_data = b.id
        print(book_data) """

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
    return book_set
def main():

    print("Welcome to ... \nfor help type 'help'")

    doneQuerying = False

    db = Utilities.connect_to_firestore()
    while not doneQuerying:

        query_prompt = input("Enter your search: ")

        if query_prompt.casefold() == 'help':
            print("Help message...")
            continue


        filter_fields_and(parse(query_prompt), db)

        print(parse(query_prompt))

        done = input("Would you like to make another query? (y/n)")

        if done.casefold() == 'n':
            doneQuerying = True



    return 0


if __name__ == "__main__":
    main()
