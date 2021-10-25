import pymysql
import os
import pymongo
import time
import pyaml

client = pymongo.MongoClient("mongodb://localhost:27017/")
Sensitivity=0.8
Model_Type="cnn"

Number_of_times_to_upsample=3


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
