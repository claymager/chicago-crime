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
from sklearn.svm import SVC
import warnings
warnings.filterwarnings("ignore")

# local imports
from queries import *
from model_test import ModelTest
from feature_processing import process_features

# SETTINGS
target = 'primary_type'
features_sql = "latitude, longitude, datetime, domestic"
    # also location_desc?

def get_models():
    """
    Returns a list of models for testing
    """
    dummies = [ DummyClassifier(strategy=s)
                for s in ["stratified", "most_frequent"]]

    trees = [ BaggingClassifier(n_estimators=50, max_features = 2, n_jobs = 3 )
                for d in range(14,25,1)] 

    knns = [ KNeighborsClassifier(n_neighbors=n, metric="manhattan", n_jobs=3)
                for n in range(80,150,9)]

    svcs = [ SVC(gamma=10**a) for a in range(-4,4) ] + \
           [ SVC(C=10**a) for a in range(-4,4) ]


    logs = [ LogisticRegression(n_jobs=2, solver="sag", tol=0.1)]

    return trees
    return dummies + knns + logs + svcs + trees

def get_id(filename = "model_results.csv"):
    """
    gets id for next model
    used for usably concattenating logs
    """
    try:
        f = open(filename, "r")
        for line in f:
            pass
        f.close()
        return int(line.split(",")[0])+1
    except (FileNotFoundError, UnboundLocalError) as e:
        return 0

def get_data():
    """
    Retrieves data ready for modeling
    (X_train, X_test, y_train, y_test)
    """
    Xs_raw, ys = get_data_from_sql(target, features_sql)
    Xs = Xs_raw[["latitude", "longitude", "domestic"]].join( 
            process_features(Xs_raw, hour_method="hcyclic",
            month_method="hcyclic") ) 

    X_train_us, X_test_us, y_train, y_test = \
            train_test_split(Xs, ys, random_state=4)
    ssc = StandardScaler()
    X_train = ssc.fit_transform(X_train_us)
    X_test = ssc.transform(X_test_us)

    return X_train, X_test, y_train, y_test

def main():
    data = get_data()
    first_id = get_id()
    models = get_models()

    for i in range(len(models)):
        m = models.pop(0)
        test = ModelTest(m, *data, id_=first_id+i)
        
        test.log()
        del m 
        del test

if __name__ == "__main__":
    main()
