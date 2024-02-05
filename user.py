import pyparsing

#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)


ex_string1 = 'genre is "Fantasy" and genre is "Fiction"'

ex_string2 = '"If you give a mouse a cookie"'

ex_string3 = 'author of "Love Hypothesis"'

ex_string4 = input("Show me: ")

field = pyparsing.Word(pyparsing.alphas)

title = pyparsing.Opt('\"') + pyparsing.Word(pyparsing.alphanums) + pyparsing.Opt('\"')

of_query = field + "of" + title

equal_query = field + "=" + title

def parse(s: str):

    parsed_str = ""

    split1 = s.split('"')
    print(f"Split: {split1}\nLength: {len(split1)}\n")

    #if len(split1) < 

    return parsed_str

parse(ex_string1)

parse(ex_string2)

parse(ex_string3)

parse(ex_string4)
