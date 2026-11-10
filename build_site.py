"""Builds hexbridgemedia.co.uk (v2, 2026-11-10): the one page every QR code points at.

Sam: "a nice place I can send people to look for information about my books, my videos or anything related",
educational, with good further-reading links, a cool mouse animation (like the HexBridge Advisory site), not overloaded.

Edit the data below (a book's status "out" shows Amazon buttons, "soon" shows Coming soon), then:
    python3 build_site.py && git add -A && git commit -m "update" && git push
Every link in GO DEEPER / LEARN was checked to load on 2026-11-10. Every fact is from the audited book or video text.
"""
import html
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
MEDIA = HERE.parent
CB = MEDIA / "Colouring Books"
FQ = MEDIA / "Fact and Quiz Books"
CHANNEL = "https://www.youtube.com/@HexbridgeMedia"
e = html.escape

FACT_BOOKS = [
    dict(t="The Most Extreme Things in the Universe", who="Ages 8–12", status="soon",
         img=FQ / "01 The Most Extreme Things in the Universe/cover/cover_front_preview.jpg", q="Most Extreme Things in the Universe Hextall",
         blurb="The hottest, coldest, fastest, deepest, loudest and rarest things ever found, starting in your kitchen and finishing at the edge of the universe. Every number wears a stamp saying how far to trust it.",
         facts=["Right now you're moving at about 67,000 mph around the Sun.",
                "A fusion experiment in Oxfordshire, JET, ran at 150 million °C: ten times hotter than the middle of the Sun.",
                "Scientists at CERN made matter at over 5 trillion °C, for far less than a blink."],
         deeper=[("NASA: facts about the Sun", "https://science.nasa.gov/sun/facts/"),
                 ("Met Office: UK weather extremes", "https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-climate-extremes"),
                 ("CERN: the hottest stuff ever made", "https://home.cern/science/physics/heavy-ions-and-quark-gluon-plasma"),
                 ("NASA Space Place (for kids)", "https://spaceplace.nasa.gov/")]),
    dict(t="Britain's Weirdest Wildlife", who="Families, 8+", status="soon",
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
    dict(t="Grandparents vs Grandkids", who="The whole family", status="soon",
         img=FQ / "07 Grandparents vs Grandkids/cover/cover_front_preview.jpg", q="Grandparents vs Grandkids Hextall",
         blurb="The grandkids get asked about the grandparents' world, and the grandparents get asked about the grandkids'. Every round ends with a Story Bonus, so you finish with a winner and your family's stories in your own handwriting.",
         facts=["Before decimal money there were 240 pennies in a pound.",
                "Britain switched to decimal money on 15 February 1971.",
                "Saying “in my day” earns a forfeit. Saying “OK boomer” loses a point."],
         deeper=[("Bank of England Museum", "https://www.bankofengland.co.uk/museum"),
                 ("The Royal Mint: the story of decimalisation", "https://www.royalmint.com/discover/decimalisation/")]),
    dict(t="The Food Lover's Quiz Book", who="Adults", status="soon",
         img=FQ / "08 The Food Lover's Quiz Book/cover/cover_front_preview.jpg", q="Food Lover's Quiz Book Hextall",
         blurb="Twelve rounds of sixteen questions, from spice wars and kitchen myths to cheese, bread and chocolate. Every round opens with a true story, and where historians disagree, the answers say so.",
         facts=["To a botanist, a banana is a berry and a strawberry isn't.",
                "A peanut isn't a nut. It's a legume, a cousin of peas and beans.",
                "Wild tomatoes come from South America, not Italy."],
         deeper=[("Food Standards Agency", "https://www.food.gov.uk/")]),
]
A = CB / "Amazon Colouring Books for Adults/covers"
K = CB / "Amazon Colouring Books for Kids/covers"
COLOUR = [
    ("The History of Christmas", "Ages 6–10", K / "05-history-of-christmas/cover_front_preview.jpg", "History of Christmas Coloring Book Hextall", "out"),
    ("Henhouse Heroes", "Ages 3–6", K / "02-henhouse-heroes/cover_front_preview.jpg", "Henhouse Heroes Hextall", "out"),
    ("Geometric Mandala", "Adults", A / "01-hex-mandalas/hex_cover_front_preview.jpg", "Geometric Mandala Coloring Book Hextall", "out"),
    ("Deep Sea Explorers", "Ages 3–6", K / "03-deep-sea-explorers/cover_front_preview.jpg", "Deep Sea Explorers Hextall", "soon"),
    ("Fastest Things on Earth", "Ages 4–8", K / "04-fastest-things/cover_front_preview.jpg", "Fastest Things on Earth Coloring Book Hextall", "soon"),
    ("Stained Glass", "Adults", A / "04-stained-glass/cover_front_preview.jpg", "Stained Glass Coloring Book Hextall", "soon"),
    ("Moroccan Star Patterns", "Adults", A / "03-moroccan-star-patterns/cover_front_preview.jpg", "Moroccan Star Patterns Coloring Book Hextall", "soon"),
    ("Sacred Geometry", "Adults", A / "05-sacred-geometry/cover_front_preview.jpg", "Sacred Geometry Coloring Book Hextall", "soon"),
    ("Kaleidoscope", "Adults", A / "06-kaleidoscope/cover_front_preview.jpg", "Kaleidoscope Coloring Book Hextall", "soon"),
    ("Patchwork Quilt", "Adults", A / "07-patchwork-quilts/cover_front_preview.jpg", "Patchwork Quilt Coloring Book Hextall", "soon"),
    ("Bold & Easy Mandala", "Adults", A / "02-bold-easy-mandalas/cover_front_preview.jpg", "Bold Easy Mandala Coloring Book Hextall", "soon"),
]
VIDEOS = [
    dict(id="9H3uEBkJVLY", t="Oxfordshire was hotter than the Sun",
         facts=["The UK's hottest day: 40.3 °C at Coningsby, 19 July 2022 (Met Office).",
                "JET, a fusion experiment in Oxfordshire, held plasma at 150 million °C. It closed in December 2023.",
                "The Sun's core is about 15 million °C, so JET ran ten times hotter.",
                "The record is CERN's: over 5 trillion °C (estimated), lasting about 10⁻²³ seconds."],
         deeper=[("UKAEA: the JET experiment", "https://ccfe.ukaea.uk/programmes/joint-european-torus/"),
                 ("CERN: heavy ions and quark-gluon plasma", "https://home.cern/science/physics/heavy-ions-and-quark-gluon-plasma"),
                 ("NASA: the Sun", "https://science.nasa.gov/sun/facts/")]),
    dict(id="1Ov7hjZHEUA", t="You're Faster Than Any Plane Right Now",
         facts=["A cheetah: 58 mph, the fastest measured by tracking collar (Nature, 2013).",
                "The X-15 rocket plane: 4,520 mph in 1967, still the fastest crewed plane.",
                "Parker Solar Probe: 430,000 mph, the fastest spacecraft ever (2024).",
                "You: about 67,000 mph around the Sun, right now."],
         deeper=[("Smithsonian: the X-15", "https://airandspace.si.edu/stories/editorial/x-15"),
                 ("NASA: Parker Solar Probe", "https://science.nasa.gov/mission/parker-solar-probe/"),
                 ("National Geographic: cheetah collars", "https://www.nationalgeographic.com/science/article/collars-reveal-why-just-how-extreme-cheetahs-can-be")]),
    dict(id="rCBY2s00kUI", t="Something in Your Kitchen Is 13.8 Billion Years Old",
         facts=["The oldest bread found: crumbs about 14,400 years old, from Jordan, before farming began.",
                "Jonathan the tortoise hatched around 1832 and is still alive on St Helena.",
                "A Greenland shark was estimated at 392 years old (Science, 2016).",
                "Almost all the hydrogen in your body was made minutes after the Big Bang. So the oldest thing in your kitchen is you."],
         deeper=[("PBS NOVA: the Greenland shark", "https://www.pbs.org/wgbh/nova/article/greenland-shark-is-officially-the-longest-living-vertebrate-on-earth"),
                 ("PBS NOVA: the star in you", "https://www.pbs.org/wgbh/nova/article/star-in-you/"),
                 ("English Heritage: Stonehenge's history", "https://www.english-heritage.org.uk/visit/places/stonehenge/history-and-stories/")]),
    dict(id="YSFKD2EPo40", t="Your Eyes Can See Light Older Than Our Species",
         facts=["The Andromeda galaxy, about 2.5 million light years away, can be seen without a telescope from a dark site.",
                "Its light set off long before our species appeared, about 300,000 years ago.",
                "Voyager 1 is predicted to reach one light-day from Earth on 18 November 2026.",
                "Webb's record galaxy, MoM-z14: its light travelled about 13.5 billion years."],
         deeper=[("NASA: Voyager", "https://science.nasa.gov/mission/voyager/"),
                 ("ESA/Webb", "https://esawebb.org/"),
                 ("NASA: galaxies", "https://science.nasa.gov/universe/galaxies/")]),
    dict(id="nsDCm556mzk", t="How Could a T. Rex Lose to an Insect?",
         facts=["T. rex's bite: about 35,000 newtons, estimated from jaw models.",
                "The strongest bite ever actually measured: a saltwater crocodile, 16,414 N (2012).",
                "The Tsavo lions were said to have killed 135 people; tests on their bones suggest about 35.",
                "Mosquitoes: malaria killed an estimated 610,000 people in 2024 (WHO). The death rate has more than halved since 2000."],
         deeper=[("WHO: malaria fact sheet", "https://www.who.int/news-room/fact-sheets/detail/malaria"),
                 ("Field Museum: the Tsavo lions", "https://www.fieldmuseum.org/blog/man-eating-lions-ate-fewer-people-believed"),
                 ("Florida Museum: shark attack data", "https://www.floridamuseum.ufl.edu/shark-attacks/yearly-worldwide-summary/")]),
    dict(id="T2_wgrx_pmU", t="Can GTA 6 Beat the Best-Selling Games of All Time?",
         facts=["GTA V: over 230 million sold (Take-Two, August 2026).",
                "The PlayStation 2 sold over 160 million, the best-selling console ever (Sony).",
                "Wii Sports: 82.9 million, the most for any game on one console (Nintendo).",
                "The Atari 2600 had 128 bytes of memory, less than one text message."],
         deeper=[("Nintendo: best-selling games", "https://www.nintendo.co.jp/ir/en/finance/software/index.html"),
                 ("Sony Interactive: sales data", "https://sonyinteractive.com/en/our-company/business-data-sales/"),
                 ("Take-Two Interactive investors", "https://www.take2games.com/ir")]),
]
LEARN = [
    ("NASA Space Place", "Space and Earth science games and explainers for kids.", "https://spaceplace.nasa.gov/"),
    ("Natural History Museum: identify nature", "Found something odd in the garden? Find out what it is.", "https://www.nhm.ac.uk/take-part/identify-nature.html"),
    ("iRecord", "Log what you spot, and real scientists use it.", "https://irecord.org.uk/"),
    ("Met Office: learn about weather", "Why the weather does what it does, from the UK's weather service.", "https://www.metoffice.gov.uk/weather/learn-about"),
    ("BBC Bitesize", "Free lessons for every school subject and age.", "https://www.bbc.co.uk/bitesize"),
    ("The Royal Institution", "Home of the Christmas Lectures, with talks and demos online.", "https://www.rigb.org/"),
    ("Woodland Trust", "Tree ID, nature activities and woods to visit near you.", "https://www.woodlandtrust.org.uk/"),
    ("ESA/Hubble", "The best space pictures ever taken, explained.", "https://esahubble.org/"),
]


def slug(t):
    return "-".join("".join(c.lower() if c.isalnum() else " " for c in t).split())


def thumb(src, name, w=520):
    out = HERE / "img" / f"{name}.jpg"
    im = Image.open(src).convert("RGB")
    im.thumbnail((w, int(w * 1.4)))
    im.save(out, quality=84, optimize=True)
    return f"img/{name}.jpg", im.size


def amazon(q):
    qq = q.replace(" ", "+")
    return (f'<a class="btn" href="https://www.amazon.co.uk/s?k={qq}" rel="noopener">Amazon UK</a>'
            f'<a class="btn ghost" href="https://www.amazon.com/s?k={qq}" rel="noopener">Amazon US</a>')


def links(items):
    return "<ul class=\"links\">" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{e(t)}<span aria-hidden="true">↗</span></a></li>' for t, u in items) + "</ul>"


def fact_book(b):
    path, (w, h) = thumb(b["img"], slug(b["t"]))
    buy = amazon(b["q"]) if b["status"] == "out" else '<span class="soon">Coming soon</span>'
    facts = "".join(f"<li>{e(f)}</li>" for f in b["facts"])
    return f'''<article class="feature reveal">
  <div class="cover tilt"><img src="{path}" width="{w}" height="{h}" alt="Cover of {e(b["t"])}" loading="lazy"><i class="shine"></i></div>
  <div class="body">
    <p class="mono">{e(b["who"])}</p>
    <h3>{e(b["t"])}</h3>
    <p>{e(b["blurb"])}</p>
    <details><summary>Three facts from inside</summary><ul class="facts">{facts}</ul></details>
    <details><summary>Go deeper</summary>{links(b["deeper"])}</details>
    <div class="buy">{buy}</div>
  </div>
</article>'''


def colour_book(c):
    t, who, src, q, status = c
    path, (w, h) = thumb(src, slug(t), 360)
    buy = f'<div class="buy small">{amazon(q)}</div>' if status == "out" else '<div class="buy small"><span class="soon">Coming soon</span></div>'
    return f'''<article class="mini reveal"><div class="cover tilt"><img src="{path}" width="{w}" height="{h}" alt="Cover of {e(t)}" loading="lazy"><i class="shine"></i></div>
<h4>{e(t)}</h4><p class="mono">{e(who)}</p>{buy}</article>'''


def video(v):
    facts = "".join(f"<li>{e(f)}</li>" for f in v["facts"])
    return f'''<article class="video reveal">
  <a class="thumb" href="https://www.youtube.com/shorts/{v["id"]}" rel="noopener" target="_blank"><img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play" aria-hidden="true">▶</span></a>
  <h4><a href="https://www.youtube.com/shorts/{v["id"]}" rel="noopener" target="_blank">{e(v["t"])}</a></h4>
  <details><summary>The facts behind it</summary><ul class="facts">{facts}</ul>{links(v["deeper"])}</details>
</article>'''


def learn(item):
    t, d, u = item
    return f'<a class="learn reveal" href="{u}" rel="noopener" target="_blank"><span class="lt">{e(t)} <span aria-hidden="true">↗</span></span><span class="ld">{e(d)}</span></a>'


CSS = r"""
:root{--ground:#0b1026;--ground2:#121838;--mauve:#42283a;--peach:#e3a07a;--amber:#ffc83a;--orange:#ff6a3d;--text:#efe8dc;--muted:#a9a3b4;--line:rgba(239,232,220,.14);--card:rgba(255,255,255,.04)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--text);font:400 17px/1.65 'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}img{display:block;max-width:100%;height:auto}
.mono{font-family:'DM Mono',monospace;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--peach);margin:0 0 6px}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;line-height:1.05;margin:0}
h2{font-size:clamp(36px,6vw,58px)}h3{font-size:clamp(26px,3.4vw,34px);margin-bottom:10px}
h4{font-size:18px;margin:12px 0 2px;font-weight:600;line-height:1.3}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
section{padding:96px 0 24px;position:relative}
.lede{color:var(--muted);max-width:640px;margin:14px 0 40px;font-size:18px}
/* hero */
.hero{position:relative;min-height:92vh;display:flex;align-items:center;overflow:hidden;padding:0}
#hex{position:absolute;inset:0;width:100%;height:100%}
.hero .wrap{position:relative;z-index:2;pointer-events:none}
.hero .wrap a{pointer-events:auto}
.brand{display:flex;align-items:center;gap:12px;margin-bottom:28px}
.brand img{width:52px;height:52px;border-radius:50%}
.hero h1{font-size:clamp(48px,9.5vw,112px);max-width:900px;letter-spacing:-.01em}
.hero h1 em{font-style:italic;color:var(--peach)}
.hero p.sub{max-width:560px;color:var(--muted);font-size:clamp(17px,2.2vw,20px);margin:22px 0 34px}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.pill{font-family:'DM Mono',monospace;font-size:13px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;padding:13px 20px;border:1px solid var(--line);border-radius:999px;background:rgba(11,16,38,.55);backdrop-filter:blur(6px);transition:border-color .2s,background .2s,transform .2s}
.pill:hover{border-color:var(--peach);background:rgba(227,160,122,.12);transform:translateY(-2px)}
.pill.hot{background:var(--peach);color:var(--ground);border-color:var(--peach)}
.scrollcue{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.2em;color:var(--muted);z-index:2}
/* spotlight that follows the mouse */
#spot{position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(420px circle at var(--mx,-999px) var(--my,-999px),rgba(227,160,122,.07),transparent 60%)}
main{position:relative;z-index:2}
/* feature books */
.feature{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:40px;align-items:start;padding:36px 0;border-top:1px solid var(--line)}
.feature .body p{color:#d9d2c6;margin:0 0 14px}
@media(max-width:720px){.feature{grid-template-columns:1fr;gap:20px}.feature .cover{max-width:260px}}
.cover{position:relative;border-radius:6px;transform-style:preserve-3d;transition:transform .25s ease-out;box-shadow:0 18px 40px rgba(0,0,0,.45);overflow:hidden;will-change:transform}
.cover img{width:100%}
.shine{position:absolute;inset:0;background:radial-gradient(circle at var(--sx,50%) var(--sy,0%),rgba(255,255,255,.28),transparent 45%);opacity:0;transition:opacity .25s;pointer-events:none}
.cover:hover .shine{opacity:1}
details{border-top:1px solid var(--line);padding:10px 0}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-family:'DM Mono',monospace;font-size:13px;letter-spacing:.12em;text-transform:uppercase;list-style:none;display:flex;justify-content:space-between;align-items:center;color:var(--text)}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';font-size:20px;color:var(--peach);transition:transform .25s}
details[open] summary::after{transform:rotate(45deg)}
.facts{margin:12px 0 4px;padding-left:20px}.facts li{margin:6px 0;color:#e2dbd0}
.facts li::marker{color:var(--peach)}
.links{list-style:none;padding:0;margin:12px 0 4px}
.links li{margin:4px 0}
.links a{text-decoration:none;border-bottom:1px solid rgba(227,160,122,.35);transition:border-color .2s,color .2s}
.links a:hover{color:var(--peach);border-color:var(--peach)}
.links span{font-size:13px;margin-left:5px;color:var(--peach)}
.buy{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.btn{text-decoration:none;font-weight:600;font-size:14px;padding:10px 16px;border-radius:999px;background:var(--peach);color:var(--ground);transition:transform .2s,background .2s}
.btn:hover{transform:translateY(-2px);background:var(--amber)}
.btn.ghost{background:transparent;color:var(--text);border:1px solid var(--line)}
.btn.ghost:hover{border-color:var(--peach);background:transparent}
.soon{font-family:'DM Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border:1px dashed var(--line);padding:8px 14px;border-radius:999px}
/* colouring grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(170px,100%),1fr));gap:26px 20px}
.mini .mono{font-size:11px}
.buy.small{margin-top:8px}.buy.small .btn{font-size:12px;padding:7px 11px}
/* videos */
.vids{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:30px 24px}
.thumb{position:relative;display:block;border-radius:8px;overflow:hidden;aspect-ratio:4/3}
.thumb img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.thumb:hover img{transform:scale(1.05)}
.play{position:absolute;left:14px;bottom:12px;width:44px;height:44px;border-radius:50%;background:rgba(11,16,38,.75);display:grid;place-items:center;font-size:15px;color:var(--peach);border:1px solid var(--line)}
.video h4 a{text-decoration:none}.video h4 a:hover{color:var(--peach)}
.video details{margin-top:8px}
/* learn + how */
.learngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:14px}
.learn{display:block;text-decoration:none;padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:var(--card);transition:border-color .2s,transform .2s,background .2s}
.learn:hover{border-color:var(--peach);transform:translateY(-3px);background:rgba(227,160,122,.06)}
.lt{display:block;font-weight:600}.lt span{color:var(--peach)}
.ld{display:block;color:var(--muted);font-size:15px;margin-top:4px}
.how{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));gap:22px;margin-top:10px}
.how div{border-top:2px solid var(--peach);padding-top:14px}
.how b{font-family:'Cormorant Garamond',serif;font-size:26px;display:block;margin-bottom:4px}
.how p{color:var(--muted);margin:0}
.stamps{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.stamp{font-family:'DM Mono',monospace;font-size:12px;letter-spacing:.14em;border:1.5px solid currentColor;padding:4px 9px;border-radius:4px;transform:rotate(-2deg)}
footer{border-top:1px solid var(--line);margin-top:90px;padding:40px 0 60px;color:var(--muted);font-size:15px}
footer a{color:var(--peach)}
/* reveal on scroll */
.reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}#spot{display:none}.cover{transition:none}html{scroll-behavior:auto}}
"""

JS = r"""
(function(){
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coarse = matchMedia('(pointer: coarse)').matches;
  var c = document.getElementById('hex'), x = c.getContext('2d');
  var W, H, dpr, cells = [], R = 34, mouse = {x:-9999, y:-9999, on:false}, ripples = [], t0 = performance.now();
  var cols = [[227,160,122],[255,200,58],[255,106,61],[150,120,200]];
  function size(){
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = c.getBoundingClientRect(); W = r.width; H = r.height;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr,0,0,dpr,0,0);
    R = W < 700 ? 26 : 34;
    cells = []; var w = Math.sqrt(3) * R, h = 1.5 * R;
    for (var row = -1, y = -R; y < H + R; row++, y += h)
      for (var col = -1, xx = (row % 2 ? w / 2 : 0) - w; xx < W + w; col++, xx += w)
        cells.push({x:xx, y:y, e:0, c:cols[(Math.abs(row * 7 + col * 3)) % cols.length], tw:Math.random() * 6.28});
  }
  function hexPath(cx, cy, r){
    x.beginPath();
    for (var i = 0; i < 6; i++){ var a = Math.PI / 6 + i * Math.PI / 3; x.lineTo(cx + r * Math.cos(a), cy + r * Math.sin(a)); }
    x.closePath();
  }
  function frame(now){
    var t = (now - t0) / 1000;
    x.clearRect(0, 0, W, H);
    // auto-wander on touch screens / before the mouse arrives
    var mx = mouse.x, my = mouse.y;
    if (!mouse.on){ mx = W * (0.5 + 0.32 * Math.sin(t * 0.35)); my = H * (0.55 + 0.22 * Math.sin(t * 0.53)); }
    for (var i = 0; i < cells.length; i++){
      var p = cells[i], dx = p.x - mx, dy = p.y - my, d = Math.sqrt(dx * dx + dy * dy);
      var target = Math.max(0, 1 - d / 230);
      for (var k = 0; k < ripples.length; k++){
        var rp = ripples[k], rd = Math.sqrt((p.x - rp.x) * (p.x - rp.x) + (p.y - rp.y) * (p.y - rp.y));
        var front = (now - rp.t) * 0.9, band = Math.abs(rd - front);
        if (band < 60) target = Math.max(target, (1 - band / 60) * (1 - (now - rp.t) / 1600));
      }
      p.e += (target - p.e) * 0.12;
      var base = 0.05 + 0.03 * Math.sin(t * 0.8 + p.tw);
      var a = base + p.e * 0.9;
      var r = R * (0.92 - 0.18 * p.e);
      // lift toward the cursor a touch
      var lx = p.x - dx * 0.06 * p.e, ly = p.y - dy * 0.06 * p.e;
      hexPath(lx, ly, r);
      if (p.e > 0.02){ x.fillStyle = 'rgba(' + p.c[0] + ',' + p.c[1] + ',' + p.c[2] + ',' + (p.e * 0.34).toFixed(3) + ')'; x.fill(); }
      x.strokeStyle = 'rgba(239,232,220,' + a.toFixed(3) + ')';
      x.lineWidth = 1 + p.e * 1.2;
      x.stroke();
    }
    ripples = ripples.filter(function(rp){ return now - rp.t < 1600; });
    if (!reduced) requestAnimationFrame(frame);
  }
  size(); addEventListener('resize', size);
  var hero = document.querySelector('.hero');
  if (!coarse){
    hero.addEventListener('mousemove', function(ev){ var r = c.getBoundingClientRect(); mouse.x = ev.clientX - r.left; mouse.y = ev.clientY - r.top; mouse.on = true; });
    hero.addEventListener('mouseleave', function(){ mouse.on = false; });
  }
  hero.addEventListener('click', function(ev){ var r = c.getBoundingClientRect(); ripples.push({x:ev.clientX - r.left, y:ev.clientY - r.top, t:performance.now()}); });
  if (reduced){ frame(performance.now()); } else { requestAnimationFrame(frame); }

  // soft spotlight that follows the cursor down the page
  if (!reduced && !coarse){
    var spot = document.getElementById('spot');
    addEventListener('mousemove', function(ev){ spot.style.setProperty('--mx', ev.clientX + 'px'); spot.style.setProperty('--my', ev.clientY + 'px'); });
  }
  // book covers tilt toward the mouse, with a moving shine
  if (!reduced && !coarse){
    document.querySelectorAll('.tilt').forEach(function(el){
      el.addEventListener('mousemove', function(ev){
        var r = el.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width, py = (ev.clientY - r.top) / r.height;
        el.style.transform = 'perspective(800px) rotateY(' + ((px - 0.5) * 14).toFixed(2) + 'deg) rotateX(' + ((0.5 - py) * 12).toFixed(2) + 'deg) scale(1.03)';
        el.style.setProperty('--sx', (px * 100) + '%'); el.style.setProperty('--sy', (py * 100) + '%');
      });
      el.addEventListener('mouseleave', function(){ el.style.transform = ''; });
    });
  }
  // fade things in as they scroll into view
  var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
})();
"""

PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hex Bridge Media: true, strange and checked</title>
<meta name="description" content="Fact books, family quiz books, colouring books and short science videos by Samuel J Hextall, with the facts behind them and where to learn more.">
<meta property="og:title" content="Hex Bridge Media">
<meta property="og:description" content="Books and short videos about the strangest true things we could find, checked properly.">
<meta property="og:image" content="https://hexbridgemedia.co.uk/img/share.jpg">
<meta property="og:url" content="https://hexbridgemedia.co.uk/">
<link rel="icon" href="img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>%CSS%</style>
</head>
<body>
<div id="spot" aria-hidden="true"></div>
<header class="hero">
  <canvas id="hex" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="brand"><img src="img/logo.png" alt="" width="52" height="52"><span class="mono" style="margin:0;color:var(--text)">Hex Bridge Media</span></div>
    <h1>True, strange, and <em>checked.</em></h1>
    <p class="sub">Books and short videos about the most surprising true things we could find, with the facts behind them and where to learn more. By Samuel J Hextall.</p>
    <nav class="cta"><a class="pill hot" href="#books">The books</a><a class="pill" href="#watch">The videos</a><a class="pill" href="#learn">Keep exploring</a></nav>
  </div>
  <div class="scrollcue" aria-hidden="true">SCROLL</div>
</header>
<main>
<section id="books"><div class="wrap">
  <p class="mono">Read &amp; play</p>
  <h2>Fact books and family quizzes</h2>
  <p class="lede">Every number is checked, and every book says how sure we are. Open a book for a taste of what's inside and where to find out more.</p>
  %FACT%
</div></section>
<section id="colour"><div class="wrap">
  <p class="mono">Colour</p>
  <h2>Colouring books</h2>
  <p class="lede">For kids and grown-ups. Many have a true fact on every picture.</p>
  <div class="grid">%COLOUR%</div>
</div></section>
<section id="watch"><div class="wrap">
  <p class="mono">Watch</p>
  <h2>Short cartoon science videos</h2>
  <p class="lede">A couple of minutes each, drawn and animated for the channel. Open one for the facts behind it and the sources we used.</p>
  <div class="vids">%VIDEOS%</div>
  <p style="margin-top:34px"><a class="pill hot" href="%CHANNEL%" rel="noopener" target="_blank">See the whole channel</a></p>
</div></section>
<section id="learn"><div class="wrap">
  <p class="mono">Keep exploring</p>
  <h2>Where we go to learn</h2>
  <p class="lede">Free, trustworthy places to keep finding things out, for curious kids and curious grown-ups.</p>
  <div class="learngrid">%LEARN%</div>
</div></section>
<section id="how"><div class="wrap">
  <p class="mono">How we check</p>
  <h2>Why you can trust a number here</h2>
  <div class="how">
    <div class="reveal"><b>Two sources</b><p>Every figure needs two independent sources, ideally the people who measured it: NASA, the Met Office, CERN, museums and journals.</p></div>
    <div class="reveal"><b>A second pair of eyes</b><p>Each book and video gets a separate fact audit whose only job is to find mistakes.</p></div>
    <div class="reveal"><b>Honest labels</b><p>We say whether a number was measured, estimated or argued about, and give records a date, because records get broken.</p></div>
  </div>
  <div class="stamps reveal" aria-hidden="true"><span class="stamp" style="color:#8fd18f">MEASURED</span><span class="stamp" style="color:var(--amber)">ESTIMATE</span><span class="stamp" style="color:var(--orange)">DISPUTED</span><span class="stamp" style="color:#a9c4ff">CHECKED NOV 2026</span></div>
  <p class="lede" style="margin-top:28px">Spotted something wrong? Tell us in a comment on any of the videos, and we'll fix it and say so.</p>
</div></section>
</main>
<footer><div class="wrap">Hex Bridge Media · books and videos by Samuel J Hextall · <a href="%CHANNEL%" rel="noopener">YouTube</a><br>
<span style="font-size:13px">Links to other sites open in a new tab. We're not responsible for their content, and none of them endorse us.</span></div></footer>
<script>%JS%</script>
</body>
</html>
"""

if __name__ == "__main__":
    (HERE / "img").mkdir(exist_ok=True)
    for old in (HERE / "img").glob("*.jpg"):
        old.unlink()
    # share image for links posted in chats/social
    sh = Image.new("RGB", (1200, 630), (11, 16, 38))
    for k, b in enumerate(FACT_BOOKS):
        im = Image.open(b["img"]).convert("RGB")
        im.thumbnail((260, 330))
        sh.paste(im, (60 + k * 280, 150))
    sh.save(HERE / "img/share.jpg", quality=86)
    page = (PAGE.replace("%CSS%", CSS).replace("%JS%", JS)
                .replace("%FACT%", "".join(fact_book(b) for b in FACT_BOOKS))
                .replace("%COLOUR%", "".join(colour_book(c) for c in COLOUR))
                .replace("%VIDEOS%", "".join(video(v) for v in VIDEOS))
                .replace("%LEARN%", "".join(learn(i) for i in LEARN))
                .replace("%CHANNEL%", CHANNEL))
    (HERE / "index.html").write_text(page)
    (HERE / "CNAME").write_text("hexbridgemedia.co.uk\n")
    print("built:", len(FACT_BOOKS), "fact books,", len(COLOUR), "colouring,", len(VIDEOS), "videos,", len(LEARN), "learn links")
