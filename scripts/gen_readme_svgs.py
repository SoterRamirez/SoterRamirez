"""Genera los SVG del README de GitHub (marca SoterRamirez), versiones clara y oscura."""
import pathlib, sys
from xml.sax.saxutils import escape as esc

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

T = {
    "light": dict(bg="#F5F7FA", sup="#FFFFFF", linea="#D5DEE9", tinta="#0E1B2E", suave="#4A5A70",
                  pizarra="#1D3557", senal="#1F5FAE", sobre="#FFFFFF", logo_bg="#1D3557", logo_s="#F5F7FA",
                  raya="#F2B705", raya_txt="#8A6A00", chip_bg="#DCE8F6", chip_txt="#1D3557"),
    "dark": dict(bg="#0B1420", sup="#12203A", linea="#24344A", tinta="#E8EEF6", suave="#A7B6CA",
                 pizarra="#8FB3E0", senal="#6FA8EE", sobre="#0B1420", logo_bg="#0E1B2E", logo_s="#DCE8F6",
                 raya="#F2B705", raya_txt="#F2B705", chip_bg="#16263D", chip_txt="#8FB3E0"),
}
TITLE = "font-family:'Barlow Condensed','Arial Narrow','Roboto Condensed','Helvetica Neue',sans-serif;font-weight:700"
BODY = "font-family:Barlow,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "font-family:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
S_PATH = "M48 15H26.5a9.5 9.5 0 0 0 0 19h11a9.5 9.5 0 0 1 0 19H16"


def logo(c, x, y, s):
    return f'''<g transform="translate({x},{y}) scale({s})">
<rect width="64" height="64" rx="14" fill="{c['logo_bg']}"/>
<path d="{S_PATH}" fill="none" stroke="{c['logo_s']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<path d="{S_PATH}" fill="none" stroke="{c['raya']}" stroke-width="1.6" stroke-dasharray="3.2 3.2"/>
<circle cx="48" cy="15" r="4.6" fill="{c['logo_bg']}" stroke="{c['raya']}" stroke-width="2.4"/>
<circle cx="16" cy="53" r="5.2" fill="{c['raya']}" stroke="{c['logo_bg']}" stroke-width="1.6"/>
</g>'''


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>\n{body}\n</svg>\n')


def banner(c):
    b = f'''<rect width="1280" height="300" rx="16" fill="{c['sup']}" stroke="{c['linea']}" stroke-width="2"/>
<path d="M40 262H1240" stroke="{c['raya']}" stroke-width="5" stroke-dasharray="34 24"/>
{logo(c, 56, 48, 2.9)}
<text x="290" y="118" fill="{c['tinta']}" style="{TITLE};font-size:76px;letter-spacing:1px">SOTER RAMÍREZ</text>
<text x="292" y="162" fill="{c['suave']}" style="{BODY};font-size:28px">Dirección de proyectos y software para el transporte</text>
<rect x="292" y="186" width="330" height="48" rx="6" fill="{c['senal']}"/>
<text x="312" y="219" fill="{c['sobre']}" style="{BODY};font-size:24px;font-weight:600">De la fuente a la cabina</text>
<text x="648" y="219" fill="{c['raya_txt']}" style="{MONO};font-size:22px;letter-spacing:2px">LEO EL DOF POR TI</text>'''
    return svg(1280, 300, "Soter Ramírez · Dirección de proyectos y software para el transporte", b)


CARDS = [
    ("cotizador", "01", "Cotizador", ["Cotiza camiones FAW y es la fuente", "única de precios del negocio."], "Next.js · Prisma · Supabase"),
    ("odette", "02", "Odette", ["Agente de IA que atiende, califica", "y pasa los leads a un asesor."], "LLM · webhooks · CRM"),
    ("escuela", "03", "Escuela", ["Rutas de capacitación con video y", "progreso para vendedores nuevos."], "Next.js · video · progreso"),
    ("crm", "04", "CRM omnicanal", ["Bandeja, embudo y WhatsApp sobre", "una base de datos propia."], "TypeScript · PostgreSQL"),
]


def card(c, km, name, lines, stack):
    desc = "".join(f'<text x="32" y="{120 + i * 30}" fill="{c["suave"]}" style="{BODY};font-size:21px">{esc(l)}</text>' for i, l in enumerate(lines))
    b = f'''<rect x="1" y="1" width="598" height="238" rx="14" fill="{c['sup']}" stroke="{c['linea']}" stroke-width="2"/>
<rect x="32" y="30" width="78" height="30" rx="5" fill="{c['senal']}"/>
<text x="71" y="51" text-anchor="middle" fill="{c['sobre']}" style="{MONO};font-size:15px;font-weight:600">KM {km}</text>
<text x="126" y="58" fill="{c['tinta']}" style="{TITLE};font-size:38px">{esc(name)}</text>
{desc}
<text x="32" y="200" fill="{c['pizarra']}" style="{MONO};font-size:17px">{esc(stack)}</text>
<path d="M32 222H568" stroke="{c['raya']}" stroke-width="3" stroke-dasharray="16 11"/>'''
    return svg(600, 240, f"{name}: {' '.join(lines)} ({stack})", b)


STACK = ["Next.js", "TypeScript", "React", "NestJS", "Prisma", "Supabase", "PostgreSQL",
         "Docker", "Shopify", "Claude Code", "Ollama", "Scrum"]


def stack(c):
    x, y, parts = 0, 0, []
    for s in STACK:
        w = int(len(s) * 11.5 + 36)
        if x + w > 1240:
            x, y = 0, y + 56
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="8" fill="{c["chip_bg"]}"/>'
                     f'<text x="{x + w / 2}" y="{y + 28}" text-anchor="middle" fill="{c["chip_txt"]}" style="{BODY};font-size:20px;font-weight:600">{esc(s)}</text>')
        x += w + 12
    return svg(1240, y + 42, "Con qué trabajo: " + ", ".join(STACK), "\n".join(parts))


for mode, c in T.items():
    (OUT / f"banner-{mode}.svg").write_text(banner(c))
    (OUT / f"stack-{mode}.svg").write_text(stack(c))
    for slug, km, name, lines, st in CARDS:
        (OUT / f"card-{slug}-{mode}.svg").write_text(card(c, km, name, lines, st))
print("ok", sorted(p.name for p in OUT.iterdir()))
