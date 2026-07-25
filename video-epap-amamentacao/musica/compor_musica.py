"""
Faixa original para o vídeo da Especialização em Motricidade Orofacial (EPAP).
Ré maior, 108 BPM, 35 s — luminosa e com pulso, para segurar a atenção.
Sintetizada de raiz: sem samples nem bibliotecas de terceiros.
"""
import numpy as np, wave

SR = 44100
DUR = 32.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(21)

BPM = 108.0
BAT = 60.0 / BPM          # 0.5556 s por tempo
COMP = 4 * BAT            # 2.2222 s por compasso

def nota(nome):
    passos = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    n, oit = nome[:-1], int(nome[-1])
    return 440.0 * 2 ** ((passos[n] + 12 * (oit - 4) - 9) / 12.0)

# ---------------------------------------------------------------- utilitários
def coloca(dest, buf, ini, ganho=1.0):
    """Soma um buffer curto na posição temporal indicada."""
    i0 = int(ini * SR)
    if i0 >= N or i0 < 0:
        return
    i1 = min(N, i0 + len(buf))
    dest[i0:i1] += buf[: i1 - i0] * ganho

def lowpass_fft(x, corte, ordem=2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1.0 + (f / corte) ** 2) ** (ordem / 2.0), n=len(x))

def highpass_fft(x, corte, ordem=2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    r = f / max(corte, 1e-9)
    return np.fft.irfft(X * (r ** 2 / (1.0 + r ** 2)) ** (ordem / 2.0), n=len(x))

def eq(x, bandas):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = np.ones_like(f)
    for centro, larg, db in bandas:
        with np.errstate(divide='ignore'):
            d = np.log2(np.maximum(f, 1e-6) / centro)
        H *= 10 ** ((db / 20.0) * np.exp(-(d ** 2) / (2 * larg ** 2)))
    return np.fft.irfft(X * H, n=len(x))

def env(n_amostras, a, d, s, r, dur):
    """Envelope ADSR sobre um buffer curto."""
    seg = np.arange(n_amostras) / SR
    out = np.zeros(n_amostras)
    ia = seg < a
    idd = (seg >= a) & (seg < a + d)
    isus = (seg >= a + d) & (seg < dur - r)
    ire = seg >= dur - r
    out[ia] = seg[ia] / max(a, 1e-6)
    out[idd] = 1 - (1 - s) * (seg[idd] - a) / max(d, 1e-6)
    out[isus] = s
    if ire.any():
        out[ire] = s * np.clip(1 - (seg[ire] - (dur - r)) / max(r, 1e-6), 0, 1)
    return np.clip(out, 0, None)

# ---------------------------------------------------------------- instrumentos
_cache_pluck = {}
def pluck(freq, dur=0.62, damp=0.9955):
    """Karplus-Strong — corda dedilhada, brilhante e curta."""
    chave = (round(freq, 2), round(dur, 3))
    if chave in _cache_pluck:
        return _cache_pluck[chave]
    L = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, L)
    buf = np.convolve(buf, np.ones(3) / 3, mode='same')   # suaviza o ataque
    n = int(dur * SR)
    out = np.empty(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        nxt = (idx + 1) % L
        buf[idx] = damp * 0.5 * (buf[idx] + buf[nxt])
        idx = nxt
    out *= env(n, 0.002, 0.05, 0.85, 0.18, dur)
    _cache_pluck[chave] = out
    return out

_cache_bell = {}
def bell(freq, dur=1.6):
    chave = (round(freq, 2), round(dur, 2))
    if chave in _cache_bell:
        return _cache_bell[chave]
    n = int(dur * SR)
    seg = np.arange(n) / SR
    y = np.zeros(n)
    for mult, amp, dec in ((1.0, 1.0, 1.0), (2.01, 0.40, 0.62),
                           (3.01, 0.22, 0.42), (4.2, 0.11, 0.26)):
        y += amp * np.sin(2 * np.pi * freq * mult * seg) * np.exp(-seg / (dec * dur * 0.42))
    _cache_bell[chave] = y * 0.5
    return _cache_bell[chave]

def kick(dur=0.40):
    n = int(dur * SR)
    seg = np.arange(n) / SR
    f = 50 + 95 * np.exp(-seg / 0.032)          # queda de altura
    ph = 2 * np.pi * np.cumsum(f) / SR
    corpo = np.sin(ph) * np.exp(-seg / 0.115)
    clique = rng.normal(0, 1, n) * np.exp(-seg / 0.004) * 0.30
    return np.tanh((corpo + clique) * 1.5) * 0.95

def hat(dur=0.055, aberto=False):
    d = 0.20 if aberto else dur
    n = int(d * SR)
    seg = np.arange(n) / SR
    ruido = highpass_fft(rng.normal(0, 1, n), 7500, ordem=3)
    return ruido * np.exp(-seg / (d * 0.30)) * 0.5

def clap(dur=0.34):
    n = int(dur * SR)
    seg = np.arange(n) / SR
    ruido = eq(highpass_fft(rng.normal(0, 1, n), 1300, ordem=2), [(1900, 0.9, 5.0)])
    e = np.exp(-seg / 0.055)
    for atraso in (0.008, 0.017, 0.026):        # ecos curtos = palmas múltiplas
        i = int(atraso * SR)
        e[i:] += np.exp(-seg[: n - i] / 0.05) * 0.75
    return ruido * e * 0.42

def baixo(freq, dur):
    n = int(dur * SR)
    seg = np.arange(n) / SR
    y = np.sin(2 * np.pi * freq * seg) + 0.30 * np.sin(4 * np.pi * freq * seg) \
        + 0.12 * np.sin(6 * np.pi * freq * seg)
    return np.tanh(y * 1.3) * env(n, 0.006, 0.12, 0.72, 0.10, dur) * 0.5

def pad_acorde(freqs, dur):
    n = int(dur * SR)
    seg = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        for det in (0.0, 0.14, -0.15):
            ff = f * (1 + det / 100.0)
            for h in range(1, 5):
                y += np.sin(2 * np.pi * ff * h * seg) / h ** 1.6
    y *= env(n, 0.35, 0.4, 0.85, 0.55, dur)
    return highpass_fft(y, 220, ordem=2) * 0.07

# ---------------------------------------------------------------- harmonia
# I - V - vi - IV em ré maior: D - A - Bm - G  (progressão luminosa)
prog = [
    ('D',  ['F#4', 'A4', 'D5'],  'D2',  ['D4', 'F#4', 'A4', 'D5']),
    ('A',  ['E4', 'A4', 'C#5'],  'A1',  ['A3', 'C#4', 'E4', 'A4']),
    ('Bm', ['F#4', 'B4', 'D5'],  'B1',  ['B3', 'D4', 'F#4', 'B4']),
    ('G',  ['G4', 'B4', 'D5'],   'G1',  ['G3', 'B3', 'D4', 'G4']),
]

NCOMP = int(np.ceil(DUR / COMP))     # ~16 compassos

# níveis por compasso: entra suave, ganha corpo, cresce e resolve
niv_pad = [.35,.45,.60,.70, .85,.95,1.0,1.0, 1.0,1.0,1.0,1.0, .95,.90,.75,.55]
niv_arp = [.00,.35,.55,.70, .90,1.0,1.0,1.0, 1.0,1.0,1.0,1.0, 1.0,.90,.65,.30]
bat_desde, bat_ate = 2, 14           # bateria entra no 3.º compasso e sai perto do fim

mix = np.zeros(N)
arp_seq = [0, 1, 2, 3, 2, 1]          # padrão do arpejo dentro do compasso

for c in range(NCOMP):
    ini = c * COMP
    if ini >= DUR:
        break
    nome, notas_pad, nbaixo, notas_arp = prog[c % 4]
    lp = niv_pad[min(c, len(niv_pad) - 1)]
    la = niv_arp[min(c, len(niv_arp) - 1)]

    # pad sustentado
    coloca(mix, pad_acorde([nota(x) for x in notas_pad], COMP + 0.7), ini, lp)

    # baixo: fundamental nos tempos 1 e 3, oitava no 4.º meio tempo
    if c >= 1:
        coloca(mix, baixo(nota(nbaixo), BAT * 1.6), ini, 0.55)
        coloca(mix, baixo(nota(nbaixo), BAT * 1.2), ini + 2 * BAT, 0.48)
        coloca(mix, baixo(nota(nbaixo) * 2, BAT * 0.5), ini + 3.5 * BAT, 0.26)

    # arpejo em colcheias
    if la > 0:
        for k in range(8):
            golpe = ini + k * BAT / 2
            if golpe >= DUR:
                break
            f = nota(notas_arp[arp_seq[k % len(arp_seq)]])
            acento = 0.30 if k % 2 == 0 else 0.19
            coloca(mix, pluck(f, 0.60), golpe, acento * la)

    # bateria
    if bat_desde <= c <= bat_ate:
        forca = 1.0 if c >= 4 else 0.6
        coloca(mix, kick(), ini, 0.62 * forca)
        coloca(mix, kick(), ini + 2 * BAT, 0.58 * forca)
        if c >= 4:
            coloca(mix, kick(), ini + 3.5 * BAT, 0.34)
        coloca(mix, clap(), ini + 1 * BAT, 0.34 * forca)
        coloca(mix, clap(), ini + 3 * BAT, 0.34 * forca)
        for k in range(8):
            coloca(mix, hat(aberto=(k == 7)), ini + k * BAT / 2,
                   (0.16 if k % 2 == 0 else 0.10) * forca)

    # sino a marcar o início de cada ciclo de 4 compassos
    if c % 4 == 0 and 1 <= c <= 12:
        coloca(mix, bell(nota('D6'), 1.8), ini, 0.16)

# camada de ar
ar = lowpass_fft(rng.normal(0, 1, N), 1100, ordem=3)
mix += ar * (0.45 + 0.55 * np.sin(2 * np.pi * 0.09 * t - 1.1)) * 0.013

# ---------------------------------------------------------------- reverb
def reverb(x, seg=1.9, mistura=0.24):
    L = int(seg * SR)
    imp = rng.normal(0, 1, L) * np.exp(-np.arange(L) / (0.28 * L))
    imp = lowpass_fft(imp, 4200, ordem=2)
    imp[: int(0.010 * SR)] = 0
    imp /= np.abs(imp).sum() / 16
    return (1 - mistura) * x + mistura * np.convolve(x, imp)[:N]

mix = reverb(mix)
mix = highpass_fft(mix, 30, ordem=2)
mix = eq(mix, [
    (300,  0.9, -3.0),    # limpa a lama
    (2600, 0.8, +1.8),    # presença dos plucks
    (7500, 1.1, +3.2),    # brilho
])
mix = lowpass_fft(mix, 15000, ordem=2)
mix = np.tanh(mix * 1.15)

# fades alinhados com o vídeo (fade a negro a 34,1 s)
mix *= np.clip(t / 0.6, 0, 1) * np.clip((DUR - t) / 1.9, 0, 1) ** 1.1
mix /= np.max(np.abs(mix)) + 1e-9

# estéreo com largura moderada
atraso = int(0.009 * SR)
dir_ = np.concatenate([np.zeros(atraso), mix[:-atraso]]) * 0.80 + mix * 0.20
est = np.stack([mix, dir_], axis=1)
est /= np.max(np.abs(est)) + 1e-9
est *= 0.92

with wave.open('assets/musica-epap.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((est * 32767).astype(np.int16).tobytes())

rms = np.sqrt(np.mean(est ** 2))
print(f'escrito: assets/musica-epap.wav  {DUR}s  {BPM:.0f} BPM  ré maior  '
      f'pico={np.max(np.abs(est)):.3f}  rms={20*np.log10(rms):.1f} dBFS')
