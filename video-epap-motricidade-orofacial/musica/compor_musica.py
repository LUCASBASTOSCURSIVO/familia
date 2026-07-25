"""
Faixa original para o vídeo da Especialização em Motricidade Orofacial (EPAP).
Ré menor, ~69 BPM, 35 s. Sintetizada de raiz — sem samples de terceiros.
"""
import numpy as np, wave, struct

SR = 44100
DUR = 35.0
N = int(SR * DUR)
t = np.arange(N) / SR

def nota(nome):
    """Frequência a partir do nome (A4 = 440 Hz)."""
    passos = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    n, oit = nome[:-1], int(nome[-1])
    return 440.0 * 2 ** ((passos[n] + 12 * (oit - 4) - 9) / 12.0)

def env_adsr(ini, dur, a, d, s, r, pico=1.0):
    """Envelope ADSR posicionado no tempo absoluto."""
    e = np.zeros(N)
    i0 = int(ini * SR)
    i1 = min(N, i0 + int(dur * SR))
    if i0 >= N or i1 <= i0:
        return e
    seg = np.arange(i1 - i0) / SR
    out = np.zeros_like(seg)
    ia, idd = seg < a, (seg >= a) & (seg < a + d)
    isus = (seg >= a + d) & (seg < dur - r)
    ire = seg >= dur - r
    out[ia] = seg[ia] / max(a, 1e-6)
    out[idd] = 1 - (1 - s) * (seg[idd] - a) / max(d, 1e-6)
    out[isus] = s
    if ire.any():
        out[ire] = s * np.clip(1 - (seg[ire] - (dur - r)) / max(r, 1e-6), 0, 1)
    e[i0:i1] = out * pico
    return e

def lowpass(x, corte, ordem=2):
    """Filtro passa-baixo de 1.ª ordem aplicado repetidamente."""
    a = np.exp(-2 * np.pi * corte / SR)
    y = x.copy()
    for _ in range(ordem):
        out = np.zeros_like(y)
        z = 0.0
        for i in range(len(y)):
            z = (1 - a) * y[i] + a * z
            out[i] = z
        y = out
    return y

def lowpass_rapido(x, corte, ordem=2):
    """Versão vetorizada via FFT — muito mais rápida para sinais longos."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1.0 / (1.0 + (f / corte) ** 2) ** (ordem / 2.0)
    return np.fft.irfft(X * H, n=len(x))

def highpass_rapido(x, corte, ordem=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    r = f / corte
    H = (r ** 2 / (1.0 + r ** 2)) ** (ordem / 2.0)
    return np.fft.irfft(X * H, n=len(x))

def eq(x, bandas):
    """EQ por multiplicação no domínio da frequência.
    bandas: lista de (centro_hz, largura_oitavas, ganho_db)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    H = np.ones_like(f)
    for centro, larg, db in bandas:
        with np.errstate(divide='ignore'):
            oct_dist = np.log2(np.maximum(f, 1e-6) / centro)
        H *= 10 ** ((db / 20.0) * np.exp(-(oct_dist ** 2) / (2 * larg ** 2)))
    return np.fft.irfft(X * H, n=len(x))

# ---------------------------------------------------------------- pad
def pad(freq, ini, dur, ganho):
    """Serras ligeiramente desafinadas, filtradas — textura de fundo."""
    e = env_adsr(ini, dur, a=1.6, d=1.0, s=0.82, r=2.2, pico=ganho)
    voz = np.zeros(N)
    for det, pan in ((0.0, 1.0), (0.16, 0.7), (-0.19, 0.7)):
        f = freq * (1 + det / 100.0)
        fase = 2 * np.pi * f * t
        # poucos harmónicos e com queda rápida — evita acumular médios-graves
        s = np.zeros(N)
        for h in range(1, 6):
            s += np.sin(fase * h) / h ** 1.5
        voz += s * pan
    # ligeiro vibrato de conjunto
    voz *= 1 + 0.02 * np.sin(2 * np.pi * 0.23 * t)
    # deixa o fundo livre para o sub
    voz = highpass_rapido(voz, 190, ordem=2)
    return voz * e

# ---------------------------------------------------------------- sino
def sino(freq, ini, ganho):
    """Timbre de sino/celesta: parciais inarmónicos com decaimentos distintos."""
    y = np.zeros(N)
    parciais = ((1.0, 1.0, 3.2), (2.01, 0.42, 2.1), (2.99, 0.26, 1.5),
                (4.18, 0.14, 0.9), (5.43, 0.08, 0.6))
    for mult, amp, dec in parciais:
        e = env_adsr(ini, dec, a=0.004, d=dec * 0.85, s=0.0, r=0.05, pico=amp)
        y += np.sin(2 * np.pi * freq * mult * t) * e
    return y * ganho

