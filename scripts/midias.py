#!/usr/bin/env python3
"""
Prepara as mídias do site preservando o máximo de qualidade possível.

Como usar
---------
1. Coloque seus arquivos originais na pasta `midias/`, nomeados com o nome do
   slot (a extensão pode ser qualquer uma):

       midias/hero.mp4          ou .mov, .mkv, .webm ...
       midias/card-petshop.jpg  ou .png, .heic, .webp, .tif ...

2. Rode:

       python3 scripts/midias.py

   Para mudar o nível de qualidade:

       python3 scripts/midias.py --qualidade maxima
       python3 scripts/midias.py --qualidade leve

3. Os arquivos otimizados são gravados em `images/`, que é o que o site usa.
   Seus originais em `midias/` nunca são alterados.

Princípios de qualidade aplicados
---------------------------------
* Nunca amplia. Se o original for menor que o alvo, mantém o tamanho original
  (ampliar só geraria borrão) e avisa que a imagem vai ficar mole na tela.
* JPEG com croma 4:4:4 (sem subamostragem), progressivo.
  4:4:4 preserva a cor nas bordas — é o que evita franja colorida em texto,
  pelo de animal e detalhe fino.
* PNG mantém transparência e é gravado sem perdas.
* Vídeo em H.264, preset slow, faststart, sem áudio (é fundo mudo).
* Metadados de rotação de celular são aplicados antes de redimensionar.
"""

import os
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "midias")
DESTINO = os.path.join(RAIZ, "images")

# ---------------------------------------------------------------------------
# Níveis de qualidade.
#
# `escala` multiplica o tamanho alvo de cada slot. `crf` é a compressão do
# vídeo (menor = melhor e mais pesado; cada -6 dobra o arquivo). `jpeg` é a
# qualidade das fotos.
#
# O padrão é `alta`, que já fica no ponto de retorno decrescente para web: daí
# para cima o arquivo cresce muito e a diferença na tela some. Use `maxima` se
# você tem tela 4K e prioriza fidelidade acima de tempo de carregamento.
# ---------------------------------------------------------------------------
NIVEIS = {
    "maxima": {"escala": 2.0, "crf": 16, "jpeg": 97,
               "resumo": "fidelidade acima de tudo; arquivos bem maiores"},
    "alta":   {"escala": 1.0, "crf": 20, "jpeg": 92,
               "resumo": "padrão; equilíbrio entre nitidez e carregamento"},
    "leve":   {"escala": 0.7, "crf": 25, "jpeg": 86,
               "resumo": "carregamento rápido; aceita perder algum detalhe"},
}
NIVEL_PADRAO = "alta"

# Preenchidos em main() a partir do nível escolhido.
JPEG_QUALIDADE = NIVEIS[NIVEL_PADRAO]["jpeg"]
VIDEO_CRF = NIVEIS[NIVEL_PADRAO]["crf"]
ESCALA = NIVEIS[NIVEL_PADRAO]["escala"]

