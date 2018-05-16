#!/run/current-system/sw/bin/python
from flask import Flask, render_template, abort, request
import pandas as pd
import numpy as np
import json
import pickle

from queries import get_loc_desc
from feature_processing import process_features

loc_descs = [loc for loc in get_loc_desc()["loc_desc"] if loc]
models = dict()
def load_model(modelname):
    if modelname not in models.keys():
        models[modelname] = dict()
        with open("static/models/"+modelname+".pkl", "rb") as picklefile:
            models[modelname]["model"] = pickle.load(picklefile)
        with open("static/stats/"+modelname+".json", "r") as jsonfile:
            models[modelname]["stats"] = jsonfile.read()
        with open("static/models/"+modelname+"_scaler.pkl", "rb") as picklefile:
            models[modelname]["ssc"] = pickle.load(picklefile)


app = Flask(__name__)
app.debug = True

def testable_record(record):
    """
    Takes input dictionary
    Returns features pd.DataFrame ready for scaling in model.
    (hard-coded, not generizable!)
    """
    record["latitude"] = float(record["latitude"])
    record["longitude"] = 0-float(record["longitude"])
    temp_df = pd.DataFrame(record, index=range(2))
    temp_df["loc_desc"][0] = "ABANDONED BUILDING" # So drop_first works
    temp_df["datetime"] = pd.to_datetime(temp_df["datetime"])
    temp_df = temp_df[["latitude","longitude"]].join(process_features(temp_df, "hcyclic","mcyclic"))
    with open("empty_df.pkl","rb") as picklefile:
        empty_df = pickle.load(picklefile)
    temp_df = temp_df.combine_first(empty_df)
    temp_df = temp_df[empty_df.columns]
    return temp_df.iloc[1].reshape(1,-1)

@app.route("/model/<modelname>", methods=["POST"])
def foo(modelname):
    if not request.json:
        abort(400)
    # loading pklfiles takes a while. try memoizing.
    # not recommended if large numbers of models are available.
    dummyname = "dummy_"+"_".join(modelname.split("_")[1:])
    load_model(modelname)
    load_model(dummyname)


    model = models[modelname]["model"]
    stats = models[modelname]["stats"]
    ssc = models[modelname]["ssc"]

    record_dict = request.json
    X = ssc.transform( testable_record(record_dict) )
    prediction = model.predict(X)

    response = json.loads(stats)
    response["dummy_accuracy"] = json.loads(models[dummyname]["stats"])["accuracy"]
    response["prediction"] = str(prediction[0])
    response["proba"] = model.predict_proba(X).tolist()
    print(response,"\n\n\n")
    return json.dumps(response), 200



@app.route("/")
def index():
    return render_template("index.html", options=loc_descs)

if __name__ == "__main__":
    app.run()
