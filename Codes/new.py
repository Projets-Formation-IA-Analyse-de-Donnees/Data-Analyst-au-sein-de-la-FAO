# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:27:39 2024

@author: naouf
"""
%matplotlib 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
#Lecture des csv:

df_population2013=pd.read_csv(r"FAOSTAT_2013_population.csv", sep=',', usecols=["Country Code","Value","Country"])
df_animal2013=pd.read_csv(r"FAOSTAT_2013_animal.csv",sep=',',usecols=["Code Pays","Code Élément",  "Code Produit","Valeur","Élément","Produit"])
df_cereal2013=pd.read_csv(r"FAOSTAT_2013_cereal.csv",sep=',',usecols=["Code Pays","Code Élément","Code Produit","Valeur","Élément","Valeur","Produit"])
df_sous_alimentation2013=pd.read_csv(r"FAOSTAT_2013_sous_alimentation.csv",sep=',')
df_vegetal2013=pd.read_csv(r"FAOSTAT_2013_vegetal.csv",sep=',',usecols=["Code Pays","Code Élément","Code Produit","Valeur","Élément","Valeur","Produit"])

#,"Code Élément":"Code Animal","Code Produit":"Code Animal","Produit":"Produit Animal","Valeur":"Valeur Animal"
#,"Code Élément":"Code Cereal","Code Produit":"Code Cereal","Produit":"Produit Cereal","Valeur":"Valeur Animal"

df_population2013=df_population2013.rename(columns={"Country Code":"Code Pays", "Value":"Pays Valeur","Country":"Pays"})
df_animal2013=df_animal2013.rename(columns={"Élément":"Element"})
df_cereal2013=df_cereal2013.rename(columns={"Élément":"Element"})
df_vegetal2013=df_vegetal2013.rename(columns={"Élément":"Element"})

#question1

print(df_population2013["Pays Valeur"].sum())
df_population2013=df_population2013.drop(df_population2013[df_population2013["Code Pays"]== 351].index)
print(df_population2013["Pays Valeur"].sum())

#question3
df_Animal_Vegetal=pd.concat([df_animal2013,df_vegetal2013])
df_Animal_Vegetal_pop=pd.merge(df_population2013,df_Animal_Vegetal,on="Code Pays")

df_Animal_Vegetal_pop=df_Animal_Vegetal_pop[(df_Animal_Vegetal_pop["Element"]=="Disponibilité alimentaire (Kcal/personne/jour)")|(df_Animal_Vegetal_pop["Element"]=="Disponibilité de protéines en quantité (g/personne/jour)")]
df_Animal_Vegetal_pop["Disponibilité Kcal"]=df_Animal_Vegetal_pop["Valeur"]*df_Animal_Vegetal_pop["Pays Valeur"]

#df_dispoAli.loc[:,"Disponibilité Kcal"]=df_dispoAli["Valeur"]*df_dispoAli["Pays Valeur"]
#df_dispoProt.loc[:,"Disponibilité Prot"]=df_dispoProt["Valeur"]*df_dispoProt["Pays Valeur"]/1000


#question4

#df_dispoAli=df_dispoAli[df_dispoAli.loc[:,"Disponibilité Kcal"]!=0]
#df_dispoProt=df_dispoProt[df_dispoProt.loc[:,"Disponibilité Prot"]!=0]
#df_dispoAli_Prot["Ratio"]=df_dispoProt["Disponibilité Prot"]/df_dispoProt["Disponibilité Prot"]





#df_Animal_Vegetal_pop.loc[:,"Disponibilité Kcal"]=df_dispoAli["Valeur"]*df_dispoAli["Pays Valeur"]






#print(df_cereal2013.describe(include="object"))
#print(set(df_Animal_Vegetal["Produit"]))
#df_Animal_Vegetal_pop=df_Animal_Vegetal_pop[(df_Animal_Vegetal_pop["Element"]=="Disponibilité alimentaire (Kcal/personne/jour)")(df_Animal_Vegetal_pop["Element"]=="Disponibilité de protéines en quantité (g/personne/jour)")]