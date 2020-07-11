import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import mean_squared_error
import numpy as np

#---------------------------------------------------------------------------------------------------------

#This model is used to predict the number of COVID-19 cases in a county on a specific day.
#It uses a csv that I created with variables such as population density, population, and
#the previous day's cases. Using these variables the model predicts how many cases there
#will be the next  day.

#I found a lot of the information I used to create this model from
#Nueral Networks Projects on Python, a textbook that introduces
#beginners to neural  networks. Ch. 2 has a project that predicts
#the price of a taxi. A lot of the code is similar, and followed the outline
#of the program in an effort to learn more about making neural networks.

#All data used in this specific program can be found on the New York Times github page. I use
#the file that tracks total COVID-19 cases at the county level. I also used US census data from
#voter registration to find the total population of each county. Another census study that lists
#the land area of each county in the country. Finally, I used one file that tracks which counties are adjacent
#to each other. I will place a screenshot or description of what this looks like in the readme file.
#
#1. https://github.com/nytimes/covid-19-data
#
#2. https://www.census.gov/programs-surveys/geography/library/reference/county-adjacency-file.html
#
#3. https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html
#
#4. https://www.census.gov/quickfacts/fact/note/US/LND110210
#
#So far this is an incredibly simple model, and I hope to improve on it in the future by adding more
#variables, and strengthening how the data is  presented. Once this model complete it will save the
#model as a directory called 'one_county_model'. I will provide a program that will use a random set of
#data in order to test my model. Currently, it isn't very accurate, but it was a nice start for me
#to build off of, as it is my first neural network.

#---------------------------------------------------------------------------------------------------------

def main():

    #The neuralNetworkData.csv file is a file I created that is currently fairly large. Essentially, for
    #each recorded instance of a new case it uses NY-Times there will be a new row in the datafile. This
    #file is parsed, and generated through the createCSV.py file.

    df = pd.read_csv("nueralNetworkData.csv")

    filtered = df[["Previous Cases", "Cases", "County Population Density", "Population", "Day Number"]]

    #My input consists of three columns: 'Previous Cases', 'County Population Density', 'Population'
    #This is my input variable.

    input = filtered.loc[:, filtered.columns != 'Cases']

    #My output is just the 'Cases' columns, so this is what I pass through as my output variable.

    output = filtered.Cases

    #I read that it was a good rule of thumb to split 20% of your data into training, and
    #keep 80% of data for testing.

    X_train, X_test, y_train, y_test = train_test_split(input, output, test_size=0.2)

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

    model = Sequential()

    #These next three lines of codes represent the layers of my neural networks.
    #I have three layers as I have three layers of input. I chose that 'relu'
    #for the activation of my hidden layer as this is what the book recomended.

    model.add(Dense(64, activation='relu', input_dim= 4))

    model.add(Dense(32, activation='relu'))

    model.add(Dense(16, activation='relu'))

    model.add(Dense(8, activation='relu'))

    model.add(Dense(1))

    #I used mean sqaured error as I believe this form of regression would be optimal
    #for this sitatuion.

    model.compile(optimizer='adam', loss= 'mse', metrics=['mean_squared_error'])

    #This line of code will run the model. I used 500 epochs for my model

    model.fit(X_train, y_train, epochs=500)

    #This block of code will show me how well my model predicts the remaining 80%
    #of my code and it will show me how accurate my model is through the test_rmse
    #variable which

    train_pred = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_pred = model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    print("Stastics on the Model: ")
    print(" ")
    print("Train RMSE: {:0.2f}".format(train_rmse))
    print("Test RMSE: {:0.2f}".format(test_rmse))
    print(" ")

    #This code below is for me to save my model.

    #model.save("one_county_model")

main()
