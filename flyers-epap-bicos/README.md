# Carrossel — Bicos artificiais na abordagem clínica da disfunção oral no lactente

Dois slides de Instagram em 1080 × 1350 (4:5), desenhados de raiz. Arte final chapada,
sem mockups.

## Estado

| Peça | Situação |
|---|---|
| Slide 1 — capa | Composto. Falta a **imagem clínica** e o **retrato da formadora** |
| Slide 2 — informação | **Completo** |

Os dois espaços em falta estão marcados no slide 1 com moldura tracejada, de propósito,
para não passarem despercebidos.

## O que falta e porquê

**Retrato de Joana Caçoeiro** — não foi carregado nesta sessão. Não gero um rosto para
o apresentar como sendo o de uma pessoa real identificada pelo nome. Anexe a fotografia
e ela entra em `assets/retrato-joana.jpg`; o slot já está dimensionado (104 × 104, corte
por `object-fit: cover`).

**Imagem clínica** — foi gerada (still life de bicos artificiais e material de
alimentação infantil, sem pessoas), mas o CDN onde ficou alojada está bloqueado pela
política de rede deste ambiente, tal como o Google Drive. Guarde-a e anexe-a; entra em
`assets/clinico.png`.

Depois de colocar os dois ficheiros, troque nos HTML os blocos `<div class="vazio">`
por `<img src="assets/...">` e volte a exportar.

## Sistema visual

- **Tipografia** Manrope (400–800), servida localmente
- **Cores** azul-escuro `#0E2350`, azul `#1F4BA8`, azul muito claro `#E8EFFB`,
  papel `#FBFAF9`, bege quente `#E7DCCB`, texto `#46536C`
- **Marca** faixa fina no topo em gradiente do azul-escuro ao bege; logo EPAP original,
  sem alterações de forma ou cor
- Linhas finas e sombras discretas apenas; ícones de traço; sem círculos decorativos
  nos cantos e sem caixas arredondadas em excesso

## Exportar

```bash
CH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
for n in 1 2; do
  $CH --headless --disable-gpu --no-sandbox --hide-scrollbars \
      --force-device-scale-factor=1 --window-size=1080,1350 \
      --virtual-time-budget=6000 --screenshot="slide-$n.png" \
      "file://$PWD/slide-$n.html"
done
```

## Texto

Todo o texto em português foi reproduzido exatamente como fornecido, incluindo acentos,
cedilha, travessões (`–`) e o ponto médio (`·`). Não foram inventados preços,
certificados, contactos, sítios web nem informação de inscrição.
