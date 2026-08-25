"""Build the Tom Trow 3D process deck as ONE self-contained HTML file.

Palette: coral #ED5C45 (accent only, never big backgrounds), cream #F4F3ED,
black #0E0E0E, white #FFFFFF. Poppins display / Instrument Sans body.
Approved pairings only - never white-on-cream.

Everything is inlined: fonts (woff2 base64) and the tool logos (simple-icons
single-path SVGs). No network calls at runtime, so it works offline on a call.
"""
import base64
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent

# Writes to the repo root by default, so a fresh clone builds with no edits.
# Override with: python src/build_deck.py <output.html>
if len(sys.argv) > 1:
    OUTPUTS = [pathlib.Path(sys.argv[1])]
else:
    root = HERE.parent
    OUTPUTS = [root / "order-process-deck.html", root / "index.html"]


def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode("ascii")


def icon_path(slug):
    """Pull the single path d= out of a simple-icons SVG."""
    svg = (HERE / "logos" / (slug + ".svg")).read_text(encoding="utf-8")
    m = re.search(r'<path\s+d="([^"]+)"', svg)
    if not m:
        raise SystemExit("no path in " + slug)
    return m.group(1)


REAL = ["shopify", "typeform", "clickup", "claude", "googledrive", "gmail", "n8n"]
PATHS = {s: icon_path(s) for s in REAL}

# Tools with no mark in simple-icons get an honest typographic chip, never a fake logo.
# NB: the EPS artwork does not come from Adobe. The outlines come from vehicleoutlines.co.uk.
CHIPS = {"klaviyo": "K", "shipstation": "SS", "outlines": "VO", "dvla": "VD"}

# Some simple-icons entries are full WORDMARKS, not glyphs. Squeezed into a 12px square next
# to their own name they read as a smudge, so crop the viewBox to the inked band and let the
# wordmark be its own label. Offsets are the path's real getBBox(), measured in a browser
# rather than eyeballed from the path data - guessing clipped the ascenders by ~1.1 units.
WORDMARKS = {"typeform": (9.21, 5.59)}  # bbox y=9.31 h=5.39, plus a little breathing room


def logo(slug, label):
    if slug in WORDMARKS:
        dy, h = WORDMARKS[slug]
        return ('<span class="tool wm" title="%s">'
                '<svg viewBox="0 0 24 %s" aria-hidden="true" role="img">'
                '<title>%s</title><g transform="translate(0,-%s)">'
                '<path d="%s"/></g></svg></span>'
                % (label, h, label, dy, PATHS[slug]))
    if slug in PATHS:
        return (
            '<span class="tool" title="%s">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s"/></svg>'
            '<em>%s</em></span>' % (label, PATHS[slug], label)
        )
    return ('<span class="tool" title="%s"><i class="chip">%s</i><em>%s</em></span>'
            % (label, CHIPS.get(slug, "?"), label))


def tools(*pairs):
    return '<div class="tools">' + "".join(logo(s, l) for s, l in pairs) + "</div>"


T_SHOPIFY = ("shopify", "Shopify")
T_KLAVIYO = ("klaviyo", "Klaviyo")
T_TYPEFORM = ("typeform", "Typeform")
T_CLICKUP = ("clickup", "ClickUp")
T_CLAUDE = ("claude", "Claude")
T_DRIVE = ("googledrive", "Drive")
T_GMAIL = ("gmail", "Gmail")
T_N8N = ("n8n", "n8n")
T_SHIP = ("shipstation", "ShipStation")
T_OUTLINES = ("outlines", "Vehicle Outlines")  # full domain stays in prose, not on the chip
T_DVLA = ("dvla", "Vehicle Data")

# --------------------------------------------------------------------- slides
S = []


def slide(theme, body, label=None):
    S.append((theme, body, label))


# 1 -- cover
slide("black cover", """
<div class="cover-grid">
  <div>
    <p class="wordmark">Riz</p>
    <p class="eyebrow">Engagement walkthrough</p>
    <h1>Taking the manual middle<br>out of your order process</h1>
    <p class="lede">Your orders arrive on their own and ship on their own.
      Everything in between is people. Here is what that costs you, and what
      it looks like once it isn't.</p>
  </div>
  <div class="cover-side">
    <div class="stat"><b>13</b><span>steps today</span></div>
    <div class="stat"><b>4</b><span>done by hand</span></div>
    <div class="stat coral-stat"><b>0</b><span>after</span></div>
  </div>
</div>
<p class="hint">Use <kbd>&rarr;</kbd> or click to move through &middot; <kbd>F</kbd> for fullscreen</p>
""")

