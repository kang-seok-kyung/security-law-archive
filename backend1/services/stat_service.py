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

def count_cases_by_year():
    result = defaultdict(int)
    for doc in col_case.find({}, {"date": 1}):
        year = str(doc.get("date", "")[:4])
        if year:
            result[year] += 1
    return dict(result)