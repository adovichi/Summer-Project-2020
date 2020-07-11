import sys
import csv
import numpy

#---------------------------------------------------------------------------------------------------------

#This program is what I have been using to make the  neuralNetworkData.csv file used in the majority of
#the programs. This program so far is far from opitimzed I advise not running it currently. It takes anywhere
#between  2-5 minutes to run completely. Essentially it uses a County class which will store specific
#county level data in order be replicated multiple times. It then will parse through 4 seperate files in
#order to store information specifically about counties(Explained further later). Then it will use the
#csv module in order to write the csv.

#All COVID-19 data used in this program can be found on the New York Times github page. I use
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

#Ultimatley, the final file will have following columns:
#
#Fips, County Name, County Population Density, Adjacent Counties, Date, Cases, Population, Day Number, Previous Cases

#Some of this code is  quite redundant and I hope to streamline this program after finishing more of  the
#model. Currently, I only have to run this  daily in order to update new cases that have recorded from the
#day before.

#I learned how to write a .csv file  here:
#
#*https://docs.python.org/3/library/csv.html

#---------------------------------------------------------------------------------------------------------

#This county class was created so I could store data about counties that needed to be repeated multiple times in
#order for my model to train. (I hope to optimize this portion of the program in the future). Also, the cases


class County():

    def __init__(self, name, fips, adjacentCounties, cases):

        self.name = name

        self.previous_cases = cases

        self.fips = fips

        self.density = 0.0

        self.adjacentCounties = adjacentCounties

        self.population = 0

