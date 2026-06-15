"""
Genera el icono de la aplicación (assets/lca_icon.ico) y una vista previa PNG.

Tema: energía solar comunitaria — un sol sobre un horizonte, en verde
sostenibilidad. Se exporta como .ico multitamaño para el acceso directo de
escritorio.

Uso:  python tools/crear_icono.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
ASSETS.mkdir(exist_ok=True)

S = 256  # lienzo base


def _gradiente_vertical(c_top, c_bot):
    base = Image.new("RGB", (1, S))
    for y in range(S):
        t = y / (S - 1)
        base.putpixel((0, y), tuple(int(c_top[i] * (1 - t) + c_bot[i] * t) for i in range(3)))
    return base.resize((S, S))


def construir():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # Fondo: cuadrado redondeado con gradiente verde -> teal.
    grad = _gradiente_vertical((46, 170, 110), (18, 110, 100)).convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=58, fill=255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    cx, cy = 128, 116
    blanco = (255, 255, 255, 255)
    sol = (255, 206, 84, 255)

    # Rayos del sol (con punta redondeada).
    r0, r1, w = 60, 96, 13
    for k in range(12):
        a = math.radians(k * 30)
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=blanco, width=w)
        d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=blanco)

    # Núcleo del sol.
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=sol)
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=blanco, width=6)

    # Horizonte / base comunitaria.
    d.rounded_rectangle([52, 198, 204, 216], radius=9, fill=(255, 255, 255, 240))
    d.rounded_rectangle([84, 224, 172, 238], radius=7, fill=(255, 255, 255, 175))

    return img


def main():
    img = construir()
    ico = ASSETS / "lca_icon.ico"
    png = ASSETS / "lca_icon.png"
    img.save(ico, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    img.save(png)
    print("Icono:", ico)
    print("Vista previa:", png)


if __name__ == "__main__":
    main()
