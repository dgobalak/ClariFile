import pandas as pd
from googletrans import Translator as google_translator

# TODO: Move the dataframe to an SQLite database or AWS S3
df = pd.read_csv("data/Translation/google-lang-codes.csv")


def detect_lang(text):
    return lang_code_to_name(google_translator().detect(text).lang)


# Convert the 2 character language code to its full name
def lang_code_to_name(code):
    name = df.loc[df['Code'] == code.lower(), 'Name'].iloc[0]
    return name


# Convert a language's full name to its 2 character language code
def lang_name_to_code(name):
    code = df.loc[df['Name'] == name.lower(), 'Code'].iloc[0]
    return code
