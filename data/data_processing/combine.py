import pandas
import csv

def combine(output_path):
    cities = ["bandung",
            "bogor",
            "jakarta",
            "palembang",
            "pandeglang",
            "semarang"]

    for i in range(len(cities)):
        meteoFilepath = "../processed/meteorological_" + cities[i] + ".csv"
        hydroFilepath = "../processed/hydrological_" + cities[i] + ".csv"
        meteoDf = pandas.read_csv(meteoFilepath)
        hydroDf = pandas.read_csv(hydroFilepath)

        combinedDf = pandas.concat([hydroDf, meteoDf], axis=1, ignore_index=True)

        newColumns = ["DATE", "SM_ROOTZONE", "SM_SURFACE", "PRECTOTCORR",
                      "T2M", "T2M_MAX", "T2M_MIN", "QV2M", "RH2M", "WS10M", "PS"]
        combinedDf.columns = newColumns

        combinedDf.to_csv(output_path + cities[i] + ".csv", index=False)

def main():
    combinedPath = "../processed/combined/"
    combine(combinedPath)

main()
