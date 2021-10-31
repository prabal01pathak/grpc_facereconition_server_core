import pymysql
import os
import pymongo
import time
import yaml

with open('project.yaml', 'r') as f:
    doc = yaml.load(f,Loader=yaml.FullLoader)


config = {
    "username": "root",
    "password": "Secret",
    "server": "mongo",
}
connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
try:
    client = pymongo.MongoClient(connector)
    print("DB connection sucessfull ")
except:
    print("DB connection un sucessfull....")



#client = pymongo.MongoClient("mongodb+srv://suraj258:suraj258@cluster0.a1dx7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
Sensitivity= doc["settings"]["sensitivity"]
Model_Type= doc["settings"]["model_Type"]

Number_of_times_to_upsample= doc["settings"]["upsample"]


BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
UPLOAD_PATH=os.path.abspath(os.path.join(BASE_DIRECTORY,'uploads'))

# try:
#     # Open database connection
#     DB = pymysql.connect(host='localhost', user='root', password='',port=3306)
#     #create database
#     DB.cursor().execute('create database faceginis')
# except:
#     DB = pymysql.connect(host='localhost', user='root', password='',database='faceginis' ,port=3306)
#     #create database
#     #db.cursor().execute('create database faceginis')


