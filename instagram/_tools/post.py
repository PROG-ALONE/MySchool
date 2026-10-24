"""مدرستي launch carousel — 8 slides, 1080x1350 (4:5)."""
from common import *
import os

W, H = 1080, 1350
M = 96
R = W - M
OUT = "/home/claude/ms/out/post"
os.makedirs(OUT, exist_ok=True)
N = 8


def frame(i, glow=(0.8, 0.15)):
    img = background(W, H, glow=glow)
    d = ImageDraw.Draw(img)
    brand_mark(d, R, 70, 40)
    text(d, (M, 78), f"{ar(i)} / {ar(N)}", font("semi", 30), MUTED, "la")
    return img, d


def footer(d, s="اسحب للتالي"):
    f = font("body", 30)
    w = tw(s, f)
    x0 = W / 2 - (w + 60) / 2
    text(d, (x0 + 60 + w, H - 100), s, f, MUTED)
    y = H - 80
    d.line((x0, y, x0 + 38, y), fill=MUTED, width=3)
    d.line((x0, y, x0 + 14, y - 12), fill=MUTED, width=3)
    d.line((x0, y, x0 + 14, y + 12), fill=MUTED, width=3)


def kicker(d, y, s):
    f = font("semi", 34)
    w = tw(s, f)
    rrect(d, (R - w - 44, y, R, y + 66), 33, outline=GOLD, width=2)
    text(d, (R - 22, y + 10), s, f, GOLD)


def card(d, box, fill=PANEL, outline=None):
    rrect(d, box, 34, fill=fill, outline=outline, width=2)


def s1():
    img, d = frame(1, glow=(0.5, 0.35))
    cx = W / 2
    rrect(d, (cx - 300, 250, cx + 300, 600), 40, fill=PANEL, outline=GOLD, width=3)
    badge(d, cx, 425, 92, GOLD, 4)
    badge(d, cx, 425, 52, GOLD, 2)
    text(d, (cx, 760), "مدرستي", font("head", 130), GOLD, "ma")
    text(d, (cx, 970), "نظام إدارة شامل صممته لكل معلّم", font("bold", 50), CREAM, "ma")
    text(d, (cx, 1060), "الدرجات، الجداول، الأسئلة، وقاعات الامتحان… في مكان واحد", font("body", 36), MUTED, "ma")
    footer(d)
    return img


def s2():
    img, d = frame(2)
    kicker(d, 200, "لماذا بنيته؟")
    y = 330
    y = para(d, R, y, "كل معلّم يقضي ساعات في حساب الدرجات يدوياً…", font("bold", 56), CREAM, W - 2 * M, 1.45)
    y = para(d, R, y + 20, "وساعات أخرى في توزيع قاعات الامتحان ورقياً.", font("bold", 56), GOLD, W - 2 * M, 1.45)
    y += 70
    for s in ["دفاتر درجات منفصلة لكل صف ومادة", "لا رابط بين الدرجات والجدول والأسئلة", "توزيع القاعات يدوياً كل فصل دراسي"]:
        d.ellipse((R - 26, y + 18, R, y + 44), fill=RED)
        text(d, (R - 50, y), s, font("body", 40), CREAM)
        y += 86
    y += 40
    text(d, (R, y), "فصممت نظاماً واحداً يجمعها كلها", font("head", 56), TEAL)
    footer(d)
    return img


def s3():
    img, d = frame(3)
    kicker(d, 200, "الدرجات الشهرية والسنوية")
    text(d, (R, 300), "قوالب جاهزة لكل مادة", font("bold", 56), CREAM)
    text(d, (R, 385), "تُحسب المعدلات تلقائياً شهرياً وسنوياً", font("body", 40), MUTED)
    rows = [("أحمد كريم", "٨٥", TEAL), ("سارة علي", "٩٢", GOLD), ("محمد ياسر", "٧٨", (120, 160, 220))]
    y = 480
    for n, sc, c in rows:
        card(d, (M, y, R, y + 150))
        text(d, (R - 36, y + 50), n, font("semi", 42), CREAM)
        rrect(d, (M + 30, y + 42, M + 130, y + 112), 20, fill=c)
        text(d, (M + 80, y + 54), sc, font("bold", 40), BG, "ma")
        y += 190
    footer(d)
    return img


