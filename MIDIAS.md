# Como trocar as mídias do site

Cada foto e vídeo da página tem um **slot** com nome fixo. Você não precisa
mexer no código: basta subir o arquivo com o nome certo.

---

## Pelo site do GitHub (sem instalar nada)

1. Abra a pasta **`midias/`** no GitHub e clique em
   **Add file → Upload files**.

2. Suba o arquivo com o **nome do slot**. A extensão pode ser qualquer uma:

   ```
   hero.mp4                 (vídeo do topo)
   card-petshop.jpg
   cobertura-anapolis.png
   ```

3. Clique em **Commit changes**.

Pronto. Um robô do próprio GitHub (o arquivo
`.github/workflows/midias.yml`) percebe o arquivo novo, otimiza e grava o
resultado em `images/` sozinho, num commit separado. Leva cerca de um minuto.
Você pode acompanhar na aba **Actions** do repositório.

> **Limite de 25 MB por arquivo.** É uma restrição do upload pelo navegador do
> GitHub, não do projeto. Se o seu vídeo passar disso, veja
> "Arquivo grande demais" mais abaixo.

---

## Pelo terminal (se você tiver o projeto na máquina)

1. Coloque os originais — os maiores que você tiver, direto da câmera ou do
   celular — na pasta `midias/`, com o nome do slot.

2. Rode:

   ```bash
   python3 scripts/midias.py
   ```

3. Os arquivos otimizados vão para `images/`, que é o que o site usa.
   **Seus originais nunca são alterados** — dá para rodar quantas vezes quiser.

O script avisa se algum arquivo estiver com resolução baixa demais para o
espaço em que vai aparecer. Esse aviso é o mais importante de todos: é a causa
número um de foto borrada em tela grande.

---

## Níveis de qualidade

O padrão é `alta`. Para mudar:

```bash
python3 scripts/midias.py --qualidade maxima
python3 scripts/midias.py --qualidade leve
```

| Nível | Foto | Vídeo | Para quem |
|---|---|---|---|
| `maxima` | 2800px, JPEG 97 | CRF 16 | Prioriza fidelidade acima do tempo de carregamento |
| `alta` *(padrão)* | 1400px, JPEG 92 | CRF 20 | Equilíbrio entre nitidez e carregamento |
| `leve` | 980px, JPEG 86 | CRF 25 | Site rápido em conexão ruim |

Medido com o mesmo original de 4000×4000:

```
leve      979×979     259 KB
alta     1400×1400    630 KB
maxima   2800×2800  2.596 KB
```

**Vale usar `maxima`?** Na maior parte dos casos, não. Os cards aparecem com
cerca de 590px na tela; `alta` já entrega o dobro disso, que cobre telas
retina. De `alta` para `maxima` o arquivo quadruplica e a diferença só aparece
se alguém der zoom. Como é um site que abre no celular do dono do petshop,
peso de página costuma valer mais que nitidez que ninguém vê.

Onde `maxima` compensa: se você for reaproveitar as fotos em outro lugar
(impresso, catálogo) e quiser um único arquivo servindo aos dois.

**Importante:** o nível nunca amplia. Se o seu original tem 1024px, `maxima`
não vai inventar resolução — só melhora a compressão. Qualidade máxima de
verdade começa no arquivo que entra.

---

## Arquivo grande demais (acima de 25 MB)

Um vídeo de fundo **não precisa** ser grande. Um original de câmera pode ter
200 MB, mas depois de otimizado ele fica entre 1 e 3 MB, sem diferença visível
na tela. O problema é só subir o original bruto pelo navegador.

Três saídas, da mais simples para a mais técnica:

1. **Corte a duração.** O vídeo do topo roda em loop — 8 a 12 segundos bastam.
   Cortar no editor do celular já costuma resolver o tamanho.

2. **Exporte em 1080p.** Se estiver gravando em 4K, exporte em 1920×1080. É a
   resolução que o site usa de qualquer forma.

3. **Use o terminal.** O limite de 25 MB é só do navegador; pelo `git` o teto
   é 100 MB:

   ```bash
   git add midias/hero.mp4
   git commit -m "Adiciona vídeo do topo"
   git push
   ```

---

## O jeito mais rápido de todos (substituição direta)

Se preferir, substitua direto o arquivo dentro de **`images/`**, mantendo o
mesmo nome e a mesma extensão. Vale na hora, sem passar pelo robô. A diferença
é que aí a compressão fica por sua conta — o script existe justamente para
acertar isso sozinho.

---

## Os slots

