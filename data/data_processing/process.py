import pandas
import numpy

def compute(data):
    count = data["FLOOD"].value_counts(normalize=False)
    mean = data.groupby("CITY")["FLOOD"].mean()
    missingValues = data.isna().mean()
    return count, mean, missingValues

def process(data):
    data = data.sort_values(["CITY", "DATE"])
    data["FLOOD TOMORROW"] = (data.groupby("CITY")["FLOOD"].shift(-1))
    data = data.dropna(subset=["FLOOD TOMORROW"])
    data["FLOOD TOMORROW"] = data["FLOOD TOMORROW"].astype(int)

def main():
    data = pandas.read_csv("../processed/combined/master_dataset.csv")
    [count, mean, missingValues] = compute(data)
    print(count)
    print(mean)
    print(missingValues)

main()