def main():

    #This block of code is used as a baseline for information regarding:
    #1. Every Counties Fips in the US
    #2. All adjacent counties for each county in the US
    #3. The name of the  county.
    #4. Storing all the county objecting in the array called, allCounties
    #
    #To do this, I used a file from link below:
    #
    #* https://www.census.gov/programs-surveys/geography/library/reference/county-adjacency-file.html

    allCounties = []

    try:

        myfile = open("adjacentCounty.txt")

    except FileNotFoundError:

        print('It seems that the file, adjacentCounty.txt, was not found, please download it from GitHub and try again')

        exit()

    info = myfile.readlines()

    name = ""

    fips = 0

    adjacentCounty = []

    for i in range(len(info)):

        #This file had wierd  syntax, so I had to split by tab.
        #All adjacent counties were seperated from the central county
        #by two tabs. For example:
        #
        #"Autauga County, AL"	01001	"Autauga County, AL"	01001
		#         "Chilton County, AL"	01021
		#         "Dallas County, AL"	01047
		#         "Elmore County, AL"	01051
		#         "Lowndes County, AL"	01085
		#         "Montgomery County, AL"	01101
        #
        #To combat this, the program would append subsquent rows only
        #if there was a tab at the front of the row. If not, the county
        #object would be created and appended to the allCounties list.

        currentParse = info[i]

        current = currentParse.split('\t')

        #1st Case:
        #Because the file distinguishes adjacent counties with two tabs,
        #the first index of current would be '' as there  is nothing
        #betweent the two tabs. In this case, I would add the third index
        #to the adjCounty list. This would purely be the Fips code.

        if(current[0] == ''):

            adjCounty = current[3]

            adjCounty = adjCounty[:len(adjCounty) - 1]

            adjacentCounty.append(adjCounty)

        #2nd Case:
        #On the first pass of the for loop, name would not be intialized
        #so this elif statement will intialize the name variable. Then it
        #will keep running in order to find  the rest of the  adjacent
        #counties.

        elif(name == ""):

            name = current[0]

            name = name.replace(',', '')

            fips = current[1]

        #3rd Case:
        #This last case occurs when a new full line occurs without
        #a tab. Therefore, we will store the county object as there
        #a no more adjacent counties left. It will also replace, the
        #',' char, with '' to prevent errors later in the created csv.
        #Then the new lines data will be processed  and the data will
        #be repeated.

        else:

            name = name.replace(',', '')

            c = County(name, fips, adjacentCounty, 0)

            allCounties.append(c)

            adjacentCounty = []

            name = current[0]

            fips = current[1]

    #Next, this block of code will open a csv file that contains information  about
    #the population of each county in the US. Later it opens a file called, 'land.csv'
    #which contains the land area of each county. Both of these will later be  used
    #to find a counties population density as I could not find any csvs with this
    #data. Both of these values will be added to a respective list, and stored as
    #a string with the  counties fips, and the value.
    #
    #These files were found  here:
    #
    #* https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html
    #
    #* https://www.census.gov/quickfacts/fact/note/US/LND110210

    try:

        myfile = open("countyPop.csv")

    except FileNotFoundError:

        print('It seems that the file, countyPop.csv, was not found, please download it from GitHub and try again')

        exit()

    info = myfile.readlines()

    fipsAndPopulation = []

    fipsAndLandArea = []

    #Variable geoid, is the fips code

    for a in range(len(info)):

        currentParse = info[a]

        current =  currentParse.split(',')

        append = current[2] + "," + current[36]

        geoid = current[2]

        fipsAndPopulation.append(append)

    try:

        myfile = open("land.csv")

    except FileNotFoundError:

        print('It seems that the file, land.csv, was not found, please download it from GitHub and try again')

        exit()

    info  = myfile.readlines()

    for b in range(len(info)):

        currentParse =  info[b]

        current = currentParse.split(",")

        if(len(current)  > 3):

            #This if statement adds a leading 0 to the fips code, if it doesn't already have one.

            if(len(current[2]) != 5):

                geoid = "0" + current[2]

            else:

                geoid = current[2]

            landArea = current[4]

            newData =  geoid + "," + current[0] + "," + landArea

            fipsAndLandArea.append(newData)

    populationDensity = []

    count = 0

    #This double nested for-loop will run through each list entirely and
    #calculate the population density(Population/Land Area). I will optimize
    #this in the future. Afterwards, it goes through each county and adds the
    #population density through a double nested for-loop.

    for c in range(len(fipsAndLandArea)):

        currentParse = fipsAndLandArea[c]

        current = currentParse.split(",")

        if(len(current[0]) == 5):

            for d in range(len(fipsAndPopulation)):

                cParse = fipsAndPopulation[d]

                cP = cParse.split(",")

                cD = cP[0]

                if(current[0] == cD and float(current[2]) > 0.0):

                    populationD = float(cP[1])/float(current[2])

                    newStr = current[0] + "," + str(populationD)  + "," + cP[1]

                    populationDensity.append(newStr)

                    count = count + 1

    for e in range(len(populationDensity)):

        currentParse = populationDensity[e]

        current = currentParse.split(",")

        for f in range(len(allCounties)):

            if(current[0] == allCounties[f].fips):

                allCounties[f].density = int(float(current[1]))

                allCounties[f].population  =  current[2]

    #This block of code will go through the New York Times COVID-19 file and will
    #add a new row of data for each line in the file. This data is already sorted,
    #and will be used to add other variables. Essentially, this will add the
    #date, cases, and  day number.

    try:

        myfile = open('COVID-7-7-20.txt')

    except FileNotFoundError:

        print('It seems that the file, covid-7-7-20.txt, was not found, please download it from GitHub and try again')

        exit()

    info = myfile.readlines()

    datesAndCases = []

    dayNum = -1

    currentDate = ""

    for i in range(len(info)):

        currentParse = info[i]

        fullRow = currentParse.split(',')

        if(fullRow[0] != currentDate):

            currentDate = fullRow[0]

            dayNum += 1

        newStr = fullRow[3] + "," + fullRow[0] + "," + fullRow[4] + "," + str(dayNum)

        datesAndCases.append(newStr)

    #This next block of code will be used to merge  all the data into on large list in order
    #to write a file containing it. This list is called "finalData". It uses a string, and
    #concatenates all the rows values. This is also were the pervious cases  are stored,
    #as once a county's has been stored for a given date, the new number of cases will be
    #stored in the county object for the next date. Therefore, all the COVID-19  data, will
    #be sorted by date. This also needs to be optimzed.

    sorted(datesAndCases)

    finalData = []

    finalStr =  ""

    for b in range(len(datesAndCases)):

        newStr = datesAndCases[b].split(",")

        for h in range(len(allCounties)):

            if(allCounties[h].fips  == newStr[0]):

                adjCounty = ""

                for i in range(len(allCounties[h].adjacentCounties)):

                    adjCounty += allCounties[h].adjacentCounties[i]

                    adjCounty  += " "

                finalStr = allCounties[h].fips + "," +  allCounties[h].name[1:len(allCounties[h].name)-1] + "," + str(allCounties[h].density) + "," + adjCounty  + "," + newStr[1] + "," + newStr[2] + "," + str(allCounties[h].population) + "," + newStr[3]  + "," +  str(allCounties[h].previous_cases)

                allCounties[h].previous_cases = int(newStr[2])

                finalData.append(finalStr)

    sorted(finalData)

    #This is where I write the csv. Essentially it just iterates through the final data, and it is written to the CSV.
    #I learned  how to do  this here:
    #
    #*https://docs.python.org/3/library/csv.html
    #
    #I commented out this section of code so it won't write a massive file to your computer. 

    # with open('nueralNetworkData.csv', mode='w') as csv_file:
    #
    #     fieldnames = ['Fips', 'County Name', 'County Population Density', 'Adjacent Counties', 'Date', 'Cases', 'Population', 'Day Number', 'Previous Cases']
    #
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #
    #     writer.writeheader()
    #
    #     for j in range(len(finalData)):
    #
    #         currentParse = finalData[j]
    #
    #         current = currentParse.split(",")
    #
    #         writer.writerow({'Fips': current[0], 'County Name': current[1], 'County Population Density': current[2], 'Adjacent Counties': current[3], 'Date': current[4], 'Cases': current[5], 'Population': current[6], 'Day Number': current[7], 'Previous Cases': current[8]})

main()
