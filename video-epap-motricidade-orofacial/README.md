# Vídeo — Especialização em Motricidade Orofacial (EPAP) 2026/2028

Composição [HyperFrames](https://github.com/heygen-com/hyperframes) que gera um vídeo
vertical (1080x1920, 32 s, 30 fps) de apresentação da especialização, a partir do
cronograma MOF 2026/2028.

## Estrutura do vídeo

| Tempo | Cena | Conteúdo |
|---|---|---|
| 0,0 – 5,6 s | Abertura | Logo EPAP + "Apresenta" |
| 5,2 – 11,8 s | Título | Especialização em Motricidade Orofacial · 2026 — 2028 |
| 11,4 – 17,8 s | O programa | 14 unidades curriculares · 196 h · 100 % online |
| 17,4 – 23,6 s | Horários | Sábado 17h–21h · Domingo 09h–13h · Zoom + EAD |
| 23,2 – 28,8 s | Início | 10 e 11 de outubro de 2026 · Tema 1 |
| 28,4 – 32,0 s | Encerramento | Logo EPAP + nome da especialização |

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

Os números vêm do cronograma MOF 2026/2028. A carga horária total de **196 h** foi
obtida somando as horas declaradas em cada um dos 14 temas (sessões síncronas em Zoom
mais atividades de autoestudo na plataforma EAD); o documento original não indica um
total, por isso convém confirmar antes de publicar.
