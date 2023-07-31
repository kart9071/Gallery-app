from pymongo import MongoClient

DATABASE_NAME='admin'
try:
    client=MongoClient('localhost',27017)
    db=client[DATABASE_NAME]
    print("Database connected successfully")
except Exception as e:
    print(f"client error:{e}")
