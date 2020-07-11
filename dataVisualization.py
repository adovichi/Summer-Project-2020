import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing

#---------------------------------------------------------------------------------------------------------

#This program is what I have been using to look at the relationship of cases between counties.
#Essentially, it will take a random sample from my dataset, where a county has its first case.
#Then, it will track all the adjacent counties cases each day going forward. I will implement
#this information into my next model. To, write this program I mostly used information about
#matplotlib's library. Specifically:
#
#1. https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
#
#2. https://matplotlib.org/tutorials/introductory/pyplot.html
#
#All data used in this specific program can be found on the New York Times github page. I used
#the file that tracks total COVID-19 cases at the county level.
#
#1. https://github.com/nytimes/covid-19-data
#
#
#It also will display variables which are used for both models. I am currently working on normalizing
#the data in order for the model to become more accurate for the majority of the data. The first
#couple of graphs is what I used to strengthen my first model. These graphs will show different
#columns within the 'neuralNetworkData.csv' file, and compare it to the number of cases. Then
#it will show data from the 'adjacent_Counties_DataFrame.csv' file. In total there are 15 graphs,
#and I learned that some variables had little to no effect on cases.

#---------------------------------------------------------------------------------------------------------

#This method see_relationship is a simple method I made for myself to plot different columns of together
#to see their relationship. It takes a sample of 1000 from the Dataset then graphs it. 

def see_relationship(df, xcolumn, ycolumn):

    sample = df.sample(1000)

    ts = sample.plot.scatter(x= xcolumn, y= ycolumn)

    ts.plot()

    plt.show()

