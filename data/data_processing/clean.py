import pandas

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

def hydroCleaning(inputFile, outputFile):
    hydroDf = pandas.read_csv(inputFile)
    hydroDf = hydroDf[hydroDf["date"] >= "2016-01-01"]

    hydroDf = hydroDf.drop("system:index", axis=1)
    hydroDf = hydroDf.drop(".geo", axis=1)

    hydroDf.to_csv(outputFile, index=False)

def main():
    cities = ["bandung", "bogor", "jakarta", "palembang", "pandeglang", "semarang"]

    for i in range(len(cities)):
        meteoInputFile = "../raw/meteorological/" + cities[i] + "_2015.csv"
        hydroInputFile = "../raw/hydrological/sm_" + cities[i] + ".csv"

        meteoOutputFile = "../processed/meteorological_" + cities[i] + ".csv"
        hydroOutputFile = "../processed/hydrological_" + cities[i] + ".csv"

        meteoCleaning(meteoInputFile, meteoOutputFile)
        hydroCleaning(hydroInputFile, hydroOutputFile)

main()