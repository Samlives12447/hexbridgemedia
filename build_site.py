"""Builds hexbridgemedia.co.uk (v3, 2026-11-10): the one page every QR code points at.

v3 because Sam scored v2 2/10. v2 was dark and muted (a consultancy look), it showed no products on the
first screen, and text ran off the side on phones. v3 follows the research:
  * show the books on the first screen, with one clear next step (author-site guidance: Kit, Unbounce)
  * be bright and match the products: the covers and Shorts use Anton/Archivo + orange/amber on navy
  * a playful "annotated textbook" feel (Kurzgesagt's 2024 BUCK redesign) with Barry, stamps and scribbles
  * something to DO: a True-or-False game built from facts in the books and videos
  * books open in a pop-up instead of one long wall of text, and the videos play on the page

Edit the data below (a book's status "out" shows Amazon buttons, "soon" shows Coming soon), then:
    python3 build_site.py && git add -A && git commit -m "update" && git push
Every link in GO DEEPER / LEARN was checked to load on 2026-11-10. Every fact is from the audited book or video text.
"""
import html
import json
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
MEDIA = HERE.parent
CB = MEDIA / "Colouring Books"
FQ = MEDIA / "Fact and Quiz Books"
EP = MEDIA / "YouTube Shorts" / "episodes"
CHANNEL = "https://www.youtube.com/@HexbridgeMedia"
e = html.escape

