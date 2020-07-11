ReadMe.txt - Alex Dovichi - Summer 2020 - COVID-19 Project

Hi! Thanks for checking out my summer project. I worked on this project as a
simple way to get some exposure with machine learning and data science concepts.
My hope is to create a program that uses machine learning, and data on the US,
in order to simulate COVID-19 spread. Currently, I am using US census data, and
the New York Times COVID-19 data on their GitHub. This data includes population,
land area, total COVID-19 cases for each county in the country, counties adjacent
counties, and Fips codes. Using this data, I have currently created a simple
program that predicts COVID-19 cases based on the number of previous cases,
population density, and population. I hope to add other variables in the future,
to improve it, and I am currently working on cleaning up the data for my programs
to be more precise.
Here is where I got my data I have been using for this project:

1. https://github.com/nytimes/covid-19-data

2. https://www.census.gov/programs-surveys/geography/library/reference/county-adjacency-file.html

3. https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html

4. https://www.census.gov/quickfacts/fact/note/US/LND110210

graphCases.py - Graphs COVID-19 cases using Fips codes and the number of cases

This program is a basic program that will help me visualize how my model will
predict COVID-19 spread. I won't use this exact program for that but I  created
it for some experience with plotly's chloropleth map. Currently it has two
options, showing cases on a specific day, or saving a series of maps froland.csvlly,
this doesn't have to much with the Machine Learning portion of my project, but
will be useful  once I make a more accurate model. I also commented out all
lines which will cause files to be saved and downloaded to your computer.

I learned  about plotly, and os at these websites:

1. https://plotly.com/python/county-choropleth/

2. https://docs.python.org/3/library/os.html

In order for this program to run you'll need the following modules:

1. numpy

2. pandas

3. plotly

Runtime is about 30 seconds

createCSV.py - Parses through Data, and Concatenates it into a .csv file

This program is what I have been using to make the CSV which is used to create the
machine learning model. Currently it is quite slow, and I hope to optimize it in
the future. After parsing through all the other data, it will then write its own
file named: nueralNetworkData.csv. Currently this process is not fast, and I hope
to optimize it after finishing the model. Currently, I only run it to update
the COVID-19 cases. The four files used in this program are listed above, and the
program reads 4 files:

1. adjacentCounty.txt

2. countyPop.csv

3. land.csv

4. COVID-7-5-20.txt

Running this program will just overwrite the current nueralNetworkData.csv.

To run this program you will need the following:

1. sys

2. csv

3. numpy

This program usually takes a couple of minutes to run.

dataVisualization.py - Graphs Adjacent Counties Cases and Other variables

This program will use matplotlib's graphing module to showcases trends in data
between different variables within my nueralNetworkData.csv file. Currently,
it shows the relationship between a counties cases, and the surrounding counties
cases. In order to do this you can enter a Fips code for a specific county, or
insert random which will select a random set from my data. The program will isolate
the fist case present within the county, and will show every counties total
number of cases for the remainder of the dataset. This program is fast, and will
show you how I plan to implement the next version of my machine learning program.
I have used this to find that there is a strong correlation of cases between
counties.

In order to run this program you will need:

1. pandas

2. matplotlib

3. numpy

This runs and displays a graph within seconds.

covidNeuralNet.py - This program builds my current model

This program uses the nueralNetworkData.csv file used above in order to build
a machine learning model the predicts COVID-19 cases. It uses a regression
based model in order to predict the number of cases. It uses three variables
such as the number of previous cases, the population density, and density to
predict the number of new cases. Currently it runs with an Root Mean Square Error
of 64 when I run it with 50 epochs. The currently model is set to 10 in order to
decrease run time. I used tensorflow, and sklearn in order to write this program.
I learned a lot from this textbook:
*https://www.amazon.com/Neural-Network-Projects-Python-ultimate-ebook/dp/B07P77QWW7

Overall, I hope to improve this program by adding more variables and using it to
predict more than just one county at a time.

In order for this program to run you'll need the following modules:

1. pandas

2. sklearn

3. keras

4. numpy

This program runs in about 4-5 seconds and each epoch takes about 4 seconds.

In conclusion this is a basic start to my project and I hope to make my code
faster and my model more accurate by the end of the summer. So far I have found
that I really enjoy machine learning and hope to learn more in the future.

createAdjacentCountiesData.py - This creates a csv used for the main model

This program uses the nueralNetworkData.csv file in order to create another csv,
adjacent_Counties_DataFrame.csv. This csv will be used to create a model that
predicts adjacent counties data. It keeps the row from the nueralNetworkData
file, but then appends 5 new columns from each adjacent county.

In order to run this program you'll need:

1. numpy

2. pandas

This program took me about an hour to run.

createAdjacentCountyModel.py - Creates the model that predicts an adjacent Counties cases

This program uses adjacent_Counties_DataFrame.csv to create a model that predicts an
adjacent counties cases. It has 7 layers, and the current model was created using
500 epochs. Currently this is the most accurate model I have.

testFirstModel.py & testSecondModel.py - Tests the Models that I have

Both of these are short programs that test my data and see how accurate it
is. They take a couple of seconds and are the optimal way to see how my
models work.

You'll need:

1. numpy

2. pandas

3. tensorflow

To see what a few of my programs output is like I have added the following screenshots:

1. graphCases.png - Shows what graphCases.py, daily Chloropleth map looks like.

2. dataVisualization.png - Show dataVisualization.py graph which tracks a central and
adjacent counties positive COVID-19 cases.

3. Total_Spread.gif - Shows the gif which graphCases.py will create
