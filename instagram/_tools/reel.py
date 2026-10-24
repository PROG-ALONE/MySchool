"""مدرستي launch reel — 1080x1920, 30fps, motion graphics synced to music (112 BPM, bar = 2.14s)."""
from common import *
import subprocess, sys, math

W, H, FPS = 1080, 1920, 30
BAR = 60 / 112 * 4
M = 100
R = W - M
DUR = 32.0
SC = [(0, 2), (2, 4), (4, 6), (6, 7.5), (7.5, 9), (9, 10.5), (10.5, 12), (12, 14.93)]

BGIMG = background(W, H, glow=(0.75, 0.3)).convert("RGBA")


def col(c, a):
    return (*c, int(255 * max(0, min(1, a))))


def T(d, xy, s, f, c, a, anchor="ra"):
    if a > 0.01:
        text(d, xy, s, f, col(c, a), anchor)


def ph(t, start, dur=0.5):
    return ease((t - start) / dur)


def kicker(d, y, s, a):
    f = font("semi", 40)
    w = tw(s, f)
    rrect(d, (R - w - 52, y, R, y + 78), 39, outline=col(GOLD, a), width=3)
    T(d, (R - 26, y + 12), s, f, GOLD, a)


def sc_hook(d, t):
    a1 = ph(t, 0.1, 0.6)
    T(d, (W / 2, 620 - 30 * (1 - a1)), "تعبت من حساب درجات طلابك يدوياً؟", font("bold", 72), CREAM, a1, "ma")
    a2 = ph(t, 1.6, 0.6)
    T(d, (W / 2, 780 - 30 * (1 - a2)), "ومن توزيع قاعات الامتحان كل فصل؟", font("bold", 72), GOLD, a2, "ma")
    for k in range(9):
        p = ph(t, 0.3 + k * 0.12, 1.2)
        x = 140 + k * 100
        y = 1020 + 220 * p + 40 * math.sin(k * 1.7)
        if p > 0:
            rrect(d, (x - 34, y - 24, x + 34, y + 24), 8, outline=col(GOLD, p * 0.8), width=3)
            T(d, (x, y - 18), "٪" if k % 2 else "٩٠", font("bold", 30), GOLD, p * 0.8, "ma")
    a3 = ph(t, 3.0, 0.6)
    T(d, (W / 2, 1420), "الدفاتر الورقية لا تكفي بعد اليوم…", font("body", 46), MUTED, a3, "ma")


def sc_logo(d, t):
    p = ph(t, 0.0, 1.0)
    cx, cy = W / 2, 680
    rot = 0
    for rr, wd, sp in ((190, 5, 1), (120, 3, -1.4)):
        rot = sp * 25 * (1 - p) + sp * t * 4
        pts = [(cx + rr * p * math.cos(math.radians(60 * k - 90 + rot)),
                cy + rr * p * math.sin(math.radians(60 * k - 90 + rot))) for k in range(6)]
        if p > 0.02:
            d.polygon(pts, outline=col(GOLD, p), width=wd)
    a = ph(t, 0.7, 0.8)
    T(d, (cx, 940 + 40 * (1 - a)), "مدرستي", font("head", 150), GOLD, a, "ma")
    b = ph(t, 1.6, 0.7)
    T(d, (cx, 1230), "نظام إدارة شامل لكل معلّم", font("bold", 58), CREAM, b, "ma")


def sc_grades(d, t):
    kicker(d, 310, "الدرجات الشهرية والسنوية", ph(t, 0))
    T(d, (R, 430), "كل طلابك… بدرجاتهم كاملة", font("bold", 66), CREAM, ph(t, 0.15))
    rows = [("أحمد كريم", "٨٥", TEAL), ("سارة علي", "٩٢", GOLD), ("محمد ياسر", "٧٨", (120, 160, 220))]
    for k, (n, sc, c) in enumerate(rows):
        p = ph(t, 0.5 + k * 0.3, 0.6)
        if p <= 0:
            continue
        x = R + (1 - p) * 500
        y = 580 + k * 180
        rrect(d, (x - (R - M), y, x, y + 150), 28, fill=col(PANEL, p))
        T(d, (x - 36, y + 26), n, font("semi", 42), CREAM, p)
        rrect(d, (x - (R - M) + 30, y + 90, x - (R - M) + 130, y + 136), 18, fill=col(c, p))
        T(d, (x - (R - M) + 80, y + 95), sc, font("bold", 36), BG, p, "ma")
    p = ph(t, 2.2, 0.6)
    rrect(d, (M, 1150, R, 1370), 32, outline=col(GOLD, p), width=3)
    T(d, (R - 40, 1180), "قوالب جاهزة لكل مادة", font("semi", 44), GOLD, p)
    T(d, (R - 40, 1260), "تحسب المعدل تلقائياً شهرياً وسنوياً", font("body", 40), CREAM, p)


def sc_timetable(d, t):
    kicker(d, 310, "الجدول الأسبوعي", ph(t, 0))
    T(d, (R, 430), "حصصك كلها أمامك دفعة واحدة", font("bold", 66), CREAM, ph(t, 0.15))
    days = ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس"]
    cw = (R - M) / 5
    for k, dname in enumerate(days):
        p = ph(t, 0.3 + k * 0.12, 0.5)
        if p <= 0:
            continue
        x1 = R - k * cw
        rrect(d, (x1 - cw + 8, 600, x1 - 8, 600 + 420 * p), 18,
              fill=col(GOLD if k == 2 else PANEL, p))
        T(d, (x1 - cw / 2, 630), dname, font("semi", 34), CREAM if k != 2 else BG, p, "ma")


