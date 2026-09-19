# Bourbaki Joint Research Project Archive (Jekyll)

arXiv.org 의 레이아웃·타이포그래피·색을 그대로 따른 **Jekyll** 사이트다.
GitHub Pages 가 Jekyll 을 기본 지원하므로, 저장소에 push 하면 별도 빌드 없이 바로 배포된다.

**프로젝트를 추가하려면 `_projects/` 에 `.md` 파일을 하나 넣으면 된다.**
목록 페이지, 초록 페이지, 분류 필터, 검색 색인, prev/next 링크가 전부 자동으로 따라온다.

---

## 1. 프로젝트 추가하기

### 방법 A — 파일을 직접 만든다 (추천)

`_projects/2608.00009.md` 처럼 `<식별자>.md` 이름으로 만든다.

```markdown
---
identifier: "2608.00009"
permalink: /abs/2608.00009/
team: "T9"
title: "Spectral Gaps of Random Cayley Graphs"
title_en: ""                       # 제목이 한국어일 때 괄호로 함께 보일 영문 제목
authors:
  - Team T9
email: ""                          # 비우면 arXiv 처럼 [view email] 로만 표시된다
submitted: 2026-09-01 14:20:00
subjects:                          # 첫 번째가 primary, 굵게 표시된다
  - math.CO
  - math.PR
comments: "Interim presentation, 2026 Bourbaki Joint Research Project"
slides_url: "https://drive.google.com/open?id=XXXXXXXX"
slides_id: "XXXXXXXX"              # 위 링크의 id. 넣으면 Download 버튼이 생긴다
license: "Non-exclusive license to distribute"
---

여기서부터 본문이 초록이 된다. 수식은 $\lambda_2 < 1 - \varepsilon$ 처럼
달러 기호로 감싸면 MathJax 가 렌더링한다.
```

- `identifier` 는 arXiv 형식 `yymm.nnnnn`. 파일 이름·permalink 와 같게 맞춘다.
- `subjects` 에 쓰는 코드는 `_data/categories.yml` 에 있어야 한다. 없으면 코드가 그대로 출력된다.
- `title`, `team` 정도만 있어도 페이지는 만들어진다. 나머지는 없으면 그 줄이 생략된다.

### 방법 B — 스크립트로 만든다

식별자를 자동으로 붙여 준다. 질문에 답하거나 인자로 넘기면 된다.

```bash
python3 tools/new_project.py
python3 tools/new_project.py --team T9 --title "제목" --subjects math.CO math.PR \
        --slides "https://drive.google.com/open?id=XXXX"
```

### 방법 C — Form 응답(xlsx)에서 한 번에 가져온다

```bash
pip install openpyxl
python3 tools/import_xlsx.py "2026_Bourbaki_Joint_Interim_Presentation__Responses_.xlsx"
```

기본은 **없는 팀만 추가**다. 이미 있는 파일은 건드리지 않으므로 손으로 고쳐 둔
분류·저자·영문 제목이 날아가지 않는다. 전부 새로 쓰려면 `--overwrite` 를 붙인다.

### 방법 D — GitHub 웹에서

저장소 → `_projects` → **Add file → Create new file** → 위 템플릿을 붙여넣고 commit.
1~2분 뒤 사이트에 반영된다. 로컬 환경 없이도 된다.

---

## 2. 배포

```bash
git init && git add . && git commit -m "Bourbaki archive"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

저장소 → **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.

`USERNAME.github.io/REPO/` 형태(프로젝트 사이트)로 배포한다면
`_config.yml` 의 `baseurl` 을 `"/REPO"` 로 바꿔야 CSS·링크가 깨지지 않는다.
사용자 사이트(`USERNAME.github.io`)나 커스텀 도메인이면 `""` 그대로 둔다.

### 로컬에서 미리 보기

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

`--livereload` 를 붙이면 파일을 저장할 때마다 새로고침된다.
단 `_config.yml` 은 감시 대상이 아니라 고칠 때마다 서버를 다시 띄워야 한다.

---

## 3. 구조

```
_config.yml              사이트 이름·연락처·baseurl·컬렉션 설정
_data/categories.yml     분류 코드표 (math.NT → Number Theory 등)
_projects/*.md           프로젝트 하나 = 파일 하나  ← 여기만 건드리면 된다
_layouts/default.html    공통 뼈대
_layouts/abs.html        초록 페이지 (arXiv /abs)
_includes/               헤더·푸터·분류 줄
index.html               목록 페이지 (arXiv /list)
search.html              검색 페이지 (arXiv /search)
assets/css/arxiv.css     arXiv 스타일시트 재현
assets/js/site.js        검색·분류 필터
assets/js/projects-data.js  Liquid 로 생성되는 검색 색인 (직접 수정하지 말 것)
tools/                   xlsx 임포터, 새 프로젝트 스캐폴드 (사이트에 배포되지 않음)
```

### 분야를 새로 추가하려면

`_data/categories.yml` 에 한 줄 추가한다.

```yaml
math.AT:
  archive: Mathematics
  name: Algebraic Topology
```

### 사이트 이름·연락처

`_config.yml` 의 `title`, `id_prefix`, `collection_title`, `collection_subtitle`,
`contact`, `repo_url` 을 고친다. `contact` 와 `repo_url` 은 자리표시자이므로
배포 전에 반드시 교체할 것.

---

## 4. 알아 둘 점

- **이메일은 기본 비공개다.** Form 에 모인 주소는 파일에 들어가지 않고 초록 페이지에는
  arXiv 와 동일하게 `[view email]` 로만 표시된다. 공개하려면
  `tools/import_xlsx.py` 의 `SHOW_EMAILS = True` 로 바꾸고 다시 임포트한다.
- **빈 문자열 주의.** Liquid 에서 `""` 는 참으로 취급된다. 템플릿은 이미
  `!= ""` 로 비교하도록 써 두었으니, 새 필드를 추가할 때도 같은 방식을 쓸 것.
- **T2 초록의 수식 구분자.** 원본의 `\( ... \)` 에서 백슬래시가 Form 을 거치며 사라져
  `(D=2^A-3^r)` 형태로 남아 있다. `_projects/2608.00002.md` 에서 `$D=2^A-3^r$` 로
  고치면 수식으로 렌더링된다.
- **Markdown 이 초록에 적용된다.** `*`, `_`, `#` 로 시작하는 줄은 서식으로 해석될 수 있다.
  수식은 `$...$` 안에 두면 대체로 안전하지만, 이상하게 보이면 해당 문자 앞에 `\` 를 붙인다.
- **Google Drive 링크는 "링크가 있는 모든 사용자" 로 공개해야** 방문자에게 권한 요청
  화면이 뜨지 않는다.
- **arXiv 와 무관한 사이트다.** 페이지 디자인 관례만 따랐고 로고·상표는 쓰지 않았다.
  이 점을 푸터에 명시해 두었다.
