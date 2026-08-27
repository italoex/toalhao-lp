#!/usr/bin/env python3
"""
Recupera fotos que chegaram comprimidas (WhatsApp, print de tela, download de
rede social) para uso nos cards do site.

Não inventa resolução. O que dá para fazer numa foto já comprimida é:

  1. tirar o quadriculado da compressão, que é o que mais chama atenção nas
     áreas lisas (céu, parede, carroceria);
  2. corrigir o dominante de cor, quando ele é mensurável;
  3. ampliar com um filtro decente, em vez de deixar o navegador esticar;
  4. devolver micro-contraste, sem halo.

O ganho é real, mas tem teto. Arquivo grande de origem continua sendo a única
forma de ter detalhe de verdade.

Uso:
    python3 scripts/realce-foto.py entrada.png saida.png --lado 1200 \
        --amostra 0.40,0.52,0.62,0.60 --forca-cor 0.7
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def corrigir_dominante(img, amostra, forca):
    """
    Neutraliza o dominante de cor usando uma região que se sabe branca —
    tipicamente a carroceria do veículo.

    Corrige só uma fração do desvio. Zerar o dominante deixa a foto chapada e
    com cara de tratada: parte do azul numa carroceria à sombra é o céu
    refletido, e isso é informação verdadeira da cena.
    """
    arr = np.asarray(img.convert("RGB")).astype(np.float64)
    h, w, _ = arr.shape
    x0, y0, x1, y1 = amostra
    reg = arr[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    if reg.size == 0:
        return img, None

    # dentro da amostra, os 20% mais claros são o branco de referência
    lum = reg.mean(axis=2)
    branco = reg[lum >= np.percentile(lum, 80)].mean(axis=0)
    if branco.min() <= 0:
        return img, None

    ganho = branco.mean() / branco          # levaria o branco ao neutro
    ganho = 1.0 + (ganho - 1.0) * forca     # aplica só parte do caminho
    return Image.fromarray(
        np.clip(arr * ganho, 0, 255).astype(np.uint8)), ganho


def tratar(entrada, saida, lado, amostra, forca_cor):
    img = Image.open(entrada)
    origem_lado = min(img.size)

    if amostra:
        img, ganho = corrigir_dominante(img, amostra, forca_cor)
        if ganho is not None:
            print("  cor: ganho R=%.3f G=%.3f B=%.3f" % tuple(ganho))

    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    try:
        img.save(tmp.name)

        # fspp  desfaz o quadriculado da compressão
        # nlmeans tira o ruído sem comer as bordas (s baixo: conservador)
        # lanczos amplia melhor que o esticamento do navegador
        # cas    devolve micro-contraste sem criar halo, como o unsharp cria
        filtros = (
            "fspp=5,"
            "nlmeans=s=1.0:p=5:r=11,"
            f"scale={lado}:{lado}:flags=lanczos,"
            "cas=0.45"
        )
        subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-i", tmp.name,
             "-vf", filtros, "-q:v", "1", saida, "-y"],
            check=True)
    finally:
        os.unlink(tmp.name)

    if lado > origem_lado:
        print(f"  atenção: ampliado de {origem_lado}px para {lado}px. "
              f"O tratamento limpa defeito de compressão, não cria detalhe.")
    print(f"  gravado: {saida}")


def fracoes(texto):
    partes = [float(v) for v in texto.split(",")]
    if len(partes) != 4:
        raise argparse.ArgumentTypeError("use x0,y0,x1,y1 em frações de 0 a 1")
    return partes


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--lado", type=int, default=1200,
                   help="lado do quadrado de saída (padrão: 1200)")
    p.add_argument("--amostra", type=fracoes, default=None,
                   help="região branca de referência, x0,y0,x1,y1 em frações")
    p.add_argument("--forca-cor", type=float, default=0.7,
                   help="quanto do dominante corrigir, de 0 a 1 (padrão: 0.7)")
    a = p.parse_args()

    if not os.path.isfile(a.entrada):
        sys.exit(f"não encontrei {a.entrada}")
    print(os.path.basename(a.entrada))
    tratar(a.entrada, a.saida, a.lado, a.amostra, a.forca_cor)


if __name__ == "__main__":
    main()
