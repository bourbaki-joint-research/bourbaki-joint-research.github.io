#!/usr/bin/env python3
"""
Google Form(xlsx) 응답 파일을 data/projects.json 으로 변환한다.

사용법:
    python tools/import_xlsx.py "2026_Bourbaki_Joint_Interim_Presentation__Responses_.xlsx"

이미 data/projects.json 이 있으면, 사람이 직접 채워 넣은 필드
(categories, comments, authors, title_en, license 등)는 팀 번호 기준으로
그대로 보존하고 Form 에서 온 필드(title/abstract/slides/timestamp)만 갱신한다.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.json"

# Form 응답 열 이름(부분 일치)
COL_KEYS = {
    "timestamp": ["timestamp", "타임스탬프"],
    "email": ["email"],
    "team": ["team number", "팀 번호"],
    "title": ["title", "연구 제목"],
    "abstract": ["abstract", "초록"],
    "slides": ["presentation slide", "발표 자료"],
}

# 공개 사이트에 제출자 이메일을 노출할지 여부.
# 기본값 False: 학생 메일 주소가 그대로 공개되는 것을 막는다.
SHOW_EMAILS = False


def find_columns(header):
    idx = {}
    for key, names in COL_KEYS.items():
        for i, cell in enumerate(header):
            low = str(cell or "").lower()
            if any(n in low for n in names):
                idx[key] = i
                break
    return idx


def drive_id(url):
    m = re.search(r"[?&]id=([\w-]+)", url or "")
    if m:
        return m.group(1)
    m = re.search(r"/d/([\w-]+)", url or "")
    return m.group(1) if m else None


def main(xlsx_path):
    from openpyxl import load_workbook

    wb = load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    idx = find_columns(rows[0])

    old = {}
    if DATA.exists():
        old = {p["team"]: p for p in json.loads(DATA.read_text(encoding="utf-8"))}

    records = []
    for row in rows[1:]:
        if not any(row):
            continue
        team = str(row[idx["team"]]).strip()
        ts = row[idx["timestamp"]]
        if not isinstance(ts, datetime):
            ts = datetime.fromisoformat(str(ts))
        prev = old.get(team, {})
        url = str(row[idx["slides"]] or "").strip()
        rec = {
            "team": team,
            "id": prev.get("id", ""),
            "title": str(row[idx["title"]] or "").strip(),
            "title_en": prev.get("title_en", ""),
            "authors": prev.get("authors", [f"Team {team}"]),
            "email": str(row[idx["email"]] or "").strip() if SHOW_EMAILS else "",
            "abstract": re.sub(r"[ \t]+", " ", str(row[idx["abstract"]] or "")).strip(),
            "submitted": ts.isoformat(timespec="seconds"),
            "slides_url": url,
            "slides_id": drive_id(url),
            "primary": prev.get("primary", ""),
            "categories": prev.get("categories", []),
            "comments": prev.get("comments", ""),
            "license": prev.get("license", "arXiv-style non-exclusive license to distribute"),
        }
        records.append(rec)

    records.sort(key=lambda r: (len(r["team"]), r["team"]))
    for n, rec in enumerate(records, start=1):
        if not rec["id"]:
            ym = datetime.fromisoformat(rec["submitted"]).strftime("%y%m")
            rec["id"] = f"{ym}.{n:05d}"

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(records)} entries -> {DATA}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
