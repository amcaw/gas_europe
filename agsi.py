import os
import requests
import csv
import pandas as pd
from datetime import datetime

## https://agsi.gie.eu/api/data/be #

headers = {
    'x-key': (os.environ['api_key']),
}

response = requests.get('https://agsi.gie.eu/api?', headers=headers)

response_be = requests.get('https://agsi.gie.eu/api?country=BE&from=2022-01-01&page=1&size=3000', headers=headers)

myjson = response.json()

myjson_BE = response_be.json()

ourdata_EU = []

ourdata_NON_EU = []

ourdata_BE = []

ourdata_EU_NON_EU = []

csvheader = ["name", "gasInStorage", "gasDayStart", "full", "trend"]

#EU countries

for x in myjson ['data'][0]['children']:
    listing = [x['name'],x['gasInStorage'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_EU.append(listing)
    
#NON EU countries

for x in myjson ['data'][1]['children']:
    listing = [x['name'],x['gasInStorage'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_NON_EU.append(listing)
    
#EU_NON_EU countries

for x in myjson ['data']:
    listing = [x['name'],x['gasInStorage'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_EU_NON_EU.append(listing)
   
df_EU = pd.DataFrame (ourdata_EU, columns = ['country', 'in_storage', 'date', 'percentage_full', 'trend'])

df_NON_EU = pd.DataFrame (ourdata_NON_EU, columns = ['country', 'in_storage', 'date', 'percentage_full', 'trend'])

df_EU_NON_EU = pd.DataFrame (ourdata_EU_NON_EU, columns = ['country', 'in_storage', 'date', 'percentage_full', 'trend'])

# Concat files

df_ALL = pd.concat([df_EU, df_NON_EU, df_EU_NON_EU])

# Drop rows with empty values

df_ALL = df_ALL[df_ALL.percentage_full != '-']

# Merge base FR

df_base = pd.read_csv('https://raw.githubusercontent.com/amcaw/gas_europe/main/base_fr.csv')

df_ALL_FR = pd.merge(df_base, df_ALL)

# Select columns

df_ALL_FR = df_ALL_FR[["name_fr", "in_storage", "date", "percentage_full", "trend", "latitude", "longitude", "total_TWh", "pourcentage_conso", "deno"]]

# Cleaning to add up and down arrows

df_ALL_FR['trend'] = '<span style="color:green">&#x25B2;</span> ' + df_ALL_FR['trend'].astype(str)
df_ALL_FR['trend'] = df_ALL_FR['trend'].str.replace('<span style="color:green">&#x25B2;</span> -','<span style="color:red">&#x25BC;</span> -')
df_ALL_FR['trend'] = df_ALL_FR['trend'].replace({'^<span style="color:green">&#x25B2;</span> 0$':'stable'}, regex = True)
df_ALL_FR['today']= datetime.today().strftime('%d/%m/%Y')

#BE

for x in myjson_BE ['data']:
    listing = [x['name'],x['gasInStorage'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_BE.append(listing)

# Cleaning BE data

df_BE = pd.DataFrame (ourdata_BE, columns = ['country', 'TWh en stock', 'date', 'Pourcentage', 'trend'])
df_BE = df_BE.reindex(index=df_BE.index[::-1])
df_BE["date_fr"] = pd.to_datetime(df_BE["date"]).dt.strftime('%d/%m/%Y')
df_BE = df_BE[["date", "Pourcentage", "date_fr"]]

# Export to csv


df_ALL_FR.to_csv("./gas_all.csv", index=False)
df_BE.to_csv("./gas_be.csv", index=False)
