"""Builds hexbridgemedia.co.uk: the one page every QR code points at.

Edit the lists below (status "out" shows Amazon buttons, "soon" shows Coming soon), then:
    python3 build_site.py && git add -A && git commit -m "update" && git push
GitHub Pages serves it; CNAME holds the domain.
"""
import html
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
MEDIA = HERE.parent
CB = MEDIA / "Colouring Books"
FQ = MEDIA / "Fact and Quiz Books"
CHANNEL = "https://www.youtube.com/@HexbridgeMedia"

# (title, one line, cover image, amazon search words, status)
FACT = [
    ("The Most Extreme Things in the Universe", "The hottest, fastest, oldest and weirdest facts, and how anyone knows. Ages 8–12.",
     FQ / "01 The Most Extreme Things in the Universe/cover/cover_front_preview.jpg", "Most Extreme Things in the Universe Hextall", "soon"),
    ("Britain's Weirdest Wildlife", "A field guide to 38 real British creatures that refuse to behave. Families, 8+.",
     FQ / "03 Britain's Weirdest Wildlife/cover/cover_front_preview.jpg", "Britain's Weirdest Wildlife Hextall", "soon"),
    ("Grandparents vs Grandkids", "The family quiz that settles it once and for all, plus a keepsake of your stories.",
     FQ / "07 Grandparents vs Grandkids/cover/cover_front_preview.jpg", "Grandparents vs Grandkids Hextall", "soon"),
    ("The Food Lover's Quiz Book", "200 questions and 12 true stories for people who read the back of the packet.",
     FQ / "08 The Food Lover's Quiz Book/cover/cover_front_preview.jpg", "Food Lover's Quiz Book Hextall", "soon"),
]
A = CB / "Amazon Colouring Books for Adults/covers"
K = CB / "Amazon Colouring Books for Kids/covers"
COLOUR = [
    ("The History of Christmas", "The story of Christmas, from long ago to today, with a quiz. Ages 6–10.", K / "05-history-of-christmas/cover_front_preview.jpg",
     "History of Christmas Coloring Book Hextall", "out"),
    ("Henhouse Heroes", "Chickens with a fun fact on every picture. Ages 3–6.", K / "02-henhouse-heroes/cover_front_preview.jpg", "Henhouse Heroes Hextall", "out"),
    ("Geometric Mandala Coloring Book", "Hexagon mandalas, from bold and easy to properly detailed. Adults.", A / "01-hex-mandalas/hex_cover_front_preview.jpg",
     "Geometric Mandala Coloring Book Hextall", "out"),
    ("Deep Sea Explorers", "Whales, octopuses and the deep. Ages 3–6.", K / "03-deep-sea-explorers/cover_front_preview.jpg", "Deep Sea Explorers Hextall", "soon"),
    ("Fastest Things on Earth", "Cheetahs, rockets and racing cars, with a speed fact on every page. Ages 4–8.", K / "04-fastest-things/cover_front_preview.jpg",
     "Fastest Things on Earth Coloring Book Hextall", "soon"),
    ("Stained Glass Coloring Book", "Picture panels to colour like light through glass. Adults.", A / "04-stained-glass/cover_front_preview.jpg", "Stained Glass Coloring Book Hextall", "soon"),
    ("Moroccan Star Patterns", "45 geometric tile designs. Adults.", A / "03-moroccan-star-patterns/cover_front_preview.jpg", "Moroccan Star Patterns Coloring Book Hextall", "soon"),
    ("Sacred Geometry", "Flower of life, circles and stars. Adults.", A / "05-sacred-geometry/cover_front_preview.jpg", "Sacred Geometry Coloring Book Hextall", "soon"),
    ("Kaleidoscope", "45 mirror-symmetry designs. Adults.", A / "06-kaleidoscope/cover_front_preview.jpg", "Kaleidoscope Coloring Book Hextall", "soon"),
    ("Patchwork Quilt", "Classic blocks, samplers and hexagon quilts. Adults.", A / "07-patchwork-quilts/cover_front_preview.jpg", "Patchwork Quilt Coloring Book Hextall", "soon"),
    ("Bold & Easy Mandala", "40 big, simple designs with thick lines. Adults.", A / "02-bold-easy-mandalas/cover_front_preview.jpg", "Bold Easy Mandala Coloring Book Hextall", "soon"),
]
VIDEOS = [
    ("9H3uEBkJVLY", "Oxfordshire was hotter than the Sun"),
    ("1Ov7hjZHEUA", "You're Faster Than Any Plane Right Now"),
    ("rCBY2s00kUI", "Something in Your Kitchen Is 13.8 Billion Years Old"),
    ("YSFKD2EPo40", "Your Eyes Can See Light Older Than Our Species"),
    ("nsDCm556mzk", "How Could a T. Rex Lose to an Insect?"),
    ("T2_wgrx_pmU", "Can GTA 6 Beat the Best-Selling Games of All Time?"),
]


