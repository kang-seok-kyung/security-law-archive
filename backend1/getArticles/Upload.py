import json
import pymongo
import os
import sys

# backend/config.py 불러오기 위한 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config  # backend/config.py에서 Mongo 설정 import

def replace_json_in_mongodb(json_path, collection_name):
    # MongoDB 클라이언트 연결
    client = pymongo.MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    collection = db[collection_name]

    # 기존 컬렉션 데이터 전부 삭제
    delete_result = collection.delete_many({})
    print(f"[초기화] 기존 문서 {delete_result.deleted_count}개 삭제 완료")

    # 새 데이터 삽입
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print(f"[완료] {len(data)}개 문서를 '{collection_name}' 컬렉션에 새로 저장했습니다.")

if __name__ == "__main__":
    # 예시: summarized_news.json → cases 컬렉션에 전체 덮어쓰기
    replace_json_in_mongodb("summarized_news.json", config.COLLECTION_NAME2)
