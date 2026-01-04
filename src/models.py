import pandas
import numpy
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

def build_pipeline(dataset, ):
    completeFile = "../data/processed/combined/master_dataset.csv"
    dataset = pandas.read_csv(completeFile)

    # city_code = ColumnTransformer(
    #     transformers=[
    #         ("city_code", OneHotEncoder(), dataset)
    #     ]
    # )

    trainData = dataset[dataset["DATE"] < "2022-01-01"]
    validationData = dataset[(dataset["DATE"] >= "2022-01-01") & (dataset["DATE"] < "2024-01-01")]
    testData = dataset[dataset["DATE"] >= "2024-01-01"]

    X_train, y_train = trainData[features], trainData["FLOOD_TOMORROW"]
    X_validation, y_validation = validationData[features], validationData["FLOOD_TOMORROW"]
    X_test, y_test = testData[features], testData["FLOOD_TOMORROW"]

    model = Pipeline([
        ("randomForest", RandomForestClassifier(
        n_estimators=350, random_state=10, n_jobs=1, class_weight="balanced")),
        ()
    ])












