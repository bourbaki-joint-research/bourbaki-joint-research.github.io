#!/usr/bin/env python3
"""
Bourbaki Joint Research Project — arXiv 스타일 정적 사이트 빌더.

    python build.py

data/projects.json 을 읽어 다음을 생성한다.

    index.html                 목록 페이지  (arXiv /list)
    search.html                검색 결과   (arXiv /search)
    abs/<id>/index.html        초록 페이지 (arXiv /abs)
    js/projects-data.js        클라이언트 검색용 데이터
    preview.html               전체 사이트를 담은 단일 파일(미리보기용)

수정한 뒤 다시 실행하기만 하면 된다. 의존성 없음(표준 라이브러리만 사용).
"""

import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ------------------------------------------------------------------ 설정 --
SITE_NAME = "Bourbaki"
SITE_TAGLINE = "Joint Research Project Archive"
ID_PREFIX = "Bourbaki"          # arXiv:2608.00001 의 "arXiv" 자리
COLLECTION = "2026 Bourbaki Joint Research Project"
COLLECTION_SHORT = "Interim Presentations, August 2026"
CONTACT = "bourbaki-archive@example.org"   # 실제 주소로 교체할 것
REPO_URL = "https://github.com/USERNAME/REPO"  # 실제 저장소로 교체할 것

CATS = {
    "math.NT": ("Mathematics", "Number Theory"),
    "math.CO": ("Mathematics", "Combinatorics"),
    "math.RA": ("Mathematics", "Rings and Algebras"),
    "math.AG": ("Mathematics", "Algebraic Geometry"),
    "math.GT": ("Mathematics", "Geometric Topology"),
    "math.MG": ("Mathematics", "Metric Geometry"),
    "math.PR": ("Mathematics", "Probability"),
    "cs.DS": ("Computer Science", "Data Structures and Algorithms"),
    "cs.DM": ("Computer Science", "Discrete Mathematics"),
    "cs.LG": ("Computer Science", "Machine Learning"),
    "physics.chem-ph": ("Physics", "Chemical Physics"),
    "physics.comp-ph": ("Physics", "Computational Physics"),
    "q-bio.QM": ("Quantitative Biology", "Quantitative Methods"),
}

MATHJAX = (
    '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]],'
    'displayMath:[["$$","$$"],["\\\\[","\\\\]"]]},'
    'options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]}};</script>\n'
    '<script id="MathJax-script" async '
    'src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"></script>'
)


# ------------------------------------------------------------- 유틸리티 --
def e(s):
    return html.escape(str(s or ""), quote=True)


def archive_of(cat):
    return cat.split(".")[0]


def cat_label(cat):
    return CATS.get(cat, (cat, cat))[1]


def cat_heading(cat):
    a, n = CATS.get(cat, (cat, cat))
    return f"{a} &gt; {n}"


def fmt_date(iso):
    d = datetime.fromisoformat(iso)
    return d.strftime("%-d %b %Y") if hasattr(d, "strftime") else iso


def fmt_stamp(iso):
    return datetime.fromisoformat(iso).strftime("%a, %-d %b %Y %H:%M:%S UTC")


def drive_download(p):
    return f"https://drive.google.com/uc?export=download&id={p['slides_id']}" if p.get("slides_id") else p["slides_url"]


def normalize_math(text):
    """$...$ 앞뒤에 붙어버린 단어를 띄어 준다. 내용은 건드리지 않는다."""
    if "$" not in text or text.count("$") % 2 != 0:
        return text
    parts, res = text.split("$"), ""
    for i, seg in enumerate(parts):
        if i % 2 == 1:
            if res and res[-1].isalnum():
                res += " "
            res += "$" + seg + "$"
        else:
            if res.endswith("$") and seg and seg[0].isalnum():
                res += " "
            res += seg
    return res


def full_title(p):
    t = p["title"]
    if p.get("title_en"):
        t += f" ({p['title_en']})"
    return t


def bibtex(p):
    d = datetime.fromisoformat(p["submitted"])
    key = f"bourbaki{p['team'].lower()}{d.year}"
    authors = " and ".join(p["authors"])
    return (
        f"@misc{{{key},\n"
        f"      title={{{full_title(p)}}}, \n"
        f"      author={{{authors}}},\n"
        f"      year={{{d.year}}},\n"
        f"      eprint={{{p['id']}}},\n"
        f"      archivePrefix={{{ID_PREFIX}}},\n"
        f"      primaryClass={{{p['primary']}}}\n"
        f"}}"
    )


