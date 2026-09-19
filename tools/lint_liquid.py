#!/usr/bin/env python3
"""
push 하기 전에 Liquid 문법을 점검한다.

    python3 tools/lint_liquid.py

Ruby Liquid(= Jekyll)의 토크나이저는 변수의 끝을 /\\}\\}?/ 로 찾는다.
즉 `{{` 뒤에 나오는 **첫 번째 `}`** 에서 토큰을 끊고, 그것이 `}}` 가 아니면
"Variable was not properly terminated" 오류를 낸다. 그래서 아래 두 줄은
파이썬 Liquid 구현에서는 통과해도 Jekyll 빌드에서는 실패한다.

    {{ "}" }}            ← 문자열 안의 중괄호
    {{ ob }}}            ← 변수 바로 뒤에 붙은 중괄호

BibTeX 처럼 중괄호를 출력해야 하면 변수에 담아서 쓴다.

    {% assign ob = '{' %}{% assign cb = '}' %}
    title={{ ob }}{{ page.title }}{{ cb }},
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ["_layouts/*.html", "_includes/*.html", "*.html", "assets/js/*.js", "_projects/*.md"]


def check(text):
    """(줄번호, 문제가 된 토큰) 목록을 돌려준다."""
    problems, i = [], 0
    while True:
        i = text.find("{{", i)
        if i == -1:
            return problems
        j = text.find("}", i + 2)
        if j == -1:
            problems.append((text[:i].count("\n") + 1, text[i:i + 40] + "  (닫히지 않음)"))
            return problems
        if text[j:j + 2] != "}}":
            problems.append((text[:i].count("\n") + 1, text[i:j + 1]))
        # 여는 중괄호가 토큰 안에 또 있으면 거의 항상 실수다
        elif "{" in text[i + 2:j]:
            problems.append((text[:i].count("\n") + 1, text[i:j + 2] + "  (안에 '{' 가 있음)"))
        i = j + 2


def main():
    bad = 0
    for pattern in TARGETS:
        for f in sorted(ROOT.glob(pattern)):
            for line, token in check(f.read_text(encoding="utf-8")):
                bad += 1
                print(f"{f.relative_to(ROOT)}:{line}: {token!r}")
    if bad:
        print(f"\n{bad}건. Jekyll 빌드가 실패한다. 위 설명을 참고해 고칠 것.")
        sys.exit(1)
    print("Liquid 문법 이상 없음.")


if __name__ == "__main__":
    main()
