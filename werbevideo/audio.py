#!/usr/bin/env python3
"""Soundtrack für den AquaForce-Nord-Spot (30 s, 48 kHz, Stereo) → soundtrack.wav

Alles wird synthetisiert (nur numpy) und an dieselbe Timeline wie index.html gebunden:
120 BPM, damit jeder Szenenwechsel (4 / 9 / 16 / 22 s) exakt auf einem Schlag liegt.

  Musik   : dunkles Pad (D-Moll-Farben) mit langsam öffnender Klangfarbe,
            gedämpftes Arpeggio ab Szene 2, weiche Kick nur im Ergebnis-Teil,
            Auflösung nach Dsus2 beim Logo.
  Sound   : Licht-Whoosh, Tropfen-Plink, Riser vor jedem Schnitt, tiefe Bassimpulse,
            Hochdruckstrahl (Zeitlupe = tiefer & gefiltert, Stereo folgt dem Strahl),
            Gischt-Prasseln, Logo-Hit mit Glocke + Schimmer, dezente UI-Ticks.

  python3 audio.py              → soundtrack.wav
"""
import wave
import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(2026)

mix = np.zeros((2, N))      # trocken
send = np.zeros((2, N))     # Hall-Send


def sstep(a, b, x):
    k = np.clip((x - a) / (b - a), 0, 1)
    return k * k * (3 - 2 * k)


def place(sig, t0, pan=0.0, gain=1.0, rev=0.0):
    """Mono- oder Stereo-Signal bei t0 einfügen (Equal-Power-Panorama, pan -1…1)."""
    i0 = int(round(t0 * SR))
    if sig.ndim == 1:
        p = np.asarray(pan, dtype=float)
        l = np.cos((p + 1) * np.pi / 4)
        r = np.sin((p + 1) * np.pi / 4)
        sig = np.vstack([sig * l, sig * r])
    if i0 < 0:
        sig = sig[:, -i0:]
        i0 = 0
    n = min(sig.shape[1], N - i0)
    if n <= 0:
        return
    mix[:, i0:i0 + n] += sig[:, :n] * gain
    send[:, i0:i0 + n] += sig[:, :n] * gain * rev


def shaped_noise(n, shape, seed=None):
    """Rauschen mit beliebigem Betragsspektrum shape(freq_hz)."""
    r = np.random.default_rng(seed) if seed is not None else rng
    f = np.fft.rfftfreq(n, 1 / SR)
    spec = (r.normal(size=f.size) + 1j * r.normal(size=f.size)) * shape(np.maximum(f, 1))
    x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-9)


def band(lo, hi, slope=2.0):
    return lambda f: 1 / (1 + (lo / f) ** (2 * slope)) / (1 + (f / hi) ** (2 * slope))


def note(n):  # MIDI → Hz
    return 440.0 * 2 ** ((n - 69) / 12)


# ── Musik ────────────────────────────────────────────────────────────────────
# Akkorde (MIDI): Dm(add9) → B♭maj7 → Fmaj9 → Dsus2
CHORDS = [
    (0.0, 9.6, [50, 57, 64, 65]),        # D3 A3 E4 F4
    (8.6, 16.6, [46, 53, 57, 62]),       # B♭2 F3 A3 D4
    (15.6, 22.9, [53, 60, 64, 67, 69]),  # F3 C4 E4 G4 A4
    (21.9, 30.0, [50, 57, 62, 64, 69]),  # D3 A3 D4 E4 A4
]


def brightness(t):
    # Anzahl hörbarer Obertöne: dunkel → öffnet sich zur Transformation → hell beim Ergebnis
    b = 1.6 + 1.6 * sstep(1, 9, t) + 1.8 * sstep(9, 16, t) + 1.4 * sstep(16, 18, t) - 1.0 * sstep(22.4, 26, t)
    b -= 1.4 * sstep(10.4, 10.9, t) * (1 - sstep(13.0, 13.6, t))  # Zeitlupe: dumpf
    return b


def pad_voice(f0, t, bright):
    out = np.zeros_like(t)
    for det, ph in ((-0.0023, 0.3), (0.0, 1.1), (0.0021, 2.4)):
        f = f0 * (1 + det) * (1 + 0.0012 * np.sin(2 * np.pi * 0.21 * t + ph))
        phase = 2 * np.pi * np.cumsum(f) / SR
        for k in range(1, 11):
            out += np.exp(-k / bright) / k * np.sin(k * phase + ph * k)
    return out / 3


