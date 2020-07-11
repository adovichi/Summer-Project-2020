import pandas as pd
import numpy as np


#---------------------------------------------------------------------------------------------------------

#This program reads the 'neuralNetworkData.csv' file and then expands of this data in order to create
#a csv which contains information about two counties. The program will parse multiple rows from the
#orginal csv, then add them to a new DataFrame. After doing this 50000 times, it will be saved as
#a new csv file which will be used to train the model which predicts an adjacent county. This new
#file will have 5 new columns:
#
#1. Adjacent Cases
#
#2. Adjacent Fips
#
#3. Adjacent Population
#
#4. Adjacent County Population Density
#
#5. Adjacent Previous Cases
#
#Similar to the createCSV.py program, it is quite slow, and I hope to improve it more as I learn more
#about using pandas. The links where I found this data are on the FeadMe.txt file. They are the same
#as the createCSV.py file. Currently this file takes a long time to run, so I suggest using the file
#already in this directory when running the createAdjacentCountyModel.py, which is
#'adjacent_Counties_DataFrame.csv'.

#---------------------------------------------------------------------------------------------------------

def main():

    #This block of code will use the normal nueralNetworkData.csv, which was created using
    #covidRunner.py. Then it creates a empty version of df, and then adds a couple of
    #columns to it. This variable, finalDataFrame will be used in order to train and
    #test the program.

    df = pd.read_csv("nueralNetworkData.csv")

    finalDataFrame = df.iloc[0:0]

    finalDataFrame['Adjacent Cases'] = []

    finalDataFrame['Adjacent Fips'] = []

    finalDataFrame['Adjacent Population'] = []

    finalDataFrame['Adjacent County Population Density'] = []

    finalDataFrame['Adjacent Previous Cases'] = []

    #This for loop will run 50000 and each iteration take a random sample in order to
    #find data on adjacent counties. It takes a row of data from nueralNetworkData.csv
    #then finds all the adjacent counties corresponding rows on the same day, and
    #append them to another DataFrame, 'finalDataFrame'. The 'finalDataFrame' will
    #be saved as a .csv at the end of this file.

    for i in range(50000):

        startingpoint = df.sample(n= 1)

        startingpoint = startingpoint.reset_index()

        #Finds the 'Adjacent Counties', 'Day Number', 'Fips' for the row. Because
        #it is only one row I can use the .iloc[[0]] as it returns the first
        #row available. It then sorts this information into the central counties,
        #fips (home_fips), which is used to distinguish this county from others.
        #Then it creates an array counties which countains an array of every other
        #adjacent county. The first_case_daynumber will be used in order to locate
        #a corresponding row with the same date for each county.

        counties = startingpoint['Adjacent Counties'].iloc[[0]].astype(str).to_string()

        day_number_array_frame = startingpoint['Day Number'].iloc[[0]].astype(str).to_string()

        home_fips_df = startingpoint['Fips'].iloc[[0]].astype(str).to_string()

        home_fips_array = home_fips_df.split(' ')

        home_fips = int(home_fips_array[len(home_fips_array)-1])

        day_number_array = day_number_array_frame.split(' ')

        specific_case_daynumber = int(day_number_array[len(day_number_array) - 1])

        counties = counties.split(' ')

        #This for loop will go through each index in the counties array,
        #and use the fips code and the 'specific_case_daynumber' in
        #order to find the adjacent counties data for the correct
        #date. After finding this, it will append this data to the
        #main DataFrame.

        for fips in counties:

            if(len(fips) == 4 or len(fips) == 5):

                if(len(fips) == 4):

                    fips = '0' + fips

                try:

                    int_fips = int(fips)

                except ValueError:

                    print('There is an error in the DataFrame, ', fips, 'cannont be convereted to an int.')

                    exit()

                new_df = df.loc[((df['Fips'] == int_fips) & (df['Day Number'] == specific_case_daynumber))]

                if((not len(new_df) == 0) and int_fips != home_fips):

                    startingpoint = startingpoint.append(new_df)

        #I'm not that familiar with pandas so I have been messing up the indexing, so these
        #two lines of code allow for correct indexing.

        startingpoint = startingpoint.reset_index()

        startingpoint = startingpoint.drop(['index', 'level_0'], axis = 1)

        #These next arrays will be used to create a new column in a DataFrame.
        #Each variable name corresponds to what data it will be storing(cp_density
        #is county population density)

        cases = []

        fips = []

        population = []

        cp_density = []

        prevcases = []

        #This loop will now fill each of the values for these arrays. It also checks
        #to make sure that the central county will not be added twice to the dataset.


        for county in counties:

            if((not (county == '' or county == ' ')) and (len(county) == 4 or len(county) == 5)):

                specific_county_data = df.loc[((df['Fips'] == int(county)) & (df['Day Number'] == specific_case_daynumber))]

                if(len(specific_county_data) > 0 and home_fips != int(county)):

                    case = specific_county_data['Cases'].iloc[0]

                    currentfips = specific_county_data['Fips'].iloc[0]

                    adj_population = specific_county_data['Population'].iloc[0]

                    density = specific_county_data['County Population Density'].iloc[0]

                    pcases = specific_county_data['Previous Cases'].iloc[0]

                    cases.append(case)

                    fips.append(currentfips)

                    population.append(adj_population)

                    cp_density.append(density)

                    prevcases.append(pcases)

        #Creates a new DataFrame with only one row, which is the central county.

        appending_dataFrame = startingpoint.loc[startingpoint['Fips'] == home_fips]

        #This if statement is to prevent the rare chance of the central county having no adjacent counties, or
        #that none of the adjacent counties have any confirmed cases yet. It then will copy the central county's
        #row in the dataframe by the number of adjacent counties, that have any confirmed cases. Then it creates,
        #the five new columns, and appends each array to the new column. Then it resets its index in order to prevent
        #issues.

        if(len(cases) > 0):

            appending_dataFrame = appending_dataFrame.append([appending_dataFrame] * (len(cases)-1), ignore_index=True)

            appending_dataFrame['Adjacent Cases'] = cases

            appending_dataFrame['Adjacent Fips'] = fips

            appending_dataFrame['Adjacent Population'] = population

            appending_dataFrame['Adjacent County Population Density'] = cp_density

            appending_dataFrame['Adjacent Previous Cases'] = prevcases

            finalDataFrame = finalDataFrame.append([appending_dataFrame])

            finalDataFrame = finalDataFrame.reset_index()

            finalDataFrame = finalDataFrame.drop(['index'], axis=1)

    #I commented this out so it won't save the large .csv file on your computer, or rewrite the current file.

    #finalDataFrame.to_csv('adjacent_Counties_DataFrame.csv')

main()
