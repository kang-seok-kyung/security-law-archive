import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import json
import time
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from datetime import datetime

# ===== 설정 =====
BASE_URL = "https://www.boannews.com"
START_URL = "https://www.boannews.com/search/news_hash.asp?find=%BB%E7%B0%C7%BB%E7%B0%ED"
HEADERS = {"User-Agent": "Mozilla/5.0"}
RAW_SAVE = "boan_news_raw.json"
SUMMARY_SAVE = "boan_news_summarized.json"

# ===== 추정 가능한 한국 법률 목록 =====
import torch

LAW_LIST = [
    "개인정보보호법",
    "정보통신망법",
    "통신비밀보호법",
    "정보보호산업법",
    "전자금융거래법",
    "사이버보안기본법(안)",
    "국가정보화기본법"
]

# 예시 가중치 사전 (키워드: {법률: 가중치})
KEYWORD_WEIGHTS = {
    # 개인정보보호법 관련
    "개인정보 유출": {"개인정보보호법": 0.25},
    "개인정보": {"개인정보보호법": 0.15},
    "주민등록번호": {"개인정보보호법": 0.2},
    "고객 정보": {"개인정보보호법": 0.2},
    "이름, 주소": {"개인정보보호법": 0.1},
    "휴대전화번호": {"개인정보보호법": 0.15},
    "의료 정보": {"개인정보보호법": 0.25},
    "유출 사고": {"개인정보보호법": 0.15},
    "유출": {
        "개인정보보호법": 0.20,
        "정보통신망법": 0.10,
        "국가정보화기본법": 0.10
    },

    # 정보통신망법 관련
    "해킹": {"정보통신망법": 0.2, "통신비밀보호법": 0.15},
    "랜섬웨어": {"정보통신망법": 0.25, "사이버보안기본법(안)": 0.2},
    "디도스": {"정보통신망법": 0.2, "사이버보안기본법(안)": 0.15},
    "DDoS": {
        "사이버보안기본법(안)": 0.25,
        "정보통신망법": 0.15,
        "정보통신기반보호법": 0.15
    },
    "백도어": {"정보통신망법": 0.2},
    "웹쉘": {"정보통신망법": 0.15},
    "악성코드": {"정보통신망법": 0.2},

    # 통신비밀보호법 관련
    "감청": {"통신비밀보호법": 0.25},
    "도청": {"통신비밀보호법": 0.25},
    "패킷 분석": {"통신비밀보호법": 0.2},
    "트래픽 가로채기": {"통신비밀보호법": 0.2},

    # 전자금융거래법 관련
    "전자금융": {"전자금융거래법": 0.25},
    "금융 사고": {"전자금융거래법": 0.15},
    "피싱": {"전자금융거래법": 0.25, "정보통신망법": 0.15},
    "스미싱": {
        "개인정보보호법": 0.15,
        "전자금융거래법": 0.20,
        "통신비밀보호법": 0.10
    },
    "계좌 탈취": {"전자금융거래법": 0.2},
    "OTP": {"전자금융거래법": 0.15},
    "가상자산": {"전자금융거래법": 0.15},
    "결제": {
        "전자금융거래법": 0.20,
        "전자문서 및 전자거래 기본법": 0.15,
        "개인정보보호법": 0.10
    },
    "금융": {
        "전자금융거래법": 0.25,
        "개인정보보호법": 0.10
    },
    "금융정보": {
        "전자금융거래법": 0.20,
        "개인정보보호법": 0.15,
        "신용정보의이용및보호에관한법률": 0.20
    },

    # 사이버보안기본법(안) 관련
    "사이버 공격": {"사이버보안기본법(안)": 0.2},
    "보안 취약점": {"사이버보안기본법(안)": 0.15},
    "제로데이": {"사이버보안기본법(안)": 0.2},
    "APT": {"사이버보안기본법(안)": 0.2},
    "침해 사고": {"사이버보안기본법(안)": 0.2},
    "C2 서버": {"사이버보안기본법(안)": 0.2},

    # 국가정보화기본법 관련
    "국가 정보": {"국가정보화기본법": 0.15},
    "행정망": {"국가정보화기본법": 0.2},
    "공공기관 시스템": {"국가정보화기본법": 0.2},

    # 정보보호산업법 관련
    "보안 솔루션": {"정보보호산업법": 0.15},
    "정보보호 제품": {"정보보호산업법": 0.15},
    "보안 기업": {"정보보호산업법": 0.15},

    # 기타 키워드
    "인증서 탈취": {"전자금융거래법": 0.2, "정보통신망법": 0.15},
    "디지털 증명서": {"전자금융거래법": 0.15},
    "딥페이크": {
        "정보통신망법": 0.20,
        "통신비밀보호법": 0.10,
        "개인정보보호법": 0.15
    },
    "도박 사이트": {
        "정보통신망법": 0.20,
        "사이버보안기본법(안)": 0.15
    }
}

