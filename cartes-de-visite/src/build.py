"""Génère le QR code et les cartes de visite recto verso (PNG + PDF d'impression).

Dépendances : reportlab, playwright (Chromium ou Chrome), opencv-python pour la vérification.
Lancement depuis la racine du repo : python cartes-de-visite/src/build.py
"""
from pathlib import Path
from string import Template

import cv2
from playwright.sync_api import sync_playwright
from reportlab.graphics.barcode import qrencoder

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "cartes-de-visite"
QR_URL = "https://matheo-g.github.io/Communication/"

CONTACT = {
    "email": "gerardinmatheo@gmail.com",
    "linkedin": "linkedin.com/in/matheo-gerardin",
}

VARIANTES = {
    "onet": {
        "accent": "#2EC4C7",
        "surtitre": "UX/UI Designer",
        "ligne2": "Onet Airport Services",
        "ligne3": "Design system · Applications métier",
        "badge": "",
        "tag": "Vous",
    },
    "recherche": {
        "accent": "#F5A83C",
        "surtitre": "UX/UI &amp; Product Designer",
        "ligne2": "Île-de-France · mobile partout en France",
        "ligne3": "Design system · Outils métier · Recherche utilisateur",
        "badge": '<div class="badge"><span class="dot"></span>Disponible pour un CDI</div>',
        "tag": "Vous",
    },
}


def qr_svg(data: str, size_mm: float, module_color: str = "#111111") -> str:
    qr = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.M)
    qr.addData(data)
    qr.make()
    n = qr.getModuleCount()
    quiet = 4
    total = n + quiet * 2
    rects = []
    for r in range(n):
        for c in range(n):
            if qr.isDark(r, c):
                rects.append(f'<rect x="{c + quiet}" y="{r + quiet}" width="1" height="1"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total} {total}" '
        f'width="{size_mm}mm" height="{size_mm}mm" shape-rendering="crispEdges" role="img" '
        f'aria-label="QR code vers {data}">'
        f'<rect width="{total}" height="{total}" fill="#FFFFFF"/>'
        f'<g fill="{module_color}">{"".join(rects)}</g></svg>'
    )


CSS = Template("""
@page { size: 91mm 61mm; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; color: #F2F4F5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.face { position: relative; width: 91mm; height: 61mm; overflow: hidden; page-break-after: always;
  background-color: #1E1E1E; background-image: radial-gradient(#3A3A3A 0.28mm, transparent 0.3mm); background-size: 4mm 4mm; }
.trim { position: absolute; left: 3mm; top: 3mm; width: 85mm; height: 55mm; }
.safe { position: absolute; left: 7mm; top: 7mm; right: 7mm; bottom: 7mm; }
.mono { font-family: 'DejaVu Sans Mono', monospace; }
.label { font-size: 5.6pt; color: #0D99FF; }
.frame { position: relative; display: inline-block; padding: 1.4mm 3mm 2mm 3mm; border: 0.35mm solid #0D99FF; }
.h { position: absolute; width: 1.5mm; height: 1.5mm; background: #FFFFFF; border: 0.3mm solid #0D99FF; }
.tl { left: -0.95mm; top: -0.95mm; } .tr { right: -0.95mm; top: -0.95mm; }
.bl { left: -0.95mm; bottom: -0.95mm; } .br { right: -0.95mm; bottom: -0.95mm; }
.name { font-family: 'Lora', serif; font-size: 19pt; line-height: 1.05; letter-spacing: -0.01em; color: #FFFFFF; white-space: nowrap; }
.cursor { position: absolute; }
.tag { position: absolute; padding: 0.6mm 2mm; border-radius: 0.6mm 2.2mm 2.2mm 2.2mm; background: $accent; color: #0B0D10; font-size: 6.2pt; font-weight: 600; white-space: nowrap; }
.surtitre { font-size: 6.4pt; letter-spacing: 0.08em; text-transform: uppercase; color: $accent; }
.l2 { font-size: 8.4pt; color: #FFFFFF; font-weight: 500; }
.l3 { font-size: 6.6pt; color: #B4BBC3; }
.badge { align-self: flex-start; display: inline-flex; align-items: center; gap: 1.4mm; padding: 0.8mm 2.4mm; border-radius: 4mm; background: #14301F; border: 0.25mm solid #2E7D4F; font-size: 6.2pt; font-weight: 500; color: #D6F5E1; }
.dot { width: 1.6mm; height: 1.6mm; border-radius: 50%; background: #4ADE80; }
.contact { font-size: 7pt; line-height: 1.75; color: #FFFFFF; }
.contact .k { display: block; font-size: 5.4pt; letter-spacing: 0.08em; text-transform: uppercase; color: $accent; line-height: 1.2; margin-top: 2mm; }
.contact .k:first-child { margin-top: 0; }
.qrbox { position: relative; padding: 1.2mm; background: #FFFFFF; border-radius: 1.2mm; }
""")