FACT_BOOKS = [
    dict(t="The Most Extreme Things in the Universe", who="Ages 8–12", aud="kids", status="soon",
         img=FQ / "01 The Most Extreme Things in the Universe/cover/cover_front_preview.jpg", q="Most Extreme Things in the Universe Hextall",
         blurb="The hottest, coldest, fastest, deepest, loudest and rarest things ever found, starting in your kitchen and finishing at the edge of the universe. Every number wears a stamp saying how far to trust it.",
         facts=["Right now you're moving at about 67,000 mph around the Sun.",
                "A fusion experiment in Oxfordshire, JET, ran at 150 million °C: ten times hotter than the middle of the Sun.",
                "Scientists at CERN made matter at over 5 trillion °C, for far less than a blink."],
         deeper=[("NASA: facts about the Sun", "https://science.nasa.gov/sun/facts/"),
                 ("Met Office: UK weather extremes", "https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-climate-extremes"),
                 ("CERN: the hottest stuff ever made", "https://home.cern/science/physics/heavy-ions-and-quark-gluon-plasma"),
                 ("NASA Space Place (for kids)", "https://spaceplace.nasa.gov/")]),
    dict(t="Britain's Weirdest Wildlife", who="Families, 8+", aud="family", status="soon",
         img=FQ / "03 Britain's Weirdest Wildlife/cover/cover_front_preview.jpg", q="Britain's Weirdest Wildlife Hextall",
         blurb="A field guide to 38 real British creatures that refuse to behave, sorted by where you'll actually find them, with night walks, pond dipping and rock pooling. The Society for the Promotion of Normal Behaviour in British Animals objects throughout.",
         facts=["A woodlouse is a crustacean: a land-living cousin of crabs and lobsters.",
                "Deathwatch beetles find a mate by tapping their heads on old wood.",
                "Upset a ladybird and it oozes bitter yellow fluid from its knees."],
         deeper=[("Buglife: Britain's invertebrates", "https://www.buglife.org.uk/"),
                 ("Natural History Museum: identify what you found", "https://www.nhm.ac.uk/take-part/identify-nature.html"),
                 ("iRecord: send in your sightings", "https://irecord.org.uk/"),
                 ("Barn Owl Trust", "https://www.barnowltrust.org.uk/"),
                 ("People's Trust for Endangered Species", "https://ptes.org/")]),
    dict(t="Grandparents vs Grandkids", who="The whole family", aud="family", status="soon",
         img=FQ / "07 Grandparents vs Grandkids/cover/cover_front_preview.jpg", q="Grandparents vs Grandkids Hextall",
         blurb="The grandkids get asked about the grandparents' world, and the grandparents get asked about the grandkids'. Every round ends with a Story Bonus, so you finish with a winner and your family's stories in your own handwriting.",
         facts=["Before decimal money there were 240 pennies in a pound.",
                "Britain switched to decimal money on 15 February 1971.",
                "Saying “in my day” earns a forfeit. Saying “OK boomer” loses a point."],
         deeper=[("Bank of England Museum", "https://www.bankofengland.co.uk/museum"),
                 ("The Royal Mint: the story of decimalisation", "https://www.royalmint.com/discover/decimalisation/")]),
    dict(t="The Food Lover's Quiz Book", who="Grown-ups", aud="adults", status="soon",
         img=FQ / "08 The Food Lover's Quiz Book/cover/cover_front_preview.jpg", q="Food Lover's Quiz Book Hextall",
         blurb="Twelve rounds of sixteen questions, from spice wars and kitchen myths to cheese, bread and chocolate. Every round opens with a true story, and where historians disagree, the answers say so.",
         facts=["To a botanist, a banana is a berry and a strawberry isn't.",
                "A peanut isn't a nut. It's a legume, a cousin of peas and beans.",
                "Wild tomatoes come from South America, not Italy."],
         deeper=[("Food Standards Agency", "https://www.food.gov.uk/")]),
]
A = CB / "Amazon Colouring Books for Adults/covers"
K = CB / "Amazon Colouring Books for Kids/covers"
# (title, who, audience, cover, amazon search, status, one-line description from the book's own cover/listing)
COLOUR = [
    ("The History of Christmas", "Ages 6–10", "kids", K / "05-history-of-christmas/cover_front_preview.jpg", "History of Christmas Coloring Book Hextall", "out",
     "Colour your way through where our Christmas traditions came from."),
    ("Henhouse Heroes", "Ages 3–6", "kids", K / "02-henhouse-heroes/cover_front_preview.jpg", "Henhouse Heroes Hextall", "out",
     "A chicken colouring book with a fun fact on every picture."),
    ("Geometric Mandala", "Grown-ups", "adults", A / "01-hex-mandalas/hex_cover_front_preview.jpg", "Geometric Mandala Coloring Book Hextall", "out",
     "45 calming hexagon mandalas, from bold and easy to detailed."),
    ("Deep Sea Explorers", "Ages 3–6", "kids", K / "03-deep-sea-explorers/cover_front_preview.jpg", "Deep Sea Explorers Hextall", "soon",
     "An ocean colouring book for little explorers."),
    ("Fastest Things on Earth", "Ages 4–8", "kids", K / "04-fastest-things/cover_front_preview.jpg", "Fastest Things on Earth Coloring Book Hextall", "soon",
     "Speedy animals and machines to colour in."),
    ("Stained Glass", "Grown-ups", "adults", A / "04-stained-glass/cover_front_preview.jpg", "Stained Glass Coloring Book Hextall", "soon",
     "Stained-glass designs that glow once they're coloured."),
    ("Moroccan Star Patterns", "Grown-ups", "adults", A / "03-moroccan-star-patterns/cover_front_preview.jpg", "Moroccan Star Patterns Coloring Book Hextall", "soon",
     "Interlocking star patterns in the Moroccan tradition."),
    ("Sacred Geometry", "Grown-ups", "adults", A / "05-sacred-geometry/cover_front_preview.jpg", "Sacred Geometry Coloring Book Hextall", "soon",
     "Circles, stars and symmetry to colour slowly."),
    ("Kaleidoscope", "Grown-ups", "adults", A / "06-kaleidoscope/cover_front_preview.jpg", "Kaleidoscope Coloring Book Hextall", "soon",
     "Mirror-image kaleidoscope patterns."),
    ("Patchwork Quilt", "Grown-ups", "adults", A / "07-patchwork-quilts/cover_front_preview.jpg", "Patchwork Quilt Coloring Book Hextall", "soon",
     "Quilt blocks to colour, square by square."),
    ("Bold & Easy Mandala", "Grown-ups", "adults", A / "02-bold-easy-mandalas/cover_front_preview.jpg", "Bold Easy Mandala Coloring Book Hextall", "soon",
     "Big, bold mandalas with no tiny fiddly bits."),
]
VIDEOS = [
    dict(id="9H3uEBkJVLY", t="Oxfordshire was hotter than the Sun", cover=EP / "ep001-hotter-than-the-sun/05_thumbnail/ep001_short_cover.png",
         facts=["The UK's hottest day: 40.3 °C at Coningsby, 19 July 2022 (Met Office).",
                "JET, a fusion experiment in Oxfordshire, held plasma at 150 million °C. It closed in December 2023.",
                "The Sun's core is about 15 million °C, so JET ran ten times hotter.",
                "The record is CERN's: over 5 trillion °C (estimated), lasting about 10⁻²³ seconds."],
         deeper=[("UKAEA: the JET experiment", "https://ccfe.ukaea.uk/programmes/joint-european-torus/"),
                 ("CERN: heavy ions and quark-gluon plasma", "https://home.cern/science/physics/heavy-ions-and-quark-gluon-plasma"),
                 ("NASA: the Sun", "https://science.nasa.gov/sun/facts/")]),
    dict(id="1Ov7hjZHEUA", t="You're Faster Than Any Plane Right Now", cover=EP / "ep006-fastest-things/05_thumbnail/ep006_short_cover.png",
         facts=["A cheetah: 58 mph, the fastest measured by tracking collar (Nature, 2013).",
                "The X-15 rocket plane: 4,520 mph in 1967, still the fastest crewed plane.",
                "Parker Solar Probe: 430,000 mph, the fastest spacecraft ever (2024).",
                "You: about 67,000 mph around the Sun, right now."],
         deeper=[("Smithsonian: the X-15", "https://airandspace.si.edu/stories/editorial/x-15"),
                 ("NASA: Parker Solar Probe", "https://science.nasa.gov/mission/parker-solar-probe/"),
                 ("National Geographic: cheetah collars", "https://www.nationalgeographic.com/science/article/collars-reveal-why-just-how-extreme-cheetahs-can-be")]),
    dict(id="rCBY2s00kUI", t="Something in Your Kitchen Is 13.8 Billion Years Old", cover=EP / "ep005-oldest-things/05_thumbnail/ep005_short_cover.png",
         facts=["The oldest bread found: crumbs about 14,400 years old, from Jordan, before farming began.",
                "Jonathan the tortoise hatched around 1832 and is still alive on St Helena.",
                "A Greenland shark was estimated at 392 years old (Science, 2016).",
                "Almost all the hydrogen in your body was made minutes after the Big Bang. So the oldest thing in your kitchen is you."],
         deeper=[("PBS NOVA: the Greenland shark", "https://www.pbs.org/wgbh/nova/article/greenland-shark-is-officially-the-longest-living-vertebrate-on-earth"),
                 ("PBS NOVA: the star in you", "https://www.pbs.org/wgbh/nova/article/star-in-you/"),
                 ("English Heritage: Stonehenge's history", "https://www.english-heritage.org.uk/visit/places/stonehenge/history-and-stories/")]),
    dict(id="YSFKD2EPo40", t="Your Eyes Can See Light Older Than Our Species", cover="https://i.ytimg.com/vi/YSFKD2EPo40/oardefault.jpg",
         facts=["The Andromeda galaxy, about 2.5 million light years away, can be seen without a telescope from a dark site.",
                "Its light set off long before our species appeared, about 300,000 years ago.",
                "Voyager 1 is predicted to reach one light-day from Earth on 18 November 2026.",
                "Webb's record galaxy, MoM-z14: its light travelled about 13.5 billion years."],
         deeper=[("NASA: Voyager", "https://science.nasa.gov/mission/voyager/"),
                 ("ESA/Webb", "https://esawebb.org/"),
                 ("NASA: galaxies", "https://science.nasa.gov/universe/galaxies/")]),
    dict(id="nsDCm556mzk", t="How Could a T. Rex Lose to an Insect?", cover=EP / "ep003-deadliest-animals/05_thumbnail/ep003_short_cover.png",
         facts=["T. rex's bite: about 35,000 newtons, estimated from jaw models.",
                "The strongest bite ever actually measured: a saltwater crocodile, 16,414 N (2012).",
                "The Tsavo lions were said to have killed 135 people; tests on their bones suggest about 35.",
                "Mosquitoes: malaria killed an estimated 610,000 people in 2024 (WHO). The death rate has more than halved since 2000."],
         deeper=[("WHO: malaria fact sheet", "https://www.who.int/news-room/fact-sheets/detail/malaria"),
                 ("Field Museum: the Tsavo lions", "https://www.fieldmuseum.org/blog/man-eating-lions-ate-fewer-people-believed"),
                 ("Florida Museum: shark attack data", "https://www.floridamuseum.ufl.edu/shark-attacks/yearly-worldwide-summary/")]),
    dict(id="T2_wgrx_pmU", t="Can GTA 6 Beat the Best-Selling Games of All Time?", cover=EP / "ep004-gta6/05_thumbnail/ep004_short_cover.png",
         facts=["GTA V: over 230 million sold (Take-Two, August 2026).",
                "The PlayStation 2 sold over 160 million, the best-selling console ever (Sony).",
                "Wii Sports: 82.9 million, the most for any game on one console (Nintendo).",
                "The Atari 2600 had 128 bytes of memory, less than one text message."],
         deeper=[("Nintendo: best-selling games", "https://www.nintendo.co.jp/ir/en/finance/software/index.html"),
                 ("Sony Interactive: sales data", "https://sonyinteractive.com/en/our-company/business-data-sales/"),
                 ("Take-Two Interactive investors", "https://www.take2games.com/ir")]),
]
# True or False game: every answer comes from the audited book/video facts above.
QUIZ = [
    ("Right now, you're moving at about 67,000 mph.", True,
     "That's Earth carrying you round the Sun. Faster than any plane ever built.", "The Most Extreme Things in the Universe"),
    ("A strawberry is a berry.", False,
     "To a botanist, a strawberry isn't a berry. A banana is!", "The Food Lover's Quiz Book"),
    ("A woodlouse is an insect.", False,
     "It's a crustacean: a land-living cousin of crabs and lobsters.", "Britain's Weirdest Wildlife"),
    ("T. rex has the strongest bite ever measured.", False,
     "Nobody could measure a T. rex. Its ~35,000 N bite is an estimate. The strongest MEASURED bite is a saltwater crocodile's, 16,414 N.", "Video: How Could a T. Rex Lose to an Insect?"),
    ("An experiment in Oxfordshire got hotter than the middle of the Sun.", True,
     "JET's plasma hit 150 million °C, about ten times hotter than the Sun's core.", "Video: Oxfordshire was hotter than the Sun"),
    ("Upset a ladybird and it oozes yellow fluid from its knees.", True,
     "It's bitter, and it tells birds: don't eat me.", "Britain's Weirdest Wildlife"),
    ("A peanut is a nut.", False,
     "It's a legume, a cousin of peas and beans.", "The Food Lover's Quiz Book"),
    ("Before 1971 there were 240 pennies in a pound.", True,
     "Britain went decimal on 15 February 1971. Ask a grandparent how they coped.", "Grandparents vs Grandkids"),
]
LEARN = [
    ("NASA Space Place", "Space and Earth science games and explainers for kids.", "https://spaceplace.nasa.gov/", "space"),
    ("Natural History Museum", "Found something odd in the garden? Find out what it is.", "https://www.nhm.ac.uk/take-part/identify-nature.html", "nature"),
    ("iRecord", "Log what you spot, and real scientists use it.", "https://irecord.org.uk/", "nature"),
    ("Met Office", "Why the weather does what it does, from the UK's weather service.", "https://www.metoffice.gov.uk/weather/learn-about", "earth"),
    ("BBC Bitesize", "Free lessons for every school subject and age.", "https://www.bbc.co.uk/bitesize", "school"),
    ("The Royal Institution", "Home of the Christmas Lectures, with talks and demos online.", "https://www.rigb.org/", "science"),
    ("Woodland Trust", "Tree ID, nature activities and woods to visit near you.", "https://www.woodlandtrust.org.uk/", "nature"),
    ("ESA/Hubble", "The best space pictures ever taken, explained.", "https://esahubble.org/", "space"),
]
TICKER = [
    "A woodlouse is a crustacean", "You're doing 67,000 mph right now", "A banana is a berry. A strawberry isn't",
    "Deathwatch beetles flirt by head-banging", "JET ran 10× hotter than the Sun's core", "A Greenland shark: est. 392 years old",
    "The Atari 2600 had 128 bytes of memory", "Ladybirds bleed from their knees", "A peanut isn't a nut",
]


