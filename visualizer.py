from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd
#Initialize Data
operations_matrix = {0: "NULL", 1: "AVERAGE"}
df_Iris = pd.read_csv("data/Iris.csv",delimiter=',')
df_Setosa = df_Iris[df_Iris['Species']=='Iris-setosa']
df_Versicolor = df_Iris[df_Iris['Species']=='Iris-versicolor']
df_Virginica = df_Iris[df_Iris['Species']=='Iris-virginica']

metrics_by_species ={'Iris-setosa':{df_Setosa['SepalLengthCm'].mean()}}
print(metrics_by_species)


#Sanitize

#print(df_Iris_Setosa)