for t0, t1, notes in CHORDS:
    i0, i1 = int(t0 * SR), int(t1 * SR)
    t = T[i0:i1]
    e = sstep(t0, t0 + 1.0, t) * (1 - sstep(t1 - 1.0, t1, t))
    if t0 == 0.0:
        e = (0.35 + 0.65 * sstep(0.0, 2.5, t)) * sstep(0.0, 0.15, t) * (1 - sstep(t1 - 1.0, t1, t))
    if t1 == 30.0:
        e = sstep(t0, t0 + 0.6, t) * (1 - sstep(28.4, 30.0, t))
    br = brightness(t)
    sig = np.zeros((2, t.size))
    for j, n in enumerate(notes):
        v = pad_voice(note(n), t, br) * e
        pan = (j / max(1, len(notes) - 1) - 0.5) * 0.7
        sig[0] += v * np.cos((pan + 1) * np.pi / 4)
        sig[1] += v * np.sin((pan + 1) * np.pi / 4)
    swell = 0.55 + 0.25 * sstep(4, 9, t) + 0.25 * sstep(9, 15.5, t) - 0.15 * sstep(16, 17, t) + 0.2 * sstep(22.4, 23.5, t)
    place(sig * swell, t0, gain=0.075, rev=0.5)

# Arpeggio (8tel bei 120 BPM)
ARP = [(4.0, 9.0, [62, 65, 69, 72, 69, 65]), (9.0, 16.0, [58, 62, 65, 69, 65, 62]),
       (16.0, 22.5, [65, 69, 72, 76, 72, 69])]


def arp_gain(t):
    g = sstep(4.0, 6.5, t) * 0.7 + 0.3 * sstep(8, 9, t)
    g *= 1 - sstep(10.3, 10.6, t) * (1 - sstep(13.3, 14.2, t))
    g *= 1 - sstep(22.2, 22.5, t)
    return g


for a0, a1, pat in ARP:
    step = 0.25
    for i in range(int((a1 - a0) / step)):
        ts = a0 + i * step
        g = arp_gain(ts)
        if g < 0.01:
            continue
        f = note(pat[i % len(pat)])
        d = np.arange(int(SR * 0.6)) / SR
        env = (1 - np.exp(-d / 0.003)) * np.exp(-d / (0.16 + 0.08 * (ts > 16)))
        cutoff = 2.5 if ts < 16 else 4.0
        s = sum(np.exp(-k / cutoff) / k * np.sin(2 * np.pi * f * k * d) for k in range(1, 6)) * env
        place(s, ts, pan=0.35 * np.sin(i * 1.3), gain=0.05 * g * (0.85 + 0.15 * (i % 2 == 0)), rev=0.6)


def kick(level=1.0):
    d = np.arange(int(SR * 0.6)) / SR
    f = 46 + 70 * np.exp(-d / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-d / 0.28) * (1 - np.exp(-d / 0.002)) * level


for i in range(12):                     # weiche Kick im Ergebnis-Teil, Halbtempo
    ts = 16.0 + i * 0.5
    if ts >= 22.0:
        break
    place(kick(1.0 if i % 2 == 0 else 0.45), ts, gain=0.32)


# ── Sounddesign ─────────────────────────────────────────────────────────────
def sub_hit(dur=2.2, f0=52, f1=36, noise=0.25):
    d = np.arange(int(SR * dur)) / SR
    f = f1 + (f0 - f1) * np.exp(-d / 0.4)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / (dur / 3.2)) * (1 - np.exp(-d / 0.004))
    nz = shaped_noise(d.size, band(30, 300)) * np.exp(-d / 0.08) * noise
    return s + nz


for t0, g in ((4.0, 0.3), (9.0, 0.5), (16.0, 0.32), (18.0, 0.15), (20.0, 0.15), (22.45, 0.5)):
    place(sub_hit(), t0, gain=g, rev=0.15)


def riser(dur, peak_hz=5000):
    n = int(SR * dur)
    d = np.linspace(0, 1, n)
    lo = shaped_noise(n, band(300, 1500))
    hi = shaped_noise(n, band(2500, peak_hz * 2))
    e = d ** 3
    s = (lo * (1 - d) + hi * d) * e
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 700 * d ** 2) / SR) * e * 0.25
    return s + sweep


for t_hit, dur, g in ((4.0, 1.3, 0.13), (9.0, 1.9, 0.2), (16.0, 1.1, 0.12), (22.45, 1.6, 0.16)):
    place(riser(dur), t_hit - dur, gain=g, rev=0.4)