# ---------------------------------------------------------------- sub
def sub(freq, ini, dur, ganho):
    e = env_adsr(ini, dur, a=0.5, d=0.6, s=0.85, r=1.2, pico=ganho)
    s = np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(4 * np.pi * freq * t)
    return np.tanh(s * 1.2) * e

# ---------------------------------------------------------------- estrutura
# i - VI - III - VII em ré menor: Dm - Bb - F - C
acordes = [
    ('Dm', ['D4', 'F4', 'A4'],  'D2'),
    ('Bb', ['D4', 'F4', 'A#4'], 'A#1'),
    ('F',  ['C4', 'F4', 'A4'],  'F2'),
    ('C',  ['C4', 'E4', 'G4'],  'C2'),
]

COMP = 4.375          # duração de cada acorde (s) — 8 acordes em 35 s
mix = np.zeros(N)

for i in range(8):
    ini = i * COMP
    nome, notas, baixo = acordes[i % 4]
    # o pad cresce ao longo do vídeo e recua no final
    g = [0.09, 0.17, 0.26, 0.31, 0.31, 0.28, 0.21, 0.13][i]
    for nt in notas:
        mix += pad(nota(nt), ini, COMP + 1.6, g)
    mix += sub(nota(baixo), ini, COMP + 0.8, 0.30)

# arpejo de sinos — entra na cena do título (5,2 s) e sai antes do fecho
padrao = [0.0, 1.09, 2.19, 3.28]     # 4 ataques por acorde
oitava = ['D5', 'F5', 'A5', 'F5', 'D5', 'A4', 'F5', 'A5']
for i in range(1, 7):
    ini = i * COMP
    nome, notas, _ = acordes[i % 4]
    for k, off in enumerate(padrao):
        golpe = ini + off
        if golpe < 5.0 or golpe > 30.5:
            continue
        alvo = notas[k % 3]
        f = nota(alvo) * 2                     # uma oitava acima
        amp = 0.21 if k % 2 == 0 else 0.135
        mix += sino(f, golpe, amp)

# pulso grave suave nas cenas de dados (11 s → 29 s)
for p in np.arange(11.0, 29.0, 1.74):
    mix += sub(nota('D2'), p, 0.9, 0.13)

# camada de ar (ruído filtrado) para dar cola ao conjunto
rng = np.random.default_rng(11)
ar = rng.normal(0, 1, N)
ar = lowpass_rapido(ar, 900, ordem=3)
ar *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t - 1.2)) * 0.016
mix += ar

# ---------------------------------------------------------------- reverb
def reverb(x, seg=2.6, mistura=0.34):
    """Convolução com resposta impulsiva sintética (ruído com decaimento)."""
    L = int(seg * SR)
    imp = rng.normal(0, 1, L) * np.exp(-np.arange(L) / (0.34 * L))
    imp = lowpass_rapido(imp, 3200, ordem=2)
    imp[: int(0.012 * SR)] = 0          # pré-atraso
    imp /= np.abs(imp).sum() / 18
    molhado = np.convolve(x, imp)[:N]
    return (1 - mistura) * x + mistura * molhado

mix = reverb(mix)
mix = highpass_rapido(mix, 32, ordem=2)       # limpa o infrassom
mix = eq(mix, [
    (330,  0.9, -4.5),   # tira a lama dos médios-graves
    (1100, 0.8, -1.5),   # abre espaço ao centro
    (6500, 1.1, +3.0),   # ar / brilho dos sinos
])
mix = lowpass_rapido(mix, 13000, ordem=2)     # tira o topo áspero
mix = np.tanh(mix * 1.05)                     # saturação suave

# ---------------------------------------------------------------- masterização
# fade de entrada e saída alinhados com o vídeo (fade a negro a 34,1 s)
fade_in = np.clip(t / 2.2, 0, 1) ** 1.4
fade_out = np.clip((DUR - t) / 2.4, 0, 1) ** 1.2
mix *= fade_in * fade_out

mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89

# estéreo com ligeira largura (Haas)
atraso = int(0.011 * SR)
esq = mix.copy()
dir_ = np.concatenate([np.zeros(atraso), mix[:-atraso]]) * 0.94 + mix * 0.06
est = np.stack([esq, dir_], axis=1)
est /= np.max(np.abs(est)) + 1e-9
est *= 0.9

dados = (est * 32767).astype(np.int16)
with wave.open('assets/musica-epap.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(dados.tobytes())

pico = np.max(np.abs(est))
rms = np.sqrt(np.mean(est ** 2))
print(f'escrito: assets/musica-epap.wav  {DUR}s  pico={pico:.3f}  rms={rms:.4f} '
      f'({20*np.log10(rms):.1f} dBFS)')
