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
| `card-petshop` | `card-petshop.jpg` | Card "Não é lavanderia" | 1400×1400, quadrado |
| `card-clinica` | `card-clinica.jpg` | Card "Higiene com protocolo" | 1400×1400, quadrado |
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