class L:
    """모드에 따라 링크를 만들어 준다. static: 실제 파일 경로 / preview: 해시 라우트."""

    def __init__(self, mode, depth=0):
        self.mode = mode
        self.base = "" if mode == "preview" else "../" * depth

    def index(self):
        return "#/" if self.mode == "preview" else self.base + "index.html"

    def abs(self, pid):
        return f"#/abs/{pid}" if self.mode == "preview" else f"{self.base}abs/{pid}/"

    def search(self, query="", stype="all"):
        from urllib.parse import quote

        qs = f"query={quote(query)}&searchtype={stype}"
        return f"#/search?{qs}" if self.mode == "preview" else f"{self.base}search.html?{qs}"

    def asset(self, path):
        return self.base + path


# ------------------------------------------------------------- 공통 조각 --
def header(l):
    return f"""<div class="top-banner"><div class="container">
  We gratefully acknowledge the teams, mentors and reviewers of the <strong>{COLLECTION}</strong>.
</div></div>
<header class="site-header"><div class="container">
  <a class="logo" href="{l.index()}">
    <span class="wordmark">Bourba<span class="glyph">&#954;</span>i</span>
    <span class="tagline">{SITE_TAGLINE}</span>
  </a>
  <div class="header-tools">
    <nav class="header-nav">
      <a href="{l.index()}">Listing</a>
      <a href="{l.search()}">Search</a>
      <a href="{REPO_URL}" rel="noopener">Source</a>
    </nav>
    <form class="search-form" role="search" action="{'#' if l.mode == 'preview' else l.asset('search.html')}" method="get">
      <label class="sr-only" for="q" style="position:absolute;left:-9999px">Search term</label>
      <input type="text" id="q" name="query" placeholder="Search&hellip;" autocomplete="off">
      <select name="searchtype" aria-label="Field to search">
        <option value="all">All fields</option>
        <option value="title">Title</option>
        <option value="abstract">Abstract</option>
        <option value="team">Team</option>
        <option value="id">Identifier</option>
      </select>
      <button type="submit">Search</button>
    </form>
  </div>
</div></header>"""


def footer(l):
    return f"""<footer class="site-footer"><div class="container">
  <p class="footer-links">
    <a href="{l.index()}">Listing</a> &middot;
    <a href="{l.search()}">Search</a> &middot;
    <a href="{REPO_URL}" rel="noopener">Repository</a> &middot;
    <a href="mailto:{CONTACT}">Contact</a>
  </p>
  <p>{COLLECTION}. Abstracts are the work of the submitting teams and are posted here with their consent.</p>
  <p class="contact">This archive is an independent student project. It follows the page design conventions of
     arXiv.org but is not affiliated with, endorsed by, or connected to arXiv or Cornell University.</p>
</div></footer>"""


