#!/usr/bin/env python3
"""
프로젝트 하나를 새로 추가한다. 식별자는 이번 달 기준으로 비어 있는
가장 작은 번호가 자동으로 붙는다.

    python3 tools/new_project.py
    python3 tools/new_project.py --team T9 --title "제목" --subjects math.CO cs.DS

질문에 그냥 엔터를 치면 기본값이 들어가고, 초록은 나중에 파일을 열어
직접 채워도 된다. 표준 라이브러리만 쓴다.
"""
import argparse
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "_projects"


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def drive_id(url):
    m = re.search(r"[?&]id=([\w-]+)", url or "") or re.search(r"/d/([\w-]+)", url or "")
    return m.group(1) if m else ""


def next_identifier(when):
    taken = {f.stem for f in PROJECTS.glob("*.md")}
    ym = when.strftime("%y%m")
    n = 1
    while f"{ym}.{n:05d}" in taken:
        n += 1
    return f"{ym}.{n:05d}"


def ask(label, default=""):
    suffix = f" [{default}]" if default else ""
    return input(f"{label}{suffix}: ").strip() or default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team")
    ap.add_argument("--title")
    ap.add_argument("--title-en", default=None)
    ap.add_argument("--authors", nargs="*")
    ap.add_argument("--subjects", nargs="*")
    ap.add_argument("--slides", default=None)
    ap.add_argument("--abstract", default=None)
    a = ap.parse_args()

    PROJECTS.mkdir(exist_ok=True)
    now = datetime.now()

    team = a.team or ask("팀 번호", "T9")
    title = a.title or ask("제목")
    title_en = a.title_en if a.title_en is not None else ask("영문 제목(제목이 한국어일 때만, 없으면 엔터)")
    authors = a.authors or [x.strip() for x in ask("저자(쉼표로 구분)", f"Team {team}").split(",")]
    subjects = a.subjects or ask("분류(공백으로 구분)", "math.CO").split()
    slides = a.slides if a.slides is not None else ask("발표자료 링크")
    abstract = a.abstract if a.abstract is not None else ask("초록(비워 두고 나중에 파일에서 작성해도 된다)")

    ident = next_identifier(now)
    body = (
        "---\n"
        f"identifier: {yaml_str(ident)}\n"
        f"permalink: /abs/{ident}/\n"
        f"team: {yaml_str(team)}\n"
        f"title: {yaml_str(title)}\n"
        f"title_en: {yaml_str(title_en)}\n"
        "authors:\n" + "".join(f"  - {x}\n" for x in authors) +
        'email: ""\n'
        f"submitted: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "subjects:\n" + "".join(f"  - {s}\n" for s in subjects) +
        'comments: "Interim presentation, 2026 Bourbaki Joint Research Project"\n'
        f"slides_url: {yaml_str(slides)}\n"
        f"slides_id: {yaml_str(drive_id(slides))}\n"
        'license: "Non-exclusive license to distribute"\n'
        "---\n\n"
        + (abstract or "여기에 초록을 쓴다. 수식은 $x^2+1$ 처럼 달러 기호로 감싸면 된다.")
        + "\n"
    )
    path = PROJECTS / f"{ident}.md"
    path.write_text(body, encoding="utf-8")
    print(f"\n만들었다: {path.relative_to(ROOT)}  →  /abs/{ident}/")
    print("분류 코드가 _data/categories.yml 에 있는지 확인할 것.")


if __name__ == "__main__":
    main()
