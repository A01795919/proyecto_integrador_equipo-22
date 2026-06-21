"""Render profesional del Avance 7 con weasyprint + CSS APA.

Pipeline: Markdown -> HTML (pandoc) -> PDF (weasyprint).
Estilo APA: texto justificado, links azul subrayado, sangria francesa en
referencias, encabezado del equipo con saltos de linea claros.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Avance7_Equipo22_ResumenEjecutivo.md"
OUTPUT = ROOT / "Avance7.Equipo22.pdf"
CHART_PATH = ROOT / "_aa_detection_chart.png"


def generate_aa_detection_chart() -> Path:
    """Genera la Figura 1 (recuperacion de la clase AA) como PNG."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = [
        ("PLS-DA paper base", 0.00, "AA no clasificada"),
        ("Regresion Logistica", 0.38, "baseline interpretable"),
        ("Decision Tree", 0.55, "modelo individual"),
        ("Bagging Tree final", 0.78, "modelo elegido"),
        ("Top 15 candidato", 0.83, "validacion futura"),
    ]
    labels = [d[0] for d in data]
    values = [d[1] for d in data]
    notes = [d[2] for d in data]

    # Colores por valor (replica logica del script original)
    def color_for(v: float) -> str:
        if v >= 0.75:
            return "#15709a"
        if v >= 0.50:
            return "#4a8c52"
        if v > 0:
            return "#d18c2a"
        return "#b33333"

    colors = [color_for(v) for v in values]

    fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=160)
    bars = ax.barh(range(len(labels)), values, color=colors, height=0.55, edgecolor="white", linewidth=1.2)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10.5, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xticks([0, 0.25, 0.50, 0.75, 1.00])
    ax.set_xticklabels(["0.00", "0.25", "0.50", "0.75", "1.00"], fontsize=9)
    ax.set_xlabel("F1 reportado o estimado para la clase AA", fontsize=10, labelpad=8)
    ax.set_title(
        "Figura 1. Recuperacion de la clase preventiva AA\n"
        "Comparacion de desempeno reportado o estimado por etapa/modelo",
        fontsize=11.5, fontweight="bold", color="#1a3a6e", pad=14, loc="left"
    )

    # Valores al final de cada barra + nota debajo
    for i, (bar, v, note) in enumerate(zip(bars, values, notes)):
        ax.text(v + 0.012, bar.get_y() + bar.get_height() / 2,
                f"{v:.2f}", va="center", ha="left",
                fontsize=10, fontweight="bold", color="#1a3a6e")
        ax.text(-0.01, bar.get_y() + bar.get_height() + 0.08,
                note, va="top", ha="left",
                fontsize=8.5, style="italic", color="#555", transform=ax.transData)

    ax.set_facecolor("#f7faff")
    fig.patch.set_facecolor("white")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#bbb")
    ax.spines["bottom"].set_color("#bbb")
    ax.tick_params(axis="x", colors="#555")
    ax.tick_params(axis="y", colors="#1a1a1a")
    ax.grid(axis="x", color="#dde4ed", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    fig.text(0.02, 0.02,
             "Lectura: la mejora clave no es solo global; es recuperar AA, la ventana de prevencion.",
             fontsize=8.5, color="#444", style="italic")

    plt.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(CHART_PATH, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return CHART_PATH


# CSS profesional estilo APA
CSS = r"""
@page {
    size: Letter;
    margin: 2.54cm 2.54cm 2.54cm 2.54cm;

    @bottom-center {
        content: "Avance 7. Resumen ejecutivo - Equipo 22  |  Pagina " counter(page) " de " counter(pages);
        font-family: "Liberation Serif", "Times New Roman", serif;
        font-size: 9pt;
        color: #555;
    }
}

html, body {
    font-family: "Liberation Serif", "Times New Roman", "Georgia", serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a1a;
    text-align: justify;
    hyphens: auto;
}

/* Portada y encabezado del equipo */
.cover {
    text-align: center;
    margin-bottom: 1.5em;
}
.logo-block {
    text-align: center;
    margin: 0 0 1.2em 0;
}
.logo-block img {
    max-width: 280pt;
    height: auto;
    display: block;
    margin: 0 auto;
}
.cover h1 {
    font-size: 22pt;
    margin-bottom: 1em;
    color: #1a3a6e;
    border-bottom: 2pt solid #1a3a6e;
    padding-bottom: 0.4em;
    text-align: center;
}
.team-block {
    margin: 1em 0 1em 0;
    line-height: 1.45;
}
.team-block p {
    margin: 0.1em 0;
    text-align: center;
}
.team-block strong {
    font-size: 12pt;
}
.advisor-block {
    margin: 0.6em 0 1.2em 0;
    padding: 0.5em 0;
    border-top: 0.5pt solid #c5cfdb;
    border-bottom: 0.5pt solid #c5cfdb;
}
.advisor-block p {
    margin: 0.1em 0;
    text-align: center;
    font-size: 10.5pt;
}
.advisor-block p:first-child {
    color: #555;
    font-size: 9.5pt;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.advisor-block p:last-child {
    font-size: 11.5pt;
    font-style: italic;
    color: #1a3a6e;
}
.meta-block p {
    margin: 0.2em 0;
    text-align: center;
    font-size: 10pt;
    color: #444;
}

/* Encabezados */
h1 {
    font-size: 18pt;
    color: #1a3a6e;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    text-align: left;
    border-bottom: 1pt solid #1a3a6e;
    padding-bottom: 0.2em;
    page-break-after: avoid;
}
h2 {
    font-size: 14pt;
    color: #1a3a6e;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    text-align: left;
    page-break-after: avoid;
}
h3 {
    font-size: 11.5pt;
    color: #234876;
    margin-top: 1em;
    margin-bottom: 0.3em;
    text-align: left;
    font-style: italic;
    page-break-after: avoid;
}
h4, h5 {
    font-size: 11pt;
    color: #234876;
    margin-top: 0.8em;
    margin-bottom: 0.2em;
    page-break-after: avoid;
}

/* Parrafos */
p {
    margin: 0.4em 0 0.7em 0;
    orphans: 3;
    widows: 3;
}

/* Listas */
ul, ol {
    margin: 0.4em 0 0.8em 1.5em;
    padding-left: 0.5em;
}
li {
    margin: 0.2em 0;
    text-align: justify;
}

/* Enlaces (links) - estilo APA, azul y subrayado */
a, a:visited {
    color: #1d4a8f;
    text-decoration: underline;
    word-break: break-word;
}

/* Codigo inline y bloques */
code {
    font-family: "Menlo", "Consolas", monospace;
    font-size: 9.5pt;
    background-color: #f0f3f7;
    padding: 0.05em 0.3em;
    border-radius: 2pt;
    color: #34495e;
}
pre {
    background-color: #f0f3f7;
    border: 1pt solid #d4d9e0;
    padding: 0.6em 0.8em;
    border-radius: 3pt;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.3;
    text-align: left;
    page-break-inside: avoid;
}
pre code {
    background: none;
    padding: 0;
    border-radius: 0;
}

/* Tablas - estilo APA simplificado */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0 1.2em 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
thead {
    background-color: #1a3a6e;
    color: white;
}
th, td {
    padding: 0.5em 0.6em;
    text-align: left;
    vertical-align: top;
    border-bottom: 0.5pt solid #bbb;
}
th {
    font-weight: bold;
    border-bottom: 1.5pt solid #1a3a6e;
    text-align: left;
}
tbody tr:nth-child(even) {
    background-color: #f7f9fc;
}
tbody tr:last-child td {
    border-bottom: 1pt solid #1a3a6e;
}

/* Citas (blockquotes) */
blockquote {
    border-left: 3pt solid #1a3a6e;
    margin: 0.8em 0;
    padding: 0.4em 0.9em;
    background-color: #f7f9fc;
    font-style: italic;
    color: #333;
    page-break-inside: avoid;
}
blockquote p {
    margin: 0.3em 0;
}

/* Negritas y enfasis */
strong, b {
    color: #1a1a1a;
    font-weight: bold;
}
em, i {
    font-style: italic;
}

/* Seccion de referencias con sangria francesa APA */
.references {
    margin-top: 1em;
}
.references p {
    padding-left: 0.5in;
    text-indent: -0.5in;
    margin: 0.5em 0 0.5em 0;
    text-align: left;
    line-height: 1.5;
}

/* Saltos de pagina y control de huerfanos */
.section {
    page-break-before: auto;
}

/* Figuras (graficos generados) */
.figure-block {
    margin: 1em 0 1.4em 0;
    text-align: center;
    page-break-inside: avoid;
}
.figure-block img {
    max-width: 100%;
    height: auto;
    border: 0.5pt solid #c5cfdb;
    border-radius: 3pt;
    box-shadow: 0 1pt 2pt rgba(0,0,0,0.04);
    background: white;
}
"""


def normalize_md(raw: str) -> str:
    """Aplica ajustes especificos al markdown para mejor render HTML.

    - Anade un `<div class="cover">` alrededor del titulo y bloque de equipo.
    - Marca la seccion de referencias con `<div class="references">` para
      que la sangria francesa se aplique solo ahi.
    """
    lines = raw.splitlines()
    out: list[str] = []

    # Construir bloque de portada (titulo + equipo + meta)
    in_header = True
    cover_buffer: list[str] = []
    body_started = False

    i = 0
    while i < len(lines):
        line = lines[i]

        if in_header and line.strip().startswith("# "):
            # Titulo principal con logo arriba
            cover_buffer.append(f'<div class="cover">')
            cover_buffer.append(f'<div class="logo-block"><img src="logo_tec.jpeg" alt="Tecnologico de Monterrey" /></div>')
            cover_buffer.append(f'<h1>{line.lstrip("# ").strip()}</h1>')
            # Buscar bloque de equipo (lineas con ** y nombres) hasta primera ##
            j = i + 1
            team_lines: list[str] = []
            meta_lines: list[str] = []
            while j < len(lines) and not lines[j].strip().startswith("## "):
                s = lines[j].strip()
                if s.startswith("**Equipo"):
                    team_lines.append(f'<p><strong>{s.replace("**", "")}</strong></p>')
                elif " - A0" in s:
                    # Nombre - matricula
                    team_lines.append(f'<p>{s}</p>')
                elif s.startswith("**Proyecto:**") or s.startswith("**Fecha:**") or s.startswith("**Entregable:**"):
                    meta_lines.append(f'<p>{s.replace("**", "")}</p>')
                j += 1
            if team_lines:
                cover_buffer.append('<div class="team-block">')
                cover_buffer.extend(team_lines)
                cover_buffer.append('</div>')
            # Asesora
            cover_buffer.append('<div class="advisor-block">')
            cover_buffer.append('<p><strong>Asesora del proyecto:</strong></p>')
            cover_buffer.append('<p>Dra. Grettel Barceló Alonso</p>')
            cover_buffer.append('</div>')
            if meta_lines:
                cover_buffer.append('<div class="meta-block">')
                cover_buffer.extend(meta_lines)
                cover_buffer.append('</div>')
            cover_buffer.append('</div>')
            out.extend(cover_buffer)
            i = j
            in_header = False
            body_started = True
            continue

        # Reemplazar placeholder de la Figura 1 por bloque HTML con imagen
        if line.strip() == "[[CHART:AA_DETECTION]]":
            out.append('<div class="figure-block">')
            out.append(f'<img src="{CHART_PATH.name}" alt="Figura 1. Recuperacion de la clase preventiva AA" />')
            out.append('</div>')
            i += 1
            continue

        # Detectar inicio de seccion de referencias
        if line.strip().startswith("## ") and "Referencias" in line:
            out.append('<div class="references">')
            out.append(line)
            i += 1
            # Hasta el final del documento, todo es referencias
            while i < len(lines):
                out.append(lines[i])
                i += 1
            out.append('</div>')
            break

        out.append(line)
        i += 1

    return "\n".join(out)


def md_to_html(md_text: str) -> str:
    """Convierte markdown a HTML usando pandoc."""
    proc = subprocess.run(
        ["pandoc", "-f", "markdown+pipe_tables+yaml_metadata_block", "-t", "html5", "--no-highlight"],
        input=md_text.encode("utf-8"),
        capture_output=True,
        check=True,
    )
    return proc.stdout.decode("utf-8")


def linkify_references(html: str) -> str:
    """Convierte URLs y DOIs sin envoltura en links clickables, dentro
    de la seccion de referencias."""
    # Si pandoc no convirtio URLs en links (porque estan en texto sin <>),
    # detectamos URLs sueltas y las envolvemos en <a>.
    url_pattern = re.compile(r"(?<!href=\")(?<!\")(https?://[^\s<]+)")
    def repl(m: re.Match) -> str:
        url = m.group(1).rstrip(".,;)")
        return f'<a href="{url}">{url}</a>'
    return url_pattern.sub(repl, html)


def build_full_html(body_html: str) -> str:
    """Construye el documento HTML completo con el CSS embebido."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Avance 7. Resumen ejecutivo - Equipo 22</title>
<style>{CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def main() -> None:
    # 1. Generar la Figura 1 (chart AA detection) como PNG
    generate_aa_detection_chart()

    md_raw = SOURCE.read_text(encoding="utf-8")
    md_processed = normalize_md(md_raw)
    body_html = md_to_html(md_processed)
    body_html = linkify_references(body_html)
    full_html = build_full_html(body_html)

    html_path = ROOT / "Avance7_render.html"
    html_path.write_text(full_html, encoding="utf-8")

    # weasyprint
    from weasyprint import HTML
    HTML(string=full_html, base_url=str(ROOT)).write_pdf(str(OUTPUT))
    print(f"PDF generado: {OUTPUT}")


if __name__ == "__main__":
    main()