# 2 -- goals
slide("cream", """
<p class="eyebrow">What we are optimising for</p>
<h2>Two questions, and nothing else</h2>
<div class="two">
  <div class="numcard">
    <span class="bignum">01</span>
    <h3>Time from order to delivery</h3>
    <p>How long a customer waits between paying and receiving their design.
      Starting with the wait nobody currently measures.</p>
  </div>
  <div class="numcard">
    <span class="bignum">02</span>
    <h3>Manual work removed</h3>
    <p>How much of each order still needs a human to move it along.
      Four steps today. Zero after, with three review points kept on purpose.</p>
  </div>
</div>
<p class="note">If a change moves neither of these, it isn't in the plan.</p>
""")

# 3 -- the stack
slide("black", """
<p class="eyebrow">Your stack today</p>
<h2>Nothing here gets removed</h2>
<p class="lede wide">Klaviyo, Typeform and ShipStation all stay exactly as they are. So does your
  print and finishing process. You never once complained about tools &mdash; you complained about
  manual work, so that is what the plan goes after.</p>
""" + tools(T_SHOPIFY, T_KLAVIYO, T_TYPEFORM, T_CLICKUP, T_CLAUDE, T_N8N, T_DRIVE, T_GMAIL,
            T_OUTLINES, T_SHIP) + """
<p class="note dim">One thing to ask rather than assume: where n8n currently sits. It&rsquo;s named in your
  brief but didn&rsquo;t appear anywhere in the walkthrough, and it changes how the integration layer
  gets built.</p>
""")

# 4 -- today's flow
slide("cream flow", """
<p class="eyebrow">How an order runs today</p>
<h2>Thirteen steps, four of them by hand</h2>
<div class="phases">
  <div class="phase">
    <h4>Order &amp; intake</h4>
    <ol start="1">
      <li>Customer orders &mdash; van, coverage, vinyl or magnetic""" + tools(T_SHOPIFY) + """</li>
      <li>Intake email with a pre-filled form link""" + tools(T_KLAVIYO) + """</li>
      <li>Customer sends photos, VIN, plate, logo, text""" + tools(T_TYPEFORM) + """</li>
    </ol>
  </div>
  <div class="phase">
    <h4>Spec &amp; file selection</h4>
    <ol start="4">
      <li class="man">Order card created<i>by hand</i>""" + tools(T_CLICKUP) + """</li>
      <li>Template files recommended""" + tools(T_CLAUDE) + """</li>
      <li class="man">Every order double-checked<i>by hand</i>""" + tools(T_CLAUDE) + """</li>
      <li class="man">Vehicle outline downloaded<i>by hand</i>""" + tools(T_OUTLINES) + """</li>
    </ol>
  </div>
  <div class="phase">
    <h4>Design &amp; approval</h4>
    <ol start="8">
      <li>Handed to a designer""" + tools(T_CLICKUP) + """</li>
      <li>Checked internally</li>
      <li>Three files plus a PDF proof sent""" + tools(T_GMAIL) + """</li>
      <li class="man">Revisions retyped and reassigned<i>by hand</i></li>
    </ol>
  </div>
  <div class="phase">
    <h4>Production &amp; dispatch</h4>
    <ol start="12">
      <li>Printed, laminated, magnetised, cut</li>
      <li>Stencils packed and posted""" + tools(T_SHIP) + """</li>
    </ol>
  </div>
</div>
""")

# 5 -- the finding
slide("black finding", """
<p class="eyebrow">What stood out</p>
<h2>Your problem isn&rsquo;t at either end</h2>
<div class="finding">
  <div class="fcol">
    <span class="ftag ok">Automatic</span>
    <p>An order <b>arrives</b> on its own.</p>
  </div>
  <div class="fcol mid">
    <span class="ftag bad">People</span>
    <p>Creating the card. Checking the file selection. Downloading the outline.
      Handling revisions.</p>
  </div>
  <div class="fcol">
    <span class="ftag ok">Automatic</span>
    <p>It <b>ships</b> on its own.</p>
  </div>
</div>
<p class="lede wide">Every one of those middle steps sits between a customer paying and a customer
  receiving &mdash; which is why time-to-design is the number that hurts. And one of them is
  <b>you, personally, on every order.</b></p>
<p class="note dim">At around $8 a design, the cost isn&rsquo;t the designer. It&rsquo;s the back and forth
  &mdash; and nothing currently counts it.</p>
""")

