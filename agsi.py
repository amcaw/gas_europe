import os
import requests
import csv
import pandas as pd

## https://agsi.gie.eu/api/data/be ##

headers = {
    'x-key': (os.environ['api_key']),
}

response = requests.get('https://agsi.gie.eu/api?', headers=headers)

myjson = response.json()

ourdata = []

csvheader = ["name", "gasDayStart", "full"]

for x in myjson ['data'][0]['children']:
    listing = [x['name'],x['gasDayStart'],x['full']]
    ourdata.append(listing)
    
df = pd.DataFrame (ourdata, columns = ['name', 'date', 'percentage_full'])

df_base = pd.read_csv('https://raw.githubusercontent.com/amcaw/gas_tanks/main/europe.csv')

df_all = pd.merge(df_base, df)

df_all.to_csv("./gas_data.csv")
