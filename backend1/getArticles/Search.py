import requests
import json
import random
from datetime import datetime
from newspaper import Article
from html import unescape
import re
import time

# 네이버 API 인증 정보
CLIENT_ID = 'UB1qHeQaFgZufKcwAsb7'
CLIENT_SECRET = '6CmWWur5bw'

# 검색어 관련 설정
SEARCH_QUERIES = [
    "사이버 보안 사고", "개인정보 유출", "해킹 사건", "랜섬웨어 감염",
    "DDoS 공격", "정보보호 침해", "사이버 공격 사례", "보안 사고 사례"
]
DISPLAY_PER_PAGE = 100
MAX_RESULTS = 1000

# 표현 패턴 기반 필터링 추가
SECURITY_KEYWORDS = ['해킹', '개인정보', '유출', 'DDoS', '랜섬웨어', '사이버 공격', '보안 취약점', '정보보호']
INCIDENT_PATTERNS = ['사고', '유출', '공격', '피해', '감염', '조사 중', '조사에 착수', '벌금', '피해 규모', '사건', '사건이 발생']

def is_real_incident(text):
    # 보안 키워드 + 사건성 표현 둘 다 포함된 경우만 True
    return any(k in text for k in SECURITY_KEYWORDS) and any(p in text for p in INCIDENT_PATTERNS)



def naver_news_search(query, display=100, start=1):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': 'sim'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}")
        return None

def clean_html(text):
    text = re.sub('<.*?>', '', text)
    return unescape(text)

def extract_article_text(url):
    try:
        article = Article(url, language='ko')
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"[본문 추출 실패] {url} → {e}")
        return ""

def is_security_incident(text):
    return any(keyword in text for keyword in SECURITY_KEYWORDS)

def format_date(pub_date_str):
    try:
        dt = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%Y-%m-%d')
    except:
        return pub_date_str



def extract_article_title(url):
    try:
        article = Article(url, language='ko')
        article.download()
        article.parse()
        return article.title.strip()
    except Exception as e:
        print(f"[타이틀 추출 실패] {url} → {e}")
        return None

def crawl_news(n=100):
    all_items = []

    for query in SEARCH_QUERIES:
        starts = list(range(1, MAX_RESULTS + 1, DISPLAY_PER_PAGE))
        random.shuffle(starts)
        for start_pos in starts:
            data = naver_news_search(query, DISPLAY_PER_PAGE, start_pos)
            if data and 'items' in data:
                for item in data['items']:
                    news = {
                        'title': clean_html(item['title']),
                        'date': format_date(item['pubDate']),
                        'uri': item['link']
                    }
                    all_items.append(news)
            time.sleep(0.2)
            if len(all_items) > n * 3:
                break

    # 중복 제거
    all_items = list({item['uri']: item for item in all_items}.values())
    random.shuffle(all_items)

    # 본문 파싱 및 필터링
    filtered_news = []
    for item in all_items:
        content = extract_article_text(item['uri'])
        if is_real_incident(content):
            item['content'] = content
            filtered_news.append(item)
        if len(filtered_news) >= n:
            break

    return filtered_news

def save_to_json(data, filename='filtered_news.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    N = 100  # 기본 수량
    news = crawl_news(N)
    save_to_json(news)
    print(f"[완료] {len(news)}개의 보안 사고 관련 뉴스를 저장했습니다.")