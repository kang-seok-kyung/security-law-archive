from datetime import datetime

def extract_year(date_str):
    """
    'YYYY.MM.DD' 형식의 날짜 문자열에서 연도(int)만 추출.
    실패하면 None 반환.
    """
    try:
        return datetime.strptime(date_str, "%Y.%m.%d").year
    except:
        return None