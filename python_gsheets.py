"""
Interact with Google sheets

"""

import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_client(creds_file='client_secrets.json'):
    """
    use creds to create a client to interact with the Google Drive API
    :param creds_file: 'clients_json
    :return: gspread Client object
    """
    scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    return client


client = get_client(creds_file='client_secrets.json')
workbook = client.open("python_gsheets_backend")
sheet1 = workbook.sheet1

# Extract and print all of the values
list_of_hashes = sheet1.get_all_records()
print(list_of_hashes)

df = pd.DataFrame.from_records(list_of_hashes)

print(df.head())

def get_domain(email_col):
    return email_col.split('@')[1]

df['domain'] = df['email'].apply(get_domain)

# People with a gmail domain
peeps = df.loc[df['domain'] == 'gmail.com', 'first_name']

#create tab
try:
    new_sheet = workbook.add_worksheet(title='peeps', rows="20", cols="5")
except gspread.exceptions.APIError:
    new_sheet = workbook.worksheet('peeps')


new_sheet.insert_row(list(peeps), index=1)
new_sheet.insert_row('Sitting in a tree'.split(), index=2)
new_sheet.insert_row([char for char in 'KISSING'], index=3)




