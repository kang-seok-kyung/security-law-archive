import requests
from services.precedent_service import insert_precedents

API_BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do"
OC_ID = "sk6461"

def fetch_all_by_jo(jo):
    all_data = {}  # key: 판례 id, value: 판례 dict
    page = 1
    while True:
        params = {
            "OC": OC_ID,
            "target": "prec",
            "type": "JSON",
            "JO": jo,
            "display": 100,
            "page": page
        }

        response = requests.get(API_BASE_URL, params=params)
        if response.status_code != 200:
            print(f"[❌] '{jo}' 요청 실패 (status code: {response.status_code})")
            break

        try:
            data = response.json()
        except Exception as e:
            print(f"[❌] '{jo}' 응답 JSON 파싱 오류: {e}")
            break

        prec_list = data.get("PrecSearch", {}).get("prec", [])

        if isinstance(prec_list, dict):
            prec_list = [prec_list]
        elif not isinstance(prec_list, list):
            print(f"[⚠️] '{jo}'의 판례 응답 형식 오류 → prec_list = {prec_list}")
            break

        for prec in prec_list:
            pid = prec.get("판례일련번호")
            if pid is None:
                continue

            if pid not in all_data:
                all_data[pid] = {
                    "id": pid,
                    "jo": [jo],
                    "title": prec.get("사건명"),
                    "case_number": prec.get("사건번호"),
                    "category": prec.get("사건종류명", ""),
                    "date": prec.get("선고일자", ""),
                    "url": "https://www.law.go.kr" + prec.get("판례상세링크", "")
                }
            else:
                if jo not in all_data[pid]["jo"]:
                    all_data[pid]["jo"].append(jo)

        if len(prec_list) < 100:
            break

        page += 1

    return list(all_data.values())

def collect_security_laws():
    security_laws = [
        "개인정보보호법",
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
        "전자서명법"
    ]

    all_precedents = {}

    for jo in security_laws:
        data = fetch_all_by_jo(jo)
        for p in data:
            pid = p["id"]
            if pid not in all_precedents:
                all_precedents[pid] = p
            else:
                # 기존 jo 리스트에 새 jo 병합
                for j in p["jo"]:
                    if j not in all_precedents[pid]["jo"]:
                        all_precedents[pid]["jo"].append(j)

        print(f"[✔] '{jo}' 기준으로 {len(data)}건 수집 완료")

    insert_precedents(list(all_precedents.values()))
    print(f"[✅] 총 {len(all_precedents)}건 저장 완료")

if __name__ == "__main__":
    collect_security_laws()