# Szene 1: Lichtstrahl-Whoosh (L → R, folgt dem Strahl)
n = int(SR * 2.8)
d = np.linspace(0, 1, n)
w = shaped_noise(n, band(350, 3200)) * np.exp(-((d - 0.5) / 0.22) ** 2)
place(w, 0.15, pan=np.linspace(-0.85, 0.85, n), gain=0.12, rev=0.5)


def plink(f0=900, f1=2300, level=1.0):
    d = np.arange(int(SR * 0.35)) / SR
    f = f1 - (f1 - f0) * np.exp(-d / 0.012)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / 0.045) * (1 - np.exp(-d / 0.0008))
    s += 0.5 * np.sin(2 * np.pi * 320 * d) * np.exp(-d / 0.08)
    s += shaped_noise(d.size, band(3000, 12000)) * np.exp(-d / 0.012) * 0.25
    return s * level


place(plink(), 1.72, gain=0.22, rev=0.8)
place(plink(1300, 3100, 0.5), 1.93, pan=-0.3, gain=0.2, rev=0.8)
place(plink(1500, 3600, 0.35), 2.08, pan=0.35, gain=0.2, rev=0.8)
place(sub_hit(1.6, 60, 40, 0.0), 1.72, gain=0.18)

# Szene 3: Hochdruckstrahl
J0, J1 = 9.0, 15.4


def speed(t):
    return 1 - 0.74 * sstep(10.4, 10.9, t) * (1 - sstep(13.0, 13.6, t))


tt = np.arange(J0, 16.5, 1 / 600)
simt = np.concatenate([[0], np.cumsum(speed(tt) * (1 / 600))])[:-1]
sim_end = np.interp(J1, tt, simt)
i0, i1 = int(J0 * SR), int(16.2 * SR)
t = T[i0:i1]
p = np.clip(np.interp(t, tt, simt) / sim_end, 0, 1)
pan = -0.8 + 1.6 * p
jet_env = sstep(J0, J0 + 0.06, t) * (1 - sstep(J1 - 0.3, J1 + 0.4, t))
slow = (1 - speed(t)) / 0.74
rough = 1 + 0.18 * shaped_noise(t.size, band(4, 40, 1))
hiss = shaped_noise(t.size, lambda f: band(900, 9000, 1.2)(f) + 0.6 * band(70, 400, 1.5)(f))
dull = shaped_noise(t.size, lambda f: band(40, 700, 2)(f))
jet = (hiss * (1 - slow) * 1.0 + dull * slow * 1.3) * jet_env * rough
place(jet, J0, pan=pan, gain=0.2, rev=0.15)
# Gischt-Prasseln: kurze Wassertropfen-Klicks, dichter bei Normaltempo
for k in range(int((J1 - J0) * 70)):
    ts = J0 + rng.random() * (J1 - J0)
    g = float(np.interp(ts, t[::100] + 0, (jet_env * (1 - slow))[::100]))
    if g < 0.05:
        continue
    d = np.arange(int(SR * 0.02)) / SR
    c = shaped_noise(d.size, band(2500, 11000)) * np.exp(-d / 0.003)
    pp = -0.8 + 1.6 * float(np.interp(ts, t[::100], p[::100]))
    place(c, ts, pan=np.clip(pp + rng.normal() * 0.2, -1, 1), gain=0.05 * g * rng.random())
# Zeitlupe: Ab- und Aufwärts-„Zeitdehnung" + Herzschlag-Sub
for ts, up in ((10.35, False), (12.95, True)):
    n = int(SR * 0.7)
    d = np.linspace(0, 1, n)
    f = (90 + 600 * d ** 2) if up else (690 - 600 * d ** 0.5)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * d) ** 2
    s += shaped_noise(n, band(150, 1500)) * np.sin(np.pi * d) ** 2 * 0.5
    place(s, ts, gain=0.12, rev=0.6)
for ts in (11.0, 11.9, 12.8):
    place(sub_hit(1.0, 48, 34, 0.1), ts, gain=0.22)

# Szene 4: Swishes bei den Schnitten + dezente Ticks zu den Wörtern


def swish(dur=0.4):
    n = int(SR * dur)
    d = np.linspace(0, 1, n)
    return shaped_noise(n, band(900, 7000)) * np.sin(np.pi * d) ** 3


def tick(f=4200, level=1.0):
    d = np.arange(int(SR * 0.05)) / SR
    return np.sin(2 * np.pi * f * d) * np.exp(-d / 0.006) * level