def main():

    plt.close('all')

    df = pd.read_csv("nueralNetworkData.csv")

    #Each county will  have a previous case value in  the csv of 0. Using this we can consolidate the dataframe to just
    #this rows.

    filtered = df.loc[df['Previous Cases'] == 0]

    desired_fips = input("Please insert desired fips please! Or random for random county.\n")

    #This makes a random sample from my dataset, if 'random' is specified

    if(desired_fips == 'random' or desired_fips == 'Random'):

        startingpoint = filtered.sample(1)

    #This finds the row in the dataset, given a fips code

    else:

        try:

            startingpoint = filtered.loc[filtered['Fips'] == int(desired_fips)]

        except ValueError:

            print('Please use a Fips code. These should be numeric. To find your counties code visit, https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697')

            exit()

    startingpoint = startingpoint.reset_index()

    #This block of code will filter through the county and find the adjacent counties,
    #the day number(how many days from the first reported case in the US), and the home
    #Fips as it might not have been set due to the random option.

    counties = startingpoint['Adjacent Counties'].iloc[[0]].astype(str).to_string()

    day_number_array_frame = startingpoint['Day Number'].iloc[[0]].astype(str).to_string()

    home_fips_df = startingpoint['Fips'].iloc[[0]].astype(str).to_string()

    #This block of code will go through the Fips string which would looklike so:
    #' 00000 00000 00000', by parsing this data, it creates an  array called
    #counties that will store the fips codes of all adjacent counties. There will
    #also be a string that stores the day number. This will be converted to an
    #array then the converted back to a string in order for it to be converted
    #to an int.

    home_fips_array = home_fips_df.split(' ')

    home_fips = int(home_fips_array[len(home_fips_array)-1])

    day_number_array = day_number_array_frame.split(' ')

    first_case_daynumber = int(day_number_array[len(day_number_array) - 1])

    counties = counties.split(' ')

    #This outer for-loop will parse through each day between the first day that
    #a case was reported in the county until each reaches the maximum
    #day number in the dataframe. The inner for-loop will go through each
    #fips in the counties array the and locate the number of cases that the other
    #counties had on the same day. It will then append this data to the startingpoint
    #dataframe.

    for i in range(first_case_daynumber, df['Day Number'].max()):

        for fips in counties:

            if(len(fips) == 4 or len(fips) == 5):

                if(len(fips) == 4):

                    fips = '0' + fips

                try:

                    int_fips = int(fips)

                except ValueError:

                    print('There is an error in the DataFrame, ', fips, 'cannont be convereted to an int.')

                    exit()

                #This block of code will be used to add new rows to the existing startingpoint dataframe.
                #It will look through the original dataframe(as it stores all the data), and it will locate
                #the cases on the given day. If the new_df variable(which has the portion of the larger dataframe),
                #doesn't have a row, it will not be appended to the dataset

                new_df = df.loc[((df['Fips'] == int_fips) & (df['Day Number'] == i))]

                if(not len(new_df) == 0):

                    startingpoint = startingpoint.append(new_df)

        #Finally, this if statement will add the home counties values to the startingpoint dataframe as well.
        #This will only occur when i > first_case_daynumber.

        if(first_case_daynumber != i):

            home_county = df.loc[((df['Fips'] == home_fips) & (df['Day Number'] == i))]

            if(not len(home_county) == 0):

                startingpoint = startingpoint.append(home_county)

    #This block of code is temporary. I currently am inexperienced with pandas and
    #had trouble with the indexing of the Data Frame. So currently, this will drop
    #the mulitple layers on indexing.

    startingpoint = startingpoint.reset_index()

    startingpoint = startingpoint.drop(['index', 'level_0'], axis = 1)

    #This block of code will remove extra columns that I won't need to graph my
    #data. It also will be used to find the names of each county used in the graph.
    #Then the for loop will go through each portion of the countyname_array which
    #and add the specific portions of words back together. It also appends '(starting point)'
    #as this county will be the county where all the other counties are adjacent. Essentially,
    #this  portion of code will combine all the data regarding the starting counties data into
    #a new dataframe which will be used to graph.

    startingpoint = startingpoint[['Fips', 'Day Number', 'Cases', 'County Name']]

    specific_county_data = startingpoint.loc[startingpoint['Fips'] == home_fips]

    countyname_df = specific_county_data['County Name'].iloc[[0]].astype(str).to_string()

    countyname_array = countyname_df.split(' ')

    countyname = ''

    for b in range(1, len(countyname_array)):

        countyname +=countyname_array[b]

        countyname += ' '

    countyname += '(Starting Point)'

    #This portion of code will be used to start my line graph, and adds all the rows from
    #the starting county into the graph as one group.

    ax = specific_county_data.plot.line(x= 'Day Number', y= 'Cases', label= countyname)

    #This for-loop is very similar to the code above as it essentially serves the same purpose.
    #It will go through each county in the counties array and locate all the data specific to
    #that given county and add it to the graph as a group. It then locates the counties name,
    #and parses it back together to be described on the label of the graph.

    for county in counties:

        if(not (county == '' or county == ' ')):

            specific_county_data = df.loc[df['Fips'] == int(county)]

            if(len(specific_county_data) > 0 and home_fips != int(county)):

                countyname_df = specific_county_data['County Name'].iloc[[0]].astype(str).to_string()

                countyname_array = countyname_df.split(' ')

                countyname = ''

                for b in range(1, len(countyname_array)):

                    countyname +=countyname_array[b]

                    countyname += ' '

                #This appends the data back to the graph object and adds it together as a group.

                specific_county_data.plot.line(x= 'Day Number', y= 'Cases', label= countyname, ax=ax)

    #This will plot, and show the plot.

    ax.plot()

    plt.ylabel('Total COVID-19 Cases')

    print("To exit this plot please just hit the red x button in the top left corner.")

    plt.show()

    #These generic graphs will show the relationship between multiple variables within my
    #dataset. Specifically, this data is used for the first model I made. I isolated
    #the Day Number Variable in order to see certian trends.

    maxday = df['Day Number'].max()

    certainday = df.loc[df['Day Number'] == maxday]

    see_relationship(df, 'Day Number', 'Cases')

    see_relationship(certainday, 'County Population Density', 'Cases')

    see_relationship(certainday, 'Population', 'Cases')

    see_relationship(certainday, 'Previous Cases', 'Cases')

    see_relationship(certainday, 'Fips', 'Cases')

    #These generic graphs will show the relationship between multiple variables within my
    #dataset. Specifically, this data is used for the second model I made. It also shows
    #the difference between two counties variables which I found very helpful for my
    #second project.

    adjacent_data = pd.read_csv('adjacent_Counties_DataFrame.csv')

    adjacent_data['Difference in Cases'] = adjacent_data['Cases'] - adjacent_data['Adjacent Cases']

    adjacent_data['Difference in Population'] = adjacent_data['Population'] - adjacent_data['Adjacent Population']

    adjacent_data['Difference in Population Density'] = adjacent_data['County Population Density'] - adjacent_data['Adjacent County Population Density']

    adjacent_data['Difference in Previous Cases'] = adjacent_data['Previous Cases'] - adjacent_data['Adjacent Previous Cases']

    adjacent_data.reset_index()

    see_relationship(adjacent_data, 'Cases', 'Adjacent Cases')

    see_relationship(adjacent_data, 'Previous Cases', 'Adjacent Cases')

    see_relationship(adjacent_data, 'Day Number', 'Adjacent Cases')

    see_relationship(adjacent_data, 'County Population Density', 'Adjacent Cases')

    see_relationship(adjacent_data, 'Adjacent Population', 'Adjacent Cases')

    see_relationship(adjacent_data, 'Difference in Population', 'Difference in Cases')

    see_relationship(adjacent_data, 'Difference in Population Density', 'Difference in Cases')

    see_relationship(adjacent_data, 'Difference in Previous Cases', 'Difference in Cases')


main()