RECTO = Template("""
<section class="face recto">
  <div class="trim"></div>
  <div class="safe" style="display:flex; flex-direction:column; justify-content:center; gap:2.4mm;">
    <div style="display:flex; align-items:center; gap:2.4mm;">
      <div class="surtitre mono">$surtitre</div>
    </div>
    <div>
      <div class="label mono" style="margin-bottom:1mm;">Nom</div>
      <div class="frame">
        <div class="name">Mathéo Gérardin</div>
        <span class="h tl"></span><span class="h tr"></span><span class="h bl"></span><span class="h br"></span>
        <svg class="cursor" width="3.6mm" height="3.6mm" viewBox="0 0 20 20" style="right:-4.6mm; bottom:-3.4mm;"><path d="M2 2 L17 8.2 L10.4 10.4 L8.2 17 Z" fill="$accent" stroke="#FFFFFF" stroke-width="1.5" stroke-linejoin="round"/></svg>
        <div class="tag" style="right:-12mm; bottom:-6mm;">$tag</div>
      </div>
    </div>
    <div style="margin-top:2.6mm; display:flex; flex-direction:column; gap:1mm;">
      <div class="l2">$ligne2</div>
      <div class="l3">$ligne3</div>
    </div>
    $badge
  </div>
</section>
""")

VERSO = Template("""
<section class="face verso">
  <div class="trim"></div>
  <div class="safe" style="display:flex; align-items:center; justify-content:space-between; gap:5mm;">
    <div class="contact">
      <span class="k mono">E-mail</span>$email
      <span class="k mono">LinkedIn</span>$linkedin
      <span class="k mono">Portfolio</span>Scannez le code
    </div>
    <div style="display:flex; flex-direction:column; align-items:center; gap:1.2mm;">
      <div class="label mono" style="align-self:flex-start;">Portfolio</div>
      <div class="frame" style="padding:0;">
        <div class="qrbox">$qr</div>
        <span class="h tl"></span><span class="h tr"></span><span class="h bl"></span><span class="h br"></span>
      </div>
    </div>
  </div>
</section>
""")


def page_html(faces: str, css: str) -> str:
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>{faces}</body></html>'


def build():
    qr_dir = OUT / "qr-code"
    qr_dir.mkdir(parents=True, exist_ok=True)
    (qr_dir / "qr-code.svg").write_text(qr_svg(QR_URL, 30), encoding="utf-8")
    qr_inline = qr_svg(QR_URL, 19)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        # QR seul en PNG
        page = browser.new_page(device_scale_factor=10)
        page.set_content(page_html(qr_svg(QR_URL, 30), "body{margin:0}svg{display:block}"))
        page.locator("svg").screenshot(path=str(qr_dir / "qr-code.png"))
        page.close()

        for nom, v in VARIANTES.items():
            css = CSS.substitute(accent=v["accent"])
            recto = RECTO.substitute(**v)
            verso = VERSO.substitute(qr=qr_inline, **CONTACT)
            dossier = OUT / nom
            dossier.mkdir(parents=True, exist_ok=True)
            (OUT / "src" / f"{nom}.html").write_text(page_html(recto + verso, css), encoding="utf-8")

            # PDF d'impression : 2 pages 91 x 61 mm (85 x 55 mm + 3 mm de fond perdu)
            page = browser.new_page()
            page.set_content(page_html(recto + verso, css))
            page.wait_for_timeout(300)
            page.pdf(path=str(dossier / f"carte-{nom}-impression.pdf"), width="91mm", height="61mm", print_background=True)
            page.close()

            # Aperçus PNG au format fini (85 x 55 mm, 300 dpi)
            page = browser.new_page(device_scale_factor=300 / 96, viewport={"width": 400, "height": 260})
            for face_nom, face in (("recto", recto), ("verso", verso)):
                page.set_content(page_html(face, css))
                page.wait_for_timeout(300)
                box = page.locator(".trim").bounding_box()
                page.screenshot(path=str(dossier / f"{face_nom}.png"), clip=box)
            page.close()
        browser.close()


def verify():
    det = cv2.QRCodeDetector()
    for path in [OUT / "qr-code" / "qr-code.png"] + [OUT / n / "verso.png" for n in VARIANTES]:
        data, _, _ = det.detectAndDecode(cv2.imread(str(path)))
        status = "OK" if data == QR_URL else f"ECHEC ({data!r})"
        print(f"{path.relative_to(ROOT)} : {status}")


if __name__ == "__main__":
    build()
    verify()