n = int(SR * 0.4)
for ts in (17.85, 19.85):
    place(swish(), ts, pan=np.linspace(-0.6, 0.6, n), gain=0.07, rev=0.4)
for ts in (16.35, 18.35, 20.35):
    place(tick(), ts, gain=0.05, rev=0.5)

# Szene 5: Logo-Hit, Glocke, Schimmer, Lichtkante, CTA
LOGO = 22.45
d = np.arange(int(SR * 5)) / SR
bell = sum(a * np.sin(2 * np.pi * note(74) * r * d) * np.exp(-d / dec)
           for r, a, dec in ((1, 1, 3.2), (2.0, .45, 1.9), (3.01, .22, 1.1), (4.2, .12, .7), (5.43, .07, .45)))
bell *= 1 - np.exp(-d / 0.002)
place(bell, LOGO, gain=0.09, rev=0.9)
place(sub_hit(3.0, 50, 32, 0.35), LOGO, gain=0.25)
n = int(SR * 4)
d = np.linspace(0, 1, n)
shim = sum(np.sin(2 * np.pi * note(m) * d * 4 + m) * (0.6 + 0.4 * np.sin(2 * np.pi * (3 + j) * d * 4))
           for j, m in enumerate((86, 88, 93)))
shim *= np.sin(np.pi * d) ** 2
place(shim, LOGO, gain=0.012, rev=1.0)
n = int(SR * 1.1)
place(swish(1.1), 23.1, pan=np.linspace(-0.5, 0.5, n), gain=0.05, rev=0.6)
place(tick(3000, 0.6), 24.15, gain=0.05, rev=0.6)
for j, m in enumerate((74, 78, 81)):  # CTA: weicher Akkord-Pling
    dd = np.arange(int(SR * 1.5)) / SR
    s = np.sin(2 * np.pi * note(m) * dd) * np.exp(-dd / 0.5) * (1 - np.exp(-dd / 0.003))
    place(s, 25.55 + j * 0.03, pan=(j - 1) * 0.3, gain=0.05, rev=0.8)
place(tick(3600, 0.5), 26.55, gain=0.04, rev=0.6)

# ── Hall (Faltung mit synthetischer Impulsantwort) ──────────────────────────
L = int(SR * 2.8)
dl = np.arange(L) / SR
ir = np.vstack([shaped_noise(L, lambda f: 1 / (1 + (f / 6000) ** 2), seed=s) * np.exp(-dl / 0.6) for s in (1, 2)])
ir[:, :int(SR * 0.012)] = 0
ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
nfft = 1 << int(np.ceil(np.log2(N + L)))
wet = np.vstack([np.fft.irfft(np.fft.rfft(send[c], nfft) * np.fft.rfft(ir[c], nfft), nfft)[:N] for c in range(2)])
out = mix + wet * 0.35

# ── Master ──────────────────────────────────────────────────────────────────
f = np.fft.rfftfreq(N, 1 / SR)
hp = 1 / np.sqrt(1 + (28 / np.maximum(f, 1)) ** 4)
out = np.vstack([np.fft.irfft(np.fft.rfft(out[c]) * hp, N) for c in range(2)])
out *= 1 - sstep(29.2, 30.0, T)
# Pegel auf ≈ -14 LUFS (Social-Media-Norm), Spitzen per Limiter mit Lookahead abfangen
out *= 10 ** (-15.5 / 20) / np.sqrt((out ** 2).mean())
ceil = 10 ** (-1.2 / 20)
pk = np.abs(out).max(axis=0)
win = int(SR * 0.004)
pad = np.concatenate([pk, np.zeros(win)])
env = np.max(np.lib.stride_tricks.sliding_window_view(pad, win + 1), axis=1)[:N]   # Lookahead 4 ms
g = np.minimum(1, ceil / np.maximum(env, 1e-9))
a = np.exp(-1 / (SR * 0.08))                                                      # Release 80 ms
gs = g.copy()
for i in range(1, N):
    gs[i] = min(g[i], a * gs[i - 1] + (1 - a) * g[i])
out *= gs
out = np.clip(out, -ceil, ceil)
rms = 20 * np.log10(np.sqrt((out ** 2).mean()))
pcm = (out.T * 32767).astype('<i2')
with wave.open('soundtrack.wav', 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm.tobytes())
print(f'soundtrack.wav · {DUR:.0f} s · Peak -1 dBFS · RMS {rms:.1f} dBFS')
