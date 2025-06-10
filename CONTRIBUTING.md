
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

---

## 🪄 브랜치 전략

- ⚠️ **절대 main 브랜치에 직접 push하지 마세요.**
- 작업은 `frontend` 또는 `backend` 브랜치에서 수행합니다.
- 각 파트의 작업이 완료되면 `dev` 브랜치로 merge합니다 (PR 없이 직접 병합 가능).
- `main` 브랜치에는 **오직 dev → main 병합 시에만 PR을 생성**합니다.

### 브랜치 구성

- `main`: 항상 배포/제출 가능한 안정 버전 유지
- `dev`: frontend, backend 브랜치를 통합한 테스트 브랜치
- `frontend`: 프론트엔드 작업 브랜치
- `backend`: 백엔드 작업 브랜치

---

## 💬 커밋 컨벤션

> **지금은 형식보다 "무엇을 했는지 명확하게 작성하는 것"이 중요합니다.**

- 권장 형식: `type(scope): 내용`

### 주요 타입 예시

- `feat`: 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 작성/수정
- `style`: 포맷팅 등 비기능적 수정
- `refactor`: 리팩토링
- `test`: 테스트 코드
- `chore`: 설정, 빌드 설정 등

### 커밋 메시지 예시

```bash
git commit -m "feat(front): 검색창 컴포넌트 구현"
git commit -m "fix(back): JWT 인증 오류 수정"
git commit -m "docs: README 실행 방법 업데이트"
```

---

## 🔀 PR(Pull Request) 규칙

- `main` 브랜치로 병합할 때만 PR을 생성합니다.
- `dev` 브랜치로의 병합은 직접 merge하거나 push합니다.
- PR 제목은 `[type] 작업 요약` 형식을 권장하지만 자유롭게 작성해도 됩니다.
- PR 본문은 자유롭게 작성합니다. 형식에 구애받지 않고 내용을 명확히 전달하는 것이 중요합니다.
- PR은 **Merge 전 팀원 1명 이상의 승인이 필요**합니다.

---

## 📁 디렉토리 구조

```
📁 frontend/         # 프론트엔드 소스코드
📁 backend/          # 백엔드 소스코드
📄 README.md
📄 CONTRIBUTING.md
```
