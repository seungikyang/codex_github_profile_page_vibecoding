# Developer Portfolio for GitHub Pages

GitHub Pages에 바로 배포할 수 있는 정적 개발자 포트폴리오입니다. 별도 빌드 과정 없이 `index.html`, `styles.css`, `script.js`만으로 동작합니다.

## 수정할 곳

- `script.js`: 이름, 소개, 프로젝트, 기술 스택, 연락처 링크
- `assets/developer-workspace-hero.jpg`: 첫 화면 배경 이미지
- `index.html`: 메타 설명, OG 이미지, 기본 문서 구조
- `site.webmanifest`: 브라우저 설치 정보와 테마 색상

가장 먼저 바꿀 값은 `script.js` 상단의 `profile` 객체입니다.

```js
name: "Seo Woo",
initials: "SW",
role: "Full-stack Developer",
github: "https://github.com/seoowoo",
linkedin: "https://www.linkedin.com/in/your-profile",
email: "hello@example.com",
```

프로젝트 카드는 `projects`, 기술 스택은 `stacks`, 경력/소개 흐름은 `timeline` 배열에서 수정합니다.

## GitHub Pages 배포

이 저장소는 GitHub Actions workflow로 GitHub Pages에 배포합니다.

1. GitHub 저장소 `Settings` > `Pages`로 이동합니다.
2. `Build and deployment`의 source를 `GitHub Actions`로 선택합니다.
3. `main` 브랜치에 push하면 `.github/workflows/pages.yml`이 정적 파일을 배포합니다.

사용자 사이트로 운영하려면 저장소 이름을 `<github-username>.github.io`로 만들면 됩니다.

프로젝트 사이트로 운영한다면 저장소 이름을 자유롭게 정하고, 배포 URL은 보통 `https://<github-username>.github.io/<repository-name>/` 형태가 됩니다.

## 로컬 확인

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

브라우저에서 `http://127.0.0.1:4173/`를 열면 됩니다.

## 전일 시장 요약 자동 생성

이 저장소는 GitHub Actions로 매일 오전 10시(KST)에 전일 시장 요약 HTML을 생성하고 GitHub Pages에 배포할 수 있습니다.

- 워크플로: `.github/workflows/market-summary.yml`
- 생성 스크립트: `scripts/generate_market_summary.py`
- 의존성: `requirements.txt`
- 생성 위치: `reports/latest.html`, `reports/YYYY/MM/DD/index.html`, `reports/YYYY/MM/DD/data.json`
- 공개 경로: GitHub Pages의 `/reports/latest.html` 및 `/reports/YYYY/MM/DD/`

GitHub Actions의 cron은 UTC 기준이므로 `0 1 * * *`가 한국 시간 오전 10시에 해당합니다. 수동으로 다시 생성해야 할 때는 GitHub Actions 화면에서 `Generate Daily Market Summary` 워크플로를 `workflow_dispatch`로 실행하면 됩니다.

로컬에서 생성 테스트를 하려면 다음 명령을 실행합니다.

```bash
python -m pip install -r requirements.txt
python scripts/generate_market_summary.py
```
