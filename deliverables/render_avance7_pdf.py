from __future__ import annotations

import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Avance7_Equipo22_ResumenEjecutivo.md"
OUTPUT = ROOT / "Avance7.Equipo22.pdf"

PAGE_W, PAGE_H = 595, 842
LEFT, RIGHT, TOP, BOTTOM = 54, 54, 54, 54
TEXT_W = PAGE_W - LEFT - RIGHT


def normalize(text: str) -> str:
    replacements = {
        "≥": ">=",
        "≤": "<=",
        "≈": "~",
        "→": "->",
        "—": "-",
        "–": "-",
        "×": "x",
        "χ": "chi",
        "²": "2",
        "λ": "lambda",
        "Δ": "Delta",
        "μ": "mu",
        "σ": "sigma",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"\*\*|`|<nobr>|</nobr>", "", text)
    return text


def pdf_escape(text: str) -> bytes:
    data = normalize(text).encode("cp1252", errors="replace")
    out = bytearray()
    for b in data:
        if b in (40, 41, 92):
            out.append(92)
            out.append(b)
        elif b in (10, 13):
            out.append(32)
        else:
            out.append(b)
    return bytes(out)


class SimplePdf:
    def __init__(self):
        self.pages: list[list[tuple[str, int, int, int, str]]] = []
        self.current: list[tuple[str, int, int, int, str]] = []
        self.y = TOP
        self.page_no = 0
        self.new_page()

    def new_page(self):
        if self.current:
            self._footer()
            self.pages.append(self.current)
        self.current = []
        self.y = TOP
        self.page_no += 1

    def _footer(self):
        self.add_raw(
            "Avance 7. Resumen ejecutivo - Equipo 22 | Pagina "
            f"{self.page_no}",
            8,
            PAGE_H - 28,
            "regular",
            align="center",
            width=PAGE_W,
        )

    def ensure(self, height: int):
        if self.y + height > PAGE_H - BOTTOM:
            self.new_page()

    def add_raw(self, text: str, size: int, y_from_top: int, font: str, align: str = "left", width: int = TEXT_W):
        self.current.append((text, size, y_from_top, LEFT if align == "left" else 0, font if align == "left" else f"{font}|{align}|{width}"))

    def draw(self, command: str):
        self.current.append((command, 0, 0, 0, "__raw__"))

    def text(self, text: str, size: int = 10, font: str = "regular", before: int = 0, after: int = 7, indent: int = 0):
        text = normalize(text).strip()
        if not text:
            self.y += after
            return
        self.y += before
        width_chars = max(35, int((TEXT_W - indent) / (size * 0.50)))
        lines: list[str] = []
        for raw in text.splitlines():
            prefix = ""
            s = raw.strip()
            if s.startswith("- "):
                prefix = "- "
                s = s[2:].strip()
            elif re.match(r"^\d+\. ", s):
                m = re.match(r"^\d+\. ", s)
                prefix = m.group(0)
                s = s[len(prefix):].strip()
            wrapped = textwrap.wrap(s, width=width_chars, subsequent_indent=" " * len(prefix)) or [""]
            lines.extend([prefix + wrapped[0], *wrapped[1:]])
        line_h = int(size * 1.35)
        self.ensure(len(lines) * line_h + after + before)
        for line in lines:
            self.current.append((line, size, self.y, LEFT + indent, font))
            self.y += line_h
        self.y += after

    def heading(self, text: str, level: int):
        clean = normalize(text.lstrip("#").strip())
        if level == 1:
            self.text(clean, 18, "bold", before=0, after=14)
        elif level == 2:
            self.text(clean, 13, "bold", before=8, after=8)
        else:
            self.text(clean, 11, "bold", before=5, after=6)

    def table(self, rows: list[list[str]]):
        if not rows:
            return
        self.ensure(24)
        cols = max(len(r) for r in rows)
        col_chars = {2: 39, 3: 25, 4: 18, 5: 14}.get(cols, 12)
        line_h = 10
        for idx, row in enumerate(rows):
            row = [normalize(c.strip()) for c in row] + [""] * (cols - len(row))
            cell_lines = [textwrap.wrap(c, width=col_chars) or [""] for c in row]
            height = max(len(c) for c in cell_lines)
            self.ensure(height * line_h + 8)
            if idx == 0:
                self.current.append(("-" * 96, 7, self.y, LEFT, "mono"))
                self.y += line_h
            for i in range(height):
                parts = [(cell[i] if i < len(cell) else "").ljust(col_chars) for cell in cell_lines]
                line = " | ".join(parts)
                self.current.append((line[:120], 7, self.y, LEFT, "mono_bold" if idx == 0 else "mono"))
                self.y += line_h
            if idx == 0:
                self.current.append(("-" * 96, 7, self.y, LEFT, "mono"))
                self.y += line_h
        self.current.append(("-" * 96, 7, self.y, LEFT, "mono"))
        self.y += 16

    def aa_detection_chart(self):
        data = [
            ("PLS-DA paper base", 0.00, "AA no clasificada"),
            ("Regresion Logistica", 0.38, "baseline interpretable"),
            ("Decision Tree", 0.55, "modelo individual"),
            ("Bagging Tree final", 0.78, "modelo elegido"),
            ("Top 15 candidato", 0.83, "validacion futura"),
        ]
        height = 240
        self.ensure(height + 16)
        top = self.y + 4
        x0, y0 = LEFT, PAGE_H - (top + height)
        w = TEXT_W
        self.draw(f"q 0.965 0.980 0.995 rg {x0} {y0} {w} {height} re f Q")
        self.draw(f"q 0.650 0.720 0.790 RG 0.7 w {x0} {y0} {w} {height} re S Q")
        self.add_raw("Figura 1. Recuperacion de la clase preventiva AA", 11, top + 14, "bold")
        self.add_raw("Comparacion de desempeno reportado o estimado por etapa/modelo", 8, top + 29, "regular")

        label_x = x0 + 18
        bar_x = x0 + 185
        bar_w = 250
        bar_h = 16
        base_top = top + 60
        for tick in [0, 0.25, 0.50, 0.75, 1.00]:
            x = bar_x + tick * bar_w
            self.draw(f"q 0.82 0.86 0.90 RG 0.4 w {x:.1f} {PAGE_H - (base_top + 135):.1f} m {x:.1f} {PAGE_H - (base_top - 8):.1f} l S Q")
            self.add_raw(f"{tick:.2f}", 7, base_top + 142, "regular", align="left")
            self.current[-1] = (self.current[-1][0], self.current[-1][1], self.current[-1][2], int(x - 9), self.current[-1][4])

        for idx, (label, value, note) in enumerate(data):
            y_top = base_top + idx * 28
            y_pdf = PAGE_H - (y_top + bar_h)
            self.add_raw(label, 8, y_top + 2, "bold")
            self.current[-1] = (self.current[-1][0], self.current[-1][1], self.current[-1][2], label_x, self.current[-1][4])
            self.add_raw(note, 7, y_top + 13, "regular")
            self.current[-1] = (self.current[-1][0], self.current[-1][1], self.current[-1][2], label_x, self.current[-1][4])
            self.draw(f"q 0.90 0.93 0.96 rg {bar_x} {y_pdf:.1f} {bar_w} {bar_h} re f Q")
            fill = value * bar_w
            if value >= 0.75:
                color = "0.08 0.42 0.60"
            elif value >= 0.50:
                color = "0.28 0.55 0.32"
            elif value > 0:
                color = "0.82 0.55 0.16"
            else:
                color = "0.70 0.20 0.20"
            self.draw(f"q {color} rg {bar_x} {y_pdf:.1f} {fill:.1f} {bar_h} re f Q")
            self.add_raw(f"{value:.2f}", 8, y_top + 3, "bold")
            self.current[-1] = (self.current[-1][0], self.current[-1][1], self.current[-1][2], int(bar_x + bar_w + 12), self.current[-1][4])

        self.add_raw("Lectura: la mejora clave no es solo global; es recuperar AA, la ventana de prevencion.", 8, top + 215, "regular")
        self.y += height + 14

    def finish(self):
        if self.current:
            self._footer()
            self.pages.append(self.current)
            self.current = []

    def save(self, path: Path):
        self.finish()
        objects: list[bytes] = []

        def add(obj: bytes) -> int:
            objects.append(obj)
            return len(objects)

        catalog_id = add(b"")
        pages_id = add(b"")
        font_regular = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        font_bold = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        font_mono = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
        font_mono_bold = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>")
        page_ids = []
        for page in self.pages:
            chunks = []
            for text, size, y_top, x, font in page:
                if font == "__raw__":
                    chunks.append(text.encode("ascii"))
                    continue
                font_name = {
                    "regular": "F1",
                    "bold": "F2",
                    "mono": "F3",
                    "mono_bold": "F4",
                }.get(font.split("|")[0], "F1")
                y = PAGE_H - y_top
                if "|" in font:
                    base, align, width = font.split("|")
                    width = int(width)
                    approx = len(normalize(text)) * size * 0.48
                    x = (width - approx) / 2 if align == "center" else LEFT
                    font_name = {"regular": "F1", "bold": "F2"}.get(base, "F1")
                chunks.append(b"BT " + f"/{font_name} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ".encode("ascii") + b"(" + pdf_escape(text) + b") Tj ET")
            stream = b"\n".join(chunks)
            content_id = add(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
            page_id = add(
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
                f"/Resources << /Font << /F1 {font_regular} 0 R /F2 {font_bold} 0 R /F3 {font_mono} 0 R /F4 {font_mono_bold} 0 R >> >> "
                f"/Contents {content_id} 0 R >>".encode("ascii")
            )
            page_ids.append(page_id)

        kids = " ".join(f"{pid} 0 R" for pid in page_ids).encode("ascii")
        objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii")
        objects[pages_id - 1] = b"<< /Type /Pages /Kids [" + kids + b"] /Count " + str(len(page_ids)).encode("ascii") + b" >>"

        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for idx, obj in enumerate(objects, start=1):
            offsets.append(len(output))
            output.extend(f"{idx} 0 obj\n".encode("ascii"))
            output.extend(obj)
            output.extend(b"\nendobj\n")
        xref = len(output)
        output.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
        output.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            output.extend(f"{off:010d} 00000 n \n".encode("ascii"))
        output.extend(
            b"trailer\n"
            + f"<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
        )
        path.write_bytes(output)


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        parts = [p.strip() for p in lines[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", p.replace(" ", "")) for p in parts):
            rows.append(parts)
        i += 1
    return rows, i


def main():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    pdf = SimplePdf()
    paragraph: list[str] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("|"):
            if paragraph:
                pdf.text(" ".join(paragraph))
                paragraph = []
            rows, i = parse_table(lines, i)
            pdf.table(rows)
            continue
        if stripped == "[[CHART:AA_DETECTION]]":
            if paragraph:
                pdf.text(" ".join(paragraph))
                paragraph = []
            pdf.aa_detection_chart()
            i += 1
            continue
        if stripped.startswith("#"):
            if paragraph:
                pdf.text(" ".join(paragraph))
                paragraph = []
            level = len(stripped) - len(stripped.lstrip("#"))
            pdf.heading(stripped, level)
        elif stripped == "":
            if paragraph:
                pdf.text(" ".join(paragraph))
                paragraph = []
        else:
            paragraph.append(stripped)
        i += 1
    if paragraph:
        pdf.text(" ".join(paragraph))
    pdf.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