def slug(t):
    return "-".join("".join(c.lower() if c.isalnum() else " " for c in t).split())


def thumb(src, name, w=520, h=None):
    out = HERE / "img" / f"{name}.jpg"
    if isinstance(src, str) and src.startswith("http"):
        tmp = HERE / "img" / f"_{name}.src"
        tmp.write_bytes(urllib.request.urlopen(src, timeout=30).read())
        src = tmp
    im = Image.open(src).convert("RGB")
    im.thumbnail((w, h or int(w * 1.4)))
    im.save(out, quality=84, optimize=True)
    if Path(src).name.endswith(".src"):
        Path(src).unlink()
    return f"img/{name}.jpg", im.size


def amazon(q):
    qq = q.replace(" ", "+")
    return [("Amazon UK", f"https://www.amazon.co.uk/s?k={qq}"), ("Amazon US", f"https://www.amazon.com/s?k={qq}")]


BARRY = '''<svg class="barry" viewBox="0 0 60 120" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
<circle cx="30" cy="16" r="11"/><path d="M30 27v44M30 71l-14 40M30 71l14 40M30 40l-18 18M30 40l18-14"/></g>
<circle cx="26" cy="14" r="1.8" fill="currentColor"/><circle cx="34" cy="14" r="1.8" fill="currentColor"/><path d="M25 20q5 4 10 0" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>'''
HEX = '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 4 90 27v46L50 96 10 73V27z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/></svg>'


def book_card(b, i, kind):
    status = '<span class="badge out">Out now</span>' if b["status"] == "out" else '<span class="badge soon">Coming soon</span>'
    return f'''<button class="book reveal" data-aud="{b["aud"]} {kind}" data-i="{i}" style="--d:{(i % 4) * 70}ms">
  <span class="cover tilt"><img src="{b["src"]}" width="{b["w"]}" height="{b["h"]}" alt="Cover of {e(b["t"])}" loading="lazy"><i class="shine"></i></span>
  <span class="meta"><span class="who">{e(b["who"])}</span>{status}</span>
  <span class="bt">{e(b["t"])}</span>
  <span class="peek">Take a look <span aria-hidden="true">→</span></span>
</button>'''


def video_card(v, i):
    return f'''<button class="vid reveal" data-v="{i}" style="--d:{(i % 6) * 60}ms" aria-label="Play: {e(v["t"])}">
  <img src="{v["src"]}" width="{v["w"]}" height="{v["h"]}" alt="" loading="lazy">
  <span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span>
  <span class="vt">{e(v["t"])}</span>
</button>'''


def learn_card(item, i):
    t, d, u, tag = item
    return f'<a class="learn reveal" href="{u}" rel="noopener" target="_blank" style="--d:{(i % 4) * 60}ms"><span class="tag t-{tag}">{tag}</span><span class="lt">{e(t)} <span aria-hidden="true">↗</span></span><span class="ld">{e(d)}</span></a>'


