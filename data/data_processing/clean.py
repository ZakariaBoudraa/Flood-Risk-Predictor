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
def floodCleaning(inputFile, outputFile):
    floodDf = pandas.read_csv(inputFile)

    # Translate new column names from INDONESIAN to ENGLISH
    newColumns = ["ID", "DATE", "DAY", "MONTH", "YEAR", "PROVINCE CODE", "PROVINCE",
                   "DISTRICT CODE", "CITY", "EVENT TYPE CODE", "EVENT NAME", "TYPES OF DISASTERS",
                     "FLOOD","NUMBER OF EVENTS", "DEATHS", "LOST", "WOUNDED", "SUFFERED", "EVACUATED",
                     "SEVERELY DMG HOUSES", "MODERATELY DMG HOUSES", "LIGHTLY DMG HOUSES", 
                     "SUBMERGED HOUSES", "DMG EDUCATIONAL UNITS", "DMG HOUSES OF WORSHIP", 
                     "DMG HEALTH CARE FACILITIES", "DMG OFFICES", "BROKEN BRIDGES"]
    
    floodDf.columns = newColumns
    
    # Cities of interest
    cities = ["Bandung", "Bandung Barat", "Kota Bandung", "Bogor", "Kota Bogor", "Kota Adm. Jakarta Utara",
              "Kota Adm. Jakarta Barat", "Kota Adm. Jakarta Pusat", "Kota Adm. Jakarta Selatan",
              "Kota Adm. Jakarta Timur", "Kota Palembang", "Pandeglang", "Semarang", "Kota Semarang"]
    
    # Filter only the cities of interest
    for index, row in floodDf.iterrows():
        if row["CITY"] not in cities:
            floodDf = floodDf.drop(index)
    
    # Filter only floods from  January 2016 to November 2025
    floodDf = floodDf[floodDf["YEAR"] >= 2016]
    floodDf = floodDf[~((floodDf["YEAR"] == 2025) & (floodDf["MONTH"] == 12))]

    # Convert DATE/TIME column to datetime.date format
    floodDf["DATE"] = pandas.to_datetime(floodDf["DATE"], format='mixed').dt.date

    goodColumns = ["DATE", "CITY", "FLOOD"]

    # Drop unnecessary columns
    for i in floodDf.columns:
        if i not in goodColumns:
            floodDf = floodDf.drop(i, axis=1)

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