# 6 -- ten changes, part 1
CHANGES_A = [
    ("Waiting on the customer",
     "An order waiting on photos looks the same as one placed this morning. Nothing records how "
     "long that gap is.",
     "A state with a visible age, and a timestamp on every stage transition.",
     "Likely your largest block of order-to-design time, turned into a number instead of a "
     "feeling."),
    ("Order card", "Created by hand. Answers sit in the description as text.",
     "Builds itself. Every answer its own field, every stage its own status.",
     "Filterable data, and cycle time free from status timestamps."),
    ("Intake questions",
     "Wheelbase and rear panel asked as words. Customers don't know the trade terms, so they "
     "guess.",
     "Picture choice — two photos, tap the one that looks like your van.",
     "Turns a spec question they can't answer into a recognition task they can."),
    ("Vehicle variant", "Wheelbase asked twice, and the answer is known to be unreliable.",
     "Resolved from the registration plate, with a VIN decode behind it for your top models.",
     "A record instead of a guess, for pennies an order."),
    ("Template file list", "Two methods compared. Some \u201cconflicts\u201d are the same answer "
     "written differently.",
     "One catalogue keyed to vehicle, panel, wheelbase and variant.",
     "The false conflicts disappear, so only real uncertainty reaches a person."),
    ("Vehicle outline", "Browsed and downloaded from vehicleoutlines.co.uk, order by order.",
     "A library on Drive, built within whatever that software allows, so the right outline attaches "
     "itself.",
     "A manual step deleted outright."),
]
CHANGES_B = [
    ("Verification", "You personally check every order before a designer can start.",
     "Review fires only when the plate data and the photo disagree.",
     "You come out of the per-order loop without dropping the safety net."),
    ("Revision feedback", "Arrives as email, read and retyped by hand, reassigned manually.",
     "Decision built into the proof, and replies parsed back onto the order.",
     "The actual cost centre becomes measurable rather than absorbed."),
    ("Pack sheet", "Printed by hand. A stencil can be left out of the box.",
     "Generates itself from the order.",
     "Cheap fix for a mistake that costs a reprint and a reship."),
    ("Measurement", "None. The next efficiency is a guess.",
     "Cycle time per stage, and how much still needs a human.",
     "The thing that decides what gets built after this."),
]


def change_rows(rows, start):
    out = []
    for i, (area, today, after, buys) in enumerate(rows, start=start):
        out.append(
            '<div class="chg"><span class="chgnum">%02d</span>'
            '<div class="chgarea">%s</div>'
            '<div class="chgtoday"><span class="mini">Today</span>%s</div>'
            '<div class="chgafter"><span class="mini">After</span>%s</div>'
            '<div class="chgbuys">%s</div></div>' % (i, area, today, after, buys))
    return "".join(out)


slide("cream changes", """
<p class="eyebrow">What changes &middot; 1 of 2</p>
<h2>Ten changes, each earning its place</h2>
<div class="chgtable">""" + change_rows(CHANGES_A, 1) + "</div>")

slide("cream changes", """
<p class="eyebrow">What changes &middot; 2 of 2</p>
<h2>&nbsp;</h2>
<div class="chgtable">""" + change_rows(CHANGES_B, 7) + "</div>")

# 8 -- new flow
slide("black flow dark", """
<p class="eyebrow">The order flow you end up with</p>
<h2>Fifteen steps, none of them chores</h2>
<div class="phases">
  <div class="phase">
    <h4>Order &amp; intake</h4>
    <ol start="1">
      <li>Customer orders<i class="same">unchanged</i>""" + tools(T_SHOPIFY) + """</li>
      <li class="new">Van identified from its plate<i>new</i>""" + tools(T_DVLA) + """</li>
      <li>Brief requested, and the wait now <b>timed</b><i class="chg2">changed</i>""" + tools(T_KLAVIYO) + """</li>
      <li>Shorter brief, guesswork fields become picture choice<i class="chg2">changed</i>""" + tools(T_TYPEFORM) + """</li>
    </ol>
  </div>
  <div class="phase">
    <h4>Spec &amp; file selection</h4>
    <ol start="5">
      <li>Order card builds itself, as fields<i class="chg2">changed</i>""" + tools(T_CLICKUP) + """</li>
      <li>Template files resolved by lookup<i class="chg2">changed</i></li>
      <li>Outline attaches itself from the Drive library<i class="chg2">changed</i>""" + tools(T_DRIVE) + """</li>
      <li class="gate">Claude confirms; a person settles disputes<i>human gate</i>""" + tools(T_CLAUDE) + """</li>
    </ol>
  </div>
  <div class="phase">
    <h4>Design &amp; approval</h4>
    <ol start="9">
      <li>Designer picks it up complete<i class="chg2">changed</i>""" + tools(T_OUTLINES) + """</li>
      <li class="gate">Checked internally<i>human gate</i></li>
      <li class="gate">Proof goes out with the decision in it<i>human gate</i>""" + tools(T_GMAIL) + """</li>
      <li class="new">Feedback files itself, however it arrives<i>new</i>""" + tools(T_GMAIL) + """</li>
    </ol>
  </div>
  <div class="phase">
    <h4>Production &amp; dispatch</h4>
    <ol start="13">
      <li class="new">Pack sheet writes itself<i>new</i></li>
      <li>Printed, finished, posted<i class="same">unchanged</i>""" + tools(T_SHIP) + """</li>
      <li class="new">The process reports on itself<i>new</i>""" + tools(T_CLICKUP) + """</li>
    </ol>
  </div>
</div>
""")