def apply_keyword_weights(text, base_probs):
    scores = base_probs.clone()
    text_lower = text.lower()
    
    triggered_keywords = set()

    for keyword, law_weights in KEYWORD_WEIGHTS.items():
        if keyword in text_lower:
            triggered_keywords.add(keyword)

    for keyword in triggered_keywords:
        for law, weight in KEYWORD_WEIGHTS[keyword].items():
            if law in LAW_LIST:
                idx = LAW_LIST.index(law)
                scores[idx] += weight

    total = scores.sum().item()
    if total > 0:
        scores /= total
    else:
        scores = base_probs

    return scores

def classify_laws(text, tokenizer, model, top_k=1, threshold=0.1):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        base_probs = torch.softmax(outputs.logits, dim=1)[0]
    
    # 키워드 가중치 반영 및 정규화
    weighted_probs = apply_keyword_weights(text, base_probs)

    # 가장 높은 확률의 법률 하나 추출
    top_index = weighted_probs.argmax().item()
    top_prob = weighted_probs[top_index]
    
    if top_prob > threshold:
        return LAW_LIST[top_index]
    else:
        return "미분류"

# ===== 뉴스 리스트 수집 =====
def get_article_list(page=1):
    url = f"{START_URL}&Page={page}"
    resp = requests.get(url, headers=HEADERS, verify=False)
    resp.encoding = 'euc-kr'
    soup = BeautifulSoup(resp.text, 'html.parser')
    articles = []
    for item in soup.select("div.news_list"):
        title = item.select_one("span.news_txt")
        date = item.select_one("span.news_writer")
        link = item.select_one("a[href^='/media/view.asp']")
        if title and date and link:
            # 원본: "기자명 | 2024년 10월 28일 13:39"
            raw_date = date.get_text(strip=True).split('|')[-1].strip()
            try:
                parsed_date = datetime.strptime(raw_date, "%Y년 %m월 %d일 %H:%M")
                formatted_date = parsed_date.strftime("%Y.%m.%d")
            except ValueError:
                # 예외 발생 시 원본 그대로 사용
                formatted_date = raw_date
            articles.append({
                "title": title.get_text(strip=True),
                "date": formatted_date,
                "uri": urljoin(BASE_URL, link['href']),
            })
    return articles

# ===== 뉴스 본문 수집 =====
def get_article_content(url):
    try:
        res = requests.get(url, headers=HEADERS, verify=False)
        res.encoding = "euc-kr"
        soup = BeautifulSoup(res.text, "html.parser")
        content_div = soup.select_one("div#news_content")
        if content_div:
            content = content_div.get_text(separator="\n").strip()
        else:
            print(f"[!] 본문 태그가 없습니다: {url}")
            content = ""
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
    return content

# ===== 전체 뉴스 수집 =====
def crawl_boannews(pages=2):
    all_articles = []
    for page in range(1, pages+1):
        print(f"\n📄 Fetching Page {page}")
        articles = get_article_list(page)
        for article in tqdm(articles, desc="📥 Downloading Articles"):
            content = get_article_content(article['uri'])
            article["content"] = content
            time.sleep(0.1)
        all_articles.extend(articles)
    return all_articles

# ===== KoBART 요약기 =====
def load_summarizer():
    tokenizer = PreTrainedTokenizerFast.from_pretrained("digit82/kobart-summarization")
    model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")
    return tokenizer, model

def summarize(text, tokenizer, model):
    input_ids = tokenizer.encode(text[:1024], return_tensors="pt", truncation=True)
    summary_ids = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# ===== 법률 분류기 로딩 =====
def load_law_classifier():
    tokenizer = BertTokenizer.from_pretrained("klue/roberta-base")
    model = BertForSequenceClassification.from_pretrained("klue/roberta-base", num_labels=len(LAW_LIST))
    model.eval()
    return tokenizer, model

# ===== 메인 파이프라인 =====
def main():
    print("🚀 보안뉴스 수집 및 AI 요약/법률 분석 시작")
    
    # 1. 뉴스 수집
    news_data = crawl_boannews(pages=4)
    with open(RAW_SAVE, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 뉴스 원문 {len(news_data)}건 저장: {RAW_SAVE}")

    # 2. 요약기/법률 분류기 로드
    tokenizer_kobart, model_kobart = load_summarizer()
    law_tokenizer, law_model = load_law_classifier()

    # 3. 처리
    summarized = []
    print("\n✍ 요약 및 법률 추출 중...")
    for article in tqdm(news_data):
        summary = summarize(article["content"], tokenizer_kobart, model_kobart)
        laws = classify_laws(article["content"], law_tokenizer, law_model)
        summarized.append({
            "title": article["title"],
            "date": article["date"],
            "uri": article["uri"],
            "summary": summary,
            "related_laws": laws
        })

    # 4. 저장
    with open(SUMMARY_SAVE, "w", encoding="utf-8") as f:
        json.dump(summarized, f, ensure_ascii=False, indent=2)
    print(f"🎉 최종 요약 및 법률 분석 결과 저장 완료: {SUMMARY_SAVE}")

if __name__ == "__main__":
    main()