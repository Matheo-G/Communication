# Communication – Mathéo Gérardin

Supports de communication : cartes de visite et page de contact vers laquelle pointe le QR code.

## QR code

Le QR code des cartes ouvre la page de contact publiée par GitHub Pages :
**https://matheo-g.github.io/Communication/** (fichier `index.html`).

La page renvoie vers le portfolio, LinkedIn, l'e-mail et une fiche contact (`contact/matheo-gerardin.vcf`).
Pour changer une destination, modifie `index.html` : les cartes déjà imprimées restent valables.

Activation (une seule fois) : **Settings › Pages › Source : Deploy from a branch › Branch : `main` / `/ (root)`**.

## Cartes de visite

Format fini 85 × 55 mm. Les PDF font 91 × 61 mm (3 mm de fond perdu), page 1 = recto, page 2 = verso.

| Situation | Recto | Verso | PDF d'impression |
| --- | --- | --- | --- |
| En poste chez Onet | `cartes-de-visite/onet/recto.png` | `cartes-de-visite/onet/verso.png` | `cartes-de-visite/onet/carte-onet-impression.pdf` |
| En recherche de CDI | `cartes-de-visite/recherche/recto.png` | `cartes-de-visite/recherche/verso.png` | `cartes-de-visite/recherche/carte-recherche-impression.pdf` |

Le QR code seul : `cartes-de-visite/qr-code/qr-code.svg` (vectoriel) et `qr-code.png`.

## Régénérer

```bash
pip install reportlab playwright opencv-python
python cartes-de-visite/src/build.py
```

Les textes et couleurs se modifient dans `VARIANTES` et `CONTACT` en haut du script. Le script vérifie que chaque QR code se lit.
