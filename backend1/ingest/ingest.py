from services.precedent_service import insert_precedents
import requests

API_BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do"
OC_ID = "sk6461"

SECURITY_LAWS = ["개인정보보호법",
        "정보통신망이용촉진및정보보호등에관한법률",
        "정보통신기반보호법",
        "신용정보의이용및보호에관한법률",
        "전자정부법",
        "통신비밀보호법",
        "전자금융거래법",
        "지능정보화 기본법",
        "전자문서 및 전자거래 기본법",
        "국가보안법",
        "부정경쟁방지 및 영업비밀보호에 관한 법률",
        "국가정보화 기본법",
        "전자서명법"]

def fetch_by_jo(jo):
    all_data = []
    page = 1
    while True:
        params = {
            "OC": OC_ID,
            "target": "prec",
            "type": "JSON",
            "JO": jo,
            "search": 2,
            "display": 100,
            "page": page
        }
        res = requests.get(API_BASE_URL, params=params)
        if res.status_code != 200:
            break
        data = res.json()
        precs = data.get("PrecSearch", {}).get("prec", [])

        # ⚠️ 방어: precs가 리스트가 아니면 중단
        if not isinstance(precs, list):
            print(f"[⚠️] {jo} - prec 응답이 list가 아님: {precs}")
            break

        for p in precs:
            all_data.append({
                "id": p.get("판례일련번호"),
                "jo": [jo],
                "title": p.get("사건명"),
                "case_number": p.get("사건번호"),
                "court": p.get("법원명", ""),
                "category": p.get("사건종류명", ""),
                "date": p.get("선고일자", ""),
                "url": "https://www.law.go.kr" + p.get("판례상세링크", "")
            })

        if len(precs) < 100:
            break
        page += 1
    return all_data

if __name__ == "__main__":
    for law in SECURITY_LAWS:
        data = fetch_by_jo(law)
        insert_precedents(data)
        print(f"[✔] {law} 기준 {len(data)}건 저장 완료")