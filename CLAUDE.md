# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

"Pontos da Família" (pontos-familia) is a family chore/points tracker for two children (João Neto and Liz), written entirely in Brazilian Portuguese. The whole application lives in a single file, `index.html` — all CSS and JavaScript are inlined. There is no build step, no package manager, no dependencies, no tests, and no framework.

## Development

- Run it by opening `index.html` in a browser (or `python3 -m http.server` for a local server). Nothing to build or install.
- The app is designed as an iPhone home-screen web app (see the `apple-mobile-web-app-*` meta tags); keep it mobile-friendly and self-contained in one file.
- All user-facing text, comments, and identifiers are in Portuguese (e.g. `salvar`, `registrar`, `punir`, `novaSemana`). Keep new code consistent with that.

## Architecture (all inside index.html's single `<script>` block)

**State**: One global object `estado`, whose shape is defined by `padrao()`: per-child `pontos`, `semana` (weekly points), `punicoes` (punishment count), `fimPunicao` (punishment-end timestamps), `premios`, plus shared `historico`, `notas`, `planos`, `som`, and `_meta` (`{ts, dev}` used for sync conflict resolution). Every mutation goes through `salvar()`, which stamps `_meta`, persists to localStorage (`saveLocal()`), schedules a remote push, and re-renders.

**Constants at the top of the script**: `TAREFAS` (task groups shown on each card), `FILHOS` (the two children and their theming), and the game rules `PONTO=10`, `META=100`, `PONTOS_NIVEL=50`. The rules are also stated in the `.rules` banner in the HTML — keep the two in sync if changing them.

**Sync layer**: The `SYNC` object syncs state between phones via jsonblob.com (`https://jsonblob.com/api/jsonBlob`). The blob ID is the "family code" users share. Three modes: `setup` (initial overlay), `sync`, and `local` (localStorage only). Writes are debounced 600ms (`scheduledPush`/`doPush`); `poll()` pulls every 3.5s and adopts the remote state only when `remote._meta.ts` is newer (last-write-wins). Mode/code persist in localStorage under `CODEKEY`/`LOCALKEY`; `boot()` at the bottom restores them and skips the setup screen.

**Storage**: `LS` is a safe localStorage wrapper that falls back to an in-memory object when localStorage is unavailable (e.g. private browsing). Main state is stored under `KEY="pontosFam3"` — bump this key if the state shape changes incompatibly.

**Rendering**: No virtual DOM — `render()` rebuilds the child cards, history log, and plan list from `estado` via innerHTML string concatenation. Event handlers are inline `onclick` attributes calling global functions, so any dynamic text interpolated into HTML must go through `escH()` (HTML-escape) and strings placed inside inline handlers through `esc()` (quote-escape). Timers: `setInterval(poll, 3500)` for sync and `setInterval(tickCountdowns, 1000)` for punishment countdowns.

**Domain logic**: `registrar(id, texto, pts)` is the single entry point for point changes — it updates totals, prepends to `historico`, plays sounds (`beep`), shows floating feedback (`floaty`), and triggers confetti (`festa`) when the 100-point goal is reached. Punishments escalate 24h → 48h → 72h... per child (`punir`/`liberar`).
