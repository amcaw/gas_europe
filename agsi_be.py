import os
import requests
import csv
import pandas as pd

## https://agsi.gie.eu/api/data/be ##

headers = {
    'x-key': (os.environ['api_key']),
}

response_be = requests.get('https://agsi.gie.eu/api?country=BE&from=2022-01-01&to=2022-09-18&page=1&size=3000', headers=headers)


myjson_BE = response_be.json()

ourdata_BE = []

csvheader = ["name", "gasDayStart", "full", "trend"]

df_BE = pd.DataFrame (ourdata_BE, columns = ['country', 'date', 'price', 'trend'])

for x in myjson_BE ['data']:
    listing = [x['name'],x['gasDayStart'],x['full'],x['trend']]
    ourdata_BE.append(listing)

# Cleaning BE data

df_BE = df_BE.reindex(index=df_BE.index[::-1])
df_BE["date_fr"] = pd.to_datetime(df_BE["date"]).dt.strftime('%d/%m/%Y')
df_BE = df_BE[["date", "price", "date_fr"]]

# Export to csv

df_BE.to_csv("./gas_be.csv", index=False)
