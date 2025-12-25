import pandas

#Process meteorological data
def meteoCleaning(inputFile, outputFile):
    # Skip header
    meteoDf = pandas.read_csv(inputFile, skiprows=16)
    # Drop all rows where the year is 2015 to align with hydrological datasets
    meteoDf = meteoDf[meteoDf["YEAR"] >= 2016]
    meteoDf = meteoDf[~((meteoDf["YEAR"] == 2025) & (meteoDf["MO"] == 12) & (meteoDf["DY"] == 1))]

    meteoDf = meteoDf.drop("YEAR", axis=1)
    meteoDf = meteoDf.drop("MO", axis=1)
    meteoDf = meteoDf.drop("DY", axis=1)

    meteoDf.to_csv(outputFile, index=False)

#Process hydrological data
def hydroCleaning(inputFile, outputFile):
    hydroDf = pandas.read_csv(inputFile)
    hydroDf = hydroDf[hydroDf["date"] >= "2016-01-01"]

    hydroDf = hydroDf.drop("system:index", axis=1)
    hydroDf = hydroDf.drop(".geo", axis=1)

    hydroDf.to_csv(outputFile, index=False)

#Process flood data
def floodCleaning(inputFile, outputFile)
    floodDf = pandas.read_csv(inputFile)

    # Translate new column names from INDONESIAN to ENGLISH
    newColumns = ["ID", "DATE", "DAY", "MONTH", "YEAR", "PROVINCE CODE", "PROVINCE",
                   "DISTRICT CODE", "CITY","EVENT TYPE CODE" "EVENT NAME", "TYPES OF DISASTERS",
                     "FLOOD","NUMBER OF EVENTS", "DEATHS", "LOST", "SUFFERED", "EVACUATED", 
                     "SEVERELY DMG HOUSES", "MODERATELY DMG HOUSES", "LIGHTLY DMG HOUSES", 
                     "SUBMERGED HOUSES", "DMG EDUCATIONAL UNITS", "DMG HOUSES OF WORSHIP", 
                     "DMG HEALTH CARE FACILITIES", "DMG OFFICES", "BROKEN BRIDGES"]
    
    floodDf.columns = newColumns
    
    # Cities of interest
    cities = ["Bandung","Bogor", "Jakarta", "Palembang", "Pandeglang", "Semarang"]
    
    # Filter only the cities of interest
    for i in floodDf["CITY"] not in cities:
        floodDf = floodDf.drop(i)
    
    # Filter only floods from  January 2016 to November 2025
    floodDf = floodDf[floodDf["YEAR"] >= 2016]
    floodDf = floodDf[~((floodDf["YEAR"] == 2025) & (floodDf["MONTH"] == 12))]

    # Convert DATE/TIME column to datetime.date format
    floodDf["DATE"] = pandas.to_datetime(floodDf["DATE"]).dt.date

    # Drop unnecessary columns
    floodDf = floodDf.drop("ID", axis=1)
    floodDf = floodDf.drop("DAY", axis=1)
    floodDf = floodDf.drop("MONTH", axis=1)
    floodDf = floodDf.drop("YEAR", axis=1)
    floodDf = floodDf.drop("PROVINCE CODE", axis=1)
    floodDf = floodDf.drop("PROVINCE", axis=1)
    floodDf = floodDf.drop("DISTRICT CODE", axis=1)
    floodDf = floodDf.drop("EVENT TYPE CODE", axis=1)
    floodDf = floodDf.drop("EVENT NAME", axis=1)
    floodDf = floodDf.drop("TYPES OF DISASTERS", axis=1)
    floodDf = floodDf.drop("NUMBER OF EVENTS", axis=1)
    floodDf = floodDf.drop("DEATHS", axis=1)
    floodDf = floodDf.drop("LOST", axis=1)
    floodDf = floodDf.drop("SUFFERED", axis=1)
    floodDf = floodDf.drop("EVACUATED", axis=1)
    floodDf = floodDf.drop("SEVERELY DMG HOUSES", axis=1)
    floodDf = floodDf.drop("MODERATELY DMG HOUSES", axis=1)
    floodDf = floodDf.drop("LIGHTLY DMG HOUSES", axis=1)
    floodDf = floodDf.drop("SUBMERGED HOUSES", axis=1)
    floodDf = floodDf.drop("DMG EDUCATIONAL UNITS", axis=1)
    floodDf = floodDf.drop("DMG HOUSES OF WORSHIP", axis=1)
    floodDf = floodDf.drop("DMG HEALTH CARE FACILITIES", axis=1)
    floodDf = floodDf.drop("DMG OFFICES", axis=1)
    floodDf = floodDf.drop("BROKEN BRIDGES", axis=1)
   
    floodDf.to_csv(outputFile, index=False)


def main():
    cities = ["bandung", "bogor", "jakarta", "palembang", "pandeglang", "semarang"]

    for i in range(len(cities)):
        meteoInputFile = "../raw/meteorological/" + cities[i] + "_2015.csv"
        hydroInputFile = "../raw/hydrological/sm_" + cities[i] + ".csv"
        

        meteoOutputFile = "../processed/meteorological_" + cities[i] + ".csv"
        hydroOutputFile = "../processed/hydrological_" + cities[i] + ".csv"
        

        meteoCleaning(meteoInputFile, meteoOutputFile)
        hydroCleaning(hydroInputFile, hydroOutputFile)

    floodInputFile = "../raw/floods/Indonesia floods 2008-2025.csv"   
    floodOutputFile = "../processed/floods/Indonesia floods 2008-2025.csv"
    floodCleaning(floodInputFile, floodOutputFile)
main()