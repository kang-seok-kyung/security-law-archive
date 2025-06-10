from db import db
from config import COLLECTION_NAME2

cases_col = db[COLLECTION_NAME2]

def get_all_cases():
    return list(cases_col.find({}, {"_id": 0}))

def get_case_by_id(case_id):
    return cases_col.find_one({"_id": case_id})