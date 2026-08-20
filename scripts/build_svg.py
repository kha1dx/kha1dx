#!/usr/bin/env python3
"""
Generates the two SVGs used by the profile README.

  assets/hero.svg   a VS Code window that types itself out
  assets/stack.svg  the stack, as terminal output

Run:  python3 scripts/build_svg.py
"""

import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

W = 900

# VS Code Dark+ tokens, same palette the portfolio uses.
BG      = "#1e1e1e"
CHROME  = "#323233"
BORDER  = "#3c3c3c"
GUTTER  = "#5a5a5a"
PUNCT   = "#d4d4d4"
KEYWORD = "#569cd6"
VAR     = "#9cdcfe"
PROP    = "#9cdcfe"
STRING  = "#ce9178"
COMMENT = "#6a9955"
TEAL    = "#4ec9b0"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- hero.svg

FS = 16               # code font size
CW = FS * 0.6         # monospace advance width
LH = 30               # line height
BAR = 40              # title bar height
X0 = 62               # first code column
TOP = 70              # first baseline

# Each line is a list of (text, colour) runs.
LINES = [
    [("// I build products with language models inside them.", COMMENT)],
    [],
    [("const", KEYWORD), (" ", PUNCT), ("khaled", VAR), (" = ", PUNCT), ("{", PUNCT)],
    [("  role", PROP), (":  ", PUNCT), ('"Software Engineer & AI Developer"', STRING), (",", PUNCT)],
    [("  base", PROP), (":  ", PUNCT), ('"Cairo, Egypt"', STRING), (",", PUNCT)],
    [("  stack", PROP), (": ", PUNCT), ("[", PUNCT),
     ('"TypeScript"', STRING), (", ", PUNCT), ('"Python"', STRING), (", ", PUNCT),
     ('"Google Cloud"', STRING), (", ", PUNCT), ('"OpenAI"', STRING), ("]", PUNCT), (",", PUNCT)],
    [("  now", PROP), (":   ", PUNCT), ('"Agile Translate, EN to AR decks that keep their layout"', STRING), (",", PUNCT)],
    [("}", PUNCT), (";", PUNCT)],
]

H = TOP + (len(LINES) - 1) * LH + 26

CPS = 0.017   # seconds per character
GAP = 0.09    # pause between lines