CSS = r"""
:root{--paper:#fbf4e6;--paper2:#f4e7cf;--ink:#0b1026;--ink2:#18204a;--orange:#ff6a3d;--amber:#ffc83a;--peach:#e3a07a;--sky:#3fb6ff;--green:#22a35a;--berry:#c2306b;--muted:#5a5a6e;--line:rgba(11,16,38,.14);
  --display:'Anton',Impact,sans-serif;--sans:'Space Grotesk',system-ui,sans-serif;--hand:'Caveat',cursive;--r:18px;--ease:cubic-bezier(.22,1,.36,1)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--sans);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:inherit}img{display:block;max-width:100%;height:auto}button{font:inherit;color:inherit}
h1,h2,h3{font-family:var(--display);font-weight:400;text-transform:uppercase;line-height:.95;letter-spacing:.005em;margin:0}
h2{font-size:clamp(44px,7.5vw,84px)}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
.kicker{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin:0 0 14px}
.kicker svg{width:16px;height:16px}
.lede{max-width:600px;font-size:clamp(17px,2vw,19px);color:var(--muted);margin:18px 0 0}
.hand{font-family:var(--hand);font-weight:700;text-transform:none;letter-spacing:0}
section{padding:110px 0 30px;position:relative}
.sechead{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:44px}
/* buttons */
.btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:700;font-size:16px;padding:15px 24px;border-radius:999px;border:2.5px solid var(--ink);background:var(--orange);color:var(--ink);box-shadow:4px 4px 0 var(--ink);transition:transform .18s var(--ease),box-shadow .18s var(--ease),background .2s;cursor:pointer}
.btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--ink)}
.btn:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--ink)}
.btn.alt{background:var(--paper)}.btn.amber{background:var(--amber)}
.btn.sm{font-size:14px;padding:10px 16px;box-shadow:3px 3px 0 var(--ink)}
.btn svg{width:18px;height:18px}
/* nav */
.nav{position:sticky;top:0;z-index:50;background:rgba(251,244,230,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid transparent;transition:border-color .3s}
.nav.scrolled{border-color:var(--line)}
.nav .wrap{display:flex;align-items:center;gap:20px;height:66px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:var(--display);font-size:21px;letter-spacing:.03em;text-transform:uppercase;white-space:nowrap}
.logo img{width:38px;height:38px;border-radius:50%}
.nav ul{display:flex;gap:4px;list-style:none;margin:0 0 0 auto;padding:0}
.nav ul a{text-decoration:none;font-weight:600;font-size:15px;padding:8px 13px;border-radius:999px;transition:background .2s}
.nav ul a:hover{background:var(--paper2)}
.nav .btn{margin-left:6px}
@media(max-width:900px){.nav ul{display:none}.nav .btn{margin-left:auto}}
@media(max-width:420px){.logo span{display:none}}
/* hero */
.hero{padding:40px 0 70px;overflow:hidden;background:radial-gradient(rgba(11,16,38,.09) 1.2px,transparent 1.3px) 0 0/22px 22px}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:30px;align-items:center;min-height:min(78vh,720px)}
@media(max-width:900px){.hero .wrap{grid-template-columns:minmax(0,1fr);min-height:0}}
.qr-hello{display:inline-flex;align-items:center;gap:10px;background:var(--ink);color:var(--paper);font-size:14px;font-weight:600;padding:7px 14px 7px 8px;border-radius:999px;margin-bottom:26px}
.qr-hello b{background:var(--amber);color:var(--ink);border-radius:999px;padding:2px 9px;font-size:12px;letter-spacing:.08em}
.hero h1{font-size:clamp(50px,6.7vw,100px)}@media(max-width:900px){.hero h1{font-size:clamp(46px,13vw,96px)}}
.hero h1 .line{display:block}
.hero h1 .line>span{display:inline-block;animation:rise .9s var(--ease) both}
.hero h1 .line:nth-child(2)>span{animation-delay:.1s}.hero h1 .line:nth-child(3)>span{animation-delay:.2s}
@keyframes rise{from{opacity:0;transform:translateY(40%)}}
.mark{position:relative;color:var(--ink);white-space:nowrap}
.mark::before{content:'';position:absolute;left:-.06em;right:-.08em;bottom:.2em;height:.3em;background:var(--amber);z-index:-1;transform:skew(-8deg) scaleX(0);transform-origin:left;animation:swipe .7s .75s var(--ease) forwards}
@keyframes swipe{to{transform:skew(-8deg) scaleX(1)}}
.hero .sub{font-size:clamp(18px,2.2vw,21px);max-width:520px;margin:24px 0 30px;color:#33344a}
.cta{display:flex;flex-wrap:wrap;gap:14px}
.proof{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:34px;font-weight:600;font-size:15px}
.proof span{display:inline-flex;align-items:center;gap:7px}
.proof i{width:9px;height:9px;border-radius:50%;background:var(--green);display:inline-block}
/* the book fan */
.stage{position:relative;height:560px;perspective:1200px}
@media(max-width:900px){.stage{height:420px;margin-top:10px}}
@media(max-width:520px){.stage{height:330px}}
.layer{position:absolute;inset:0;transition:transform .1s linear;will-change:transform}
.fan{position:absolute;left:50%;top:50%;width:0;height:0}
.fan a{position:absolute;width:230px;left:-115px;top:-160px;border-radius:6px;box-shadow:0 22px 40px rgba(11,16,38,.28),0 0 0 2.5px var(--ink);transform:rotate(var(--rot)) translate(var(--tx),var(--ty));transition:transform .5s var(--ease),box-shadow .3s;overflow:hidden;animation:dealin .9s var(--ease) both;animation-delay:var(--dl)}
.fan a img{width:100%}
.fan a:hover{transform:rotate(0deg) translate(var(--tx),calc(var(--ty) - 40px)) scale(1.07);z-index:9;box-shadow:0 30px 60px rgba(11,16,38,.35),0 0 0 2.5px var(--ink)}
@keyframes dealin{from{transform:rotate(0) translate(0,30px) scale(.85);opacity:0}}
@media(max-width:520px){.fan a{width:128px;left:-64px;top:-92px}}
.float{position:absolute;color:var(--ink)}
.float svg{width:100%;height:100%}
.f1{width:90px;left:2%;top:6%;color:var(--orange)}.f2{width:54px;right:4%;top:2%;color:var(--sky)}.f3{width:70px;right:0;bottom:8%;color:var(--amber)}.f4{width:40px;left:10%;bottom:4%;color:var(--berry)}
.f1 svg,.f2 svg,.f3 svg,.f4 svg{animation:spin 24s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.stamp{display:inline-block;font-weight:800;font-size:13px;letter-spacing:.14em;border:2.5px solid currentColor;padding:4px 10px;border-radius:5px;text-transform:uppercase;background:var(--paper)}
.s1{position:absolute;left:0;top:30%;color:var(--green);transform:rotate(-12deg)}
.s2{position:absolute;right:2%;top:58%;color:var(--orange);transform:rotate(9deg)}
.note{position:absolute;left:4%;bottom:6%;display:flex;align-items:flex-end;gap:4px;font-family:var(--hand);font-size:24px;line-height:1;color:var(--ink);transform:rotate(-4deg)}
.note .barry{width:30px;height:60px}
.note svg.arrow{width:60px;height:40px}
@media(max-width:520px){.note{display:none}.s1,.s2{font-size:11px}.f1{width:60px}}
/* ticker */
.tickwrap{overflow:hidden;padding:14px 0;margin-top:-14px}
.ticker{background:var(--ink);color:var(--paper);overflow:hidden;border-block:3px solid var(--ink);transform:rotate(-1.2deg);margin:0 -20px;position:relative;z-index:3}
.ticker .track{display:flex;width:max-content;animation:tick 48s linear infinite}
.ticker:hover .track{animation-play-state:paused}
.ticker span{font-family:var(--display);font-size:26px;text-transform:uppercase;letter-spacing:.02em;padding:16px 0;white-space:nowrap;display:flex;align-items:center}
.ticker span::after{content:'';width:16px;height:16px;margin:0 28px;background:var(--amber);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
@keyframes tick{to{transform:translateX(-50%)}}
/* quiz */
#quiz{padding-top:120px}
.quizbox{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:40px;align-items:center}
@media(max-width:900px){.quizbox{grid-template-columns:minmax(0,1fr)}}
.card{position:relative;background:#fff;border:3px solid var(--ink);border-radius:var(--r);box-shadow:10px 10px 0 var(--ink);padding:34px clamp(20px,4vw,40px) 30px;min-height:360px;display:flex;flex-direction:column}
.qtop{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.dots{display:flex;gap:6px}.dots i{width:12px;height:12px;border-radius:50%;border:2px solid var(--ink);background:transparent;transition:background .3s}
.dots i.ok{background:var(--green)}.dots i.no{background:var(--orange)}.dots i.now{background:var(--amber)}
.qtext{font-family:var(--display);text-transform:uppercase;font-size:clamp(30px,4.2vw,46px);line-height:1.02;margin:26px 0 24px;flex:1}
.qbtns{display:flex;gap:14px;flex-wrap:wrap}
.qbtns .btn{flex:1;justify-content:center;font-size:20px;min-width:130px;font-family:var(--display);letter-spacing:.04em;font-weight:400}
.qbtns .t{background:var(--green);color:#fff}.qbtns .f{background:var(--orange)}
.reveal-a{display:none;animation:pop .45s var(--ease)}
.card.answered .reveal-a{display:block}.card.answered .qbtns{display:none}
.verdict{font-family:var(--display);font-size:34px;text-transform:uppercase;margin:0}
.verdict.ok{color:var(--green)}.verdict.no{color:var(--orange)}
.why{margin:6px 0 4px;font-size:18px}.src{font-size:14px;color:var(--muted);margin:0 0 18px}
.bigstamp{position:absolute;right:18px;top:60px;font-size:20px;padding:6px 14px;opacity:0;pointer-events:none}
.card.answered .bigstamp{animation:slam .5s var(--ease) forwards}
@keyframes slam{0%{opacity:0;transform:scale(2.4) rotate(-14deg)}60%{opacity:1;transform:scale(.92) rotate(-9deg)}100%{opacity:1;transform:scale(1) rotate(-9deg)}}
@keyframes pop{from{opacity:0;transform:translateY(10px)}}
.done h3{font-size:clamp(40px,6vw,60px);margin:10px 0 8px}
.qside .barrybig{width:120px;height:240px;color:var(--ink);margin:28px 0 0 8px;transform-origin:50% 100%}
.qside .bubble{position:relative;display:inline-block;background:var(--amber);border:2.5px solid var(--ink);border-radius:16px;padding:10px 16px;font-family:var(--hand);font-size:26px;line-height:1.1;margin-top:18px;max-width:300px}
.qside .bubble::after{content:'';position:absolute;left:34px;bottom:-14px;width:20px;height:20px;background:var(--amber);border-right:2.5px solid var(--ink);border-bottom:2.5px solid var(--ink);transform:rotate(45deg)}
.wiggle{animation:wig .6s var(--ease)}@keyframes wig{25%{transform:rotate(-8deg)}50%{transform:rotate(7deg) translateY(-8px)}75%{transform:rotate(-3deg)}}
@media(max-width:900px){.qside .barrybig{display:none}}
/* books */
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{border:2.5px solid var(--ink);background:transparent;border-radius:999px;padding:8px 16px;font-weight:700;font-size:15px;cursor:pointer;transition:background .2s,transform .15s}
.chip:hover{transform:translateY(-2px)}.chip[aria-pressed=true]{background:var(--ink);color:var(--paper)}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(200px,44%),1fr));gap:40px 26px}
.book{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:10px;transition:opacity .35s,transform .35s var(--ease)}
.book.hide{display:none}
.book:focus-visible{outline:3px solid var(--orange);outline-offset:6px;border-radius:8px}
.cover{position:relative;display:block;border-radius:6px;overflow:hidden;box-shadow:0 0 0 2.5px var(--ink),8px 8px 0 var(--ink);transition:transform .3s var(--ease),box-shadow .3s var(--ease);will-change:transform}
.book:hover .cover{box-shadow:0 0 0 2.5px var(--ink),12px 12px 0 var(--orange)}
.cover img{width:100%}
.shine{position:absolute;inset:0;background:radial-gradient(circle at var(--sx,50%) var(--sy,0%),rgba(255,255,255,.4),transparent 45%);opacity:0;transition:opacity .25s;pointer-events:none}
.cover:hover .shine{opacity:1}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px}
.who{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.badge{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:3px 9px}
.badge.out{background:var(--green);color:#fff}.badge.soon{background:var(--paper2);color:var(--muted)}
.bt{font-weight:700;font-size:18px;line-height:1.25}
.peek{font-weight:700;font-size:14px;color:var(--orange);opacity:0;transform:translateX(-6px);transition:.25s var(--ease)}
.book:hover .peek,.book:focus-visible .peek{opacity:1;transform:none}
@media(hover:none){.peek{opacity:1;transform:none}}
/* videos */
#watch{background:var(--ink);color:var(--paper);margin-top:110px;padding-bottom:110px;overflow:hidden}
#watch .lede{color:#b9b6c8}#watch .kicker{color:var(--amber)}
.rail{display:flex;gap:22px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px 16px 26px;margin:0 -16px;scrollbar-width:thin;scrollbar-color:var(--amber) transparent}
.vid{all:unset;cursor:pointer;flex:0 0 clamp(200px,22vw,250px);scroll-snap-align:start;position:relative;border-radius:16px;overflow:hidden;aspect-ratio:9/16;box-shadow:0 0 0 2px rgba(255,255,255,.12);transition:transform .35s var(--ease),box-shadow .35s}
.vid img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease)}
.vid:hover{transform:translateY(-8px) rotate(-1deg);box-shadow:0 0 0 3px var(--amber),0 24px 50px rgba(0,0,0,.5)}
.vid:hover img{transform:scale(1.05)}
.vid:focus-visible{outline:3px solid var(--amber);outline-offset:4px}
.vid::after{content:'';position:absolute;inset:55% 0 0;background:linear-gradient(transparent,rgba(5,8,20,.92))}
.vid .play{position:absolute;left:50%;top:44%;width:66px;height:66px;margin:-33px 0 0 -33px;border-radius:50%;background:var(--amber);color:var(--ink);display:grid;place-items:center;border:3px solid var(--ink);transform:scale(.8);opacity:.0;transition:.3s var(--ease);z-index:2}
.vid .play svg{width:30px;height:30px;margin-left:4px}
.vid:hover .play,.vid:focus-visible .play{transform:scale(1);opacity:1}
@media(hover:none){.vid .play{opacity:1;transform:scale(.85)}}
.vt{position:absolute;left:14px;right:14px;bottom:14px;font-weight:700;font-size:16px;line-height:1.25;z-index:2}
.railnav{display:flex;gap:10px}
.railnav button{width:48px;height:48px;border-radius:50%;border:2.5px solid var(--paper);background:transparent;color:var(--paper);cursor:pointer;font-size:20px;transition:background .2s,color .2s}
.railnav button:hover{background:var(--amber);color:var(--ink);border-color:var(--amber)}
/* how we check */
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;counter-reset:s}
@media(max-width:860px){.steps{grid-template-columns:1fr}}
.step{position:relative;background:#fff;border:2.5px solid var(--ink);border-radius:var(--r);padding:28px 26px 26px;box-shadow:6px 6px 0 var(--ink)}
.step::before{counter-increment:s;content:counter(s);position:absolute;top:-22px;left:22px;width:44px;height:44px;border-radius:50%;background:var(--amber);border:2.5px solid var(--ink);display:grid;place-items:center;font-family:var(--display);font-size:24px}
.step h3{font-size:30px;margin:8px 0 8px}.step p{margin:0;color:#3d3d52}
.stamps{display:flex;flex-wrap:wrap;gap:14px;margin-top:40px;align-items:center}
.stamps .stamp{font-size:15px;opacity:0}
.stamps.in .stamp{animation:slam .5s var(--ease) forwards}
.stamps.in .stamp:nth-child(2){animation-delay:.15s}.stamps.in .stamp:nth-child(3){animation-delay:.3s}.stamps.in .stamp:nth-child(4){animation-delay:.45s}
.stamps .hand{font-size:24px;margin-left:6px}
/* learn */
.learngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:16px}
.learn{display:flex;flex-direction:column;gap:6px;text-decoration:none;padding:20px 20px 22px;border:2.5px solid var(--ink);border-radius:14px;background:var(--paper);transition:transform .25s var(--ease),box-shadow .25s var(--ease),background .2s}
.learn:hover{transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--ink);background:#fff}
.tag{align-self:flex-start;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:3px 8px;border-radius:5px;color:var(--ink)}
.t-space{background:#c9e8ff}.t-nature{background:#cdeec9}.t-earth{background:#ffe6a6}.t-school{background:#ffd3c4}.t-science{background:#e6d6ff}
.lt{font-weight:700;font-size:19px}.lt span{color:var(--orange)}
.ld{color:var(--muted);font-size:15px}
/* footer */
footer{margin-top:120px;background:var(--orange);border-top:3px solid var(--ink);padding:70px 0 40px}
footer .big{font-family:var(--display);text-transform:uppercase;font-size:clamp(46px,9vw,110px);line-height:.92;margin:0 0 30px}
footer .row{display:flex;flex-wrap:wrap;justify-content:space-between;gap:20px;align-items:center;border-top:2px solid var(--ink);padding-top:24px;font-weight:600}
footer small{display:block;margin-top:24px;font-size:13px;opacity:.8}
/* dialog */
dialog{border:3px solid var(--ink);border-radius:22px;padding:0;max-width:min(920px,calc(100vw - 24px));width:100%;max-height:calc(100dvh - 24px);background:var(--paper);color:var(--ink);box-shadow:12px 12px 0 var(--ink);overflow:auto}
dialog::backdrop{background:rgba(11,16,38,.7);backdrop-filter:blur(4px)}
dialog[open]{animation:dlg .4s var(--ease)}
@keyframes dlg{from{opacity:0;transform:translateY(24px) scale(.97)}}
.x{position:sticky;top:12px;float:right;margin:12px 12px 0 0;width:44px;height:44px;border-radius:50%;border:2.5px solid var(--ink);background:#fff;font-size:22px;cursor:pointer;z-index:2}
.x:hover{background:var(--amber)}
.dbody{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:34px;padding:34px clamp(18px,4vw,40px) 36px}
.dbody.v{grid-template-columns:minmax(0,320px) minmax(0,1fr)}
@media(max-width:720px){.dbody,.dbody.v{grid-template-columns:1fr;gap:22px}.dbody .dcover{max-width:220px}}
.dcover{border-radius:6px;overflow:hidden;box-shadow:0 0 0 2.5px var(--ink),8px 8px 0 var(--ink);align-self:start}
.dbody h3{font-size:clamp(34px,4.5vw,50px);margin:6px 0 14px}
.dbody p{margin:0 0 16px}
.dbody h4{font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin:22px 0 10px;color:var(--orange)}
.flist{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.flist li{background:#fff;border:2px solid var(--ink);border-radius:12px;padding:10px 14px 10px 44px;position:relative}
.flist li::before{content:'!';position:absolute;left:12px;top:10px;width:22px;height:22px;border-radius:50%;background:var(--amber);border:2px solid var(--ink);display:grid;place-items:center;font-weight:800;font-size:13px}
.links{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.links a{display:inline-block;text-decoration:none;font-size:14px;font-weight:600;border:2px solid var(--ink);border-radius:999px;padding:6px 12px;transition:background .2s}
.links a:hover{background:var(--amber)}
.dbuy{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px;align-items:center}
.player{aspect-ratio:9/16;border-radius:14px;overflow:hidden;background:#000;box-shadow:0 0 0 2.5px var(--ink)}
.player iframe{width:100%;height:100%;border:0}
/* reveals */
.reveal{opacity:0;transform:translateY(26px);transition:opacity .8s var(--ease),transform .8s var(--ease);transition-delay:var(--d,0ms)}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}.reveal{opacity:1;transform:none}html{scroll-behavior:auto}.stamps .stamp{opacity:1}}
"""

