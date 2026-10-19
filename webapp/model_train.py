import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle

dataset=pd.read_csv('Iris.csv')
dataset.drop('Id',axis=1,inplace=True)

X=dataset.iloc[:,0:4]
y=dataset.iloc[:,4]

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model=GaussianNB()
model.fit(X_train,y_train)

accuracy=accuracy_score(y_test,model.predict(X_test))
print(f"Model Accuracy: {accuracy*100:.2f}%")

with open('iris_model.pkl','wb') as f:
    pickle.dump(model,f)

