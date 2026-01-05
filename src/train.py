import pandas
import pickle
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score
from model import get_model
from features import (CAT_FEATURES, NUM_FEATURES, TARGET_FEATURE)

def evaluate(train, prob):
    prediction = (prob > 0.5).astype(int)
    print("Prediction accuracy: " + accuracy_score(train, prediction))
    print("F1 Score (Harmonic mean): " + f1_score(train, prediction))
    print("ROC AUC: " + roc_auc_score(train, prob))
    print("PR AUC: " + average_precision_score(train, prob))

def train():
    masterFile = "../data/processed/combined/master_dataset.csv"
    dataset = pandas.read_csv(masterFile)
    features = CAT_FEATURES + NUM_FEATURES + TARGET_FEATURE

    trainData = dataset[dataset["DATE"] < "2022-01-01"]
    tuningData = dataset[(dataset["DATE"] >= "2022-01-01") & (dataset["DATE"] < "2024-01-01")]
    testData = dataset[dataset["DATE"] >= "2024-01-01"]

    X_train, y_train = trainData[features], trainData["FLOOD_TOMORROW"]
    X_tuning, y_tuning = tuningData[features], tuningData["FLOOD_TOMORROW"]
    X_test, y_test = testData[features], testData["FLOOD_TOMORROW"]

    model = get_model(dataset, NUM_FEATURES, CAT_FEATURES)
    model.fit(X_train, y_train)

    y_prob_train = model.predict_proba(X_train)[:, 1]
    print("Train evaluation: ")
    evaluate(y_train, y_prob_train)

    y_prob_tuning = model.predict_proba(X_tuning)[:, 1]
    print("Tuning evaluation: ")
    evaluate(y_tuning, y_prob_tuning)

    y_prob_test = model.predict_proba(X_test)[:, 1]
    print("Test evaluation: ")
    evaluate(y_test, y_prob_test)

    return model

def main():
    model = train()
    pickleFile = open("model.pkl", "wb")
    pickle.dump(model, pickleFile)

if __name__ == "__main__":
    main()