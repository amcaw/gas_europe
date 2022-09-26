import os
import requests
import csv
import pandas as pd

## https://agsi.gie.eu/api/data/be ##

headers = {
    'x-key': (os.environ['api_key']),
}

response = requests.get('https://agsi.gie.eu/api?', headers=headers)

response_be = requests.get('https://agsi.gie.eu/api?country=BE&from=2022-01-01&to=2022-09-18&page=1&size=3000', headers=headers)

myjson = response.json()

myjson_BE = response_be.json()

ourdata_EU = []

ourdata_NON_EU = []

ourdata_BE = []

csvheader = ["name", "gasDayStart", "full", "trend"]

#EU countries

for x in myjson ['data'][0]['children']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_EU.append(listing)
    
#NON EU countries

for x in myjson ['data'][1]['children']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_NON_EU.append(listing)
    
#BE

for x in myjson_BE ['data']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_BE.append(listing)
    
df_EU = pd.DataFrame (ourdata_EU, columns = ['country', 'date', 'percentage_full', 'trend'])

df_NON_EU = pd.DataFrame (ourdata_NON_EU, columns = ['country', 'date', 'percentage_full', 'trend'])

df_BE = pd.DataFrame (ourdata_BE, columns = ['country', 'date', 'price', 'trend'])

# Concat files

df_ALL = pd.concat([df_EU, df_NON_EU])

# Drop rows with empty values

df_ALL = df_ALL[df_ALL.percentage_full != '-']

# Merge base FR

df_base = pd.read_csv('https://raw.githubusercontent.com/amcaw/gas_europe/main/base_fr.csv')

df_ALL_FR = pd.merge(df_base, df_ALL)

# Select columns

df_ALL_FR = df_ALL_FR[["name_fr", "percentage_full", "trend"]]

# Cleaning to add up and down arrows

df_ALL_FR['trend'] = '<span style="color:green">&#x25B2;</span> ' + df_ALL_FR['trend'].astype(str)
df_ALL_FR['trend'] = df_ALL_FR['trend'].str.replace('<span style="color:green">&#x25B2;</span> -','<span style="color:red">&#x25BC;</span> ')
df_ALL_FR['trend'] = df_ALL_FR['trend'].replace({'^<span style="color:green">&#x25B2;</span> 0$':'='}, regex = True)

# Cleaning BE data

df_BE = df_BE.reindex(index=df_BE.index[::-1])
df_BE["date_fr"] = pd.to_datetime(df_BE["date"]).dt.strftime('%d/%m/%Y')
df_BE = df_BE[["date", "price", "date_fr"]]

# Export to csv


df_ALL_FR.to_csv("./gas_all.csv", index=False)
df_BE.to_csv("./gas_be.csv", index=False)