def slug(t):
    return "".join(c.lower() if c.isalnum() else "-" for c in t).strip("-").replace("--", "-")


def thumb(src, name):
    out = HERE / "img" / f"{name}.jpg"
    im = Image.open(src).convert("RGB")
    im.thumbnail((480, 640))
    im.save(out, quality=84, optimize=True)
    return f"img/{name}.jpg", im.size


def book_card(t, line, src, q, status):
    path, (w, h) = thumb(src, slug(t))
    e = html.escape
    if status == "out":
        qq = q.replace(" ", "+")
        btn = (f'<div class="buy"><a href="https://www.amazon.co.uk/s?k={qq}" rel="noopener">Amazon UK</a>'
               f'<a href="https://www.amazon.com/s?k={qq}" rel="noopener">Amazon US</a></div>')
    else:
        btn = '<div class="buy"><span class="soon">Coming soon</span></div>'
    return (f'<article class="book"><img src="{path}" width="{w}" height="{h}" alt="Cover of {e(t)}" loading="lazy">'
            f'<h3>{e(t)}</h3><p>{e(line)}</p>{btn}</article>')


def video_card(vid, t):
    e = html.escape
    return (f'<a class="vid" href="https://www.youtube.com/shorts/{vid}" rel="noopener"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" '
            f'alt="" loading="lazy" width="480" height="360"><span>{e(t)}</span></a>')


PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hex Bridge Media: books and videos by Samuel J Hextall</title>
<meta name="description" content="Fact books, quiz books, colouring books and short science videos from Hex Bridge Media, all in one place.">
<link rel="icon" href="img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Cabin:wght@400;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
:root{--navy:#0b1026;--ink:#1d1a26;--cream:#f4ead6;--paper:#fbf6ea;--orange:#ff5a24;--yellow:#ffc83a;--mauve:#42283a;--peach:#af8a72}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.55 Cabin,system-ui,sans-serif}
a{color:inherit}
header{background:var(--navy);color:var(--cream);padding:28px 16px 40px;text-align:center}
header img{width:96px;height:96px;border-radius:50%}
header h1{font:400 clamp(40px,9vw,76px)/1 Anton,Impact,sans-serif;letter-spacing:.04em;margin:14px 0 8px}
header p{max-width:560px;margin:0 auto;font-size:18px;opacity:.9}
nav{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:22px}
nav a{font:400 18px Anton,sans-serif;letter-spacing:.06em;text-decoration:none;padding:10px 18px;border:2px solid var(--cream);border-radius:999px}
nav a:hover{background:var(--cream);color:var(--navy)}
section{max-width:1080px;margin:0 auto;padding:44px 16px 8px}
h2{font:400 clamp(30px,6vw,46px)/1.05 'DM Serif Display',Georgia,serif;margin:0 0 6px}
.lede{margin:0 0 24px;color:#4b4552;max-width:640px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:22px}
.book{background:#fff;border:1px solid #e6dcc6;border-radius:10px;padding:12px;display:flex;flex-direction:column}
.book img{width:100%;height:auto;border-radius:3px;box-shadow:0 2px 0 rgba(0,0,0,.08)}
.book h3{font:700 17px/1.25 Cabin,sans-serif;margin:12px 0 4px}
.book p{font-size:15px;margin:0 0 12px;color:#4b4552;flex:1}
.buy{display:flex;gap:8px;flex-wrap:wrap}
.buy a{flex:1;text-align:center;font-weight:700;font-size:14px;text-decoration:none;background:var(--navy);color:var(--cream);padding:9px 6px;border-radius:6px}
.buy a:hover{background:var(--orange)}
.soon{font-size:14px;font-weight:700;color:var(--mauve);background:#efe3d3;padding:8px 10px;border-radius:6px}
.vids{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.vid{text-decoration:none;background:var(--navy);color:var(--cream);border-radius:10px;overflow:hidden;display:block}
.vid img{width:100%;height:auto;display:block;aspect-ratio:4/3;object-fit:cover}
.vid span{display:block;padding:10px 12px 12px;font-weight:700}
.vid:hover span{color:var(--yellow)}
.big{display:inline-block;margin-top:20px;font:400 20px Anton,sans-serif;letter-spacing:.05em;text-decoration:none;background:var(--orange);color:#fff;padding:12px 22px;border-radius:999px}
.note{background:#efe3d3;border-radius:10px;padding:16px 18px;margin-top:28px;font-size:15px}
footer{margin-top:56px;background:var(--navy);color:var(--cream);text-align:center;padding:28px 16px;font-size:14px}
footer a{color:var(--yellow)}
</style>
</head>
<body>
<header>
<img src="img/logo.png" alt="Hex Bridge Media logo" width="96" height="96">
<h1>HEX BRIDGE MEDIA</h1>
<p>Books and short videos about the strangest true things we could find, checked properly, by Samuel J Hextall.</p>
<nav><a href="#read">READ &amp; PLAY</a><a href="#colour">COLOUR</a><a href="#watch">WATCH</a></nav>
</header>

<section id="read">
<h2>Read &amp; play</h2>
<p class="lede">Fact books and family quiz books. Every number checked, every answer sourced.</p>
<div class="grid">%FACT%</div>
</section>

<section id="colour">
<h2>Colour</h2>
<p class="lede">Colouring books for kids and grown-ups, many with a true fact on every picture.</p>
<div class="grid">%COLOUR%</div>
</section>

<section id="watch">
<h2>Watch</h2>
<p class="lede">Short cartoon science videos on YouTube, about the same true and strange things as the books.</p>
<div class="vids">%VIDEOS%</div>
<a class="big" href="%CHANNEL%" rel="noopener">SEE THE CHANNEL</a>
<div class="note"><strong>Grown-ups:</strong> if you scanned the code in one of our books, thank you. A kind review on Amazon helps a small publisher more than you'd think.</div>
</section>

<footer>Hex Bridge Media &middot; Samuel J Hextall &middot; <a href="%CHANNEL%">YouTube</a></footer>
</body>
</html>
"""

if __name__ == "__main__":
    (HERE / "img").mkdir(exist_ok=True)
    page = (PAGE.replace("%FACT%", "".join(book_card(*b) for b in FACT))
                .replace("%COLOUR%", "".join(book_card(*b) for b in COLOUR))
                .replace("%VIDEOS%", "".join(video_card(*v) for v in VIDEOS))
                .replace("%CHANNEL%", CHANNEL))
    (HERE / "index.html").write_text(page)
    (HERE / "CNAME").write_text("hexbridgemedia.co.uk\n")
    print("built", len(FACT) + len(COLOUR), "books,", len(VIDEOS), "videos")