# ---------------------------------------------------------------------------
# Os slots do site. `largura`/`altura` são o ALVO MÁXIMO (2x o tamanho real de
# exibição, para telas retina). `minimo` é a largura abaixo da qual a imagem
# começa a aparecer mole — o script avisa se o seu arquivo estiver abaixo disso.
# ---------------------------------------------------------------------------
SLOTS = [
    {
        "nome": "hero",
        "tipo": "video",
        "saida": "hero-video.mp4",
        "largura": 1920,
        "altura": 1080,
        "minimo": 1280,
        "onde": "Vídeo de fundo do topo da página (tela inteira)",
        "dica": "Filme na horizontal. O texto fica no canto inferior esquerdo — "
                "deixe essa área com pouca informação visual.",
        # O comercial original termina com um cartão de logo que entra em fade
        # a partir de 18,1s. Como aqui o vídeo roda em loop, esse cartão
        # apareceria e cortaria seco de volta para a primeira cena. Cortar
        # antes do fade deixa o loop limpo. Ajuste ou remova se trocar o vídeo.
        "cortar_em": 18.0,
        # Este slot fica atrás de um degradê escuro e de texto: é cenário, não
        # conteúdo que alguém assiste de perto. Comparando CRF 20/23/26 em
        # zoom 1:1 na etiqueta bordada (a textura mais fina do vídeo) não há
        # diferença visível, e CRF 20 custa 2,8 MB a mais. 23 é o ponto certo
        # aqui; os outros slots seguem o nível global.
        "crf": 23,
        # O material veio gerado por IA (Gemini/Veo) e traz a marca d'água em
        # estrela, estática, por volta de x 3400-3570 / y 1730-1920 no quadro
        # 4K. O filtro delogo apaga a estrela mas deixa um borrão retangular
        # pior que ela; recortar não deixa artefato nenhum. Esta janela 16:9
        # exclui a marca e ainda entrega 3076x1730, bem acima do 1080p final.
        # Remova esta linha se trocar por um vídeo sem marca.
        "recortar": "3076:1730:0:0",
    },
    {
        "nome": "hero-poster",
        "tipo": "imagem",
        "saida": "hero-poster.jpg",
        "largura": 1920,
        "altura": 1080,
        "minimo": 1280,
        "onde": "Primeiro quadro do topo (aparece enquanto o vídeo carrega)",
        "dica": "Se não existir, é gerado automaticamente a partir do vídeo.",
        "auto_do_video": "hero",
    },
    {
        "nome": "card-petshop",
        "tipo": "imagem",
        "saida": "card-petshop.jpg",
        "largura": 1400,
        "altura": 1400,
        "minimo": 900,
        "onde": 'Card "Não é lavanderia" (primeiro dos dois cards grandes)',
        "dica": "Enquadramento quadrado. O texto entra por baixo — deixe o "
                "terço inferior mais limpo.",
    },
    {
        "nome": "card-clinica",
        "tipo": "imagem",
        "saida": "card-clinica.jpg",
        "largura": 1400,
        "altura": 1400,
        "minimo": 900,
        "onde": 'Card "Higiene com protocolo" (segundo card grande)',
        "dica": "Enquadramento quadrado, mesmo cuidado com o terço inferior.",
    },
    {
        "nome": "cobertura-anapolis",
        "tipo": "imagem",
        "saida": "cobertura-anapolis.jpg",
        "largura": 1400,
        "altura": 1400,
        "minimo": 900,
        "onde": "Card de cobertura — Anápolis",
        "dica": "Enquadramento quadrado.",
    },
    {
        "nome": "cobertura-goiania",
        "tipo": "imagem",
        "saida": "cobertura-goiania.jpg",
        "largura": 1400,
        "altura": 1400,
        "minimo": 900,
        "onde": "Card de cobertura — Goiânia",
        "dica": "Enquadramento quadrado.",
    },
    {
        "nome": "logo",
        "tipo": "imagem",
        "saida": "logo-badge.png",
        "largura": 600,
        "altura": 600,
        "minimo": 300,
        "onde": "Logo no topo e no rodapé",
        "dica": "Pode mandar com fundo chapado — ele é recortado sozinho. "
                "O site é escuro, então a marca precisa funcionar sobre preto.",
        "preservar_alfa": True,
        # O logo vem sobre um fundo laranja chapado de mockup, que não faz
        # parte da marca. Chave de cor simples não serve: a toalha do próprio
        # logo é do mesmo laranja e sumiria junto. Ver remover_fundo().
        "remover_fundo": True,
    },
]

EXT_IMAGEM = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp",
              ".heic", ".heif", ".avif")
EXT_VIDEO = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v")

VERDE, AMARELO, VERMELHO, CINZA, RESET = (
    "\033[32m", "\033[33m", "\033[31m", "\033[90m", "\033[0m")


def remover_fundo(img, interno=26, externo=62):
    """Deixa transparente só o fundo que encosta na borda da imagem.

    Chave de cor comum (apagar todo pixel parecido com a cor de fundo) não
    serve aqui: a toalha do logo é do mesmo laranja do fundo, e some junto
    com parte do gato, do cachorro e da tagline. Este preenchimento parte das
    bordas e só se espalha por pixels contíguos parecidos com o fundo, então
    para no contorno branco do adesivo e preserva tudo que está dentro.

    A faixa entre `interno` e `externo` vira alpha parcial, para a borda ficar
    suave em vez de serrilhada.
    """
    import numpy as np

    rgb = img.convert("RGB")
    a = np.asarray(rgb).astype(np.int16)

    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    fundo = np.median(borda, axis=0)

    dist = np.sqrt(((a - fundo) ** 2).sum(axis=2))
    parecido = dist <= externo

    # Espalha a partir das bordas, só dentro de `parecido`.
    alcancado = np.zeros(parecido.shape, bool)
    alcancado[0, :] |= parecido[0, :]
    alcancado[-1, :] |= parecido[-1, :]
    alcancado[:, 0] |= parecido[:, 0]
    alcancado[:, -1] |= parecido[:, -1]
    while True:
        n = alcancado.copy()
        n[1:, :] |= alcancado[:-1, :]
        n[:-1, :] |= alcancado[1:, :]
        n[:, 1:] |= alcancado[:, :-1]
        n[:, :-1] |= alcancado[:, 1:]
        n &= parecido
        if (n == alcancado).all():
            break
        alcancado = n

    alpha = np.full(a.shape[:2], 255, np.uint8)
    rampa = np.clip((dist - interno) / (externo - interno), 0, 1) * 255
    alpha[alcancado] = rampa[alcancado].astype(np.uint8)

    from PIL import Image as _Image
    saida = _Image.fromarray(np.dstack([np.asarray(rgb), alpha]), "RGBA")
    caixa = saida.getbbox()
    return saida.crop(caixa) if caixa else saida


