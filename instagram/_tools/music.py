"""Original instrumental for «مدرستي» content: bright C-major study beat, 112 BPM.
Scene changes land on downbeats and each gets a soft chime, so the music follows the information."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
BPM = 112
BEAT = 60 / BPM
BAR = BEAT * 4
import os, json
NBARS = int(os.environ.get("NBARS", 14))
LEN = int(SR * (BAR * NBARS + 2.5))
rng = np.random.default_rng(11)
mix = np.zeros((LEN, 2))

SCENES = json.loads(os.environ.get("SCENES", "[0, 2, 4, 6, 8, 9, 10, 11, 12]"))


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= LEN:
        return
    sig = sig[: LEN - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(sig), 0] += sig * l
    mix[i:i + len(sig), 1] += sig * r


def lp(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2))
    return lfilter(b, a, x)


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def pad(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for det in (-0.1, 0.0, 0.1):
            f = hz(m + det)
            s += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t + 0.5)
    s = lp(s, 1600) * env(n, 0.5, 0.7)
    return s / (len(notes) * 3)


def pluck(m, dur=1.4, bright=0.6):
    """Karplus-Strong — bright marimba/kalimba-like pluck."""
    f = hz(m)
    N = int(SR / f)
    buf = rng.uniform(-1, 1, N)
    n = int(dur * SR)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = 0.5 * (buf[i % N] + buf[(i + 1) % N]) * (0.992 + 0.006 * bright)
    return lp(out, 4200) * env(n, 0.002, 0.25)


def kick():
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    f = 52 + 85 * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)


def snare():
    n = int(0.28 * SR)
    t = np.arange(n) / SR
    no = lp(rng.uniform(-1, 1, n), 5200) * np.exp(-t * 17)
    return 0.6 * no + 0.3 * np.sin(2 * np.pi * 200 * t) * np.exp(-t * 26)


def hat():
    n = int(0.07 * SR)
    no = rng.uniform(-1, 1, n)
    b, a = butter(2, 7500 / (SR / 2), "high")
    return lfilter(b, a, no) * np.exp(-np.arange(n) / SR * 65)


def bass(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) + 0.22 * np.sin(4 * np.pi * hz(m) * t)
    return s * env(n, 0.01, 0.15)


def chime(m):
    n = int(2.0 * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * hz(m) * k * t) * np.exp(-t * (2.2 + k)) / k for k in (1, 2.76, 5.4))
    return s * env(n, 0.003, 0.5)


# C major, uplifting progression: C | Am | F | G
CHORDS = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [65, 69, 72]), (43, [67, 71, 74])]
ARP = [[72, 67, 64, 67, 72, 74, 72, 67], [69, 64, 60, 64, 69, 72, 69, 64],
       [72, 69, 65, 69, 74, 72, 69, 65], [74, 71, 67, 71, 74, 76, 74, 71]]
# bright lead motif on the "feature" sections
LEAD = {6: [(0, 76, 1), (1, 77, 1), (2, 79, 1.5), (3.5, 81, .5)],
        7: [(0, 83, 2), (2, 81, 1), (3, 79, 1)],
        8: [(0, 81, 1), (1, 79, 1), (2, 77, 1), (3, 76, 1)],
        9: [(0, 77, 1.5), (1.5, 76, .5), (2, 74, 1), (3, 76, 1)]}

for b in range(NBARS):
    t0 = b * BAR
    root, notes = CHORDS[b % 4]
    full = 2 <= b < NBARS - 2
    last = b >= NBARS - 2
    add(pad(notes, BAR + 0.8), t0, 0, 0.5 if not last else 0.65)
    for k, m in enumerate(ARP[b % 4]):
        if (not full) and k % 2:
            continue
        add(pluck(m, 1.3), t0 + k * BEAT / 2, 0.35 if k % 2 else -0.35, 0.26)
    if full:
        add(bass(root, BAR * 0.95), t0, 0, 0.32)
        for k in range(4):
            if k in (0, 2):
                add(kick(), t0 + k * BEAT, 0, 0.72)
            if k in (1, 3):
                add(snare(), t0 + k * BEAT, 0.1, 0.33)
        for k in range(8):
            add(hat(), t0 + k * BEAT / 2 + (0.03 if k % 2 else 0), 0.2, 0.11 if k % 2 else 0.17)
    if full and (b % 16) in LEAD:
        for off, m, dur in LEAD[b % 16]:
            add(pluck(m - 12, dur * BEAT + 0.5, 1.0), t0 + off * BEAT, -0.1, 0.4)

# scene-change chimes, alternating notes of the C triad up top
for i, b in enumerate(SCENES):
    add(chime([84, 81, 79][i % 3]), b * BAR, 0.2 if i % 2 else -0.2, 0.12)
add(pluck(36, 2.6), NBARS * BAR - BAR, 0, 0.5)

mix = np.tanh(mix * 1.35) / np.tanh(1.35)
end = int((NBARS * BAR + 1.0) * SR)
fade = np.ones(LEN)
fade[end - int(2.5 * SR):end] = np.linspace(1, 0, int(2.5 * SR))
fade[end:] = 0
mix *= fade[:, None]
mix = mix[: end]
mix /= np.abs(mix).max() * 1.12
wavfile.write(os.environ.get("OUT", "/home/claude/ms/out/ms_music.wav"), SR, (mix * 32767).astype(np.int16))
print("len", len(mix) / SR)
