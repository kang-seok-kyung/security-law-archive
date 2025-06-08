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

# 예시 가중치 사전 (키워드: {법률: 가중치})
KEYWORD_WEIGHTS = {
    # 개인정보보호법
    "개인정보": {"개인정보보호법": 0.2},
    "유출": {"개인정보보호법": 0.15},
    "정보": {"개인정보보호법": 0.1},
    "주민등록번호": {"개인정보보호법": 0.2},
    "이름": {"개인정보보호법": 0.15},
    "주소": {"개인정보보호법": 0.15},
    "휴대전화번호": {"개인정보보호법": 0.15},
    "의료 정보": {"개인정보보호법": 0.1},

    # 정보통신망이용촉진및정보보호등에관한법률 (정보통신망법)
    "디도스": {"정보통신망이용촉진및정보보호등에관한법률": 0.25},
    "바이러스": {"정보통신망이용촉진및정보보호등에관한법률": 0.20},
    "웹쉘": {"정보통신망이용촉진및정보보호등에관한법률": 0.15},
    "해킹": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.30,
    "정보통신기반보호법": 0.15,
    "개인정보보호법": 0.10
    },
    "악성코드": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.20,
    "정보통신기반보호법": 0.15
    },
    "랜섬웨어": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.25,
    "정보통신기반보호법": 0.15,
    "개인정보보호법": 0.10
    },


    # 정보통신기반보호법
    "정보통신기반": {"정보통신기반보호법": 0.30},
    "서버 장애": {"정보통신기반보호법": 0.20},
    "네트워크 장애": {"정보통신기반보호법": 0.20},

    # 신용정보의이용및보호에관한법률
    "신용정보": {"신용정보의이용및보호에관한법률": 0.30},
    "신용카드": {"신용정보의이용및보호에관한법률": 0.20},
    "대출정보": {"신용정보의이용및보호에관한법률": 0.20},

    # 전자정부법
    "전자정부": {"전자정부법": 0.30},
    "행정망": {"전자정부법": 0.20},

    # 통신비밀보호법
    "감청": {"통신비밀보호법": 0.30},
    "도청": {"통신비밀보호법": 0.30},
    "통신 감청": {"통신비밀보호법": 0.25},

    # 전자금융거래법
    "전자금융": {"전자금융거래법": 0.30},

    # 지능정보화 기본법
    "인공지능": {"지능정보화 기본법": 0.30},
    "빅데이터": {"지능정보화 기본법": 0.25},
    "지능정보": {"지능정보화 기본법": 0.20},

    # 전자문서 및 전자거래 기본법
    "전자문서": {"전자문서 및 전자거래 기본법": 0.30},
    "전자거래": {"전자문서 및 전자거래 기본법": 0.30},
    "온라인 거래": {"전자문서 및 전자거래 기본법": 0.20},

    # 국가보안법
    "국가보안": {"국가보안법": 0.30},
    "국가 기밀": {"국가보안법": 0.25},
    "국가안보": {"국가보안법": 0.20},

    # 부정경쟁방지 및 영업비밀보호에 관한 법률
    "영업비밀": {"부정경쟁방지 및 영업비밀보호에 관한 법률": 0.30},
    "부정경쟁": {"부정경쟁방지 및 영업비밀보호에 관한 법률": 0.25},
    "기술 유출": {"부정경쟁방지 및 영업비밀보호에 관한 법률": 0.25},

    # 국가정보화 기본법
    "국가정보화": {"국가정보화 기본법": 0.30},
    "공공기관 정보": {"국가정보화 기본법": 0.25},

    # 전자서명법
    "전자서명": {"전자서명법": 0.30},
    "인증서": {"전자서명법": 0.25},
    "공인인증서": {"전자서명법": 0.20},

    # 중복 법률 적용 예시 (추가)
    "데이터 유출": {"개인정보보호법": 0.15, "정보통신망이용촉진및정보보호등에관한법률": 0.15},
    "정보 보호": {"개인정보보호법": 0.1, "정보통신망이용촉진및정보보호등에관한법률": 0.1},
    "네트워크 공격": {"정보통신망이용촉진및정보보호등에관한법률": 0.25, "정보통신기반보호법": 0.20},
    "계좌정보": {"신용정보의이용및보호에관한법률": 0.20, "전자금융거래법": 0.20},

    "사이버 공격": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.30,
    "정보통신기반보호법": 0.25
    },
    "딥페이크": {
        "지능정보화 기본법": 0.30,
        "개인정보보호법": 0.20
    },
    "결제": {
        "전자금융거래법": 0.30,
        "신용정보의이용및보호에관한법률": 0.25
    },
    "업데이트 문제": {
        "정보통신기반보호법": 0.25,
        "전자정부법": 0.20
    },
    "DDoS": {
        "정보통신망이용촉진및정보보호등에관한법률": 0.30
    },
    "악성 앱": {
        "정보통신망이용촉진및정보보호등에관한법률": 0.25,
        "개인정보보호법": 0.20
    },
    "금융정보": {
        "신용정보의이용및보호에관한법률": 0.30,
        "전자금융거래법": 0.25
    },
    "피싱": {
    "전자금융거래법": 0.25,
    "개인정보보호법": 0.15,
    "정보통신망이용촉진및정보보호등에관한법률": 0.15
    },
    "스미싱": {
    "전자금융거래법": 0.20,
    "개인정보보호법": 0.15,
    "정보통신망이용촉진및정보보호등에관한법률": 0.15
    },
    "계좌 탈취": {
    "전자금융거래법": 0.25,
    "개인정보보호법": 0.10
    },
    "금융사기": {
    "전자금융거래법": 0.25,
    "정보통신망이용촉진및정보보호등에관한법률": 0.10
    },
    "몸캠": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.25,
    "개인정보보호법": 0.20,
    "전자금융거래법": 0.15
    },
    "영상 유포": {
    "정보통신망이용촉진및정보보호등에관한법률": 0.25,
    "개인정보보호법": 0.15
    },
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