def alvo(slot):
    """Tamanho alvo do slot já ajustado pelo nível de qualidade escolhido."""
    return (int(slot["largura"] * ESCALA), int(slot["altura"] * ESCALA))


def achar_original(nome):
    """Procura midias/<nome>.<qualquer extensão>."""
    if not os.path.isdir(ORIGEM):
        return None
    for arquivo in sorted(os.listdir(ORIGEM)):
        base, ext = os.path.splitext(arquivo)
        if base.lower() == nome.lower() and ext.lower() in EXT_IMAGEM + EXT_VIDEO:
            return os.path.join(ORIGEM, arquivo)
    return None


def dimensoes_video(caminho):
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", caminho],
        capture_output=True, text=True).stdout.strip()
    try:
        largura, altura = saida.split("x")[:2]
        return int(largura), int(altura)
    except Exception:
        return None, None


def processar_imagem(origem, slot):
    from PIL import Image, ImageOps

    destino = os.path.join(DESTINO, slot["saida"])
    preservar_alfa = slot.get("preservar_alfa", False)

    try:
        img = Image.open(origem)
    except Exception as erro:
        # Formatos que o Pillow não abre (HEIC, por exemplo) passam pelo ffmpeg.
        temp = os.path.join(DESTINO, ".tmp-conversao.png")
        conv = subprocess.run(["ffmpeg", "-y", "-i", origem, "-update", "1",
                               "-frames:v", "1", temp],
                              capture_output=True, text=True)
        if conv.returncode != 0 or not os.path.exists(temp):
            return False, f"não foi possível abrir ({erro})"
        img = Image.open(temp)

    # Aplica a rotação gravada pelo celular antes de qualquer coisa.
    img = ImageOps.exif_transpose(img)
    largura_original, altura_original = img.size

    # Recorta o fundo chapado, se o slot pedir (ver remover_fundo).
    if slot.get("remover_fundo"):
        img = remover_fundo(img)

    # Redimensiona só para BAIXO. Ampliar não cria detalhe, só borra.
    img.thumbnail(alvo(slot), Image.LANCZOS)

    if preservar_alfa:
        img.save(destino, "PNG", optimize=True)
    else:
        if img.mode in ("RGBA", "LA", "P"):
            fundo = Image.new("RGB", img.size, (0, 0, 0))
            img = img.convert("RGBA")
            fundo.paste(img, mask=img.split()[-1])
            img = fundo
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(destino, "JPEG", quality=JPEG_QUALIDADE,
                 subsampling=0, optimize=True, progressive=True)

    temp = os.path.join(DESTINO, ".tmp-conversao.png")
    if os.path.exists(temp):
        os.remove(temp)

    aviso = None
    minimo = int(slot["minimo"] * ESCALA)
    if largura_original < minimo:
        aviso = (f"original tem só {largura_original}px de largura; "
                 f"o ideal é {minimo}px ou mais — vai aparecer mole")

    return True, aviso


