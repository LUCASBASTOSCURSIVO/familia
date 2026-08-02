# Portfólio aéreo — 1920x1080 horizontal

Showreel horizontal de 28 s em [HyperFrames](https://github.com/heygen-com/hyperframes),
para site, YouTube ou Vimeo. A filmagem de drone entra sem recorte.

> **Estado: estrutura completa com marcadores.** Os quatro planos em
> `assets/clipes/` são placeholders coloridos, não filmagem. Substitua-os pelos
> seus ficheiros e volte a renderizar.

## Estrutura

| Tempo | Momento |
|---|---|
| 0,0 – 7,4 s | Abertura sobre o plano 1: nome em duas linhas, filete e função |
| 7,2 – 12,2 s | Plano 2 com legenda 01 |
| 12,0 – 17,0 s | Plano 3 com legenda 02 |
| 16,8 – 22,0 s | Plano 4 com legenda 03 |
| 21,8 – 24,4 s | Grelha com os quatro planos |
| 24,0 – 28,0 s | Cartão final: nome, função, contacto |

Cortes brancos de um décimo de segundo marcam cada passagem. As barras
cinematográficas fecham na abertura e no fim, e abrem durante o reel. Cada plano
tem o seu movimento — aproximação, afastamento, deriva lateral e vertical — para
que nenhum fique parado.

## Como trocar a filmagem

1. Ponha os seus quatro clipes em `assets/clipes/`, com os nomes
   `clipe-01.mp4` a `clipe-04.mp4`.
2. Gere as miniaturas da grelha final (uma imagem por clipe):

   ```bash
   for i in 1 2 3 4; do
     ffmpeg -y -ss 2 -i assets/clipes/clipe-0$i.mp4 -frames:v 1 \
       -vf "scale=640:360" assets/clipes/mini-0$i.jpg
   done
   ```

3. `npm run check` e depois `npm run render`.

**A filmagem 16:9 entra sem recorte.** Se algum clipe tiver outra proporção, o
`object-fit: cover` ajusta; para escolher que parte fica visível, acrescente
`object-position` ao vídeo — por exemplo `style="object-position: 50% 30%"`.

**As barras cinematográficas** fecham na abertura e no cartão final, e abrem
completamente durante o reel, para os planos se verem em ecrã inteiro.

**Para escolher o troço de cada clipe**, use `data-media-start` no `<video>`: o
valor é o segundo do ficheiro original onde o corte começa.

## O que tem de personalizar

Tudo isto está no `index.html` com valores provisórios:

- **Nome** — está `Lucas Bastos`, deduzido da conta Google. Aparece na abertura
  (`.nm`) e no cartão final (`#fim-nome`).
- **Função** — `Imagem aérea · Drone`, em `#ab-sub` e `#fim-papel`.
- **Contacto** — `@o_seu_instagram`, em `#fim-contacto`.
- **Legendas dos planos** — `Título do plano` e `Local · Data`, em `#leg-1` a `#leg-3`.
- **Cor de acento** — `--acento: #F2C14E` (âmbar). Uma linha no `:root`.

## Música

`assets/musica-reel.m4a` é original, sintetizada de raiz em
`musica/compor_musica.py` (ré maior, 116 BPM, 28 s), normalizada a −14 LUFS. Sem
samples de terceiros, portanto sem restrições de publicação. Mudar `BPM` ou `prog`
no script gera variações.

## Comandos

```bash
npm run dev      # preview no browser com live reload
npm run check    # lint + runtime + layout + motion + contraste
npm run render   # gera o MP4 em renders/ (qualidade standard, para publicar)

# Para revisões, use o modo rascunho — mexe só na compressão, mantém os
# 1080x1920 e o texto legível, e corre bastante mais depressa:
npx hyperframes@0.7.71 render --quality draft
```

Requer Node.js 22+, `ffmpeg` e `ffprobe` no PATH.