def build_hero():
    clips, groups, carets = [], [], []
    t = 0.35

    for i, runs in enumerate(LINES):
        y = TOP + i * LH
        n = sum(len(txt) for txt, _ in runs)

        # Blank line: just hold a beat so the cadence reads naturally.
        if n == 0:
            groups.append(
                f'<text x="44" y="{y}" text-anchor="end" fill="{GUTTER}" '
                f'font-size="13" opacity="0">{i + 1}</text>'
            )
            t += 0.18
            continue

        dur = round(n * CPS, 3)
        end_x = X0 + n * CW
        cid = f"c{i}"

        clips.append(
            f'<clipPath id="{cid}"><rect x="{X0 - 4}" y="{y - 22}" width="0" height="28">'
            f'<animate attributeName="width" from="0" to="{end_x - X0 + 8:.0f}" '
            f'dur="{dur}s" begin="{t:.2f}s" fill="freeze" /></rect></clipPath>'
        )

        spans = "".join(
            f'<tspan fill="{c}">{esc(txt)}</tspan>' for txt, c in runs
        )

        groups.append(
            # Line number fades in with the line.
            f'<text x="44" y="{y}" text-anchor="end" fill="{GUTTER}" font-size="13" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{t:.2f}s" />{i + 1}</text>'
            f'<g clip-path="url(#{cid})"><text x="{X0}" y="{y}" font-size="{FS}" '
            f'xml:space="preserve">{spans}</text></g>'
        )

        carets.append(
            f'<rect x="{X0}" y="{y - 14}" width="9" height="19" fill="{TEAL}" opacity="0">'
            f'<set attributeName="opacity" to="0.85" begin="{t:.2f}s" />'
            f'<animate attributeName="x" from="{X0}" to="{end_x:.0f}" dur="{dur}s" '
            f'begin="{t:.2f}s" fill="freeze" />'
            f'<set attributeName="opacity" to="0" begin="{t + dur:.2f}s" /></rect>'
        )

        t += dur + GAP

    # The caret that stays behind and blinks, parked after the closing brace.
    final_y = TOP + (len(LINES) - 1) * LH
    final_x = X0 + 2 * CW
    carets.append(
        f'<rect x="{final_x:.0f}" y="{final_y - 14}" width="9" height="19" fill="{TEAL}" opacity="0">'
        f'<set attributeName="opacity" to="0.85" begin="{t:.2f}s" />'
        f'<animate attributeName="opacity" values="0.85;0.85;0;0;0.85" dur="1.15s" '
        f'begin="{t:.2f}s" repeatCount="indefinite" /></rect>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" role="img" aria-label="Khaled Salleh, Software Engineer and AI Developer, Cairo Egypt">
  <defs>
    <clipPath id="win"><rect x="0" y="0" width="{W}" height="{H}" rx="10" /></clipPath>
    {"".join(clips)}
  </defs>

  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="{BG}" />
    <rect width="{W}" height="{BAR}" fill="{CHROME}" />

    <circle cx="24" cy="20" r="6" fill="#ff5f57" />
    <circle cx="46" cy="20" r="6" fill="#febc2e" />
    <circle cx="68" cy="20" r="6" fill="#28c840" />

    <rect x="96" y="0" width="152" height="{BAR}" fill="{BG}" />
    <rect x="96" y="0" width="152" height="2" fill="{KEYWORD}" />
    <rect x="112" y="14" width="13" height="13" rx="2.5" fill="#3178c6" />
    <text x="118.5" y="24" font-size="8" font-weight="700" fill="#fff" text-anchor="middle">TS</text>
    <text x="133" y="25" font-size="13" fill="{PUNCT}">khaled.ts</text>

    <rect x="0" y="{BAR}" width="52" height="{H - BAR}" fill="#1c1c1c" />

    {"".join(groups)}
    {"".join(carets)}
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{BORDER}" />
</svg>
'''


# --------------------------------------------------------------- stack.svg

GROUPS = [
    ("ai", [
        ("OpenAI GPT", "#10a37f"), ("LLM Integration", "#c586c0"),
        ("Prompt Engineering", "#9d7cd8"), ("RAG Pipelines", "#7aa2f7"),
    ]),
    ("cloud", [
        ("Cloud Run", "#4285f4"), ("Cloud Storage", "#34a853"), ("Cloud SQL", "#4285f4"),
        ("Firebase", "#ffca28"), ("Cloud Build", "#fbbc04"), ("Docker", "#2496ed"),
    ]),
    ("frontend", [
        ("TypeScript", "#3178c6"), ("React", "#61dafb"), ("Next.js", "#e5e5e5"),
        ("Tailwind CSS", "#38bdf8"), ("Vue 3", "#42b883"),
    ]),
    ("backend", [
        ("Python", "#3776ab"), ("FastAPI", "#059486"), ("Node.js", "#339933"),
        ("REST APIs", "#4ec9b0"), ("PostgreSQL", "#336791"), ("Supabase", "#3ecf8e"),
    ]),
]

CFS = 13              # chip font size
CCW = CFS * 0.6
CHIP_H = 30
CHIP_GAP = 9
ROW_GAP = 14
LABEL_X = 28
CHIP_X = 150
HEAD = 62
PAD_B = 22


def build_stack():
    rows = []
    y = HEAD
    for label, chips in GROUPS:
        rows.append(
            f'<text x="{LABEL_X}" y="{y + 20}" font-size="12" fill="{GUTTER}" '
            f'letter-spacing="1.4">{label.upper()}</text>'
        )
        x = CHIP_X
        for name, colour in chips:
            w = round(len(name) * CCW + 26)
            rows.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{CHIP_H}" rx="15" '
                f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45" />'
                f'<text x="{x + w / 2:.1f}" y="{y + 20}" font-size="{CFS}" fill="{colour}" '
                f'text-anchor="middle">{esc(name)}</text>'
            )
            x += w + CHIP_GAP
        y += CHIP_H + ROW_GAP

    h = y - ROW_GAP + PAD_B

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="{MONO}" role="img" aria-label="Stack: AI, cloud, frontend and backend tools Khaled works with">
  <rect width="{W}" height="{h}" rx="10" fill="{BG}" />
  <text x="{LABEL_X}" y="36" font-size="14">
    <tspan fill="{TEAL}">&#10095;</tspan><tspan fill="{PUNCT}"> khaled --stack</tspan>
  </text>
  {"".join(rows)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="10" fill="none" stroke="{BORDER}" />
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "hero.svg").write_text(build_hero(), encoding="utf-8")
    (OUT / "stack.svg").write_text(build_stack(), encoding="utf-8")
    print(f"wrote {OUT/'hero.svg'}\nwrote {OUT/'stack.svg'}")