def classify_laws(text, tokenizer, model, top_k=3, threshold=0.08, gap_threshold=0.05):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        base_probs = torch.softmax(outputs.logits, dim=1)[0]
    
    weighted_probs = apply_keyword_weights(text, base_probs)
    print("최종 가중치:", weighted_probs.tolist())

    # 상위 top_k 인덱스와 확률 추출
    top_probs, top_indices = torch.topk(weighted_probs, top_k)

    # 최고 확률값 기준으로 gap_threshold 이하인 법률 모두 포함
    max_prob = top_probs[0].item()
    selected_laws = []
    for prob, idx in zip(top_probs, top_indices):
        if prob.item() >= threshold and (max_prob - prob.item()) <= gap_threshold:
            selected_laws.append((LAW_LIST[idx], prob.item()))

    if not selected_laws:
        return ["미분류"]
    
    # 법률 이름만 반환
    return [law for law, prob in selected_laws]

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
    summary_ids = model.generate(
        input_ids,
        max_length=128,
        min_length=30,
        num_beams=4,
        length_penalty=1.2,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def remove_duplicate_sentences(text):
    sentences = list(dict.fromkeys(text.split('다.')))  # 문장 기준 중복 제거
    return '다.'.join([s.strip() for s in sentences if s.strip()]) + '다.'

# ===== 법률 분류기 로딩 =====
def load_law_classifier():
    tokenizer = BertTokenizer.from_pretrained("klue/roberta-base")
    model = BertForSequenceClassification.from_pretrained("klue/roberta-base", num_labels=len(LAW_LIST))
    model.eval()
    return tokenizer, model

# ===== 메인 파이프라인 =====
def main():
    print("보안뉴스 수집 및 AI 요약/법률 분석 시작")
    
    # 1. 뉴스 수집
    news_data = crawl_boannews(pages=10)
    with open(RAW_SAVE, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"뉴스 원문 {len(news_data)}건 저장: {RAW_SAVE}")

    # 2. 요약기/법률 분류기 로드
    tokenizer_kobart, model_kobart = load_summarizer()
    law_tokenizer, law_model = load_law_classifier()

    # 3. 처리
    summarized = []
    print("\n요약 및 법률 추출 중...")
    for article in tqdm(news_data):
        clean_text = remove_duplicate_sentences(article["content"])
        summary = summarize(clean_text, tokenizer_kobart, model_kobart)
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
    print(f"최종 요약 및 법률 분석 결과 저장 완료: {SUMMARY_SAVE}")

if __name__ == "__main__":
    main()