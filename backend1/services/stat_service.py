from db import db
from config import COLLECTION_NAME1, COLLECTION_NAME2
from collections import defaultdict

col_prec = db[COLLECTION_NAME1]
col_case = db[COLLECTION_NAME2]

def count_precedents_by_year():
    result = defaultdict(int)
    for doc in col_prec.find({}, {"date": 1}):
        year = str(doc.get("date", "")[:4])
        if year.isdigit() and int(year) >= 1900:
            result[year] += 1
    return dict(result)

def count_cases_by_law():
    result = defaultdict(int)
    for doc in col_case.find({}, {"related_laws": 1}):
        laws = doc.get("related_laws", [])
        if isinstance(laws, str):
            laws = [laws]
        for law in laws:
            result[law] += 1
    return dict(result)