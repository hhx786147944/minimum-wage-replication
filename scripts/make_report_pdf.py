"""Render report/report.md to report.pdf (at the repository root).

A small, self-contained Markdown renderer for the constructs used in
``report/report.md``: headings, blockquotes, bullet/numbered lists, pipe tables,
fenced code, and inline ``**bold**`` / ``*italic*`` / `` `code` ``.

It uses fpdf2 and the system Arial font faces (regular/bold/italic) so the
special symbols used in the report (``≈ ≥ × − → – — § …``) render correctly.

Usage (from the project root)::

    python scripts/make_report_pdf.py

Output: ``report.pdf`` (repository root).

Note: the Arial font paths below are macOS system fonts. On other platforms,
point ``FONT_*`` at any TTF faces covering the characters used in the report
(e.g. DejaVu Sans / Liberation Sans).
"""
import re
from pathlib import Path

from fpdf import FPDF
from fpdf.fonts import FontFace

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "report" / "report.md"
OUT_PATH = ROOT / "report.pdf"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_BOLD_ITALIC = "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf"

PAGE_W, PAGE_H = 210.0, 297.0  # A4, mm
MARGIN = 16.0
BODY_W = PAGE_W - 2 * MARGIN

INK = (25, 25, 25)
MUTED = (120, 120, 120)


class ReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("F", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 4, "Minimum Wages and Employment - Replication of Card & Krueger (1994)",
                  align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("F", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, str(self.page_no()), align="C")


def register_fonts(pdf):
    pdf.add_font("F", "", FONT_REGULAR)
    pdf.add_font("F", "B", FONT_BOLD)
    pdf.add_font("F", "I", FONT_ITALIC)
    pdf.add_font("F", "BI", FONT_BOLD_ITALIC)


# --------------------------------------------------------------------------
# Markdown -> block list
# --------------------------------------------------------------------------

def _is_block_start(line):
    s = line.strip()
    return (s.startswith("#") or s.startswith(">") or s.startswith("```")
            or re.match(r"^(\s*[-*+]\s+|\s*\d+\.\s+)", s)
            or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s)
            or "|" in s)


def _split_table_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_blocks(text):
    lines = text.split("\n")
    blocks, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue

        if s.startswith("```"):
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append({"type": "code", "text": "\n".join(buf)})
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)),
                           "text": m.group(2).strip()})
            i += 1
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            blocks.append({"type": "hr"})
            i += 1
            continue

        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append({"type": "quote", "text": " ".join(buf)})
            continue

        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1].strip()):
            header = _split_table_row(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_table_row(lines[i]))
                i += 1
            blocks.append({"type": "table", "header": header, "rows": rows})
            continue

        if re.match(r"^(\s*[-*+]\s+|\s*\d+\.\s+)", s):
            items = []
            while i < n and re.match(r"^(\s*[-*+]\s+|\s*\d+\.\s+)", lines[i]):
                items.append(re.sub(r"^(\s*[-*+]\s+|\s*\d+\.\s+)", "", lines[i]).strip())
                i += 1
            blocks.append({"type": "list", "items": items})
            continue

        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not _is_block_start(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        blocks.append({"type": "para", "text": " ".join(buf)})
    return blocks


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def _plain(text):
    """Strip inline markers for plain-text contexts (width measurement)."""
    return text.replace("`", "").replace("**", "").replace("__", "")


def _column_widths(pdf, header, rows):
    cols = len(header)
    data = [header] + [r + [""] * (cols - len(r)) for r in rows]
    weights = []
    for c in range(cols):
        longest = max(len(_plain(r[c])) for r in data)
        weights.append(min(longest, 38) + 2.5)
    total = sum(weights)
    return [BODY_W * w / total for w in weights]


def render_table(pdf, header, rows):
    cols = len(header)
    header = header + [""] * max(0, cols - len(header))
    rows = [r + [""] * (len(header) - len(r)) for r in rows]
    widths = _column_widths(pdf, header, rows)

    with pdf.table(
        col_widths=tuple(widths),
        line_height=4.3,
        padding=1.2,
        text_align="LEFT",
        first_row_as_headings=True,
        headings_style=FontFace(emphasis="BOLD", fill_color=(236, 236, 236), color=(20, 20, 20)),
        markdown=True,
        repeat_headings=1,
    ) as table:
        table.row(header)
        for r in rows:
            table.row(r)
    pdf.ln(3)


def render(pdf, blocks):
    for b in blocks:
        t = b["type"]
        if t == "heading":
            sizes = {1: 15.5, 2: 12.0, 3: 10.5}
            pdf.set_font("F", "B", sizes.get(b["level"], 10.5))
            pdf.set_text_color(*INK)
            pdf.multi_cell(BODY_W, 6.2, _plain(b["text"]))
            pdf.ln(1.5)
        elif t == "para":
            pdf.set_font("F", "", 9.5)
            pdf.set_text_color(*INK)
            pdf.multi_cell(BODY_W, 4.7, b["text"].replace("`", ""), markdown=True)
            pdf.ln(1.5)
        elif t == "quote":
            pdf.set_font("F", "I", 8.8)
            pdf.set_text_color(90, 90, 90)
            pdf.set_x(MARGIN + 3)
            pdf.multi_cell(BODY_W - 3, 4.4, b["text"].replace("`", ""), markdown=True)
            pdf.set_x(MARGIN)
            pdf.ln(2)
        elif t == "list":
            pdf.set_font("F", "", 9.5)
            pdf.set_text_color(*INK)
            for it in b["items"]:
                pdf.set_x(MARGIN + 3)
                pdf.multi_cell(BODY_W - 3, 4.7, "•  " + it.replace("`", ""), markdown=True)
            pdf.ln(1.5)
        elif t == "code":
            pdf.set_font("F", "", 8.5)
            pdf.set_text_color(20, 20, 20)
            pdf.set_fill_color(244, 244, 244)
            pdf.multi_cell(BODY_W, 4.6, b["text"], fill=True)
            pdf.ln(2)
        elif t == "hr":
            y = pdf.get_y()
            pdf.set_draw_color(205, 205, 205)
            pdf.line(MARGIN, y, PAGE_W - MARGIN, y)
            pdf.ln(2)
        elif t == "table":
            render_table(pdf, b["header"], b["rows"])


def main():
    text = MD_PATH.read_text(encoding="utf-8")
    blocks = parse_blocks(text)

    pdf = ReportPDF(format="A4")
    register_fonts(pdf)
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_left_margin(MARGIN)
    pdf.set_right_margin(MARGIN)
    pdf.add_page()
    render(pdf, blocks)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT_PATH))
    print(f"wrote {OUT_PATH} ({len(blocks)} blocks, {pdf.page_no()} pages)")


if __name__ == "__main__":
    main()
