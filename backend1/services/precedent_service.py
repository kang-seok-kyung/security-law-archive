from db import db
from config import COLLECTION_NAME

collection = db[COLLECTION_NAME]


def insert_precedents(data_list):
    for doc in data_list:
        collection.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)


def find_by_title(keyword):
    results = list(collection.find({
        "title": {"$regex": keyword, "$options": "i"}
    }).limit(20))

    for r in results:
        r["_id"] = str(r["_id"])
    return results
