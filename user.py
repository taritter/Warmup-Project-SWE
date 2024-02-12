from pyparsing import one_of, OneOrMore, ZeroOrMore, Word, Opt, Suppress, alphanums, originalTextFor

#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)



# Example Strings
ex_string1 = 'genre = "Type of Genre" and author = "Hibbeler" or cost > 4'
ex_string2 = '"If you give a mouse a cookie"'
ex_string3 = 'author of "Love Hypothesis"'
#ex_string4 = input("Show me:")


# Pyparsing forms
field = one_of("title cost author date_published genre goodreads_rating our_rating")
value = Suppress(Opt('\"')) + OneOrMore(Word(alphanums)) + Suppress(Opt('\"'))
operators = one_of("= < > of")
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

            #title query bc first char is beginning of quotes
            title_query(s)

        else:
            # Figure out if its 'of query' or 'regular query'
            result = combined_query.parseString(s).as_list()


            # Read through query and separate different or queries
            query_array = []
            temp_and_list = []
            temp_or_list = []
            #--------------
            #NOTE: it does not work if there are numbers in the string. If they are in quotes its fine but
            #obvi it would be a string type which is not what we want
            #--------------
            
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

            print(query_array)
            print(len(result))

    except:
        # 
        print("failed")

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

def main():

    print("Welcome to ... \nfor help type 'help'")

    doneQuerying = False

    while not doneQuerying:
        
        query_prompt = input("Enter your search: ")

        if query_prompt.casefold() == 'help':
            print("Help message...")

        #db = Utilities.connect_to_firestore()

        #queryfunction(parse(query_prompt))

        done = input("Would you like to make another query? (y/n)")

        if done.casefold() == 'n':
            doneQuerying = True

    

    return 0

main()
