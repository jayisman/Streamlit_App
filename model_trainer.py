import pandas as pd
import numpy as np

df = pd.read_csv('data/Iris.csv')

df.drop('Id', axis = 1, inplace = True)
df['Species']= df['Species'].map({'Iris-setosa':'setosa', 'Iris-versicolor':'veriscolor', 'Iris-virginica':'virginica'})

x = df.iloc[:, :-1]
y = df.iloc[:, -1]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

from sklearn.metrics import accuracy_score
score = accuracy_score(y_test, y_pred)

import pickle
pickle_out = open("output/classifier.pkl", "wb")
pickle.dump(classifier, pickle_out)
pickle_out.close()

print(df.head())
print(score)