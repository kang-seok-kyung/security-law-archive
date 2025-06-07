import json
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch
import re

# 요약 모델 및 토크나이저 로딩 (KoBART)
tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

# 위반법률 키워드 기반 매핑 (정규표현식 기반으로 정교화)
LAW_PATTERNS = {
    # 개인정보보호법 위반
    r"(개인정보.*(유출|노출|침해|무단|도용))": "개인정보보호법",
    r"(주민등록번호|신용카드|고객정보|성명|연락처).*유출": "개인정보보호법",
    r"개인정보보호법.*위반": "개인정보보호법",

    # 정보통신망법 위반
    r"(정보통신망.*(무단|침해|해킹|도용))": "정보통신망법",
    r"정보통신망법.*위반": "정보통신망법",
    r"(랜섬웨어|DDoS|해킹|악성코드).*공격": "정보통신망법",
    r"사이버 공격.*대상": "정보통신망법",
    
    # 전자금융거래법
    r"(계좌|카드|이체|송금|인출).*사기": "전자금융거래법",
    r"(전자금융거래법.*위반)": "전자금융거래법",
    
    # 형법 일반 (불법 침입/업무방해 등)
    r"(불법.*접근|무단.*침입|업무방해|자료 훼손)": "형법",
    r"(형법.*위반)": "형법"
}


def summarize_article(content, max_input_length=1024):
    if not content:
        return "요약 실패"
    input_ids = tokenizer.encode(
        content,
        return_tensors='pt',
        max_length=max_input_length,
        truncation=True
    )
    summary_ids = model.generate(
        input_ids,
        max_length=120,
        min_length=80,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)



def extract_laws(text):
    matched = set()
    for pattern, law in LAW_PATTERNS.items():
        if re.search(pattern, text):
            matched.add(law)
    
    # 아무 것도 매칭되지 않았을 경우
    if not matched:
        matched.add("법률 미상")
    
    return list(matched)



def summarize_and_save(input_file='filtered_news.json', output_file='summarized_news.json'):
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)

    summarized_data = []
    for item in news_items:
        content = item.get('content', '')
        summary = summarize_article(content)
        laws = extract_laws(content + ' ' + summary)

        summarized_data.append({
            'title': item['title'],
            'date': item['date'],
            'uri': item['uri'],
            'summary': summary,
            'law': laws
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summarized_data, f, ensure_ascii=False, indent=2)

    print(f"[완료] {len(summarized_data)}개 뉴스 요약 및 법률 추출 완료")


if __name__ == "__main__":
    summarize_and_save()
