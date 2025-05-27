import requests
from services.precedent_service import insert_precedents

API_BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do"
OC_ID = "sk6461"

def fetch_and_store(query):
    params = {
        "OC": OC_ID,
        "target": "prec",
        "type": "JSON",
        "query": query,
        "search": 2,
        "display": 100,
        "sort": "ddes"
    }

    response = requests.get(API_BASE_URL, params=params)

    try:
        data = response.json()
    except Exception as e:
        print(f"[❌] API 응답 파싱 실패: {e}")
        return

    prec_list = data.get("PrecSearch", {}).get("prec", [])

    if not prec_list:
        print(f"[⚠️] '{query}' 키워드로 검색된 판례 없음")
        return

    cleaned_data = []
    for prec in prec_list:
        cleaned_data.append({
            "id": prec.get("판례일련번호"),
            "query": query,
            "title": prec.get("사건명"),
            "case_number": prec.get("사건번호"),
            "court": prec.get("법원명", ""),
            "category": prec.get("사건종류명", ""),
            "date": prec.get("선고일자", ""),
            "url": "https://www.law.go.kr" + prec.get("판례상세링크", "")
        })

    insert_precedents(cleaned_data)
    print(f"[✔] '{query}' 키워드로 {len(cleaned_data)}건 저장 완료")

# ✅ 단독 실행 시 작동
if __name__ == "__main__":
    fetch_and_store("보안")
