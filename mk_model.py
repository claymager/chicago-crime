#!/bin/python3
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import numpy as np
import json
import pickle

import warnings
warnings.filterwarnings("ignore")

from feature_processing import process_features
from queries import get_data_from_sql

# Settings
model = RandomForestClassifier(max_depth=18, n_estimators=150, n_jobs = 3)
     
model_str = "forestsmote"
target = "index_crime"
out_dir = "static/"
model_name = model_str + "_for_" + target

features_sql = "latitude, longitude, datetime, loc_desc"
hour_method = "hcyclic"
month_method = "mcyclic"

# Setup
Xs_raw, ys = get_data_from_sql(target, features_sql)
Xs = Xs_raw[["latitude", "longitude"]].join( 
        process_features(Xs_raw, hour_method=hour_method,
                        month_method=month_method)    )

X_train_us, X_test_us, y_train, y_test = \
        train_test_split(Xs, ys, random_state=4)#stratify=ys)
ssc = StandardScaler()
X_train = ssc.fit_transform(X_train_us)
X_test = ssc.transform(X_test_us)
X_all = ssc.transform(Xs)
sos = SMOTE(ratio="minority")
X_train, y_train = sos.fit_sample(X_train, y_train)
X_all, ys = sos.fit_sample(X_all, ys)

# Stats generation
model.fit(X_train, np.ravel(y_train))
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

stats = { "accuracy": accuracy_score(y_test, test_predictions)}
stats["test/train acc"] = stats["accuracy"] / accuracy_score(y_train, train_predictions) 
stats["precision"], stats["recall"], stats["f1"], stats["support"] = \
        precision_recall_fscore_support(y_test, test_predictions)
for k, v in stats.items():
    if type(v) != np.ndarray:
        continue
    stats[k] = v.tolist()

with open(out_dir + "stats/" + model_name + ".json", 'w') as statsfile:
    statsfile.write( json.dumps(stats) ) 

# Final model
model.fit(X_all, np.ravel(ys))

with open(out_dir + "models/" + model_name + ".pkl", "wb") as picklefile:
    pickle.dump(model, picklefile)

with open(out_dir + "models/" + model_name + "_scaler.pkl", "wb") as picklefile:
    pickle.dump(ssc, picklefile)

plt.figure(dpi=350)
sns.heatmap(confusion_matrix(y_test, test_predictions))
plt.savefig(out_dir + "plots/" + model_name + ".png")

