# Toalhão — Style Reference

> Operação de lavanderia como assinatura — logística séria por trás de uma toalha limpa que nunca falta.

**Theme:** light (invertido do sistema de referência "Sequel", que é dark)

Toalhão é a versão operacional e luminosa do "private screening after dark": em vez de um canvas preto hospedando fotografia cinematográfica, é um canvas **branco puro** hospedando prova operacional — rotas, entregas, faturas, números. O sistema é quase acromático: branco, grafite/azul-marinho para texto e estrutura, e um único acento quente (o laranja da marca) fazendo o mesmo trabalho que o "Lamp Cream" fazia no escuro — só que aqui a luz already existe, o laranja é o que se movimenta dentro dela (chama, atenção, ação). Tipografia mistura um peso leve (300) em headlines narrativas com um peso forte (700/800, ou itálico) reservado para a palavra operacional que carrega a promessa central — "nunca", "sempre", "registrado". Componentes são pill e precisos, cards elevados usam um tom de superfície muito sutil (quase-branco) em vez de sombra pesada. Movimento é contido — nunca lúdico, porque isso é logística, não brinquedo.

## Tokens — Cores

| Nome | Valor | Token | Papel |
|------|-------|-------|-------|
| Branco Puro | `#FFFFFF` | `--color-white` | Canvas da página, fundo do nav quando no topo — o estado padrão; tudo é construído SOBRE o branco |
| Azul-Marinho (texto) | `#161335` | `--color-navy` | Texto primário, headings, ícone stroke, valores em destaque dentro de listas — a cor de leitura e estrutura |
| Azul-Marinho (contraste) | `#0B1220` | `--color-navy-contrast` | Fundo da ÚNICA seção de contraste escura (CTA final + footer) e fundo por trás do vídeo do hero. Tom deliberadamente frio (G ≥ R) — nunca deve ler como roxo/violeta |
| Superfície | `#F4F4F6` | `--color-surface` | Card elevado, painéis secundários — um passo quieto e FRIO (nunca creme/amarelado) acima do branco puro, implica elevação sem sombra |
| Linha | `#E7E3DA` | `--color-hairline` | Bordas finas, contornos de badge, divisores sutis |
| Laranja Toalhão | `#FF7A1A` | `--color-orange` | Ação primária preenchida — o único acento cromático do sistema inteiro, incluindo utilitários fixos como o botão flutuante de WhatsApp (nunca usar o verde de marca do WhatsApp) |
| Grafite | `#6B6875` | `--color-graphite` | Texto secundário sobre branco, legendas, metadados, labels/tags que NÃO são a ênfase principal da seção |

**Regra central (a mais violada na prática, seguir à risca):** por seção da página, o laranja só pode aparecer em **(a)** um botão de ação preenchido e **(b)** no máximo UMA palavra de destaque no heading. Nada mais — não em números, não em valores de lista, não em ícones de estado padrão, não em tags/eyebrows de card. Quando em dúvida se um elemento "merece" laranja, a resposta é não: use `--color-navy` com peso 700 pra dar ênfase sem cor.

## Tokens — Tipografia

### Display / Corpo — `Baloo 2` (peso 400–800; **a família NÃO tem peso 300 no Google Fonts** — não pedir esse peso) + fallback `Poppins, Inter, sans-serif`
- Pesos: 400 (headline narrativa — é o peso mais leve que a fonte realmente tem), 600–700 (peso de leitura padrão), 800 (a palavra operacional de destaque)
- Tamanhos: 15, 16, 18, 21, 30, 40, 54, 72px
- Letter-spacing: -0.03em em display ≥54px; +0.06–0.08em em labels uppercase ≤13px
- Regra: nunca dois pesos fortes na mesma frase — a headline é 400 regular, só a palavra-chave sobe pra 800. O contraste vem de 400→800, não de um peso ultra-leve inexistente na fonte.

### Mono — `Space Mono` (labels operacionais)
- Uso: eyebrows, badges de rota/entrega, números de fatura, timestamps — qualquer coisa que precise "parecer um log real"
- Sempre uppercase, sempre tracking positivo (+0.06–0.08em)

### Escala Tipográfica

| Papel | Tamanho | Line-height | Tracking |
|---|---|---|---|
| label | 12px | 1.4 | +0.08em |
| body | 16px | 1.6 | — |
| body-lg | 18px | 1.6 | — |
| subheading | 21px | 1.3 | -0.01em |
| heading | 40px | 1.1 | -0.02em |
| heading-lg | 54px | 1.05 | -0.03em |
| display | 72px | 1.0 | -0.03em |

