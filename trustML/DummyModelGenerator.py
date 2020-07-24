#Load the model using pickle.
import tensorflow as tf
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

#Create a dummy model in order to practice loading it if __name__ == '__main__':

model = LogisticRegression()
w = 3
h = 3
Matrix = [[0 for x in range(w)] for y in range(h)]
model.fit(Matrix, [1,2,3])

pickle.dump(model, open('dummyModel.sav', 'wb'))

loadedModel = pickle.load(open('dummyModel.sav', 'rb'))
loadedModel.test()

#Try to match the data and models together.
