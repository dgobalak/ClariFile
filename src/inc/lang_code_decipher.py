import pandas as pd


# TODO: Move the dataframe to an SQL database
df = pd.read_csv("../datasets/Translation/google-lang-codes.csv")

# Convert the 2 character language code to its full name
def lang_code_to_name(code):
    name = df.loc[df['Code'] == code.lower(), 'Name'].iloc[0]
    return name


# COnvert a language's full name to its 2 character language code
def lang_name_to_code(name):
    code = df.loc[df['Name'] == name.lower(), 'Code'].iloc[0]
    return code

