import pandas as pd
import os,sys
from dataclasses import dataclass
import pymongo

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    # mongo_db_url="mongodb+srv://pranaliyangandul:Pranali912@cluster0.uwafxej.mongodb.net/?retryWrites=true&w=majority"

env_var = EnvironmentVariable()
print("url..",env_var.mongo_db_url)
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"