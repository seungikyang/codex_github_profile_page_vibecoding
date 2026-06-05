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

1. GitHub에서 새 저장소를 만듭니다.
2. 이 폴더의 파일을 저장소에 push합니다.
3. 저장소 `Settings` > `Pages`로 이동합니다.
4. `Build and deployment`에서 `Deploy from a branch`를 선택합니다.
5. Branch는 `main`, folder는 `/root`로 선택한 뒤 저장합니다.

사용자 사이트로 운영하려면 저장소 이름을 `<github-username>.github.io`로 만들면 됩니다.

프로젝트 사이트로 운영한다면 저장소 이름을 자유롭게 정하고, 배포 URL은 보통 `https://<github-username>.github.io/<repository-name>/` 형태가 됩니다.

## 로컬 확인

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

브라우저에서 `http://127.0.0.1:4173/`를 열면 됩니다.
