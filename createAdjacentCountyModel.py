import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import mean_squared_error

#---------------------------------------------------------------------------------------------------------

#This program uses the data from createAdjacentCountiesData.py in order to create a model that will
#predict an adjacent counties number of cases. It uses a fairly similar format to my previous model
#that takes data on a county, in order to predict its own amount of cases. It has 7 layers, and uses
#data on the central county, and adjacent county in order to make a prediction on the adjacent counties cases.
#It uses variables such as a county's, cases, population, the previous numbers of cases,
#population density(population/land area), the difference in population density, and the difference in
#previous cases, in order to make a prediction. The model that I have saved in the directory, 'my_model',
#was created using  this program and took 500 epochs to train. I will provide a program that will show the
#accuracy of the model.
#
#All the links for the data used in this model are in the ReadMe.txt file. Currently this model is
#fairly accurate in comparsion to the other model. I still hope to improve upon it by converting the data
#and removing outliers from the dataset. This will make it more accurate for the vast majority of data.

#---------------------------------------------------------------------------------------------------------

def main():

    #This chunk of code will read the csv in this directory called 'adjacent_Counties_DataFrame.csv' and
    #then it will create three new columns in order make my model more accurate. When using my
    #dataVisualization program, I noticed that +/- difference in variables such as population, county
    #population density, had a similar +/- effect on cases. Therefore, I created the three new columns
    #which track these differences.

    df = pd.read_csv('adjacent_Counties_DataFrame.csv')

    df['Difference in Population'] = df['Population'] - df['Adjacent Population']

    df['Difference in Population Density'] = df['County Population Density'] - df['Adjacent County Population Density']

    df['Difference in Previous Cases'] = df['Previous Cases'] - df['Adjacent Previous Cases']

    filtered = df[['Cases', 'Adjacent Cases', 'County Population Density', 'Difference in Population Density', 'Population', 'Difference in Population', 'Previous Cases', 'Difference in Previous Cases']]

    filtered.reset_index()

    #This will give the viewer a basic understanding of the dataset that I am using to train this model.

    print(filtered.head())

    print(filtered.describe())

    #The input variales are as follows:
    #'Cases', 'Adjacent Cases', 'County Population Density', 'Difference in Population Density', 'Population', 'Difference in Population', 'Previous Cases', 'Difference in Previous Cases'

    input = filtered.loc[:, filtered.columns != 'Adjacent Cases']

    #Output is just the number of Adjacent Cases

    output = filtered.loc[:, filtered.columns == 'Adjacent Cases']

    X_train, X_test, y_train, y_test = train_test_split(input, output, test_size=0.2)

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

    #This time I increased the number of arrays in the layers based of the number
    #of parameters I say in the model.summary() method.

    model = Sequential()

    model.add(Dense(64, activation='relu', input_dim= 7))

    model.add(Dense(256, activation='relu'))

    model.add(Dense(128, activation='relu'))

    model.add(Dense(32, activation='relu'))

    model.add(Dense(16, activation= 'relu'))

    model.add(Dense(32, activation= 'relu'))

    model.add(Dense(16, activation= 'relu'))

    model.add(Dense(1))

    model.compile(optimizer='adam', loss= 'mse', metrics=['mean_squared_error'])

    model.fit(X_train, y_train, epochs=500)

    #This next set of data sees how accuractly my model predicts the other portion of the
    #dataset.

    train_pred = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_pred = model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    print("Stastics on the Model: ")
    print(" ")
    print("Train RMSE: {}".format(train_rmse))
    print("Test RMSE: {}".format(test_rmse))
    print(" ")

    #This will print a summary of the model, which displays information  about the
    #shape of each layer and the number of parameters. It also shows the total
    #number of parameters.

    print(model.summary())

    #This is commented out to prevent a new model from being created

    #model.save("my_model")

main()
