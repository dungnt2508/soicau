import requests
from flask import current_app, g, session, jsonify
from werkzeug.local import LocalProxy
import pymongo
import json
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.write_concern import WriteConcern
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.read_concern import ReadConcern
import certifi

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
            wtimeout=2500,
            ssl_ca_certs=certifi.where()
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


def get_predict_sicbomd5():
    result, msg, items = ('0', None, {})
    uri = "https://api-go-88-somjv.ondigitalocean.app/go88/"

    try:
        resp = requests.get(uri)
        if resp.status_code != 200:
            msg = '{}'.format(resp.status_code)
        if msg is None:
            items['last_items'] = json.loads(resp.text)[-1] if json.loads(resp.text) else []
            items['total_items'] = json.loads(resp.text)
            lst_chart = []
            for i in items['total_items']:
                if i['id_phien']:
                    if 'G' not in i['id_phien']:
                        lst_chart.append([int(i['id_phien']), i['rs_number']])
            items['lst_chart'] = lst_chart
            msg = 'get done'
            result = '1'
    except Exception as e:
        result, msg = ('0', str(e))

    return jsonify(items), 200
