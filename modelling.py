#!/run/current-system/sw/bin/python
import psycopg2 as pg
import numpy as np
import pandas as pd
import pandas.io.sql as pd_sql
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.svm import LinearSVC
import warnings
warnings.filterwarnings("ignore")

# local imports
from queries import *
from model_test import ModelTest

# SETTINGS
target = 'primary_type'
features_sql = """
      latitude
    , longitude
    , extract (month FROM datetime) AS month
    , extract (dow FROM datetime) AS dow
    , domestic
    -- ,location_desc
    """

features = ["latitude"
           , "longitude"
           , "month"
           , "dow"
           , "domestic"
           ]

def get_models():
    """
    Returns a list of models for testing
    """
    trees = [RandomForestClassifier(n_estimators=250, max_depth=d, n_jobs = 3 )
                for d in range(10,25,1)] 

    knns =  [KNeighborsClassifier(n_neighbors=n, metric="manhattan", n_jobs=3)
                for n in range(80,150,9)]

    logs = [LogisticRegression(n_jobs=3, dual=False),
            LogisticRegression(n_jobs=2, solver="sag"),
            LogisticRegression(n_jobs=2, solver="sag", tol=0.1)]

    return trees + knns + logs

def process_features(Xs):
    print(Xs.columns)
    return(Xs)

# BOILERPLATE
def get_last_id(filename = "model_results.csv"):
    f = open(filename, "r")
    for line in f:
        pass
    f.close()
    return int(line.split(",")[0])

def main():
    # Data retrieval and feature engineering
    Xs, ys = get_data_from_sql(target, features_sql)
    Xs = process_features(Xs) 

    # Train-test split
    X_train_us, X_test_us, y_train, y_test = \
            train_test_split(Xs, ys, random_state=4)

    # Preprocessing
    ssc = StandardScaler()
    X_train = ssc.fit_transform(X_train_us)
    X_test = ssc.transform(X_test_us)
    
    data_tuple = (X_train, X_test, y_train, y_test)
    first_id = get_last_id() + 1
    models = get_models()

    for i, m in enumerate(models):
        test = ModelTest(m, *data_tuple, id_ =  first_id + i)
        test.log()
        print(test._to_csv())

if __name__ == "__main__":
    main()