def s4():
    img, d = frame(4)
    kicker(d, 200, "الجدول الأسبوعي")
    text(d, (R, 300), "حصصك كلها أمامك دفعة واحدة", font("bold", 56), CREAM)
    days = ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس"]
    cw = (W - 2 * M - 40) / 5
    x = R
    for k, dname in enumerate(days):
        rrect(d, (x - cw, 440, x - 8, 900), 18, fill=GOLD if k == 2 else PANEL)
        text(d, (x - cw / 2, 470), dname, font("semi", 32), CREAM if k != 2 else BG, "ma")
        x -= cw + 8
    text(d, (W / 2, 970), "أضف حصصك مرة واحدة… واطمئن", font("body", 40), MUTED, "ma")
    footer(d)
    return img


def s5():
    img, d = frame(5)
    kicker(d, 200, "دفتر الأسئلة")
    text(d, (R, 300), "بنك أسئلة جاهز لكل مادة وفصل", font("bold", 56), CREAM)
    card(d, (M, 410, R, 780))
    cx, cy, r = W / 2, 595, 150
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(26, 62, 98), width=26)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * 0.78, fill=GOLD, width=26)
    text(d, (cx, cy - 46), ar(151), font("bold", 76), CREAM, "ma")
    text(d, (cx, cy + 46), "سؤالاً", font("semi", 34), MUTED, "ma")
    text(d, (W / 2, 850), "أضف سؤالك أو استخدم البنك الجاهز", font("body", 38), CREAM, "ma")
    footer(d)
    return img


def s6():
    img, d = frame(6)
    kicker(d, 200, "قاعات الامتحان")
    text(d, (R, 300), "توزيع الطلاب على القاعات بضغطة", font("bold", 54), CREAM)
    for k in range(6):
        x = R - (k % 3) * 300
        y = 420 + (k // 3) * 230
        card(d, (x - 260, y, x, y + 190), outline=GOLD)
        text(d, (x - 130, y + 80), f"قاعة {ar(k+1)}", font("semi", 34), CREAM, "ma")
    text(d, (W / 2, 1000), "بلا تعارض أسماء… وبلا ورق", font("bold", 44), GOLD, "ma")
    footer(d)
    return img


def s7():
    img, d = frame(7)
    kicker(d, 200, "بلا إنترنت")
    text(d, (R, 300), "يعمل من دون اتصال بعد أول فتح", font("bold", 54), CREAM)
    y = para(d, R, 420, "تثبّته كتطبيق على هاتفك أو حاسوبك، وتستخدمه في الصف دون قلق من انقطاع الإنترنت.", font("body", 42), CREAM, W - 2 * M, 1.6)
    chips = ["هاتف", "حاسوب", "آيباد", "بلا سيرفر"]
    x = R
    for c in chips:
        f = font("semi", 34); w = tw(c, f) + 56
        rrect(d, (x - w, 820, x, 890), 35, outline=GOLD, width=2)
        text(d, (x - w / 2, 830), c, f, CREAM, "ma")
        x -= w + 16
    footer(d)
    return img


def s8():
    img, d = frame(8, glow=(0.5, 0.45))
    cx = W / 2
    badge(d, cx, 360, 110, GOLD, 4)
    badge(d, cx, 360, 62, GOLD, 2)
    text(d, (cx, 520), "مدرستي", font("head", 110), GOLD, "ma")
    text(d, (cx, 700), "تصميم وتطوير: حيدر نصيف", font("semi", 44), CREAM, "ma")
    card(d, (M, 840, R, 1080), outline=GOLD)
    text(d, (cx, 875), "جرّبه الآن", font("bold", 50), CREAM, "ma")
    d.text((cx, 965), "prog-alone.github.io/myschool", font=font("semi", 38), fill=GOLD, anchor="ma", direction="ltr")
    text(d, (cx, 1170), "احفظ المنشور لترجع له", font("body", 34), MUTED, "ma")
    return img


if __name__ == "__main__":
    imgs = []
    for i, fn in enumerate([s1, s2, s3, s4, s5, s6, s7, s8], 1):
        img = fn()
        img.save(f"{OUT}/ms_post_{i}.jpg", quality=94)
        imgs.append(img.convert("RGB"))
    imgs[0].save(f"{OUT}/ms_post.pdf", save_all=True, append_images=imgs[1:], resolution=150)
    print("ok")
