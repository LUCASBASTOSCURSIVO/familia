# Vídeo — Avanços na Consultoria de Amamentação (EPAP)

Composição [HyperFrames](https://github.com/heygen-com/hyperframes) que anuncia que a
formação está **confirmada**. Vídeo vertical (1080x1920, 30 s, 30 fps), construído a
partir do flyer da formação e na mesma identidade gráfica — fundo claro, azul EPAP e
o selo dourado.

## Estrutura do vídeo

| Tempo | Cena | Conteúdo |
|---|---|---|
| 0,0 – 6,4 s | Confirmação | Foto + logo EPAP + selo "Formação confirmada" |
| 6,0 – 13,0 s | Título | Avanços na Consultoria de Amamentação: do Manejo Clínico à Disfagia Pediátrica |
| 12,6 – 20,2 s | Informações | 20 h · B-learning / Zoom · datas online e presenciais · Porto |
| 19,8 – 26,2 s | Formadora | Dr.ª Vanessa Felipe de Deus + destinatários |
| 25,8 – 30,0 s | Fecho | Logo + selo + www.institutoepap.com |

Uma faixa azul com o endereço do site e uma barra de progresso acompanham todo o vídeo.

## Como editar

Todo o conteúdo está em `index.html`. Cada cena é um `<div class="scene clip">` com
`data-start` / `data-duration` / `data-track-index`; as animações estão na timeline GSAP
no fim do ficheiro, com posições absolutas em segundos. Os ícones são SVG inline, por
isso a cor muda no atributo `stroke`.

## Assets

- `assets/foto-bebe.jpg` — recorte da fotografia do flyer (região sem o selo nem a
  curva branca), ampliada 3x com LANCZOS.
- `assets/formadora.png` — retrato da formadora recortado do flyer, com máscara oval e
  fundo transparente.
- `assets/logo-epap-azul*.png` — logo EPAP com fundo removido por limiar de luminância.
  Duas cópias com nomes distintos porque o compilador avisa quando encontra media
  duplicada com a mesma origem e o mesmo tempo.
- `assets/fonts/` — Inter (400–900) servida localmente.
- `assets/js/gsap.min.js` — GSAP local; o CDN não é acessível no ambiente de render.
- `assets/musica-epap.m4a` — banda sonora original (ré maior, 108 BPM, 30 s),
  normalizada a −14 LUFS. Mesmo motor sonoro do vídeo da Especialização em
  Motricidade Orofacial, para manter a coerência de marca. Sem samples de terceiros.

> As fotografias vêm do flyer, que tem 864x1536. Foram ampliadas para o formato de
> vídeo; a nitidez é a possível a partir dessa origem. Se existirem os originais em
> alta resolução, substituí-los melhora visivelmente o resultado.

## Comandos

```bash
npm run dev      # preview no browser com live reload
npm run check    # lint + runtime + layout + motion + contraste
npm run render   # gera o MP4 em renders/ (qualidade standard, para publicar)

# Para revisões, use o modo rascunho — mexe só na compressão, mantém os
# 1080x1920 e o texto legível, e corre bastante mais depressa:
npx hyperframes@0.7.71 render --quality draft
```

O render exige `ffmpeg` e `ffprobe` no PATH e Node.js 22+.
