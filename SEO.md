# Busca e descoberta

O que já está no site, o que depende de você, e por quê.

---

## O que foi feito

| | Onde | Para quê |
|---|---|---|
| `<title>` e descrição | `index.html` | O que aparece no resultado do Google |
| `<link rel=canonical>` | as duas páginas | Diz ao Google que o endereço oficial é o **www** |
| Open Graph + Twitter | `index.html` | Card com imagem no WhatsApp, Instagram, LinkedIn |
| `images/og-card.jpg` | 1200×630 | A imagem desse card |
| Dados estruturados | `index.html` | Google entende empresa, serviço e dúvidas |
| `robots.txt` | raiz | Libera rastreamento e aponta o sitemap |
| `sitemap.xml` | raiz | Lista as páginas para indexação |
| `llms.txt` | raiz | Descreve o negócio para assistentes de IA |

### Dados estruturados (JSON-LD)

Quatro blocos, em `<script type="application/ld+json">`:

- **DryCleaningOrLaundry** — a empresa: nome, CNPJ, telefone, endereço e as duas
  cidades atendidas. É o que alimenta a ficha lateral do Google.
- **Service** — o serviço, com os nomes alternativos pelos quais as pessoas
  procuram ("aluguel de toalhas para pet shop").
- **WebPage** — a página em si.
- **FAQPage** — as 8 perguntas do site. É o bloco com maior chance de retorno
  rápido: o Google pode mostrar as perguntas expandidas direto no resultado,
  ocupando mais espaço na tela que qualquer concorrente sem isso.

Os textos são extraídos do próprio HTML por script, então não há risco de o
schema dizer uma coisa e a página dizer outra. Se você editar o FAQ, avise que
eu regenero.

---

## O que só você pode fazer

### 1. Google Search Console — o mais importante

Sem isso o Google até acha o site sozinho, mas você fica cego: não sabe por
quais termos aparece, em que posição, nem se há erro de indexação.

O tipo **Domínio** (o que o Google abre quando você digita `toalhao.com` sem o
`https://`) é o melhor: cobre `www`, sem `www` e qualquer subdomínio de uma
vez. Em troca, ele exige um registro no DNS em vez de uma tag no site.

**O DNS do toalhao.com está na Vercel** — conferido: os nameservers são
`ns1.vercel-dns.com` e `ns2.vercel-dns.com`. Então o registro se cria lá, e
não num registrador tipo GoDaddy.

1. No Search Console, clique em **COPIAR** para pegar o valor inteiro
   (`google-site-verification=...`) — na tela ele aparece cortado
2. Abra `vercel.com/italoex/~/domains` e clique em **toalhao.com**
3. Vá em **DNS Records** e adicione:

   | Campo | Valor |
   |---|---|
   | Name | *deixe em branco* (é o apex) |
   | Type | **TXT** |
   | Value | o `google-site-verification=...` copiado |
   | TTL | o padrão |

4. Salve, espere cerca de um minuto — DNS da Vercel propaga rápido
5. Volte ao Search Console e clique em **VERIFICAR**
6. Depois, em **Sitemaps**, envie `https://www.toalhao.com/sitemap.xml`

> Não havia nenhum TXT no domínio antes, então esse é o primeiro — não há
> risco de sobrescrever configuração de e-mail nem nada existente.

> Se travar, a saída alternativa é criar uma segunda propriedade do tipo
> **prefixo do URL** com `https://www.toalhao.com` e verificar por tag HTML.
> Aí é só me mandar o código que eu instalo e publico.

### 2. Perfil da Empresa no Google — o maior retorno local

Mais decisivo que o site inteiro para quem busca "aluguel de toalhas pet
perto de mim". É gratuito, em `business.google.com`.

- Categoria sugerida: **Serviço de lavanderia** (e secundária: Fornecedor
  para pet shop)
- Marque como **atendimento na área do cliente**, definindo Anápolis e Goiânia
  como região — assim o endereço não precisa aparecer publicamente
- Suba as fotos reais do veículo, que é o seu diferencial visível
- Peça avaliação aos clientes atuais: é o fator que mais move o mapa local

### 3. Bing Webmaster Tools

`bing.com/webmasters` — importa direto do Search Console em dois cliques.
Vale porque o Bing alimenta o Copilot e parte das respostas de IA.

---

## Palavras-chave

Ancoradas em busca real feita em agosto/2026, não em suposição. **Não tenho
dados de volume** — para isso seria preciso o Planejador de Palavras-chave do
Google Ads, que é gratuito e você acessa com a mesma conta.

### O que a concorrência usa

Cekão, SPEtoalhas, Lavato, Ícone Clean e Lav Sec são os nomes que aparecem —
**e praticamente todos são de São Paulo**. Não encontrei player local
estabelecido em Goiás. É a informação mais útil desta seção: os termos com
cidade estão provavelmente livres.

### Termo principal

**locação de toalhas para petshop** — é o que o mercado usa, e é o que está
adesivado no seu veículo. Entrou no título, na descrição, no primeiro
parágrafo e no schema.

### Termos secundários

`aluguel de toalhas para pet shop` · `lavanderia para petshop` ·
`toalhas higienizadas para banho e tosa` · `locação de enxoval para clínica
veterinária` · `aluguel de toalhas pet`

Note que **"pet shop" separado** e "petshop" junto são buscados. O site agora
usa as duas grafias.

### Termos locais — onde está a chance real

`aluguel de toalhas para pet shop em Goiânia` · `locação de toalhas petshop
Anápolis` · `lavanderia para petshop em Goiás`

Disputar "locação de toalhas para petshop" no Brasil inteiro é briga com
empresas de dez anos de São Paulo. Disputar com a cidade junto é briga que dá
para ganhar — e é quem realmente vira cliente, porque o serviço depende de
rota física.

---

## Peso da página

Fator de ranqueamento e, mais que isso, de desistência: o dono do petshop abre
no 4G, entre um banho e outro.

O vídeo do topo tem 6,7 MB. Agora ele **só é baixado em tela de 900px ou mais
e fora de modo de economia de dados**. No celular fica o pôster, de 53 KB.

```
celular    8,25 MB  ->  0,85 MB
desktop    8,25 MB  ->  7,68 MB
```

As imagens abaixo da dobra passaram a carregar sob demanda (`loading="lazy"`).

Para voltar a carregar o vídeo sempre, a condição está comentada no `<script>`
ao fim do `index.html`.

---

## O que ainda daria retorno

Em ordem de retorno por esforço:

1. **Depoimento real de cliente.** Continua sendo a maior lacuna do site.
2. **Página por cidade** — `/anapolis` e `/goiania`, cada uma com o texto e as
   fotos daquela praça. É o jeito normal de ranquear em duas cidades sem que
   uma canibalize a outra.
3. **Conteúdo que responde dúvida real**: "quanto custa lavar toalha no
   próprio petshop?" atrai justamente quem está insatisfeito com a solução
   atual. É o que traz visita que não te conhecia.
4. **Instagram no perfil do Google**, e o link do site na bio.
