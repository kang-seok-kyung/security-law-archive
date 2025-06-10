
# 🛡️ Security Law Archive

**Security Law Archive**는 보안 및 개인정보 보호 관련 법률 위반 사례와 판례 정보를 수집·검색하고 시각화할 수 있는 웹 애플리케이션입니다.

---

## 📁 프로젝트 구조

- `backend1/`: Flask 기반 백엔드 서버 (API, MongoDB 연동, 기사 수집 및 판례 데이터 처리)
- `frontend/`: 사용자 인터페이스(React 또는 기타 프레임워크 예정)
- `README.md`, `CONTRIBUTING.md`: 프로젝트 소개 및 기여 지침

---

## 🚀 주요 기능

- 보안/개인정보 관련 기사 수집 및 요약
- 판례 및 위반 사례 검색 API
- 통계 시각화 API
- MongoDB 기반 데이터 저장

---

## 🔧 실행 방법

### 백엔드 실행 (Flask)

```bash
cd backend1
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 프론트엔드 실행 (React 기준)

```bash
cd frontend
npm install
npm start
```

> ⚠️ 프론트엔드 실행 전 `.env` 파일에 백엔드 API 주소를 설정하세요. 예시:
>
> ```
> REACT_APP_API_URL=http://localhost:5000
> ```

---

## 📡 API 예시

- `GET /api/cases`
- `GET /api/precedents`
- `GET /api/stats`

---

## 🧑‍💻 기여 방법

1. `CONTRIBUTING.md` 참고
2. 기능별 브랜치 생성 후 Pull Request
3. 커밋 메시지는 명확하게 작성
