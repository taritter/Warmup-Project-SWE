import pyparsing

#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)



# Example Strings
ex_string1 = 'genre of "Book Title"'
ex_string2 = '"If you give a mouse a cookie"'
ex_string3 = 'author of "Love Hypothesis"'
#ex_string4 = input("Show me:")


# Pyparsing forms
field = pyparsing.one_of("title cost author date_published genre goodreads_rating our_rating")
value = pyparsing.Opt('\"') + pyparsing.OneOrMore(pyparsing.Word(pyparsing.alphanums)) + pyparsing.Opt('\"')
operators = pyparsing.one_of("= < > of")
concat = pyparsing.one_of("and or")
query_form = field + operators + value
combined_query = query_form + pyparsing.ZeroOrMore(concat + query_form)


# Parse function
def parse(s: str):

    # Remove leading + trailing whitespace
    s.strip()

    # Detect type of query
    if s[0] == '\"':

        #title query bc first char is beginning of quotes
        title_query(s)

    else: 
        result = combined_query.parseString(s).as_list()


        print(result[0])


        #if result[1] == "of":
        #    of_query(result[0], result[3])

        # return as_list() 

    return


def title_query(s:str):
    #Make call to query 
    print(s)

def of_query(field:str, title:str):
    #make single call to query
    return NotImplementedError

def operator_query(fields:list, operators:list, values:list):

    # Each item[i] in each list corresponds to 1 query. 
    # For single querys there will only be 1 item in each list
    # Concatenate queries together with for loop

    return NotImplementedError  


parse(ex_string1)
parse(ex_string2)
parse(ex_string3)
