import pandas as pd

#Import data

df = pd.read_csv('https://bestat.statbel.fgov.be/bestat/api/views/939c67bb-39fa-4f49-9d05-c446187bef1d/result/CSV')

#Put the shit in the right shape

df = df.groupby(['Jour','Produit'], sort=False)['Prix TVA incl.'].mean().unstack()

#Select column

df = df[["Essence 95 RON E10 (€/L)", "Essence 98 RON E5 (€/L)","Diesel B7 (€/L)","Gasoil chauffage 50S (moins de 2000 l) (€/L)","Gasoil chauffage 50S (à partir de 2000 l) (€/L)"]]

#Select one year ago, today, tomorrow

df = df.take([0, -2, -1])

#Send the shit to csv

df.to_csv(r'energie.csv')