## Tokens — Espaçamento & Forma

- **Unidade base:** 4px
- **Densidade:** confortável
- **Largura máxima:** 1200px
- **Gap entre seções:** 96–120px
- **Gap entre elementos:** 16–24px

### Border Radius
| Elemento | Valor |
|---|---|
| cards | 16px |
| badges/pills | 9999px |
| botões | 9999px |
| play button (vídeo) | 50% |

### Sombras
- Só duas sombras no sistema inteiro: uma leve sob o botão primário laranja (`0 12px 24px -10px rgba(255,122,26,.45)`), e um contorno "vidro" sutil nos badges flutuantes sobre o vídeo do hero. Cards NUNCA têm sombra — elevação vem só da mudança de tom (`--color-white` → `--color-surface`).

## Componentes

### Botão Pill Primário
Fundo `--color-orange`, texto branco, `9999px` radius, padding `14px 26px`, `16px` peso 700. Única cor de ação preenchida do sistema.

### Botão Pill Fantasma
Fundo transparente, borda `1.5px` `--color-navy` (sobre branco) ou `1.5px rgba(255,255,255,.5)` (sobre vídeo), texto herdado, `9999px` radius. Usado quando uma ação secundária acompanha o botão laranja.

### Badge de Vidro Flutuante (sobre o vídeo do hero)
Fundo `rgba(255,255,255,.14)` com `backdrop-filter: blur(16px) saturate(1.4)`, borda `1px rgba(255,255,255,.35)`, texto branco uppercase 12px mono, `9999px` radius, padding `8px 16px`. Usado para "ROTA CONFIRMADA", "ANÁPOLIS · GOIÂNIA" etc — a mesma função do "Frosted Glass Badge" do Sequel, só que aqui carrega dado operacional, não categoria editorial.

### Card Elevado
Fundo `--color-surface`, `16px` radius, sem sombra, sem borda. A mudança de branco puro pra `--color-surface` é o único sinal de elevação. Usado por todo card de conteúdo estático: benefícios, passos do ciclo, alternativas, cobertura, painel de rotas.

### Item de Lista Interativa (exceção documentada)
Fundo `--color-white`, borda `1px --color-hairline`, `12px` radius, sem sombra. É a ÚNICA família de componente que usa borda em vez de troca de tom — reservada pra linhas clicáveis/expansíveis (ex: FAQ accordion), onde um contorno fino comunica "isto é uma linha de lista com estado" melhor que um preenchimento sólido. Nunca usar esse tratamento em card de conteúdo estático.

### Botão de Play do Vídeo
Circular, `50%` radius, borda `1.5px rgba(255,255,255,.6)`, fundo `rgba(255,255,255,.1)` com blur, contém triângulo de play + label "Ver como funciona" 13px mono uppercase. Flutua sobre o vídeo, nunca dentro de um card.

### Heading com Palavra de Destaque
VisueltPro-equivalente (Baloo 2) peso 300 na frase, com UMA palavra em peso 800 cor laranja — ex: "Nunca fica **sem** toalha limpa." Nunca mais de uma palavra de destaque por heading.

### Barra de Navegação
Transparente sobre o vídeo do hero, vira branco sólido com hairline ao rolar. Logo à esquerda, 4 links ao centro, 1 pill CTA laranja à direita.

## Fazer / Não Fazer

### Fazer
- Manter o canvas em branco puro `#FFFFFF` — nunca crema, nunca cinza tingido
- Usar laranja só em CTA preenchido + no máximo 1 palavra de destaque por seção
- Peso 300 em headlines narrativas, 800 só na palavra operacional
- Uppercase + tracking positivo em todo label/badge/metadado
- Elevar cards só por tom (`--color-surface`), nunca por sombra
- Pill (9999px) em todo botão/badge; 16px em card

### Não Fazer
- Nunca usar uma segunda cor cromática além do laranja
- Nunca aplicar sombra decorativa em card ou imagem
- Nunca usar cantos retos (0px) em botão/badge/pill
- Nunca peso abaixo de 300 ou (fora do destaque) acima de 700 em corpo de texto
- Nunca animação com bounce/spring — só easing suave, 0.2–0.35s

## Motion
Transições padrão `0.2–0.35s`, easing `cubic-bezier(0.22,0.61,0.36,1)` — desacelera no final, nunca "mola". Fades de opacidade + pequenos slides de 12–24px no scroll-reveal. Nenhuma animação com duração abaixo de 400ms quando envolve troca de estado visível (ex: badge aparecendo).
