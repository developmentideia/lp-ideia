"""Otimiza SVGs exportados do Figma, sem dependências (só Python 3).

Uso:
    python3 scripts/otimizar-svg.py assets/img/icone-*.svg favicon.svg
    CASAS=3 python3 scripts/otimizar-svg.py assets/img/logo-ideia.svg assets/img/icone-whatsapp.svg

O que faz, sem mudar o desenho:
- arredonda as coordenadas para CASAS casas decimais (padrão 2). Use 3 nos
  arquivos com viewBox pequeno (logo e ícone do WhatsApp), onde 2 casas já
  deslocam alguns pixels de borda.
- troca os ids de gradiente do Figma por "<nome>-g0", "<nome>-g1"..., para
  não colidirem se mais de um SVG for embutido no mesmo HTML.
- passa cores hex para minúsculas e tira as quebras de linha entre tags.

Rode sobre o arquivo recém-exportado do Figma, não sobre um já otimizado.
"""
import re, sys, pathlib, os
CASAS = int(os.environ.get("CASAS", "2"))

def num(m):
    v = round(float(m.group(0)), CASAS)
    s = f"{v:.{CASAS}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""): s = "0"
    if s.startswith("0."): s = s[1:]
    elif s.startswith("-0."): s = "-" + s[2:]
    return s

for p in map(pathlib.Path, sys.argv[1:]):
    t = p.read_text()
    prefix = p.stem.replace("icone-", "").replace("logo-ideia", "logo")
    ids = re.findall(r'id="([^"]+)"', t)
    for i, old in enumerate(ids):
        new = f"{prefix}-g{i}"
        t = t.replace(f'id="{old}"', f'id="{new}"').replace(f"url(#{old})", f"url(#{new})")
    # números só em d, x1, y1, x2, y2 e offset; stroke-width fica como veio do Figma
    def attr(m):
        name, val = m.group(1), m.group(2)
        val = re.sub(r"-?\d*\.\d+|-?\d+", num, val)
        if name == "d":
            val = re.sub(r"\s*([MLHVCSQTAZmlhvcsqtaz])\s*", r"\1", val)
            val = re.sub(r" -", "-", val)
        return f'{name}="{val}"'
    t = re.sub(r'\b(d|x1|y1|x2|y2|offset)="([^"]*)"', attr, t)
    t = re.sub(r"#([0-9A-F]{6})", lambda m: "#" + m.group(1).lower(), t)
    t = re.sub(r">\s+<", "><", t).strip() + "\n"
    p.write_text(t)
    print(p.name, len(t))
