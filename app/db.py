import requests
from flask import current_app, g, session, jsonify
from werkzeug.local import LocalProxy
import pymongo
from bson import json_util
import json
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.write_concern import WriteConcern
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.read_concern import ReadConcern
import certifi
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np

from .models import User


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    APP_DB_URI = current_app.config["APP_DB_URI"]
    APP_DB_NAME = current_app.config["APP_NS"]
    if db is None:
        db = g._database = pymongo.MongoClient(
            APP_DB_URI,
            # username="root",
            # password="abcd1234",
            maxPoolSize=50,  # Set the maximum connection pool size to 50 active connections.
            w='majority',  # Set the write timeout limit to 2500 milliseconds.
            wtimeout=2500
            # ,
            # ssl_ca_certs=certifi.where()
        )[APP_DB_NAME]
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_user(email):
    if "google_id" in session:
        return User(session["email"], session["name"], '')
    else:
        user = db.users.find_one({'email': email})
        return User(user['email'], user['fullname'], user['password']) if user else None


def save_user(User):
    db.users.insert_one(User)


def get_lastid():
    result, msg, items = ('0', None, {})
    uri = "https://api-go-88-somjv.ondigitalocean.app/go88/"

    try:
        # resp = requests.get(uri)
        # if resp.status_code != 200:
        #     msg = '{}'.format(resp.status_code)
        data = json.loads(json_util.dumps((db.sicbomd5.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))))

        items['last_items'] = data[0] if data else []
        # items['total_items'] = data
        # lst_chart = []
        # for i in items['total_items']:
        #     lst_chart.append([int(i['id_phien']), i['rs_number']])
        # items['lst_chart'] = lst_chart
        # print(items)

        msg = 'get done'
        result = '1'
    except Exception as e:
        print(e)
        result, msg = ('0', str(e))

    return jsonify(items), 200


def get_predict_sicbomd5(type):
    result, msg, items = ('0', None, {})
    uri = "https://api-go-88-somjv.ondigitalocean.app/go88/"
    data = None

    try:
        if type == 1:
            data = pd.read_csv('sicbomd5_2102021.csv')  # read csv file
        if type == 2:
            data = pd.read_csv('sicbomd5_3102021.csv')  # read csv file

        features = data[[
            'xx1_current', 'xx2_current', 'xx3_current',
            'xx1_last_1', 'xx2_last_1', 'xx3_last_1',
            'xx1_last_2', 'xx2_last_2', 'xx3_last_2'
        ]]
        labels = data[['rs_number_next']]

        # training data
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels)

        scaler = StandardScaler()
        train_features = scaler.fit_transform(train_features)
        test_features = scaler.transform(test_features)

        # Create and train the model
        model = LogisticRegression()
        model.fit(train_features, train_labels)

        # Score the model on the train data
        # print(model.score(train_features, train_labels))

        # Score the model on the test data
        # print(model.score(test_features, test_labels))

        data_current = last_id_phien_get()
        # print(data_current)

        lst_cur_dice = data_current["lst_cur_dice"]
        lst_last_dice = data_current["lst_last_dice"]
        lst_last_dice_2 = data_current["lst_last_dice_2"]

        SoiCau = np.array(lst_cur_dice + lst_last_dice + lst_last_dice_2)

        combined_arrays = np.array([SoiCau])

        Phan = scaler.transform(combined_arrays)
        items['predict'] = "Tài" if int(model.predict(Phan)[0]) == 1 else "Xỉu"
        items['msg'] = "SnakeBot dự đoán phiên #{} là {}".format((int(data_current["id_phien_cur"])+1), items["predict"])
        predict_proba = model.predict_proba(Phan)
        print(items)

    except Exception as e:
        print(e)
        result, msg = ('0', str(e))

    return jsonify(items), 200

def min_max_normalize(dice):
    """chuẩn hóa data"""
    lst = [1, 2, 3, 4, 5, 6]
    minimum = min(lst)
    maximum = max(lst)
    normalized = [(i - minimum) / (maximum - minimum) for i in lst]
    return normalized[dice - 1]


def last_id_phien_get():
    """ get data cuoi cung"""
    data = list(db.sicbomd5.aggregate([{"$sort": {"_id": -1}}, {"$limit": 3}]))
    # print(data)
    lst_cur_dice = [min_max_normalize(data[0]["xx1"]), min_max_normalize(data[0]["xx2"]), min_max_normalize(data[0]["xx3"])]
    lst_last_dice = [min_max_normalize(data[1]["xx1"]), min_max_normalize(data[1]["xx2"]), min_max_normalize(data[1]["xx3"])]
    lst_last_dice_2 = [min_max_normalize(data[2]["xx1"]), min_max_normalize(data[2]["xx2"]), min_max_normalize(data[2]["xx3"])]

    return {"id_phien_cur": data[0]["id_phien"], "lst_cur_dice": lst_cur_dice, "lst_last_dice": lst_last_dice, "lst_last_dice_2": lst_last_dice_2}