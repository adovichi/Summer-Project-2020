import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

#---------------------------------------------------------------------------------------------------------

#This program is what I plan to use to show predicted COVID-19 in the county. So far, it is not complete
#but it can show the severity of cases on a given day during the pandemic or it can graph every day  of
#the COVID-19 pandemic so far and save them to a file called 'images'. I then can compile them into a gif.
#Currently this is not opitimzied, nor do I want to have to convert these into a gif myself. I currently,
#use this to visualize predicted COVID-19 spread. To do this is uses plotly's chloropleth county level map.

#I learned  about plotly, and os at these websites:
#
#1. https://plotly.com/python/county-choropleth/
#
#2. https://docs.python.org/3/library/os.html

#---------------------------------------------------------------------------------------------------------

def main():

    #This input statement is used just to distinguish what the program will do. If the user enters 'day', then it
    #will show  the viewer solely the day they list, while  the spread will compile multiple maps showcasing
    #spread overtime.

    inp = input("Would you like to see COVID-19 Spread on a specific day or its total spread? (Type day or spread)\n")

    if(inp == "day" or inp == "Day"):

        #This block of code  will open the New York Times COVID-19 data, and  parse it into a set,
        #called allCounties. This will track each counties, total cases, for each day in the
        #data set. It then will prompt you for input on the specific date you would like to see.
        #Then it graphs the data.

        try:

            myfile = open('COVID-7-7-20.txt')

        except FileNotFoundError:

            print('It seems that the file COVID-7-7-20.txt was not found please return to GitHub and download this file')

            exit()

        info = myfile.readlines()

        allCounties = set();

        for i in range(len(info)):

            currentParse = info[i]

            fullRow = currentParse.split(',')

            newLine = ""+ fullRow[3] + "," + fullRow[1] + "," + fullRow[0] + "," + fullRow[2] + "," + fullRow[4]

            allCounties.add(newLine)

        allCounties = sorted(allCounties)

        month = input("Please enter which month you'd  like to view(List as a number 1-12)\n")

        if(len(month) == 1):

            month = "0" + month

        day = input("Please enter which day you'd like to view\n")

        if(len(day) == 1):

            day = "0" + day

        date = "2020-" + month + "-" + day

        fips = []

        values = []

        for a in range(len(allCounties)):

            currentParse = allCounties[a]

            allParse = currentParse.split(",")

            if(allParse[2]  == date and allParse[0] != ""):

                fips.append(allParse[0])

                values.append(int(allParse[4]))

        if(len(fips) == 0 or len(values)  == 0):

            print("It seems like the date you have listed, ", date,  " has  no corresponding cases.")

            exit()

        #I found this color  pallet from https://colorbrewer2.org/#type=sequential&scheme=YlOrRd&n=9

        title = "COVID-19 Cases by County " +  date

        vmin, vmax = min(values), max(values)
        colorscale = ["#ffffcc", "#ffeda0","#fed976","#feb24c","#fd8d3c","#fc4e2a","#e31a1c","#bd0026","#800026"]
        endpts = list(np.geomspace(vmin, vmax, len(colorscale) - 1))
        fig = ff.create_choropleth(fips=fips, values=values, colorscale = colorscale, binning_endpoints =  endpts, exponent_format=True, legend_title= title, round_legend_values=True)
        fig.layout.template = None
        fig.show()

    elif(inp  ==  'spread' or  inp == 'Spread'):

        #This code uses pandas, and os to print multiple figures of plotly's chloropleth map. It then
        #makes a directory, 'images' which will store the figures. It uses pandas to read a csv
        #then will store its information and using a for loop plot each days data.

        #I commented out the code below as it will write a new directory and save images to it.

        #if not os.path.exists("images"):
            #os.mkdir("images")

        print("Because I have commented out the code from writing files to your computer, the progam will exit. I will provide a gif that will show you what this program will do on my github.")

        exit()

        df = pd.read_csv("sortedCovidData.csv")

        df = df.sort_values(by="Date")

        dates = df['Date']

        dates = dates.drop_duplicates()

        allGraphs = []

        i = 0

        for date in dates:

            allData = df

            allData = allData.loc[allData['Date'] == date]

            title = "COVID-19 Cases by County " +  date

            fips = allData["Fips"]

            values = allData["Cases"]

            vmin, vmax = df["Cases"].min(), df["Cases"].max()

            colorscale = ["#ffffcc", "#ffeda0","#fed976","#feb24c","#fd8d3c","#fc4e2a","#e31a1c","#bd0026","#800026"]

            endpts = []

            if(vmin == vmax or vmax<1000):
                vmin = 0
                vmax = 1000
                endpts = list(np.linspace(vmin, vmax, len(colorscale) - 1))


            else:
                endpts = list(np.geomspace(vmin, vmax, len(colorscale) - 1))

            if(i == 0):

                fig = ff.create_choropleth(fips=fips, values=values, colorscale = colorscale, binning_endpoints =  endpts, exponent_format=True, legend_title= title, round_legend_values=True)
                fig.layout.template = None
                filename = "images/fig" + str(i) + ".png"
                #fig.write_image(filename)
            else:

                fig = ff.create_choropleth(fips=fips, values=values, colorscale = colorscale, binning_endpoints =  endpts, exponent_format=True, legend_title= title, round_legend_values=True)
                fig.layout.template = None
                filename = "images/fig" + str(i) + ".png"
                #fig.write_image(filename)

            i += 1

    else:

        print('Please choose a valid option. ', inp, ' is not day or spread')

        exit()


main()
