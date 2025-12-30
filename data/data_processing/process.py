import pandas
import numpy

def check():
    data = pandas.read_csv("../processed/combined/master_dataset.csv")
    data = data.sort_values(["CITY", "DATE"])

    print(data["FLOOD"].value_counts(normalize=False))
    print(data.groupby("CITY")["FLOOD"].mean())

    print(data.isna().mean())

check()