# 9 -- human gates
slide("cream", """
<p class="eyebrow">Deliberately not automated</p>
<h2>Three places a person stays</h2>
<div class="three">
  <div class="gatecard">
    <span class="bignum">01</span>
    <h3>Genuine disagreement</h3>
    <p>When the plate data and the photo don&rsquo;t agree, or confidence is low, it goes to a
      person. The point isn&rsquo;t that nobody checks &mdash; it&rsquo;s that the queue gets small.</p>
  </div>
  <div class="gatecard">
    <span class="bignum">02</span>
    <h3>Internal review</h3>
    <p>Stays exactly as it is. Nothing reaches a customer that nobody has looked at.</p>
  </div>
  <div class="gatecard">
    <span class="bignum">03</span>
    <h3>Customer approval</h3>
    <p>The decision stays theirs. Approve and request-changes get easier to use, never automatic.</p>
  </div>
</div>
<p class="note">Four manual steps become zero. Three review points remain, by design.</p>
""")

# 10 -- new in the stack
slide("black", """
<p class="eyebrow">New in the stack</p>
<h2>Two additions. Nothing taken away.</h2>
<div class="two">
  <div class="card">
    """ + tools(T_DVLA) + """
    <h3>Vehicle data lookup</h3>
    <p>A DVLA and DVSA-backed registration lookup returning make, model, year, engine and body
      type. You already collect the plate, so it asks nothing new of the customer.</p>
    <div class="costs">
      <div><b>&pound;0.02</b><span>registration</span></div>
      <div><b>&pound;0.04</b><span>spec data</span></div>
      <div><b>~&pound;36</b><span>/mo at 600 orders</span></div>
    </div>
  </div>
  <div class="card">
    """ + tools(T_OUTLINES, T_DRIVE) + """
    <h3>Outline library on Drive</h3>
    <p>The outlines you actually use, stored on Drive and keyed the same way as the template
      catalogue, so the right outline attaches itself instead of someone browsing for it.</p>
    <p class="fine">Built within whatever vehicleoutlines.co.uk allows. A model not yet held is
      added once, and is then permanent, so the library fills itself in over time.</p>
  </div>
</div>
<div class="caveat">
  <span class="ctag">Confirmed against your data first</span>
  <p>Fifty of your past orders, each with its plate and the file selection you actually built, and
    we compare what the lookup returns with what was right. <b>Your orders settle it, not a
    vendor&rsquo;s documentation.</b> The cheap registration endpoint returns <b>wheelplan</b>, an
    axle description for tax purposes, <b>not</b> the wheelbase the file selection needs.</p>
</div>
""")

# 11 -- the fallback
slide("cream", """
<p class="eyebrow">If the plate doesn&rsquo;t resolve it</p>
<h2>Three things carry it instead</h2>
<div class="three">
  <div class="gatecard">
    <span class="bignum">01</span>
    <h3>Picture choice at intake</h3>
    <p>Customers get wheelbase wrong because <b>short, medium and long is trade jargon they
      don&rsquo;t know.</b> They&rsquo;re guessing. Show two photos and ask which looks like their
      van, and the guessing stops. Same for a glass or a solid rear.</p>
  </div>
  <div class="gatecard">
    <span class="bignum">02</span>
    <h3>The VIN you already collect</h3>
    <p>There&rsquo;s no reliable free decoder for European vans, but you don&rsquo;t need a
      universal one. A handful of models cover most of your orders, and each manufacturer encodes
      the body series in the VIN. A small table for your top five does the job.</p>
  </div>
  <div class="gatecard">
    <span class="bignum">03</span>
    <h3>Agreement routing</h3>
    <p>Where the customer&rsquo;s answer and the photo agree, the order moves. Where they
      disagree, a person looks. Still a far smaller queue than checking every order, which is
      what happens today.</p>
  </div>
</div>
<p class="note"><b>Nothing else in the plan depends on the lookup.</b> The template catalogue is
  what takes you out of checking every order, and it&rsquo;s entirely independent of it.</p>
""")

