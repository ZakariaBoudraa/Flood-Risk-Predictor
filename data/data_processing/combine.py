import requests
import csv

def combining():
    cities = ["bandung",
            "bogor",
            "jakarta",
            "palembang",
            "pandeglang",
            "semarang"]

    for i in range(len(cities)):
        meteoFilepath = cities[i] + "_2015.csv"
        hydroFilepath = "sm_daily_" + cities[i] + ".csv"
        meteoData = csv.reader(open(meteoFilepath, "r"))
        hydroData = csv.reader(open(hydroFilepath, "r"))


def main():
    combinedFile = "../processed/combined_file"
    combining(combinedFile)