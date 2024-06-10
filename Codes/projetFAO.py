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

df_pop=df_population2013.rename(columns={"Domain Code":"Code Domaine","Domain":"Domaine","Country Code":"Code Pays","Country":"Pays","Element Code":"Code Élément","Element":"Élément","Item Code":"Code Produit","Item":"Produit","Year Code":"Code Année","Year":"Année","Unit":"Unité","Value":"Valeur","Flag":"Symbole","Flag Description":"Description du Symbole"})
df_sousalim=df_sous_alimentation2013.rename(columns={"Code zone":"Code Pays","Zone":"Pays","Code année":"Code Année"})
df_totalite=pd.concat([df_cereal2013,df_vegetal2013,df_animal2013,df_pop,df_sousalim])

#%%  Question 1:



#Création d'une autre table à l'aide de "pivot table" selon les domaines afin d'isoler la population pour chaque pays
table= df_totalite.pivot_table(values="Valeur",index="Pays", columns="Domaine")
#on fait donc la somme de la colone population
print(int(table["Food Balance Sheets"].sum()*1000))
#Ce n'est pas possible qu'il y ai 8.5M de personnes sur terre en 2013, on se rend compte que la chine est compté deux fois de differente manière(mais de valeur identique), on se propose donc de supprimer l'une de ces deux valeurs


#On supprime les lignes concernant la chine afin de pouvoir utiliser les lignes concernant la chine et le detaille de ses territoires
df_totalite.drop(df_totalite.loc[df_totalite["Code Pays"] == 351].index, inplace=True)

#Création d'une autre table à l'aide de "pivot table" selon les domaines afin d'isoler la population pour chaque pays, cette table donc la précédente du meme nom
table= df_totalite.pivot_table(values="Valeur",index="Pays", columns="Domaine")
#on fait donc la somme de la colone population
print(int(table["Food Balance Sheets"].sum()*1000))
#le nombre de personne sur terre est déja plus rationnel


#%%  Question 2:
    
#on se rend compte que: Prodution + Importation + Variation de Stock - Exportation = DisponibilitéInterieur - AlimentationAnimaux - Semences - Pertes - Traitement - AutresUtilisations = Nourriture


#%%  Question 3:

#Création d'une autre table à l'aide de "pivot table" selon les domaines afin d'isoler la population pour chaque pays
df_3=pd.concat([df_vegetal2013,df_animal2013,df_pop])

#Disponibilité alimentaire donnée pour chaque produit et pour chaque pays en kcal/personne/jour

df_dispo= df_3[df_3["Élément"] == "Disponibilité alimentaire (Kcal/personne/jour)"]
df_question3=pd.merge(df_dispo,df_pop, on="Code Pays")

df_question3["Disponibilité calories"]=df_question3["Valeur_x"]*df_question3["Valeur_y"]

#Disponibilité alimentaire en protéines donnée pour chaque produit et pour chaque pays en g/personne/jour.
df_dispo= df_3[df_3["Élément"] == "Disponibilité de protéines en quantité (g/personne/jour)"]
df_question3bis=pd.merge(df_dispo,df_pop, on="Code Pays")
df_question3["Disponibilité protéine"]=df_question3bis["Valeur_x"]*df_question3bis["Valeur_y"]*1000

#%%  Question 4:
#ratio poid energie
df_question3=df_question3[df_question3["Disponibilité protéine"]!=0]
#df_question3.drop(df_question3[df_question3["Disponibilité protéine"]==0].index,inplace=True)
df_question3["Ratio poid/Energie"]=df_question3["Disponibilité calories"]/df_question3["Disponibilité protéine"]
df_question3.sort_values(by="Ratio poid/Energie", ascending=False, inplace=True)

#%%  Question 5:

data2=df_question3[["Produit_x","Ratio poid/Energie"]].groupby(["Produit_x"]).mean()
data2.sort_values(by="Ratio poid/Energie", ascending=False, inplace=True)
data2=data2.head(20)
data2=data2.sample(20)
data2=data2.reset_index()
print(data2.head(5)[["Produit_x"]])


data3=df_question3[["Produit_x","Disponibilité protéine"]].groupby(["Produit_x"]).mean()
data3.sort_values(by="Disponibilité protéine", ascending=False, inplace=True)
data3=data3.head(20)
data3=data3.sample(20)
data3=data3.reset_index()
print(data3.head(5)[["Produit_x"]])

#%%  Question 6:
    
dfdispoInterieur=df_totalite[df_totalite["Élément"] == "Disponibilité intérieure"]

dfdispoKal= df_vegetal2013[df_vegetal2013["Élément"] == "Disponibilité alimentaire (Kcal/personne/jour)"]

dfdispoProt= df_vegetal2013[df_vegetal2013["Élément"] == "Disponibilité de protéines en quantité (g/personne/jour)"]

df_dispoKalParPers =pd.merge(dfdispoKal,df_pop, on="Code Pays")

df_dispoProtParPers=pd.merge(dfdispoProt,df_pop, on="Code Pays")

df_tot=pd.merge(df_dispoProtParPers,df_dispoKalParPers, on=["Code Pays","Produit_x"],suffixes=["_a","_b"])

df_tot ["Disponibilité calories végétal"]=df_tot ["Valeur_x_a"]*df_tot ["Valeur_y_a"]*1000

df_tot["Disponibilité protéine végétal"]=df_tot["Valeur_y_a"]*df_tot["Valeur_y_b"]*1000

df_tot=pd.merge(dfdispoInterieur,df_tot, on="Code Pays")

df_tot["ratio"]=df_tot ["Disponibilité calories végétal"]/df_tot["Disponibilité protéine végétal"]

df_tot.drop(df_tot.loc[df_tot["ratio"]==0].index, inplace=True)
df_tot.drop(df_tot.loc[df_tot["Valeur"]==0].index, inplace=True)

df_tot["resultat"]=df_tot["Valeur"]*df_tot["ratio"]

print(df_tot["resultat"].sum())




"""df_totalite=df_totalite.pivot_table(values="Valeur",index=["Pays","Produit"], columns="Élément")
df_totalite=df_totalite.reset_index()
df_totalite = df_totalite.set_index(["Pays"])

liste=list(set(df_cereal2013["Produit"]))





df_pop=df_pop[["Valeur","Pays"]]
df_pop=df_pop.set_index("Pays")

df_totalite=pd.merge(df_totalite,df_pop,on=["Pays"])

df_totalite=df_totalite[df_totalite["Produit"].isin(liste)]


df_totalite.drop(df_totalite.loc[df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]==0].index, inplace=True)
df_totalite.drop(df_totalite.loc[df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]==0].index, inplace=True)
df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]=df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]
df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]=df_totalite["Disponibilité de protéines en quantité (g/personne/jour)"]*1000




df_totalite["ratio"]=df_totalite ["Disponibilité de protéines en quantité (g/personne/jour)"]/df_totalite["Disponibilité alimentaire (Kcal/personne/jour)"]
df_totalite["resultat"]=df_totalite["Valeur"]*df_totalite["ratio"]*1000


print(df_totalite["resultat"].sum())"""
    

   


    			



    


    	


	

