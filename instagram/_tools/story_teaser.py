"""Mysterious teaser story (12s): hint → reveal مدرستي → point to tomorrow's reel and post."""
from common import *
import subprocess, math

W, H, FPS, DUR = 1080, 1920, 30, 12.0
BGI = background(W, H, glow=(0.5, 0.42)).convert("RGBA")
DARK = Image.new("RGBA", (W, H), (5, 14, 24, 255))


def col(c, a):
    return (*c, int(255 * max(0, min(1, a))))


def ph(t, s, d=0.6):
    return ease((t - s) / d)


def out(t, s, d=0.4):
    return 1 - ease((t - s) / d)


def frame(i):
    t = i / FPS
    light = ease_io(t / 7.0)
    img = Image.blend(DARK, BGI, 0.25 + 0.75 * light)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    cx = W / 2
    a = min(ph(t, 0.3), out(t, 2.1))
    if a > 0.01:
        text(d, (cx, 760), "شيء كنت أبنيه لكل معلّم…", font("bold", 66), col(CREAM, a), "ma")
    b = min(ph(t, 2.4), out(t, 4.4))
    if b > 0.01:
        text(d, (cx, 760), "يُنهي الدرجات والجداول والقاعات", font("bold", 66), col(GOLD, b), "ma")
    p = ph(t, 4.6, 1.4)
    rot = 60 * (1 - p) + t * 5
    pts = [(cx + 190 * p * math.cos(math.radians(60 * k - 90 + rot)),
            700 + 190 * p * math.sin(math.radians(60 * k - 90 + rot))) for k in range(6)]
    if p > 0.02:
        d.polygon(pts, outline=col(GOLD, p), width=5)
    n = ph(t, 5.8, 0.9)
    text(d, (cx, 940 + 30 * (1 - n)), "مدرستي", font("head", 180), col(GOLD, n), "ma")
    c = ph(t, 8.6, 0.6)
    if c > 0.01:
        rrect(d, (100, 1320, W - 100, 1560), 40, outline=col(GOLD, c), width=3)
    text(d, (cx, 1350), "القصة كاملة غداً في الريلز والمنشور", font("bold", 50), col(CREAM, c), "ma")
    if c > 0.01:
        y = 1460 + 10 * math.sin(t * 6)
        d.line((cx, y, cx, y + 50), fill=col(GOLD, c), width=5)
        d.line((cx - 20, y + 30, cx, y + 52), fill=col(GOLD, c), width=5)
        d.line((cx + 20, y + 30, cx, y + 52), fill=col(GOLD, c), width=5)
    f = ph(t, 9.4, 0.6)
    d.text((cx, 1610), "@h.nj2", font=font("bold", 50), fill=col(GOLD, f), anchor="ma", direction="ltr")
    img.alpha_composite(L)
    return img.convert("RGB")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for tt in (1.5, 3.5, 7.5, 11):
            frame(int(tt * FPS)).resize((360, 640)).save(f"/tmp/claude-0/ms_ts_{tt}.jpg")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-ss", "0", "-t", str(DUR), "-i", "/home/claude/ms/out/ms_music.wav",
                          "-af", f"afade=t=out:st={DUR-1.5}:d=1.5", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          "/home/claude/ms/out/ms_story.mp4"], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("done", p.returncode)
