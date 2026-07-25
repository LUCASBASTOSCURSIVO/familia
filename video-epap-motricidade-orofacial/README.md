# Vídeo — Especialização em Motricidade Orofacial (EPAP) 2026/2028

Composição [HyperFrames](https://github.com/heygen-com/hyperframes) que gera um vídeo
vertical (1080x1920, 35 s, 30 fps) de apresentação da especialização.

## Estrutura do vídeo

| Tempo | Cena | Conteúdo |
|---|---|---|
| 0,0 – 5,6 s | Abertura | Logo EPAP + "Apresenta" |
| 5,2 – 11,8 s | Título | Especialização em Motricidade Orofacial · 2026 — 2028 · Nova edição |
| 11,4 – 17,8 s | O programa | 14 unidades curriculares · 240 h · 100 % e-learning |
| 17,4 – 23,6 s | Horários | Sábado 17h–21h · Domingo 09h–13h |
| 23,2 – 28,8 s | Datas | Início 10 de outubro de 2026 · Conclusão 09 de janeiro de 2028 |
| 28,4 – 35,0 s | Encerramento | Logo EPAP + nome + www.institutoepap.com |

## Como editar

Todo o conteúdo está em `index.html`. Cada cena é um `<div class="scene clip">` com
`data-start` / `data-duration` / `data-track-index`, e as animações vivem na timeline
GSAP no final do ficheiro (posições absolutas em segundos).

Para alterar textos, basta editar o HTML da cena correspondente. Se mudar a duração de
uma cena, ajuste também `data-duration` no `#root` e as posições das tweens.

## Assets

- `assets/bg-anatomia.mp4` — fundo anatómico em loop ping-pong contínuo (45 s),
  derivado do vídeo original 576x1024 e reescalado para 1080x1920.
- `assets/logo-epap-*.png` — logo EPAP a branco, com fundo removido por limiar de
  luminância. Existem três cópias com nomes distintos (abertura, marca persistente e
  encerramento) porque o compilador do HyperFrames avisa quando encontra media
  duplicada com a mesma origem e o mesmo tempo.
- `assets/fonts/` — Inter (400–900) servida localmente.
- `assets/js/gsap.min.js` — GSAP local; o CDN não é acessível no ambiente de render.

## Comandos

```bash
npm run dev      # preview no browser com live reload
npm run check    # lint + runtime + layout + motion + contraste
npm run render   # gera o MP4 em renders/
```

O render exige `ffmpeg` e `ffprobe` no PATH e Node.js 22+.

## Dados de origem

A estrutura dos 14 temas e os horários das sessões vêm do cronograma MOF 2026/2028.

Os restantes dados foram indicados pela coordenação e substituem o que constava do
cronograma: carga horária total de **240 h**, formato **e-learning**, início a **10 de
outubro de 2026**, conclusão a **09 de janeiro de 2028**, e inscrições em
**www.institutoepap.com**.
