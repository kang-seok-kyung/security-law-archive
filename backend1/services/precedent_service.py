from db import db
from config import COLLECTION_NAME1

col = db[COLLECTION_NAME1]

def insert_precedents(data):
    for doc in data:
        existing = col.find_one({"id": doc["id"]})
        if existing:
            existing_jo = existing.get("jo", [])
            new_jo = doc.get("jo", [])
            merged_jo = list(set(existing_jo + new_jo))
            doc["jo"] = merged_jo
        col.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)

def find_by_laws(laws):
    return list(col.find({"jo": {"$in": laws}}, {"_id": 0}))

def find_by_id(precedent_id):
    return col.find_one({"id": precedent_id}, {"_id": 0})