from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

def get_model(dataset, numericData, categoricalData):

    categorical_transformer = Pipeline([
        ("fill_missing", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder())
    ])

    transformData = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, categoricalData),
            ("impute", SimpleImputer(strategy="median"), numericData)
    ])

    model = Pipeline([
        ("transform", transformData),
        ("model", RandomForestClassifier(
            n_estimators=350, random_state=10, n_jobs=1, class_weight="balanced"
        ))
    ])

    return model