JS = r"""
(function(){
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var BOOKS = __BOOKS__, VIDS = __VIDS__, QUIZ = __QUIZ__;
  function $(s, r){ return (r || document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  // nav border once scrolled
  var nav = $('.nav');
  addEventListener('scroll', function(){ nav.classList.toggle('scrolled', scrollY > 10); }, {passive:true});

  // hero: layers drift against the mouse (or gently on their own on phones)
  var stage = $('.stage'), layers = $$('.layer', stage), tx = 0, ty = 0, cx = 0, cy = 0, t0 = performance.now();
  if (!reduced){
    if (fine) $('.hero').addEventListener('mousemove', function(ev){ tx = ev.clientX / innerWidth * 2 - 1; ty = ev.clientY / innerHeight * 2 - 1; });
    (function loop(now){
      if (!fine){ var t = (now - t0) / 1000; tx = Math.sin(t * .5) * .6; ty = Math.cos(t * .4) * .5; }
      cx += (tx - cx) * .07; cy += (ty - cy) * .07;
      layers.forEach(function(l){ var d = +l.dataset.depth; l.style.transform = 'translate3d(' + (cx * d).toFixed(2) + 'px,' + (cy * d).toFixed(2) + 'px,0)'; });
      requestAnimationFrame(loop);
    })(t0);
  }

  // cover tilt + shine
  if (fine && !reduced){
    $$('.tilt').forEach(function(el){
      el.addEventListener('mousemove', function(ev){
        var r = el.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width, py = (ev.clientY - r.top) / r.height;
        el.style.transform = 'perspective(700px) rotateY(' + ((px - .5) * 16).toFixed(2) + 'deg) rotateX(' + ((.5 - py) * 14).toFixed(2) + 'deg) translateY(-6px)';
        el.style.setProperty('--sx', px * 100 + '%'); el.style.setProperty('--sy', py * 100 + '%');
      });
      el.addEventListener('mouseleave', function(){ el.style.transform = ''; });
    });
  }

  // scroll reveals
  var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
  $$('.reveal, .stamps').forEach(function(el){ io.observe(el); });

  // ---- True or False ----
  var card = $('#qcard'), qi = 0, score = 0, dots = $('.dots', card);
  var bubble = $('#bubble'), barry = $('.barrybig');
  var cheers = ['Nailed it!', 'Correct! Show-off.', 'Yes! Big brain.', 'Spot on.'], groans = ['Nope! Most people get that one.', 'Ooh, so close.', 'Wrong, but now you know!', 'Ha! Gotcha.'];
  QUIZ.forEach(function(){ dots.appendChild(document.createElement('i')); });
  function show(){
    var q = QUIZ[qi];
    card.classList.remove('answered');
    $('.qn', card).textContent = 'Question ' + (qi + 1) + ' of ' + QUIZ.length;
    $('.qtext', card).textContent = q.s;
    $$('i', dots).forEach(function(d, k){ d.classList.toggle('now', k === qi); });
  }
  function say(t){ bubble.textContent = t; if (barry && !reduced){ barry.classList.remove('wiggle'); void barry.offsetWidth; barry.classList.add('wiggle'); } }
  function answer(v){
    var q = QUIZ[qi], ok = v === q.a;
    if (ok) score++;
    var d = $$('i', dots)[qi]; d.classList.remove('now'); d.classList.add(ok ? 'ok' : 'no');
    var vd = $('.verdict', card); vd.textContent = ok ? 'Correct!' : 'Not quite!'; vd.className = 'verdict ' + (ok ? 'ok' : 'no');
    $('.why', card).textContent = q.w;
    $('.src', card).textContent = 'From: ' + q.f;
    var st = $('.bigstamp', card); st.textContent = q.a ? 'TRUE' : 'FALSE'; st.style.color = q.a ? 'var(--green)' : 'var(--orange)';
    $('.next', card).textContent = qi === QUIZ.length - 1 ? 'See my score' : 'Next question →';
    card.classList.add('answered');
    say((ok ? cheers : groans)[qi % 4]);
    $('.next', card).focus({preventScroll:true});
  }
  $('.qbtns .t', card).onclick = function(){ answer(true); };
  $('.qbtns .f', card).onclick = function(){ answer(false); };
  $('.next', card).onclick = function(){
    if (qi < QUIZ.length - 1){ qi++; show(); return; }
    var msg = score === QUIZ.length ? 'Perfect score. Are you secretly Barry?' : score >= 6 ? 'Seriously impressive.' : score >= 4 ? 'Not bad at all!' : 'The world is weirder than you thought, eh?';
    $('.qinner', card).innerHTML = '<div class="done"><div class="qtop"><span>Final score</span></div><h3>' + score + ' out of ' + QUIZ.length + '</h3><p class="why">' + msg + ' Every one of those came from our books and videos, and there are hundreds more inside.</p><div class="cta" style="margin-top:22px"><a class="btn" href="#books">Find the books</a><button class="btn alt" id="again">Play again</button></div></div>';
    say(score >= 6 ? 'Told you it was weird.' : 'Have another go!');
    $('#again').onclick = function(){ location.hash = ''; location.reload(); };
  };
  show();

  // ---- book shelf filter ----
  $$('.chip').forEach(function(c){
    c.onclick = function(){
      $$('.chip').forEach(function(x){ x.setAttribute('aria-pressed', x === c); });
      var f = c.dataset.f;
      $$('.book').forEach(function(b){ b.classList.toggle('hide', f !== 'all' && b.dataset.aud.split(' ').indexOf(f) < 0); });
    };
  });

  // ---- pop-up for books and videos ----
  var dlg = $('#dlg'), dc = $('#dlgc');
  function links(arr){ return '<ul class="links">' + arr.map(function(l){ return '<li><a href="' + esc(l[1]) + '" rel="noopener" target="_blank">' + esc(l[0]) + ' ↗</a></li>'; }).join('') + '</ul>'; }
  function facts(arr){ return '<ul class="flist">' + arr.map(function(f){ return '<li>' + esc(f) + '</li>'; }).join('') + '</ul>'; }
  function open(html){ dc.innerHTML = html; dlg.showModal(); dlg.scrollTop = 0; }
  $$('.book').forEach(function(el){
    el.onclick = function(){
      var b = BOOKS[+el.dataset.i];
      var buy = b.status === 'out'
        ? b.buy.map(function(x, k){ return '<a class="btn ' + (k ? 'alt' : '') + '" href="' + esc(x[1]) + '" rel="noopener" target="_blank">' + esc(x[0]) + '</a>'; }).join('')
        : '<span class="badge soon" style="font-size:14px;padding:8px 14px">Coming soon to Amazon</span>';
      open('<div class="dbody"><img class="dcover" src="' + b.src + '" alt="Cover of ' + esc(b.t) + '"><div>' +
        '<p class="kicker">' + esc(b.who) + '</p><h3>' + esc(b.t) + '</h3><p>' + esc(b.blurb) + '</p>' +
        (b.facts ? '<h4>Three facts from inside</h4>' + facts(b.facts) : '') +
        (b.deeper ? '<h4>Go deeper</h4>' + links(b.deeper) : '') +
        '<div class="dbuy">' + buy + '</div></div></div>');
    };
  });
  $$('.vid').forEach(function(el){
    el.onclick = function(){
      var v = VIDS[+el.dataset.v];
      open('<div class="dbody v"><div class="player"><iframe src="https://www.youtube-nocookie.com/embed/' + v.id + '?autoplay=1&rel=0&playsinline=1" title="' + esc(v.t) + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><div>' +
        '<p class="kicker">Short · about 2 minutes</p><h3>' + esc(v.t) + '</h3>' +
        '<h4>The facts behind it</h4>' + facts(v.facts) + '<h4>Our sources</h4>' + links(v.deeper) +
        '<div class="dbuy"><a class="btn" href="https://www.youtube.com/shorts/' + v.id + '" rel="noopener" target="_blank">Watch on YouTube</a></div></div></div>');
    };
  });
  $('.x', dlg).onclick = function(){ dlg.close(); };
  dlg.addEventListener('click', function(ev){ if (ev.target === dlg) dlg.close(); });
  dlg.addEventListener('close', function(){ dc.innerHTML = ''; });

  // video rail arrows
  var rail = $('.rail');
  $$('.railnav button').forEach(function(b){ b.onclick = function(){ rail.scrollBy({left:(+b.dataset.dir) * rail.clientWidth * .8, behavior: reduced ? 'auto' : 'smooth'}); }; });
})();
"""

PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hex Bridge Media: the world is weirder than you think</title>
<meta name="description" content="Fact books, family quiz books, colouring books and short cartoon science videos by Samuel J Hextall. Every fact checked twice. Play True or False, watch the videos, find the books.">
<meta name="theme-color" content="#fbf4e6">
<meta property="og:title" content="Hex Bridge Media: the world is weirder than you think">
<meta property="og:description" content="Fact books, quiz books, colouring books and short science videos. Every fact checked twice.">
<meta property="og:image" content="https://hexbridgemedia.co.uk/img/share.jpg">
<meta property="og:url" content="https://hexbridgemedia.co.uk/">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>%CSS%</style>
</head>
<body>
<nav class="nav"><div class="wrap">
  <a class="logo" href="#top"><img src="img/logo.png" alt="" width="38" height="38"><span>Hex Bridge Media</span></a>
  <ul><li><a href="#quiz">True or False</a></li><li><a href="#books">Books</a></li><li><a href="#watch">Videos</a></li><li><a href="#how">How we check</a></li><li><a href="#learn">Explore</a></li></ul>
  <a class="btn sm amber" href="%CHANNEL%" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>YouTube</a>
</div></nav>

<header class="hero" id="top"><div class="wrap">
  <div>
    <p class="qr-hello"><b>HELLO</b> Scanned a QR code in one of our books? You're in the right place.</p>
    <h1><span class="line"><span>The world is</span></span><span class="line"><span><span class="mark">weirder</span> than</span></span><span class="line"><span>you think.</span></span></h1>
    <p class="sub">Fact books, family quizzes, colouring books and short cartoon science videos about the strangest true things we can find. Every number gets checked twice.</p>
    <div class="cta"><a class="btn" href="#quiz">Test yourself <span aria-hidden="true">→</span></a><a class="btn alt" href="#books">Browse the books</a></div>
    <div class="proof"><span><i></i>%NBOOKS% books</span><span><i></i>%NVIDS% videos</span><span><i></i>Ages 3 to 103</span></div>
  </div>
  <div class="stage" aria-label="Some of our books">
    <div class="layer" data-depth="-28"><span class="float f1">%HEX%</span><span class="float f4">%HEX%</span></div>
    <div class="layer" data-depth="-12"><span class="float f2">%HEX%</span><span class="float f3">%HEX%</span></div>
    <div class="layer" data-depth="16"><div class="fan">%FAN%</div></div>
    <div class="layer" data-depth="30" aria-hidden="true">
      <span class="stamp s1">Measured</span><span class="stamp s2">Checked twice</span>
      <span class="note">%BARRY%<span>Barry, 1.8 m<br>(for scale)</span></span>
    </div>
  </div>
