#!/usr/bin/env python3
"""
Google Form(xlsx) 응답을 _projects/*.md 로 변환한다.

    python3 tools/import_xlsx.py "2026_Bourbaki_..._(Responses).xlsx"
    python3 tools/import_xlsx.py <파일> --overwrite   # 기존 파일까지 덮어쓰기

기본 동작은 "없는 것만 추가"다. 이미 있는 팀 파일은 건드리지 않으므로,
손으로 고쳐 둔 subjects·authors·제목이 임포트 때문에 날아가지 않는다.

openpyxl 이 필요하다:  pip install openpyxl
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "_projects"

# 공개 사이트에 제출자 이메일을 노출할지. 기본값은 비공개.
SHOW_EMAILS = False

# 팀별 기본 분류. 없으면 UNCLASSIFIED 가 들어가고, 나중에 파일에서 고치면 된다.
DEFAULT_SUBJECTS = {
    "T1": ["physics.chem-ph", "physics.comp-ph", "cs.LG"],
    "T2": ["math.NT", "cs.DM"],
    "T3": ["math.RA", "math.AG"],
    "T4": ["math.CO", "math.MG"],
    "T5": ["math.GT", "math.CO"],
    "T6": ["math.CO", "cs.DM"],
    "T7": ["cs.DS", "math.CO"],
    "T8": ["math.NT", "math.PR"],
}

COL_KEYS = {
    "timestamp": ["timestamp", "타임스탬프"],
    "email": ["email"],
    "team": ["team number", "팀 번호"],
    "title": ["title", "연구 제목"],
    "abstract": ["abstract", "초록"],
    "slides": ["presentation slide", "발표 자료"],
}


def find_columns(header):
    idx = {}
    for key, names in COL_KEYS.items():
        for i, cell in enumerate(header):
            if any(n in str(cell or "").lower() for n in names):
                idx[key] = i
                break
        if key not in idx:
            sys.exit(f"열을 찾지 못했다: {key}")
    return idx


def drive_id(url):
    m = re.search(r"[?&]id=([\w-]+)", url or "") or re.search(r"/d/([\w-]+)", url or "")
    return m.group(1) if m else ""


def normalize_math(text):
    """$...$ 에 단어가 붙어버린 경우 한 칸 띄운다. 내용은 바꾸지 않는다."""
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


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def next_identifier(when, taken):
    """yymm.nnnnn 형식. 같은 달 안에서 비어 있는 가장 작은 번호를 쓴다."""
    ym = when.strftime("%y%m")
    n = 1
    while f"{ym}.{n:05d}" in taken:
        n += 1
    return f"{ym}.{n:05d}"


def existing():
    ids, teams = set(), {}
    for f in PROJECTS.glob("*.md"):
        ids.add(f.stem)
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^team:\s*(\S+)", text, re.M)
        if m:
            teams[m.group(1).strip('"')] = f
    return ids, teams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--overwrite", action="store_true", help="이미 있는 팀 파일도 새로 쓴다")
    args = ap.parse_args()

    from openpyxl import load_workbook

    wb = load_workbook(args.xlsx, read_only=True, data_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    idx = find_columns(rows[0])

    PROJECTS.mkdir(exist_ok=True)
    ids, teams = existing()
    written = skipped = 0

    entries = []
    for row in rows[1:]:
        if not any(row):
            continue
        ts = row[idx["timestamp"]]
        if not isinstance(ts, datetime):
            ts = datetime.fromisoformat(str(ts))
        entries.append((ts, row))
    entries.sort(key=lambda t: (len(str(t[1][idx["team"]]).strip()), str(t[1][idx["team"]]).strip()))

    for ts, row in entries:
        team = str(row[idx["team"]]).strip()
        if team in teams and not args.overwrite:
            skipped += 1
            continue

        ident = teams[team].stem if team in teams else next_identifier(ts, ids)
        ids.add(ident)
        url = str(row[idx["slides"]] or "").strip()
        abstract = normalize_math(re.sub(r"[ \t]+", " ", str(row[idx["abstract"]] or "")).strip())
        subjects = DEFAULT_SUBJECTS.get(team, ["math.CO"])
        email = str(row[idx["email"]] or "").strip() if SHOW_EMAILS else ""

        body = (
            "---\n"
            f"identifier: {yaml_str(ident)}\n"
            f"permalink: /abs/{ident}/\n"
            f"team: {yaml_str(team)}\n"
            f"title: {yaml_str(str(row[idx['title']] or '').strip())}\n"
            'title_en: ""\n'
            "authors:\n"
            f"  - Team {team}\n"
            f"email: {yaml_str(email)}\n"
            f"submitted: {ts.strftime('%Y-%m-%d %H:%M:%S')}\n"
            "subjects:\n"
            + "".join(f"  - {s}\n" for s in subjects)
            + 'comments: "Interim presentation, 2026 Bourbaki Joint Research Project"\n'
            f"slides_url: {yaml_str(url)}\n"
            f"slides_id: {yaml_str(drive_id(url))}\n"
            'license: "Non-exclusive license to distribute"\n'
            "---\n\n"
            + abstract
            + "\n"
        )
        (PROJECTS / f"{ident}.md").write_text(body, encoding="utf-8")
        written += 1
        print(f"  {'덮어씀' if team in teams else '추가'}  _projects/{ident}.md  ({team})")

    print(f"\n{written}개 작성, {skipped}개 건너뜀(이미 존재). 이제 jekyll 을 다시 빌드하면 된다.")


if __name__ == "__main__":
    main()
