# Bourbaki Joint Research Project Archive

arXiv.org 의 레이아웃·타이포그래피·색을 그대로 따른 GitHub Pages 정적 사이트다.
Google Form 응답(xlsx)에서 각 팀의 제목·초록·발표자료 링크를 읽어
arXiv 의 **목록 페이지(`/list`)**, **초록 페이지(`/abs`)**, **검색 페이지(`/search`)** 를 생성한다.

```
index.html                 목록  (arXiv /list  스타일)
search.html                검색  (arXiv /search 스타일, 클라이언트 측 검색)
abs/2608.00001/index.html  초록  (arXiv /abs   스타일)  … 팀별로 8개
css/arxiv.css              arXiv 스타일시트 재현
js/site.js                 검색·필터·미리보기 라우팅
js/projects-data.js        빌드 산출물(직접 수정하지 말 것)
data/projects.json         원본 데이터 — 수정은 여기서
build.py                   정적 사이트 빌더
tools/import_xlsx.py       Form 응답(xlsx) → data/projects.json
preview.html               전체 사이트를 담은 단일 파일(로컬 확인용, 배포 불필요)
```

## 1. 배포

```bash
git init
git add .
git commit -m "Bourbaki archive"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

GitHub 저장소 → **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.
1~2분 뒤 `https://USERNAME.github.io/REPO/` 에서 열린다.
`.nojekyll` 파일이 포함돼 있으므로 Jekyll 처리 없이 그대로 서빙된다.

커스텀 도메인을 쓰려면 저장소 루트에 도메인 한 줄을 적은 `CNAME` 파일을 추가한다.

## 2. 내용 수정

모든 내용은 `data/projects.json` 한 곳에 있다. 고치고 나서 다시 빌드하면 된다.

```bash
python3 build.py
```

항목별 의미:

| 필드 | 설명 |
| --- | --- |
| `team` | 팀 번호 (T1 … T8) |
| `id` | arXiv 형식 식별자 `2608.00001` (yymm.nnnnn) |
| `title` | 제출된 제목 그대로 |
| `title_en` | 제목이 한국어일 때 괄호 안에 함께 보여줄 영문 제목 |
| `authors` | 저자 표기. 실명을 쓰려면 `["홍길동", "김철수"]` 처럼 바꾼다 |
| `email` | 공개 표시용 연락처. 비워 두면 arXiv처럼 `[view email]` 로만 표시된다 |
| `abstract` | 초록. `$...$` 로 감싼 부분은 MathJax 로 렌더링된다 |
| `primary` / `categories` | 분류. 첫 번째가 primary, 굵게 표시된다 |
| `comments` | arXiv 의 Comments 줄 |
| `slides_url` | 발표자료 링크 (Google Drive) |

### 새 응답을 다시 불러오기

Form 에 응답이 추가되면:

```bash
python3 tools/import_xlsx.py "2026_Bourbaki_Joint_Interim_Presentation__Responses_.xlsx"
python3 build.py
```

`import_xlsx.py` 는 손으로 채운 필드(`categories`, `comments`, `authors`, `title_en`)를
팀 번호 기준으로 보존하고 Form 에서 온 값만 갱신한다.

### 분류 코드 추가

`build.py` 상단의 `CATS` 딕셔너리에 `"math.AT": ("Mathematics", "Algebraic Topology")`
형식으로 추가하면 목록·초록·검색 모두에 반영된다.

### 사이트 이름·연락처

`build.py` 상단의 `SITE_NAME`, `ID_PREFIX`, `COLLECTION`, `CONTACT`, `REPO_URL` 을 고친다.
`CONTACT` 와 `REPO_URL` 은 현재 자리표시자이므로 배포 전에 반드시 바꿀 것.

## 3. 알아 둘 점

- **이메일 비공개가 기본값이다.** Form 에 모인 주소는 `data/projects.json` 에 들어가지 않고,
  초록 페이지에는 arXiv 와 동일하게 `[view email]` 로만 표시된다. 공개하려면
  `tools/import_xlsx.py` 의 `SHOW_EMAILS = True` 로 바꾸고 다시 임포트한다.
- **T2 초록의 수식 구분자.** 원본에서 `\( ... \)` 의 백슬래시가 Form 을 거치며 사라져
  `(D=2^A-3^r)` 같은 형태로 남아 있다. 수식으로 렌더링하려면
  `data/projects.json` 에서 해당 부분을 `$D=2^A-3^r$` 로 고치면 된다.
- **Google Drive 링크는 공개 설정이 필요하다.** "링크가 있는 모든 사용자" 로 바꾸지 않으면
  방문자에게 권한 요청 화면이 뜬다.
- **MathJax 는 CDN(cdnjs) 에서 불러온다.** 오프라인 배포가 필요하면
  `build.py` 의 `MATHJAX` 상수에서 로컬 경로로 바꾼다.
- **arXiv 와는 무관한 사이트다.** 페이지 디자인 관례만 따랐을 뿐이며, arXiv 로고와 상표는
  쓰지 않았다. 각주로도 이 점을 푸터에 명시해 두었다.

## 4. 로컬에서 확인

```bash
python3 -m http.server 8000
# http://localhost:8000
```

`preview.html` 은 CSS·JS·데이터를 모두 인라인한 단일 파일이라 서버 없이 더블클릭으로도 열린다.
배포에 필요한 파일은 아니므로 지워도 된다.