def processar_video(origem, slot):
    destino = os.path.join(DESTINO, slot["saida"])
    largura_original, altura_original = dimensoes_video(origem)

    # scale só reduz: se já couber no alvo, mantém o tamanho original.
    alvo_l, alvo_a = alvo(slot)
    etapas = []
    # Recorte opcional, aplicado ANTES da escala (ver "recortar" no slot).
    if slot.get("recortar"):
        etapas.append(f"crop={slot['recortar']}")
    etapas.append(f"scale='min({alvo_l},iw)':'min({alvo_a},ih)'"
                  f":force_original_aspect_ratio=decrease:force_divisible_by=2")
    filtro = ",".join(etapas)

    cmd = ["ffmpeg", "-y", "-i", origem]
    # Corte opcional de duração (ver "cortar_em" na definição do slot).
    if slot.get("cortar_em"):
        cmd += ["-t", str(slot["cortar_em"])]
    cmd += ["-vf", filtro,
            "-c:v", "libx264", "-crf", str(slot.get("crf", VIDEO_CRF)),
            "-preset", "slow",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-an", destino]

    resultado = subprocess.run(cmd, capture_output=True, text=True)

    if resultado.returncode != 0:
        return False, resultado.stderr.strip().splitlines()[-1][:160]

    aviso = None
    minimo = int(slot["minimo"] * ESCALA)
    if largura_original and largura_original < minimo:
        aviso = (f"original tem só {largura_original}px de largura; "
                 f"o ideal é {minimo}px ou mais — vai aparecer mole")
    return True, aviso


def poster_do_video(slot):
    """Gera o poster a partir do vídeo do hero, se o usuário não mandou um."""
    video = os.path.join(DESTINO, "hero-video.mp4")
    if not os.path.exists(video):
        return False, "vídeo do hero não encontrado"
    destino = os.path.join(DESTINO, slot["saida"])
    resultado = subprocess.run(
        ["ffmpeg", "-y", "-ss", "0.5", "-i", video, "-frames:v", "1",
         "-q:v", "2", "-update", "1", destino],
        capture_output=True, text=True)
    if resultado.returncode != 0:
        return False, "falha ao extrair o quadro"
    return True, None


def tamanho(caminho):
    if not os.path.exists(caminho):
        return "—"
    bytes_ = os.path.getsize(caminho)
    return f"{bytes_/1024:.0f} KB" if bytes_ < 1024 * 1024 else f"{bytes_/1024/1024:.1f} MB"


def main():
    global JPEG_QUALIDADE, VIDEO_CRF, ESCALA

    import argparse
    ap = argparse.ArgumentParser(
        description="Prepara as mídias do site a partir dos originais em midias/.")
    ap.add_argument(
        "--qualidade", "-q", choices=list(NIVEIS), default=NIVEL_PADRAO,
        help="; ".join(f"{k}: {v['resumo']}" for k, v in NIVEIS.items()))
    args = ap.parse_args()

    nivel = NIVEIS[args.qualidade]
    JPEG_QUALIDADE = nivel["jpeg"]
    VIDEO_CRF = nivel["crf"]
    ESCALA = nivel["escala"]

    os.makedirs(ORIGEM, exist_ok=True)
    os.makedirs(DESTINO, exist_ok=True)

    print(f"\n  Lendo originais de {CINZA}midias/{RESET}")
    print(f"  Gravando otimizados em {CINZA}images/{RESET}")
    print(f"  Qualidade: {args.qualidade} {CINZA}— {nivel['resumo']}{RESET}\n")

    processados = feitos = avisos = 0

    for slot in SLOTS:
        origem = achar_original(slot["nome"])
        destino = os.path.join(DESTINO, slot["saida"])
        rotulo = f"  {slot['nome']:<20}"

        if origem is None:
            if slot.get("auto_do_video") and not os.path.exists(destino):
                ok, msg = poster_do_video(slot)
                if ok:
                    print(f"{rotulo} {VERDE}gerado do vídeo{RESET}  {tamanho(destino)}")
                    feitos += 1
                    continue
            estado = "mantido" if os.path.exists(destino) else "FALTANDO"
            cor = CINZA if os.path.exists(destino) else VERMELHO
            print(f"{rotulo} {cor}{estado}{RESET}"
                  f"{'  ' + tamanho(destino) if os.path.exists(destino) else ''}")
            continue

        processados += 1
        ext = os.path.splitext(origem)[1].lower()
        if slot["tipo"] == "video" or ext in EXT_VIDEO:
            ok, msg = processar_video(origem, slot)
        else:
            ok, msg = processar_imagem(origem, slot)

        if not ok:
            print(f"{rotulo} {VERMELHO}erro{RESET}  {msg}")
            continue

        feitos += 1
        print(f"{rotulo} {VERDE}ok{RESET}  {tamanho(destino)}"
              f"{CINZA}  ← {os.path.basename(origem)}{RESET}")
        if msg:
            avisos += 1
            print(f"  {' ':<20} {AMARELO}atenção:{RESET} {msg}")

    print()
    if processados == 0:
        print(f"  {AMARELO}Nenhum original encontrado em midias/.{RESET}")
        print(f"  Veja {CINZA}MIDIAS.md{RESET} para a lista de nomes de arquivo.\n")
    else:
        print(f"  {feitos} arquivo(s) gravado(s)"
              f"{f', {avisos} com aviso de resolução' if avisos else ''}.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
