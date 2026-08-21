# Critérios de Qualidade — Toalhão Landing Page

Adaptados do sistema de referência (Sequel design system, via Refero Styles), invertendo preto→branco e trocando o acento cromático por laranja Toalhão. Cada critério é verificável olhando pra tela renderizada, não pelo código.

1. **O canvas é branco puro ou superfície fria (`--color-surface`, cinza neutro) em pelo menos 70% da página.** Fora o hero (que é o vídeo) e no máximo uma seção de contraste (navy), o fundo dominante é branco ou uma superfície de elevação FRIA — nunca um tom que leia como creme/amarelado. Isso inverte literalmente a regra do sistema original ("keep the canvas at pure black") — aqui é pure white, e o passo de elevação precisa ser cinza-frio, não bege.

2. **O laranja aparece no máximo 2 vezes por "frame" de altura de tela — e nunca em números, valores de lista, ícones de estado padrão ou tags de card.** Contando qualquer momento do scroll como um frame, o laranja cromático só pode ser (a) um botão de ação e (b) no máximo uma palavra de destaque no heading daquele frame. Se ao contar você chegar a 3+, é reprovação automática deste critério, não importa quão bem os outros passem.

3. **Toda headline grande usa peso regular/leve (o mais leve que a fonte realmente suporta) com no máximo uma palavra em peso forte (800) ou laranja.** Nunca duas palavras de destaque na mesma frase, nunca a frase inteira em bold ou em laranja.

4. **O hero é o vídeo em full-bleed — sem bloco de conteúdo acima da dobra além do headline e do CTA.** A imagem/vídeo É a dobra, como no sistema original ("the photograph IS the fold"). Nada de card, stat ou formulário competindo com o vídeo na primeira tela.

5. **Botões e badges são sempre pill (cantos totalmente arredondados); cards são sempre 16px — nunca cantos retos em nenhum componente interativo.**

6. **Nenhum card tem sombra decorativa.** A hierarquia visual entre seções vem só da troca de tom de fundo (branco → superfície levemente cinza), nunca de `box-shadow` em conteúdo.

7. **Pelo menos uma seção usa linguagem/visual operacional explícito** (mono uppercase, número de rota, "entrega confirmada", fatura, timestamp) que comunica rastreabilidade — não é só bonito, parece um sistema real rodando por trás.

## Como o Crítico Visual deve avaliar

Colocar o resultado renderizado ao lado da descrição do sistema de referência (não uma imagem, mas os mecanismos acima). Perguntar: se eu tirasse a logo do Toalhão, essa página ainda pareceria pertencer à mesma família visual do Sequel (invertida pra branco)? Ou parece um site de petshop genérico com header roxo e cards com sombra? A resposta binária decide APROVADO/REPROVADO.