def document(title, body, l, description="", scripts=True, extra_body_attr=""):
    css = l.asset("css/arxiv.css")
    js = (
        f'<script src="{l.asset("js/projects-data.js")}"></script>\n'
        f'<script src="{l.asset("js/site.js")}"></script>'
        if scripts
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="{css}">
{MATHJAX}
</head>
<body{extra_body_attr}>
<a class="skip-link" href="#content">Skip to main content</a>
{header(l)}
{body}
{footer(l)}
{js}
</body>
</html>
"""


# ------------------------------------------------------------ 초록 페이지 --
def abs_body(p, prev_p, next_p, l):
    primary = p["primary"]
    cats = p["categories"]
    slides = e(p["slides_url"])

    subjects = "; ".join(
        (f'<span class="primary-subject">{cat_label(c)} ({c})</span>' if i == 0 else f"{cat_label(c)} ({c})")
        for i, c in enumerate(cats)
    )
    authors = ", ".join(f'<a href="{l.search(a, "team")}">{e(a)}</a>' for a in p["authors"])
    other = [c for c in cats[1:]]
    change_to = "<br>".join(
        f'<a href="{l.search(c, "all")}">{c}</a>' for c in [archive_of(primary)] + other
    )
    from urllib.parse import quote_plus

    scholar = f"https://scholar.google.com/scholar?q={quote_plus(p['title'])}"
    semantic = f"https://www.semanticscholar.org/search?q={quote_plus(p['title'])}"

    prev_link = f'<a href="{l.abs(prev_p["id"])}" title="previous in {primary}">&lt; prev</a>' if prev_p else "<span>&lt; prev</span>"
    next_link = f'<a href="{l.abs(next_p["id"])}" title="next in {primary}">next &gt;</a>' if next_p else "<span>next &gt;</span>"

    return f"""<div class="subheader"><div class="container">
  <h1><a href="{l.search(archive_of(primary), "all")}">{cat_heading(primary)}</a></h1>
</div></div>
<main id="content"><div class="container">
  <div class="header-breadcrumbs">
    <span class="id">{ID_PREFIX}:{p['id']}</span> <span class="arch">({archive_of(primary)})</span>
  </div>
  <div id="abs-outer">
    <div class="leftcolumn">
      <div id="abs">
        <div class="dateline">[Submitted on {fmt_date(p['submitted'])}]</div>
        <h1 class="title mathjax"><span class="descriptor">Title:</span>{e(full_title(p))}</h1>
        <div class="authors"><span class="descriptor">Authors:</span>{authors}</div>
        <div class="abs-toplinks">
          <a class="abs-inline-button" href="{slides}" rel="noopener">View Slides</a>
          <a class="abs-inline-button" href="{e(drive_download(p))}" rel="noopener">Download</a>
        </div>
        <blockquote class="abstract mathjax">
          <span class="descriptor">Abstract:</span>{e(p['abstract'])}
        </blockquote>
        <table class="metatable">
          <tr><td class="label">Comments:</td><td>{e(p['comments'])}</td></tr>
          <tr><td class="label">Subjects:</td><td>{subjects}</td></tr>
          <tr><td class="label">Team:</td><td>{e(p['team'])}</td></tr>
          <tr><td class="label">Cite as:</td><td class="tablecell arxivid">
            <a href="{l.abs(p['id'])}">{ID_PREFIX}:{p['id']}</a> [{primary}]</td></tr>
          <tr><td class="label">&nbsp;</td><td>(or <a href="{l.abs(p['id'])}">{ID_PREFIX}:{p['id']}v1</a>
            [{primary}] for this version)</td></tr>
        </table>
        <div class="submission-history">
          <h2>Submission history</h2>
          From: {e(p['authors'][0])}
          {f'&lt;<a href="mailto:{e(p["email"])}">{e(p["email"])}</a>&gt;' if p.get("email") else "[view email]"}<br>
          <span class="version">[v1]</span> {fmt_stamp(p['submitted'])}
        </div>
        <p class="abs-license">{e(p.get('license', ''))}</p>
      </div>
    </div>
    <div class="extra-services">
      <div class="full-text">
        <h2>Full-text links:</h2>
        <h3>Access presentation:</h3>
        <a class="abs-button" href="{slides}" rel="noopener">View Slides</a>
        <a class="abs-button" href="{e(drive_download(p))}" rel="noopener">Download Slides</a>
        <a class="abs-button abs-button-grey" href="{l.search(p['team'], 'team')}">Other entries by {e(p['team'])}</a>
      </div>
      <div class="browse">
        <h2>Current browse context:</h2>
        <div class="context-line"><strong>{primary}</strong></div>
        <div class="context-line">{prev_link} &nbsp;|&nbsp; {next_link}</div>
        <div class="context-line">
          <a href="{l.index()}">all</a> |
          <a href="{l.search(cat_label(primary), 'all')}">{primary}</a> |
          <a href="{l.index()}">2026-08</a>
        </div>
        <h3>Change to browse by:</h3>
        <div class="context-line">{change_to}</div>
      </div>
      <div class="references">
        <h2>References &amp; Citations:</h2>
        <ul>
          <li><a href="{scholar}" rel="noopener">Google Scholar</a></li>
          <li><a href="{semantic}" rel="noopener">Semantic Scholar</a></li>
        </ul>
      </div>
      <div class="bibtex-box">
        <details>
          <summary class="bib-toggle">Export BibTeX citation</summary>
          <pre class="bibtex">{e(bibtex(p))}</pre>
        </details>
      </div>
    </div>
  </div>
</div></main>"""


# ------------------------------------------------------------ 목록 페이지 --
def listing_body(projects, l):
    counts = {}
    for p in projects:
        for c in p["categories"]:
            counts[c] = counts.get(c, 0) + 1
    filt = " |\n    ".join(
        f'<a href="#" data-cat="{c}">{c} ({n})</a>' for c, n in sorted(counts.items())
    )

    items = []
    for i, p in enumerate(projects, start=1):
        subjects = "; ".join(
            (f'<span class="primary-subject">{cat_label(c)} ({c})</span>' if j == 0 else f"{cat_label(c)} ({c})")
            for j, c in enumerate(p["categories"])
        )
        authors = ", ".join(f'<a href="{l.search(a, "team")}">{e(a)}</a>' for a in p["authors"])
        items.append(
            f"""  <dt data-cats="{' '.join(p['categories'])}">
    <span class="list-identifier">[{i}]&nbsp; <a href="{l.abs(p['id'])}" title="Abstract"><span class="id">{ID_PREFIX}:{p['id']}</span></a>
    [<a href="{e(p['slides_url'])}" rel="noopener" title="Presentation slides">slides</a>]</span>
  </dt>
  <dd>
    <div class="list-title mathjax"><span class="descriptor">Title:</span> {e(full_title(p))}</div>
    <div class="list-authors"><span class="descriptor">Authors:</span> {authors}</div>
    <div class="list-comments"><span class="descriptor">Comments:</span> {e(p['comments'])}</div>
    <div class="list-subjects"><span class="descriptor">Subjects:</span> {subjects}</div>
  </dd>"""
        )

    return f"""<div class="subheader"><div class="container">
  <h1>{COLLECTION}</h1>
</div></div>
<main id="content"><div class="container">
  <div class="header-breadcrumbs">{COLLECTION_SHORT}</div>
  <div class="browse-bar" id="subject-filter">
    <strong>Browse by subject:</strong>
    <a href="#" data-cat="all" style="font-weight:bold">all ({len(projects)})</a> |
    {filt}
  </div>
  <p class="listing-intro">Authors and titles for August 2026</p>
  <p class="paging">Total of <span id="entry-total">{len(projects)}</span> entries: <strong>1-{len(projects)}</strong></p>
  <dl id="articles">
{chr(10).join(items)}
  </dl>
  <p class="paging">Total of <span>{len(projects)}</span> entries: <strong>1-{len(projects)}</strong></p>
</div></main>"""


# ------------------------------------------------------------ 검색 페이지 --
def search_body(l):
    return f"""<div class="subheader"><div class="container">
  <h1>{SITE_NAME} Search</h1>
</div></div>
<main id="content"><div class="container">
  <p class="search-summary" id="search-summary"></p>
  <ul id="search-results" style="padding-left:0;margin:0"></ul>
</div></main>"""


# ----------------------------------------------------------------- 빌드 --
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("  wrote", path.relative_to(ROOT))


def main():
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    projects.sort(key=lambda p: p["id"])
    for p in projects:
        p["abstract"] = normalize_math(p["abstract"])

    # ---- 클라이언트 데이터
    write(
        ROOT / "js" / "projects-data.js",
        "window.BOURBAKI_PROJECTS = "
        + json.dumps(projects, ensure_ascii=False, indent=1)
        + ";\nwindow.BOURBAKI_CATS = "
        + json.dumps(CATS, ensure_ascii=False)
        + ";\n",
    )

    # ---- 목록 / 검색
    ls = L("static", 0)
    write(
        ROOT / "index.html",
        document(
            f"{COLLECTION} — {SITE_NAME}",
            listing_body(projects, ls),
            ls,
            description=f"Listing of interim presentations from the {COLLECTION}.",
        ),
    )
    write(
        ROOT / "search.html",
        document(f"{SITE_NAME} Search", search_body(ls), ls, description="Search the archive."),
    )

    # ---- 초록 페이지
    for i, p in enumerate(projects):
        la = L("static", 2)
        prev_p = projects[i - 1] if i > 0 else None
        next_p = projects[i + 1] if i < len(projects) - 1 else None
        write(
            ROOT / "abs" / p["id"] / "index.html",
            document(
                f"[{p['id']}] {full_title(p)}",
                abs_body(p, prev_p, next_p, la),
                la,
                description=p["abstract"][:280],
            ),
        )

    # ---- 단일 파일 미리보기
    lp = L("preview")
    sections = [f'<section data-route="/">{listing_body(projects, lp)}</section>',
                f'<section data-route="/search" hidden>{search_body(lp)}</section>']
    for i, p in enumerate(projects):
        prev_p = projects[i - 1] if i > 0 else None
        next_p = projects[i + 1] if i < len(projects) - 1 else None
        sections.append(f'<section data-route="/abs/{p["id"]}" hidden>{abs_body(p, prev_p, next_p, lp)}</section>')

    css = (ROOT / "css" / "arxiv.css").read_text(encoding="utf-8")
    data_js = (ROOT / "js" / "projects-data.js").read_text(encoding="utf-8")
    site_js = (ROOT / "js" / "site.js").read_text(encoding="utf-8")
    preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{COLLECTION} — {SITE_NAME}</title>
<style>
{css}
</style>
{MATHJAX}
</head>
<body data-mode="preview">
<a class="skip-link" href="#content">Skip to main content</a>
{header(lp)}
{chr(10).join(sections)}
{footer(lp)}
<script>
{data_js}
</script>
<script>
{site_js}
</script>
</body>
</html>
"""
    write(ROOT / "preview.html", preview)
    print(f"\n{len(projects)} entries built.")


if __name__ == "__main__":
    main()