# 11 -- order of work
slide("cream", """
<p class="eyebrow">Order of work</p>
<h2>The time savings land first</h2>
<div class="steps">
  <div class="stepcard"><b>01</b><h4>Order card populates itself</h4>
    <p>Details as proper fields. Unblocks everything downstream and starts the clock.</p></div>
  <div class="stepcard"><b>02</b><h4>Waiting time made visible</h4>
    <p>The wait on each order becomes a number. Cheapest fix against the biggest delay.</p></div>
  <div class="stepcard"><b>03</b><h4>Catalogue and Drive outline library</h4>
    <p>The foundation. Kills the phantom conflicts so verification can narrow.</p></div>
  <div class="stepcard"><b>04</b><h4>Plate lookup, confirmed first</h4>
    <p>Fifty of your past orders decide how much of the variant question survives.</p></div>
  <div class="stepcard"><b>05</b><h4>Proof approval and parsed feedback</h4>
    <p>Turns the real cost centre into something with numbers attached.</p></div>
  <div class="stepcard"><b>06</b><h4>Measurement, then mock-ups</h4>
    <p>Last on purpose. Once revisions are measured, we&rsquo;ll know if mock-ups prevent them.</p></div>
</div>
""")

# 12 -- what you have
slide("black", """
<p class="eyebrow">What you have at the end</p>
<h2>Owned by you, not by me</h2>
<ul class="end">
  <li>The ten changes built and live, as corrected in week one.</li>
  <li>A canonical template catalogue and a stored outline library, both yours.</li>
  <li>A written answer on the plate lookup &mdash; what it resolves, what it doesn&rsquo;t, and the fallback.</li>
  <li>Structured revision capture through both routes, with a watched queue for anything unmatched.</li>
  <li>Cycle-time reporting: stage durations, waiting time, revisions per order and their causes.</li>
  <li>A one-page runbook per automation &mdash; what it does, what it touches, who owns it.</li>
  <li>A sized backlog of everything not built inside the first three months.</li>
  <li>An assessment of how much of this the second brand can inherit directly.</li>
  <li>The mock-up question answered with data rather than opinion.</li>
</ul>
""")

# 13 -- close
slide("black cover close", """
<div class="closing">
  <p class="wordmark">Riz</p>
  <h1>Where you end up</h1>
  <div class="closestats">
    <div class="stat"><b>4&rarr;0</b><span>manual steps</span></div>
    <div class="stat"><b>3</b><span>human gates, by design</span></div>
    <div class="stat"><b>0</b><span>tools removed</span></div>
  </div>
  <p class="lede">Out of the middle of your own process, and looking at the numbers instead.</p>
</div>
""")

# --------------------------------------------------------------------- assemble
slides_html = []
for i, (theme, body, _label) in enumerate(S):
    slides_html.append(
        '<section class="slide %s" data-i="%d" aria-hidden="%s">'
        '<div class="inner">%s</div>'
        '<footer class="sfoot"><span>Tom Trow</span>'
        '<span class="pg">%02d / %02d</span></footer>'
        '</section>' % (theme, i, "false" if i == 0 else "true", body, i + 1, len(S)))

TEMPLATE = (HERE / "deck_template.html").read_text(encoding="utf-8")
html = (TEMPLATE
        .replace("{{SLIDES}}", "\n".join(slides_html))
        .replace("{{COUNT}}", str(len(S)))
        .replace("{{POPPINS600}}", b64(HERE / "fonts" / "poppins-600.woff2"))
        .replace("{{POPPINS700}}", b64(HERE / "fonts" / "poppins-700.woff2"))
        .replace("{{INSTRUMENT}}", b64(HERE / "fonts" / "instrument-var.woff2")))

for out in OUTPUTS:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out)
print("slides:", len(S), "| size:", round(len(html.encode()) / 1024), "KB")
print("real marks:", ", ".join(sorted(PATHS)))
print("typographic chips:", ", ".join(sorted(CHIPS)))
