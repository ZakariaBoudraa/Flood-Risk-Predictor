import pandas
import csv

def combine(cities, output_path):
    for i in range(len(cities)):
        meteoFilepath = "../processed/meteorological_" + cities[i] + ".csv"
        hydroFilepath = "../processed/hydrological_" + cities[i] + ".csv"
        floodFilepath = "../processed/flood.csv"
        meteoDf = pandas.read_csv(meteoFilepath)
        hydroDf = pandas.read_csv(hydroFilepath)
        floodDf = pandas.read_csv(floodFilepath)

        meteoCombined = pandas.concat([hydroDf, meteoDf], axis=1, ignore_index=True)
        newColumns = ["DATE", "SM_ROOTZONE", "SM_SURFACE", "PRECTOTCORR",
                      "T2M", "T2M_MAX", "T2M_MIN", "QV2M", "RH2M", "WS10M", "PS"]
        meteoCombined.columns = newColumns
        meteoCombined["CITY"] = cities[i]

        mergedDf = meteoCombined.merge(floodDf, on=["DATE", "CITY"], how="left")

        for row in mergedDf.iterrows():
            if (row["FLOOD"] == True):
                row["FLOOD"] = 1
            row["FLOOD"] = 0

        mergedDf.to_csv(output_path + cities[i] + ".csv", index=False)

def main():
    combinedPath = "../processed/combined/"
    cities = ["bandung",
              "bogor",
              "jakarta",
              "palembang",
              "pandeglang",
              "semarang"]
    combine(cities, combinedPath)

main()