</div></header>

<div class="tickwrap"><div class="ticker" aria-hidden="true"><div class="track">%TICKER%%TICKER%</div></div></div>

<main>
<section id="quiz"><div class="wrap quizbox">
  <div class="qside reveal">
    <p class="kicker">%HEXS% Quick game</p>
    <h2>True or <span class="mark">false?</span></h2>
    <p class="lede">Eight real facts from our books and videos. Most people get about half. Can you beat Barry?</p>
    <div class="bubble" id="bubble" aria-live="polite">Go on, have a go!</div><br>
    <svg class="barrybig" viewBox="0 0 60 120" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="30" cy="16" r="11"/><path d="M30 27v44M30 71l-14 40M30 71l14 40M30 40l-18 18M30 40l20-18"/></g><circle cx="26" cy="14" r="1.6" fill="currentColor"/><circle cx="34" cy="14" r="1.6" fill="currentColor"/><path d="M25 20q5 4 10 0" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
  </div>
  <div class="card reveal" id="qcard" aria-live="polite"><div class="qinner">
    <div class="qtop"><span class="qn"></span><span class="dots"></span></div>
    <p class="qtext"></p>
    <div class="qbtns"><button class="btn t">True</button><button class="btn f">False</button></div>
    <div class="reveal-a"><p class="verdict"></p><p class="why"></p><p class="src"></p><button class="btn amber next"></button></div>
    <span class="stamp bigstamp" aria-hidden="true"></span>
  </div></div>
</div></section>

<section id="books"><div class="wrap">
  <div class="sechead">
    <div><p class="kicker">%HEXS% Read, play, colour</p><h2>The books</h2>
    <p class="lede">Fact books for curious kids, quiz books that get the whole family arguing, and colouring books for every age. Tap a book to look inside.</p></div>
    <div class="chips" role="group" aria-label="Filter books">
      <button class="chip" data-f="all" aria-pressed="true">All</button><button class="chip" data-f="fact" aria-pressed="false">Fact &amp; quiz</button><button class="chip" data-f="colour" aria-pressed="false">Colouring</button><button class="chip" data-f="kids" aria-pressed="false">Kids</button><button class="chip" data-f="family" aria-pressed="false">Families</button><button class="chip" data-f="adults" aria-pressed="false">Grown-ups</button>
    </div>
  </div>
  <div class="shelf">%SHELF%</div>
</div></section>

