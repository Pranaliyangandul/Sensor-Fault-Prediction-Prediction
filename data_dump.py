import pymongo
import pandas as pd
import json
import os
# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"))

DATA_FILE_PATH=r"aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")
    print(df)
    # #Convert dataframe to json so that we can dump these record in mongo db
    df.reset_index(drop=True,inplace=True)
    # print(df.T.to_json())
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # #insert converted json record to mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)