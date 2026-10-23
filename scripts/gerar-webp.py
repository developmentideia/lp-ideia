"""Gera os WebP das ilustrações a partir dos PNGs exportados do Figma.

Uso (precisa de Pillow: pip install pillow):
    python3 scripts/gerar-webp.py <pasta-com-os-png>

Exporte do Figma, na página "LP IDeia · v09 · 5 breakpoints", frame de 1440,
cada camada "Ilustração / ..." em PNG 2x (a hero é "Ilustração / personagens
com computadores · transparente"), com o nome do arquivo igual à chave
de LARGURAS (hero.png, boy.png, girl.png, duo.png, 3d.png). Exceção: o boy
sai cortado do frame 1440; exporte o componente "IDeia DS/Asset/Menino" da
página "IDeia · Design System v1" (PNG de 1080 x 720).

Cada imagem sai em duas larguras (1x e 2x do tamanho exibido no desktop),
WebP qualidade 80, mantendo a transparência.
"""
import os
import sys

from PIL import Image

LARGURAS = {
    "hero": [400, 800, 1200, 1600],  # personagens com computadores, fundo transparente
    "boy": [540, 1080],
    "girl": [460, 920],
    "duo": [372, 744],
    "3d": [390, 780],
}
DESTINO = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

pasta = sys.argv[1]
for nome, larguras in LARGURAS.items():
    origem = os.path.join(pasta, f"{nome}.png")
    if not os.path.exists(origem):
        print(f"{nome}: {origem} não encontrado, pulando")
        continue
    im = Image.open(origem)
    for w in larguras:
        if w > im.width:
            print(f"{nome}: PNG com {im.width} px, menor que {w}; exporte em 2x")
            continue
        h = round(im.height * w / im.width)
        saida = os.path.join(DESTINO, f"{nome}-{w}.webp")
        im.resize((w, h), Image.LANCZOS).save(saida, "WEBP", quality=80, method=6, alpha_quality=90)
        print(f"{nome}-{w}.webp  {w}x{h}  {os.path.getsize(saida) / 1024:.1f} KB")
