import os
import requests
import csv
import pandas as pd

## https://agsi.gie.eu/api/data/be ###

headers = {
    'x-key': (os.environ['api_key']),
}

response = requests.get('https://agsi.gie.eu/api?', headers=headers)

myjson = response.json()

ourdata_EU = []

ourdata_NON_EU = []

csvheader = ["name", "gasDayStart", "full", "trend"]

#EU countries

for x in myjson ['data'][0]['children']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_EU.append(listing)
    
#NON EU countries

for x in myjson ['data'][1]['children']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_NON_EU.append(listing)
    
df_EU = pd.DataFrame (ourdata_EU, columns = ['country', 'date', 'percentage_full', 'trend'])

df_NON_EU = pd.DataFrame (ourdata_NON_EU, columns = ['country', 'date', 'percentage_full', 'trend'])

# Concat files

df_ALL = pd.concat([df_EU, df_NON_EU])

# Drop rows with empty values

df_ALL = df_ALL[df_ALL.percentage_full != '-']

# Merge base FR

df_base = pd.read_csv('https://raw.githubusercontent.com/amcaw/gas_europe/main/base_fr.csv')

df_ALL_FR = pd.merge(df_base, df_ALL)

df_ALL_FR = df_ALL_FR[["name_fr", "percentage_full", "trend"]]

df_ALL_FR.to_csv("./gas_all.csv", index=False)
