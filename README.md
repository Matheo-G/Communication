# Communication – Mathéo Gérardin

Supports de communication : cartes de visite et QR code.

## QR code

Le QR code ouvre directement le portfolio : **https://matheo-gerardin.fr**.
Fichiers : `cartes-de-visite/qr-code/qr-code.svg` (vectoriel) et `qr-code.png`.

## Cartes de visite

Format fini 85 × 55 mm. Les PDF font 91 × 61 mm (3 mm de fond perdu), page 1 = recto, page 2 = verso.

| Situation | Recto | Verso | PDF d'impression |
| --- | --- | --- | --- |
| En poste chez Onet | `cartes-de-visite/onet/recto.png` | `cartes-de-visite/onet/verso.png` | `cartes-de-visite/onet/carte-onet-impression.pdf` |
| En recherche de CDI | `cartes-de-visite/recherche/recto.png` | `cartes-de-visite/recherche/verso.png` | `cartes-de-visite/recherche/carte-recherche-impression.pdf` |

## Régénérer

```bash
pip install reportlab playwright opencv-python
python cartes-de-visite/src/build.py
```

Les textes, l'adresse du QR code et les couleurs se modifient en haut du script (`QR_URL`, `CONTACT`, `VARIANTES`). Le script vérifie que chaque QR code se lit.
