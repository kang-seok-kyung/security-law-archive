# 🤝 Contributing Guidelines

이 문서는 우리 팀 프로젝트에서 효율적이고 깔끔한 협업을 위해 작성되었습니다. 모든 팀원은 아래 가이드라인을 따라주세요.

---

## 🧑‍💻 팀원이 처음 해야 할 일

1. GitHub 초대 수락 후 레포지토리 접근
2. 아래 명령어로 레포지토리 클론
   ```bash
   git clone https://github.com/kang-seok-kyung/security-law-archive.git
   cd security-law-archive
   ```
3. main 브랜치 최신 상태로 가져오기
   ```bash
   git checkout main
   git pull origin main
   ```
4. 기능 개발용 브랜치 생성
   ```bash
   git checkout -b feature/front-login  # 예시
   ```
5. 작업 후 커밋 및 원격 저장소로 푸시
   ```bash
   git add .
   git commit -m "feat(front): 로그인 페이지 구현"
   git push origin feature/front-login
   ```
6. GitHub에서 Pull Request 생성 및 리뷰 요청

---

## 📁 디렉토리 구조

```
📁 frontend/         # 프론트엔드 소스코드
📁 backend/          # 백엔드 소스코드
📄 README.md
📄 CONTRIBUTING.md
```

---

## 🪄 브랜치 전략

- ⚠️ **절대 main 브랜치에 직접 push하지 마세요.** 모든 작업은 브랜치를 생성하여 Pull Request를 통해 병합해야 합니다.

- **main**: 항상 배포/제출 가능한 안정 버전 유지
- 기능 작업은 반드시 새로운 브랜치에서 수행합니다.

### 브랜치 네이밍 규칙

```
feature/front-기능명     # 프론트엔드 기능 개발
feature/back-기능명      # 백엔드 기능 개발
fix/front-버그명         # 프론트엔드 버그 수정
fix/back-버그명          # 백엔드 버그 수정
docs/문서명              # 문서 작성/수정
```

### 브랜치 생성 예시

```bash
git checkout main
git pull origin main
git checkout -b feature/front-login
```

---

## 💬 커밋 컨벤션

> 형식: `type(scope): 내용`

### 주요 타입

- `feat`: 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 작성/수정
- `style`: 코드 포맷팅, 세미콜론 등 비기능적 수정
- `refactor`: 리팩토링
- `test`: 테스트 코드
- `chore`: 설정, 패키지, 빌드 설정 등

### 예시

```bash
git commit -m "feat(front): 로그인 페이지 구현"
git commit -m "fix(back): 로그인 시 JWT 오류 수정"
git commit -m "docs: README 실행 방법 추가"
```

---

## 🔀 PR(Pull Request) 규칙

- 브랜치 작업 완료 후 PR 생성
- PR 제목 컨벤션: `[type/파트] 작업 요약`
- PR 본문에 작업 내용, 변경 파일, 기타 참고사항 등을 작성
- PR은 **Merge 전 팀원 1명 이상의 승인(Approve)이 필요**합니다.

### PR 본문 예시

```md
## 작업 내용
- 로그인 UI 구성
- 이메일, 비밀번호 입력 필드 추가

## 변경된 파일
- src/pages/Login.jsx
- src/components/InputField.jsx

## 기타
- submit 기능은 추후 구현 예정입니다.
```

### 제목 예시

```
[feat/front] 로그인 폼 UI 구성
[fix/back] 토큰 만료 오류 수정
```

---
