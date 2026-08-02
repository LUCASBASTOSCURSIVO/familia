# Vídeo — Disfagia Pediátrica: Avaliação e Intervenção (EPAP)

Composição [HyperFrames](https://github.com/heygen-com/hyperframes) que gera um vídeo
vertical (1080x1920, 32 s, 30 fps) de anúncio da formação, no mesmo sistema visual do
vídeo da Especialização em Motricidade Orofacial.

## Estrutura do vídeo

| Tempo | Cena | Conteúdo |
|---|---|---|
| 0,0 – 5,6 s | Abertura | Logo EPAP · "Apresenta" · selo Formação confirmada |
| 5,2 – 11,8 s | Título | Disfagia Pediátrica · Avaliação e Intervenção |
| 11,4 – 17,8 s | O programa | 20 h · 4 dias · Porto |
| 17,4 – 23,6 s | Forma de ensino | Online (Zoom) 13 e 15 Out. · Presencial (Porto) 31 Out. e 01 Nov. |
| 23,2 – 28,8 s | Formadora | Prof.ª Doutora Carolina Silvério · destinatários |
| 28,4 – 35,0 s | Encerramento | Logo · selo · www.institutoepap.com |

## Como editar

Todo o conteúdo está em `index.html`. Cada cena é um `<div class="scene clip">` com
`data-start` / `data-duration` / `data-track-index`; as animações vivem na timeline
GSAP no fim do ficheiro, com posições absolutas em segundos.

Os corpos de letra dos blocos críticos foram aferidos com as métricas reais da Inter
(via fontTools), não estimados. Se alterar textos longos, vale a pena voltar a medir:
o título dispõe de 888 px entre margens e os cartões de 796 px internos.

## Assets

- `assets/fundo-disfagia.mp4` — fundo de 36 s composto a partir do clipe clínico de
  5 s (criança em cadeira de alimentação com terapeuta). O clipe é escalado a
  1080x602, transformado em loop ping-pong contínuo e sobreposto a um gradiente azul
  da marca com uma máscara alfa que o dissolve a partir dos 52 % da sua altura. Assim
  a cena está presente em todas as cenas sem esticar a filmagem horizontal para
  vertical.
- `assets/logo-epap-branco*.png` — logo EPAP a branco, fundo removido por limiar de
  luminância. Três cópias com nomes distintos porque o compilador avisa quando
  encontra media duplicada com a mesma origem e o mesmo tempo.
- `assets/fonts/` — Inter (400–900) servida localmente.
- `assets/js/gsap.min.js` — GSAP local; o CDN não é acessível no ambiente de render.
- `assets/musica-epap.m4a` — banda sonora original (ré maior, 108 BPM, 35 s),
  normalizada a −14 LUFS. Sem samples de terceiros. Gerada por
  `musica/compor_musica.py`.

## Dados sensíveis ao tempo

O flyer traz "Últimas 5 vagas", mas essa informação foi deliberadamente deixada
de fora do vídeo: envelhece mal e obrigaria a voltar a renderizar quando o número
mudasse.

**"4 dias de formação"** é a contagem das quatro datas do flyer (13, 15 e 31 de
outubro e 1 de novembro).

## Comandos

```bash
npm run dev      # preview no browser com live reload
npm run check    # lint + runtime + layout + motion + contraste
npm run render   # gera o MP4 em renders/ (qualidade standard, para publicar)

# Para revisões: --fps 24 corta 20% dos fotogramas e é o que realmente
# acelera. O gargalo é o Chrome a rasterizar cada fotograma, não a
# compressão, por isso --quality draft sozinho quase não muda o tempo
# (medido: 20m22s em draft contra 20m39s em standard) — só reduz o
# tamanho do ficheiro.
npx hyperframes@0.7.71 render --fps 24 --quality draft
```

O render exige `ffmpeg` e `ffprobe` no PATH e Node.js 22+.