<section id="watch"><div class="wrap">
  <div class="sechead">
    <div><p class="kicker">%HEXS% Watch</p><h2>Two-minute science</h2>
    <p class="lede">Hand-made cartoon Shorts about the hottest, fastest, oldest and furthest things there are. Press play right here, then see the facts and sources behind each one.</p></div>
    <div class="railnav"><button data-dir="-1" aria-label="Scroll videos left">←</button><button data-dir="1" aria-label="Scroll videos right">→</button></div>
  </div>
  <div class="rail">%VIDEOS%</div>
  <p style="margin-top:30px"><a class="btn amber" href="%CHANNEL%" rel="noopener" target="_blank">See every video on YouTube</a></p>
</div></section>

<section id="how"><div class="wrap">
  <div class="sechead"><div><p class="kicker">%HEXS% No made-up facts</p><h2>How we check</h2>
  <p class="lede">The internet is full of “facts” that aren't. Here's what every number goes through before it goes in a book or a video.</p></div></div>
  <div class="steps">
    <div class="step reveal"><h3>Two sources</h3><p>Every figure needs two independent sources, ideally the people who measured it: NASA, the Met Office, CERN, museums and journals.</p></div>
    <div class="step reveal" style="--d:100ms"><h3>A fact hunt</h3><p>Each book and video then gets a separate audit whose only job is to find mistakes. It always finds some, and we fix them.</p></div>
    <div class="step reveal" style="--d:200ms"><h3>Honest labels</h3><p>We say whether a number was measured, estimated or argued about, and we date records, because records get broken.</p></div>
  </div>
  <div class="stamps" aria-hidden="true"><span class="stamp" style="color:var(--green)">Measured</span><span class="stamp" style="color:#c48a00">Estimate</span><span class="stamp" style="color:var(--orange)">Disputed</span><span class="stamp" style="color:#2a6fd6">Checked Nov 2026</span><span class="hand">← you'll see these in the books</span></div>
  <p class="lede">Spotted something wrong? Tell us in a comment on any video. We'll fix it and say so.</p>
</div></section>

<section id="learn"><div class="wrap">
  <div class="sechead"><div><p class="kicker">%HEXS% Keep exploring</p><h2>Where we go to learn</h2>
  <p class="lede">Free, trustworthy places to keep finding things out, for curious kids and curious grown-ups.</p></div></div>
  <div class="learngrid">%LEARN%</div>
</div></section>
</main>

<footer><div class="wrap">
  <p class="big">Stay<br>curious.</p>
  <div class="row"><span>Hex Bridge Media · books and videos by Samuel J Hextall</span><a class="btn alt sm" href="%CHANNEL%" rel="noopener" target="_blank">YouTube</a></div>
  <small>Links to other sites open in a new tab. We're not responsible for their content, and none of them endorse us. Videos play from YouTube in privacy-enhanced mode.</small>
</div></footer>

<dialog id="dlg" aria-label="Details"><button class="x" aria-label="Close">×</button><div id="dlgc"></div></dialog>
<script>%JS%</script>
</body>
</html>
"""


def jsdump(x):
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/")


if __name__ == "__main__":
    (HERE / "img").mkdir(exist_ok=True)
    for old in (HERE / "img").glob("*.jpg"):
        old.unlink()

    books = []
    for b in FACT_BOOKS:
        src, (w, h) = thumb(b["img"], slug(b["t"]), 600)
        books.append(dict(kind="fact", t=b["t"], who=b["who"], aud=b["aud"], status=b["status"], src=src, w=w, h=h,
                          blurb=b["blurb"], facts=b["facts"], deeper=b["deeper"], buy=amazon(b["q"])))
    for t, who, aud, img, q, status, line in COLOUR:
        src, (w, h) = thumb(img, slug(t), 480)
        books.append(dict(kind="colour", t=t, who=who, aud=aud, status=status, src=src, w=w, h=h,
                          blurb=line, facts=None, deeper=None, buy=amazon(q)))
    # colouring books that are out go first after the fact books, so the shelf leads with things you can buy
    order = [b for b in books if b["kind"] == "fact"] + [b for b in books if b["kind"] == "colour" and b["status"] == "out"] + \
            [b for b in books if b["kind"] == "colour" and b["status"] != "out"]

    vids = []
    for v in VIDEOS:
        src, (w, h) = thumb(v["cover"], "v-" + v["id"], 360, 640)
        vids.append(dict(id=v["id"], t=v["t"], facts=v["facts"], deeper=v["deeper"], src=src, w=w, h=h))

    # hero fan: 5 covers dealt like cards
    fan_pick = ["The Most Extreme Things in the Universe", "Britain's Weirdest Wildlife", "Henhouse Heroes",
                "Grandparents vs Grandkids", "The Food Lover's Quiz Book"]
    pose = [(-16, -150, 30), (-8, -75, 0), (0, 0, -12), (8, 75, 0), (16, 150, 30)]
    fan = ""
    for k, (name, (rot, x, y)) in enumerate(zip(fan_pick, pose)):
        b = next(bb for bb in order if bb["t"] == name)
        fan += (f'<a href="#books" style="--rot:{rot}deg;--tx:{x}px;--ty:{y}px;--dl:{200 + k * 90}ms;z-index:{[1,2,5,3,2][k]}" '
                f'aria-label="{e(name)}"><img src="{b["src"]}" alt="" width="{b["w"]}" height="{b["h"]}"></a>')
    # phones: tighten the spread with a CSS override
    fan_css = "@media(max-width:520px){" + "".join(
        f".fan a:nth-child({k + 1}){{--tx:{int(x * .5)}px;--ty:{int(_y * .6)}px}}" for k, (_, x, _y) in enumerate(pose)) + "}"

    # share image for links posted in chats/social: paper background, five covers fanned
    sh = Image.new("RGB", (1200, 630), (251, 244, 230))
    for k, b in enumerate(FACT_BOOKS):
        im = Image.open(b["img"]).convert("RGB")
        im.thumbnail((250, 330))
        sh.paste(im, (70 + k * 275, 150))
    sh.save(HERE / "img/share.jpg", quality=86)

    hexs = HEX.replace("<svg ", '<svg width="16" height="16" ')
    page = (PAGE.replace("%CSS%", CSS + fan_css)
                .replace("%JS%", JS.replace("__BOOKS__", jsdump(order)).replace("__VIDS__", jsdump(vids))
                         .replace("__QUIZ__", jsdump([dict(s=s, a=a, w=w, f=f) for s, a, w, f in QUIZ])))
                .replace("%FAN%", fan)
                .replace("%SHELF%", "".join(book_card(b, i, b["kind"]) for i, b in enumerate(order)))
                .replace("%VIDEOS%", "".join(video_card(v, i) for i, v in enumerate(vids)))
                .replace("%LEARN%", "".join(learn_card(it, i) for i, it in enumerate(LEARN)))
                .replace("%TICKER%", "".join(f"<span>{e(t)}</span>" for t in TICKER))
                .replace("%BARRY%", BARRY + '<svg class="arrow" viewBox="0 0 60 40" aria-hidden="true"><path d="M4 30C20 34 40 26 52 8M52 8l-10 2M52 8l-1 10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>')
                .replace("%HEXS%", hexs).replace("%HEX%", HEX)
                .replace("%NBOOKS%", str(len(order))).replace("%NVIDS%", str(len(vids)))
                .replace("%CHANNEL%", CHANNEL))
    (HERE / "index.html").write_text(page)
    (HERE / "CNAME").write_text("hexbridgemedia.co.uk\n")
    print("built:", len(FACT_BOOKS), "fact books,", len(COLOUR), "colouring,", len(VIDEOS), "videos,", len(QUIZ), "quiz,", len(LEARN), "learn links")
