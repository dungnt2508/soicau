import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np


# import datetime

def get_db():
    """
    Configuration method to return db instance
    """
    db = None
    APP_DB_URI = 'mongodb+srv://dungnt196:25Tuananh08@1stcluster17032020.dabsg.azure.mongodb.net/test?retryWrites=true&w=majority'
    APP_DB_NAME = 'snake_bot'
    if db is None:
        db = pymongo.MongoClient(
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
db = get_db()


def min_max_normalize(dice):
    """chuẩn hóa data"""
    lst = [1, 2, 3, 4, 5, 6]
    minimum = min(lst)
    maximum = max(lst)
    normalized = [(i - minimum) / (maximum - minimum) for i in lst]
    return normalized[dice - 1]


def write_csv(year, month, day):
    """get data theo ngay
        out to csv
    """
    pipeline_bydate_get = "[{'$project':{'_id': 0, 'id_phien': 1, 'xx1':1, 'xx2': 1, 'xx3': 1, 'rs_number': 1, 'bs': 1, 'date_created': {'$dateFromString':{'dateString':'$date_created','format':'%d/%m/%Y %H:%M:%S'}}   }}, {'$match': {'$expr': {'$and':[{'$eq':[{'$year':'$date_created'}," + str(
        year) + "]},{'$eq':[{'$month':'$date_created'}, " + str(
        month) + "]},{'$eq':[{'$dayOfMonth':'$date_created'}," + str(day) + "]}]}   }}]"
    # print(pipeline_bydate_get)
    data = list(db.sicbomd5.aggregate(eval(pipeline_bydate_get)))
    """get list 4 phien"""
    id_last_2 = []
    xx1_last_2 = []
    xx2_last_2 = []
    xx3_last_2 = []

    id_last_1 = []
    xx1_last_1 = []
    xx2_last_1 = []
    xx3_last_1 = []

    id_current = []
    xx1_current = []
    xx2_current = []
    xx3_current = []

    id_next = []
    xx1_next = []
    xx2_next = []
    xx3_next = []
    rs_number_next = []
    for i in range(len(data[0:-4])):
        id_last_2.append(data[0:-4][i]["id_phien"])
        xx1_last_2.append(min_max_normalize(data[0:-4][i]["xx1"]))
        xx2_last_2.append(min_max_normalize(data[0:-4][i]["xx2"]))
        xx3_last_2.append(min_max_normalize(data[0:-4][i]["xx3"]))

        id_last_1.append(data[1:-3][i]["id_phien"])
        xx1_last_1.append(min_max_normalize(data[1:-3][i]["xx1"]))
        xx2_last_1.append(min_max_normalize(data[1:-3][i]["xx2"]))
        xx3_last_1.append(min_max_normalize(data[1:-3][i]["xx3"]))

        id_current.append(data[2:-2][i]["id_phien"])
        xx1_current.append(min_max_normalize(data[2:-2][i]["xx1"]))
        xx2_current.append(min_max_normalize(data[2:-2][i]["xx2"]))
        xx3_current.append(min_max_normalize(data[2:-2][i]["xx3"]))

        id_next.append(data[3:-1][i]["id_phien"])
        xx1_next.append(min_max_normalize(data[3:-1][i]["xx1"]))
        xx2_next.append(min_max_normalize(data[3:-1][i]["xx2"]))
        xx3_next.append(min_max_normalize(data[3:-1][i]["xx3"]))
        rs_number_next.append(0 if data[3:-1][i]["rs_number"] < 11 else 1)

    df = pd.DataFrame(
        data={"id_last_2": id_last_2, "xx1_last_2": xx1_last_2, "xx2_last_2": xx2_last_2, "xx3_last_2": xx3_last_2,
              "id_last_1": id_last_1, "xx1_last_1": xx1_last_1, "xx2_last_1": xx2_last_1, "xx3_last_1": xx3_last_1,
              "id_current": id_current,
              "xx1_current": xx1_current, "xx2_current": xx2_current, "xx3_current": xx3_current, "id_next": id_next,
              "xx1_next": xx1_next, "xx2_next": xx2_next, "xx3_next": xx3_next, "rs_number_next": rs_number_next})
    df.to_csv('sicbomd5_{}{}{}.csv'.format(day, month, year), index=False)
    print("done")


def last_id_phien_get():
    """ get data cuoi cung"""
    # data = list(db.sicbomd5.aggregate([{"$sort": {"_id": -1}}, {"$limit": 3}]))
    # print(data)
    # cur_xx1 = data[0]["xx1"]
    # cur_xx2 = data[0]["xx2"]
    # cur_xx3 = data[0]["xx3"]
    # last_xx1 = data[1]["xx1"]
    # last_xx2 = data[1]["xx2"]
    # last_xx3 = data[1]["xx3"]
    # last2_xx1 = data[2]["xx1"]
    # last2_xx2 = data[2]["xx2"]
    # last2_xx3 = data[2]["xx3"]
    cur_xx1 = 6
    cur_xx2 = 6
    cur_xx3 = 3
    last_xx1 = 6
    last_xx2 = 6
    last_xx3 = 3
    last2_xx1 = 2
    last2_xx2 = 3
    last2_xx3 = 5
    lst_cur_dice = [min_max_normalize(cur_xx1), min_max_normalize(cur_xx2), min_max_normalize(cur_xx3)]
    lst_last_dice = [min_max_normalize(last_xx1), min_max_normalize(last_xx2), min_max_normalize(last_xx3)]
    lst_last_dice_2 = [min_max_normalize(last2_xx1), min_max_normalize(last2_xx2), min_max_normalize(last2_xx3)]

    return {"lst_cur_dice": lst_cur_dice, "lst_last_dice": lst_last_dice, "lst_last_dice_2": lst_last_dice_2}


# write_csv()

def sicbomd5_predict():
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
    print(model.score(train_features, train_labels))

    # Score the model on the test data
    print(model.score(test_features, test_labels))

    data_current = last_id_phien_get()

    lst_cur_dice = data_current["lst_cur_dice"]
    lst_last_dice = data_current["lst_last_dice"]
    lst_last_dice_2 = data_current["lst_last_dice_2"]

    SoiCau = np.array(lst_cur_dice + lst_last_dice + lst_last_dice_2)

    combined_arrays = np.array([SoiCau])

    Phan = scaler.transform(combined_arrays)
    predict = model.predict(Phan)
    predict_proba = model.predict_proba(Phan)
    print(predict)



# write_csv(year=2021, month=10, day=3)
# print(last_id_phien_get())
# sicbomd5_predict()


a = [7,6,5,4,3,2,1]
a.sort()
print(a)