def sc_bank(d, t):
    kicker(d, 310, "دفتر الأسئلة", ph(t, 0))
    T(d, (R, 430), "بنك أسئلة لكل مادة وفصل", font("bold", 66), CREAM, ph(t, 0.15))
    cx, cy, r = W / 2, 900, 220
    a = ph(t, 0.2, 0.4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col((30, 70, 110), a), width=34)
    g = ph(t, 0.3, 1.3)
    if g > 0:
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * 0.78 * g, fill=col(GOLD, 1), width=34)
    T(d, (cx, cy - 60), ar(151), font("bold", 100), CREAM, a, "ma")
    b = ph(t, 1.1, 0.5)
    T(d, (cx, 1190), "سؤالاً جاهزاً للاستخدام الفوري", font("semi", 46), GOLD, b, "ma")


def sc_exam(d, t):
    kicker(d, 310, "قاعات الامتحان", ph(t, 0))
    T(d, (R, 430), "توزيع الطلاب على القاعات بضغطة", font("bold", 62), CREAM, ph(t, 0.1))
    for k in range(6):
        p = ph(t, 0.3 + k * 0.1, 0.4)
        if p <= 0:
            continue
        x = R - (k % 3) * 260
        y = 620 + (k // 3) * 260
        rrect(d, (x - 220, y, x, y + 200), 22, fill=col(PANEL, p), outline=col(GOLD, p), width=2)
        T(d, (x - 110, y + 80), f"قاعة {ar(k+1)}", font("semi", 36), CREAM, p, "ma")
    b = ph(t, 1.3, 0.5)
    T(d, (W / 2, 1330), "بلا تعارض أسماء… وبلا ورق", font("bold", 50), GOLD, b, "ma")


def sc_offline(d, t):
    kicker(d, 330, "بلا إنترنت", ph(t, 0))
    T(d, (R, 450), "يعمل من دون اتصال بعد أول فتح", font("bold", 68), CREAM, ph(t, 0.15))
    a = ph(t, 0.6, 0.6)
    T(d, (W / 2, 900), "على هاتفك أو حاسوبك، كتطبيق مثبّت", font("semi", 50), GOLD, a, "ma")


def sc_end(d, t):
    p = ph(t, 0.0, 0.9)
    cx = W / 2
    rot = t * 6
    pts = [(cx + 150 * p * math.cos(math.radians(60 * k - 90 + rot)),
            560 + 150 * p * math.sin(math.radians(60 * k - 90 + rot))) for k in range(6)]
    if p > 0.02:
        d.polygon(pts, outline=col(GOLD, p), width=5)
    a = ph(t, 0.4, 0.7)
    T(d, (cx, 770), "مدرستي", font("head", 150), GOLD, a, "ma")
    b = ph(t, 1.0, 0.6)
    T(d, (cx, 1000), "تصميم وتطوير: حيدر نصيف", font("semi", 50), CREAM, b, "ma")
    c = ph(t, 1.8, 0.6)
    rrect(d, (M, 1140, R, 1390), 34, outline=col(GOLD, c), width=3)
    T(d, (cx, 1170), "جرّبه الآن", font("bold", 58), CREAM, c, "ma")
    if c > 0.01:
        d.text((cx, 1270), "prog-alone.github.io/myschool", font=font("semi", 42), fill=col(GOLD, c),
               anchor="ma", direction="ltr")


SCENES = [sc_hook, sc_logo, sc_grades, sc_timetable, sc_bank, sc_exam, sc_offline, sc_end]


def render(i):
    t = i / FPS
    img = BGIMG.copy()
    for (b0, b1), fn in zip(SC, SCENES):
        s, e = b0 * BAR, b1 * BAR
        if not (s - 0.01 <= t < e):
            continue
        lt = t - s
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fn(ImageDraw.Draw(layer), lt)
        last = fn is sc_end
        fade_out = 1.0 if last else ease_io((e - t) / 0.3)
        fade_in = ease_io(lt / 0.25) if fn is not sc_hook else 1.0
        if last:
            fade_out = ease_io((DUR - t) / 1.2)
        k = min(fade_in, fade_out)
        if k < 1:
            al = layer.getchannel("A").point(lambda v: int(v * k))
            layer.putalpha(al)
        dy = int(-40 * (1 - fade_out)) if not last else 0
        img.alpha_composite(layer, (0, dy))
    d = ImageDraw.Draw(img)
    brand_mark(d, R, 150, 44)
    d.rectangle((W - (W * t / DUR), 0, W, 8), fill=GOLD)
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for tt in [3.5, 8, 13.5, 18.8, 23, 26, 28.5, 30.5]:
            render(int(tt * FPS)).resize((360, 640)).save(f"/tmp/claude-0/ms_{tt}.jpg", quality=85)
        sys.exit()
    n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "/home/claude/ms/out/ms_music.wav",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          "/home/claude/ms/out/ms_reel.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(render(i).tobytes())
    p.stdin.close(); p.wait()
    print("done", p.returncode)
