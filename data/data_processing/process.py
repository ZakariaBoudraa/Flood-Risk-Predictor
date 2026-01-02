import pandas
import numpy

def data_stats(data):
    count = data["FLOOD"].value_counts(normalize=False)
    mean = data.groupby("CITY")["FLOOD"].mean()
    missingValues = data.isna().mean()
    return count, mean, missingValues

def check_imp_values(data):
    ranges = {"SM_ROOTZONE": (0, 1), "SM_SURFACE": (0, 1), "PRECTOTCORR": (0, 500), "T2M_MAX": (-50, 60),
               "T2M_MIN": (-50, 60), "QV2M": (0, 40), "RH2M": (0, 100), "WS10M": (0, 70), "PS": (80, 120)}
    for feature, (min, max) in ranges.items():
        for index, value in data[feature].items():
            if value < min or value > max:
                print(f"Impossible value in {feature} at line {index}: {value}")

def create_rolling_features(data):
    data["PRECTOTCORR_1d"] = data.groupby("CITY")["PRECTOTCORR"].shift(1)
    data["PRECTOTCORR_3d"] = data.groupby("CITY")["PRECTOTCORR"].shift(1).rolling(3).sum()
    data["PRECTOTCORR_7d"] = data.groupby("CITY")["PRECTOTCORR"].shift(1).rolling(7).sum()
    data["PRECTOTCORR_14d"] = data.groupby("CITY")["PRECTOTCORR"].shift(1).rolling(14).sum()

    data["SM_ROOTZONE_3d_MEAN"] = data.groupby("CITY")["SM_ROOTZONE"].shift(1).rolling(3).mean()
    data["SM_SURFACE_3d_MEAN"] = data.groupby("CITY")["SM_SURFACE"].shift(1).rolling(3).mean()

    data["SM_ROOTZONE_7d_MEAN"] = data.groupby("CITY")["SM_ROOTZONE"].shift(1).rolling(7).mean()
    data["SM_SURFACE_7d_MEAN"] = data.groupby("CITY")["SM_SURFACE"].shift(1).rolling(7).mean()

    data["FLOOD_IN_LAST_30d"] = data.groupby("CITY")["FLOOD"].shift(1).rolling(30).max().fillna(0).astype(int)

def process(data):
    data = data.sort_values(["CITY", "DATE"])
    data["FLOOD TOMORROW"] = (data.groupby("CITY")["FLOOD"].shift(-1))
    data = data.dropna(subset=["FLOOD TOMORROW"])
    data["FLOOD TOMORROW"] = data["FLOOD TOMORROW"].astype(int)

    create_rolling_features(data)

    data["PRECTOTCORR_1d_CHANGE"] = data.groupby("CITY")["PRECTOTCORR"].diff()
    data["SM_ROOTZONE_1d_CHANGE"] = data.groupby("CITY")["SM_ROOTZONE"].diff()
    data["SM_SURFACE_1d_CHANGE"] = data.groupby("CITY")["SM_SURFACE"].diff()

    data["DAY_OF_YEAR"] = pandas.to_datetime(data["DATE"], format="mixed").dt.dayofyear
    data["DOFY_SINE"] = numpy.sin((2 * numpy.pi + data["DAY_OF_YEAR"]) / 365.25)
    data["DOFY_COSINE"] = numpy.cos((2 * numpy.pi + data["DAY_OF_YEAR"]) / 365.25)

    data = data.dropna().reset_index(drop=True)

    data["CITY_CODE"] = data["CITY"].astype("category").cat.codes

def main():
    floodFile = pandas.read_csv("../processed/combined/master_dataset.csv")

    [count, mean, missingValues] = data_stats(floodFile)
    print(count, mean, missingValues)

    check_imp_values(floodFile)
    process(floodFile)

main()