# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:32:41 2024

@author: naouf
"""

import pandas as pd
import numpy as np
import matplotlib as mlt
import random
#Lecture des csv:

df_population2013=pd.read_csv(r"FAOSTAT_2013_population.csv", sep=',')
df_animal2013=pd.read_csv(r"FAOSTAT_2013_animal.csv",sep=',')
df_cereal2013=pd.read_csv(r"FAOSTAT_2013_cereal.csv",sep=',')
df_sous_alimentation2013=pd.read_csv(r"FAOSTAT_2013_sous_alimentation.csv",sep=',')
df_vegetal2013=pd.read_csv(r"FAOSTAT_2013_vegetal.csv",sep=',')



# Renommage des colonnes & concatenation des csv:

df_pop=df_population2013.rename(columns={"Domain Code":"Code Domaine","Domain":"Domaine","Country Code":"Code Pays","Country":"Pays","Element Code":"Code Élément","Element":"Élément","Item Code":"Code Produit","Item":"Item","Year Code":"Code Année","Year":"Année","Unit":"Unité","Value":"Valeur","Flag":"Symbole","Flag Description":"Description du Symbole"})
df_sousalim=df_sous_alimentation2013.rename(columns={"Code zone":"Code Pays","Zone":"Pays","Code année":"Code Année","Produit":"Item"})
df_totalite=pd.concat([df_cereal2013,df_vegetal2013,df_animal2013,df_pop,df_sousalim])




df_totalite=df_totalite.pivot_table(values="Valeur",index=["Pays","Produit"], columns="Élément")
df_totalite=df_totalite.reset_index()
df_totalite = df_totalite.set_index(["Pays"])

liste=list(set(df_cereal2013["Produit"]))





df_pop=df_pop[["Valeur","Pays"]]
df_pop=df_pop.set_index("Pays")

df_totalite=pd.merge(df_totalite,df_pop,on=["Pays"])

df_totalite=df_totalite[df_totalite["Produit"].isin(liste)]


df_totalite.drop(df_totalite.loc[df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]==0].index, inplace=True)
df_totalite.drop(df_totalite.loc[df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]==0].index, inplace=True)


df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]=df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]*1000
df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]=df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]




df_totalite["ratio"]=df_totalite ["Disponibilité de protéines en quantité (g/personne/jour)"]/df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]
df_totalite["resultat"]=df_totalite["Valeur"]*df_totalite["ratio"]*1000000


print(df_totalite["resultat"].sum())






