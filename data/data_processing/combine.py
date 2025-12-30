import pandas
import numpy

def combine(cities, output_path):
    for i in range(len(cities)):
        meteoFilepath = "../processed/meteorological_" + cities[i] + ".csv"
        hydroFilepath = "../processed/hydrological_" + cities[i] + ".csv"
        floodFilepath = "../processed/floods/Indonesia floods 2008-2025.csv"
        meteoDf = pandas.read_csv(meteoFilepath)
        hydroDf = pandas.read_csv(hydroFilepath)
        floodDf = pandas.read_csv(floodFilepath)

        meteoCombined = pandas.concat([hydroDf, meteoDf], axis=1, ignore_index=True)
        newColumns = ["DATE", "SM_ROOTZONE", "SM_SURFACE", "PRECTOTCORR",
                      "T2M", "T2M_MAX", "T2M_MIN", "QV2M", "RH2M", "WS10M", "PS"]
        meteoCombined.columns = newColumns
        meteoCombined["CITY"] = cities[i][0:1].capitalize() + cities[i][1:]

        floodDf["CITY"] = floodDf["CITY"].replace(["Bandung Barat", "Kota Bandung"], "Bandung")
        floodDf["CITY"] = floodDf["CITY"].replace(["Kota Bogor"], "Bogor")
        floodDf["CITY"] = floodDf["CITY"].replace(["Kota Adm. Jakarta Utara", "Kota Adm. Jakarta Barat",
                                                   "Kota Adm. Jakarta Pusat", "Kota Adm. Jakarta Selatan",
                                                   "Kota Adm. Jakarta Timur"], "Jakarta")
        floodDf["CITY"] = floodDf["CITY"].replace(["Kota Palembang"], "Palembang")
        floodDf["CITY"] = floodDf["CITY"].replace(["Kota Semarang"], "Semarang")

        mergedDf = meteoCombined.merge(floodDf, on=["DATE", "CITY"], how="left")
        mergedDf["FLOOD"] = numpy.where(mergedDf["FLOOD"] == True, 1, 0)

        mergedDf.to_csv(output_path + cities[i] + ".csv", index=False)

def make_master(cities):
    masterDf = pandas.read_csv("../processed/combined/" + cities[0] + ".csv")
    for i in range(1, len(cities), 1):
        cityDf = pandas.read_csv("../processed/combined/" + cities[i] + ".csv")
        masterDf = pandas.concat([masterDf, cityDf], axis=0, ignore_index=True)
    masterDf.to_csv("../processed/combined/master_dataset.csv", index = False)

def main():
    combinedPath = "../processed/combined/"
    cities = ["bandung",
              "bogor",
              "jakarta",
              "palembang",
              "pandeglang",
              "semarang"]
    combine(cities, combinedPath)
    make_master(cities)

main()