| Slot em `midias/` | Vira | Onde aparece | Tamanho ideal |
|---|---|---|---|
| `hero` | `hero-video.mp4` | Vídeo de fundo do topo, tela inteira | 1920×1080, horizontal |
| `hero-poster` | `hero-poster.jpg` | Primeiro quadro do topo, enquanto o vídeo carrega | 1920×1080 |
| `card-petshop` | `card-petshop.jpg` | Card "Você nunca espera a sua toalha voltar" | 1400×1400, quadrado |
| `card-clinica` | `card-clinica.jpg` | Card "Higiene com protocolo" | 1400×1400, quadrado |
| `passo-entrega` | `passo-entrega.jpg` | Passo 01 — Entrega | 1400×1050, deitada |
| `passo-uso` | `passo-uso.jpg` | Passo 02 — Uso | 1400×1050, deitada |
| `passo-coleta` | `passo-coleta.jpg` | Passo 03 — Coleta | 1400×1050, deitada |
| `passo-ciclo` | `passo-ciclo.jpg` | Passo 04 — Lavagem | 1400×1050, deitada |
| `cobertura-anapolis` | `cobertura-anapolis.jpg` | Card de cobertura — Anápolis | 1400×1400, quadrado |
| `cobertura-goiania` | `cobertura-goiania.jpg` | Card de cobertura — Goiânia | 1400×1400, quadrado |
| `logo` | `logo-badge.png` | Logo no topo e no rodapé | PNG com fundo transparente, 600px |

O `hero-poster` é opcional: se você não mandar um, o script extrai
automaticamente o primeiro quadro do seu vídeo.

---

## Enquadramento — onde o texto entra

Isso muda mais o resultado do que a resolução:

- **Vídeo do topo:** o título grande fica no **canto inferior esquerdo** e o
  texto de apoio no **canto inferior direito**. Escolha uma cena que tenha
  pouca informação visual nesses dois cantos — parede, bancada, chão.
- **Cards quadrados:** o texto entra **por baixo**, sobre um degradê escuro.
  Deixe o **terço inferior** mais limpo e mantenha o assunto principal na
  metade de cima.
- **Passos do processo:** deitadas, 4:3. O texto entra **abaixo** da imagem,
  não por cima — então aqui não é preciso poupar canto nenhum.
- **Logo:** o site é preto. A marca precisa funcionar sobre fundo escuro — de
  preferência com contorno claro ou versão clara.

---

## O que o script faz para preservar qualidade

- **Nunca amplia.** Se o seu arquivo for menor que o alvo, ele mantém o tamanho
  original em vez de esticar, porque esticar só gera borrão.
- **JPEG em qualidade 92 com croma 4:4:4.** Sem subamostragem de cor — é o que
  evita franja colorida em pelo de animal, texto pequeno e borda de toalha.
- **PNG sem perdas**, com a transparência preservada.
- **Vídeo em H.264 CRF 20, preset slow**, com `faststart` (começa a tocar antes
  de baixar tudo) e sem faixa de áudio, já que é fundo mudo.
- **Corrige a rotação** gravada pelo celular antes de redimensionar.

---

## Formatos aceitos

**Imagem:** JPG, PNG, WebP, TIFF, BMP, HEIC/HEIF, AVIF
**Vídeo:** MP4, MOV, MKV, WebM, AVI, M4V

Arquivos que o Python não abre sozinho (HEIC do iPhone, por exemplo) são
convertidos pelo ffmpeg automaticamente.

---

## Requisitos

- `python3` com Pillow — instale com `pip install pillow`
- `ffmpeg` — no Ubuntu/Debian, `sudo apt install ffmpeg`

---

## Foto que chegou comprimida

Foto que passou por WhatsApp, print de tela ou download de rede social chega
pequena e com quadriculado nas áreas lisas. Dá para recuperar parte disso:

```bash
python3 scripts/realce-foto.py entrada.jpg saida.png --lado 1200 \
    --amostra 0.40,0.52,0.62,0.60 --forca-cor 0.7
```

O script desfaz o quadriculado da compressão, corrige o dominante de cor,
amplia com um filtro melhor que o do navegador e devolve micro-contraste.

O `--amostra` é uma região que você sabe que é branca, em frações da imagem
(`x0,y0,x1,y1`) — numa foto do veículo, a carroceria. É a partir dela que o
dominante é medido. Sem esse parâmetro, a correção de cor é pulada.

**O que isso não faz:** criar detalhe que não está no arquivo. Ampliar de
450px para 1200px limpa defeito, não inventa nitidez. Arquivo grande de
origem continua sendo a única forma de ter detalhe de verdade — o script
existe para quando esse arquivo não existe mais.
