"""Build index.html for the GH-Pages post, in the plvch design system.
Reuses the exact CSS + theme-toggle JS from indexes_cost/post/index.html
(same design language), fills in our post, and rebuilds the two charts as
inline .lc-svg / table figures using the plvch tokens (navy/forest/ochre).
Run from this folder: python3 build_site.py  ->  index.html
"""
import csv, re

REF = "/Users/mplvch/Documents/claude_projects/indexes_cost/post/index.html"
ref = open(REF).read()
REF_CSS = re.search(r"<style>(.*?)</style>", ref, re.S).group(1)
REF_JS = re.findall(r"<script>(.*?)</script>", ref, re.S)[-1]

# ---------- data ----------
def lorenz(sub):
    return sorted((float(r["cum_share_units"]), float(r["cum_share_amount"]))
                  for r in csv.DictReader(open("data/gini.csv")) if sub in r["dataset"])
CORP, PERS = lorenz("turnover"), lorenz("income")
EUGINI = sorted(((r["country"], r["geo"], float(r["turnover_gini_5band_2023"]))
                 for r in csv.DictReader(open("data/eurostat_turnover_gini.csv"))), key=lambda x: -x[2])
HHI = [("Slovakia",2.50),("Switzerland",1.21),("Czechia",0.80),("Netherlands",0.78),
       ("Finland",0.73),("Germany",0.62),("France",0.20),("Italy",0.13)]

# ---------- chart css (plain string; uses reused tokens) ----------
CHART_CSS = """
.lc-svg .axis-line{stroke:var(--oi-rule-strong);stroke-width:1.1}
.lc-svg .cnum{font-family:var(--font-display);font-weight:600;font-size:23px;fill:var(--oi-ink-1)}
.lc-svg .clab{font-family:var(--font-display);font-size:11px;letter-spacing:.1em;text-transform:uppercase;fill:var(--oi-ink-3)}
.lc-svg .lbl{font-weight:600;font-size:13px;font-family:var(--font-display)}
.lc-svg .t-med{fill:var(--oi-brand)}.lc-svg .t-aw{fill:var(--oi-brand-2)}
.lc-svg .eqlab{fill:var(--oi-ink-3);font-family:var(--font-display);font-size:11px}
.fig-legend{display:flex;gap:22px;flex-wrap:wrap;font-size:12px;color:var(--oi-ink-3);margin:0 0 6px}
.fig-legend span{display:inline-flex;align-items:center;gap:7px}
.fig-legend i{width:22px;height:3px;border-radius:2px;display:inline-block}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:2px}
@media(max-width:640px){.duo{grid-template-columns:1fr;gap:30px}}
.duo h4{font-family:var(--font-display);font-size:15px;margin:0 0 4px;color:var(--oi-ink-1)}
.duo .ex{font-size:12.5px;color:var(--oi-ink-3);line-height:1.45;margin:0 0 14px;min-height:36px}
table.mini{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:14px}
table.mini th{text-align:right;border-bottom:1.5px solid var(--oi-rule-strong);padding:6px 6px;font-family:var(--font-display);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--oi-ink-3)}
table.mini th:first-child{text-align:left}
table.mini td{text-align:right;padding:6px 6px;border-bottom:1px solid var(--oi-rule);color:var(--oi-ink-2)}
table.mini td:first-child{text-align:left}
table.mini tr.de td{background:var(--oi-highlight);color:var(--oi-ink-1);font-weight:600}
.gbar{display:grid;grid-template-columns:92px 1fr 36px;gap:9px;align-items:center;margin:6px 0;font-size:13px}
.gbar .gl{text-align:right;color:var(--oi-ink-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gbar .gt{background:var(--oi-surface-sunk);border-radius:2px;height:15px;overflow:hidden}
.gbar .gf{height:100%;background:var(--oi-brand-2);border-radius:2px}
.gbar.de .gf{background:var(--oi-accent)}
.gbar.de .gl{color:var(--oi-ink-1);font-weight:600}.gbar .gv{color:var(--oi-ink-2)}
.gbar.head{border-bottom:1.5px solid var(--oi-rule-strong);padding-bottom:6px;margin-bottom:6px;font-family:var(--font-display);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--oi-ink-3)}
"""

def lorenz_svg():
    M, P = 72, 356
    y0 = M + P
    px = lambda u: M + u*P
    py = lambda a: (M+P) - a*P
    pl = lambda pts: " ".join(f"{px(u):.1f},{py(a):.1f}" for u, a in pts)
    grid = "".join(
        f'<line class="grid" x1="{px(t):.1f}" y1="{M}" x2="{px(t):.1f}" y2="{y0}"/>'
        f'<line class="grid" x1="{M}" y1="{py(t):.1f}" x2="{px(1):.1f}" y2="{py(t):.1f}"/>'
        for t in (.25,.5,.75))
    co = [("Bottom 72% of firms (under €100k)", "1.2% of turnover"),
          ("Top 1% of firms", "≈ 80% of turnover"),
          ("Top 3,190 firms — 0.04%", "51.5% of turnover")]
    cx, cy0 = 545, 132
    callouts = "".join(
        f'<text class="clab" x="{cx}" y="{cy0+i*96}">{l}</text>'
        f'<text class="cnum" x="{cx}" y="{cy0+i*96+33}">{v}</text>' for i,(l,v) in enumerate(co))
    return f'''<svg class="lc-svg" viewBox="0 0 880 470" role="img" aria-label="Lorenz curves: corporate turnover vs personal income">
      {grid}
      <line class="l-ew" x1="{M}" y1="{y0}" x2="{px(1):.1f}" y2="{py(1):.1f}"/>
      <polyline class="l-aw" points="{pl(PERS)}"/>
      <polyline class="l-med" points="{pl(CORP)}"/>
      <line class="axis-line" x1="{M}" y1="{M}" x2="{M}" y2="{y0}"/>
      <line class="axis-line" x1="{M}" y1="{y0}" x2="{px(1):.1f}" y2="{y0}"/>
      <text class="axis" x="{px(.5):.0f}" y="{y0+32}" text-anchor="middle">share of businesses / people →</text>
      <text class="axis" x="{M-28}" y="{py(.5):.0f}" text-anchor="middle" transform="rotate(-90 {M-28} {py(.5):.0f})">share of turnover / income →</text>
      <text class="lbl t-med" x="{px(.46):.0f}" y="{py(.20):.0f}">Corporate turnover · Gini 0.96</text>
      <text class="lbl t-aw" x="{px(.05):.0f}" y="{py(.50):.0f}">Personal income · Gini 0.49</text>
      <text class="eqlab" x="{px(.78):.0f}" y="{py(.88):.0f}">equality</text>
      {callouts}
    </svg>'''

def fig2_body():
    hhi = "".join(
        f'<tr class="{"de" if c=="Germany" else ""}"><td>{c}</td><td>{h:.2f}</td></tr>'
        for c, h in HHI)
    vmax = max(g for _,_,g in EUGINI)
    bars = '<div class="gbar head"><div class="gl">Country</div><div></div><div class="gv">Gini</div></div>'
    bars += "".join(
        f'<div class="gbar {"de" if geo=="DE" else ""}"><div class="gl">{c}</div>'
        f'<div class="gt"><div class="gf" style="width:{100*g/vmax:.1f}%"></div></div>'
        f'<div class="gv">{g:.2f}</div></div>' for c,geo,g in EUGINI[:10])
    return f'''<div class="duo">
      <div>
        <h4>Market dominance — HHI ×100</h4>
        <p class="ex">How much a market is run by its biggest players. Higher = more concentrated. Selected of 15 countries.</p>
        <table class="mini"><tr><th>Country</th><th>HHI ×100</th></tr>{hhi}</table>
      </div>
      <div>
        <h4>Turnover spread — Gini</h4>
        <p class="ex">How unevenly turnover is split across firms, 0 (even) to 1 (all in one). Top 10 of 34.</p>
        {bars}
      </div>
    </div>'''

# ---------- page ----------
MAST = '''<header class="masthead"><div class="masthead-inner">
  <a class="wordmark" href="https://plvch.github.io/">plvch</a>
  <div class="mh-meta">
    <span class="hide-sm">Note · Germany</span><span>2026</span>
    <span class="theme-toggle">
      <button data-theme-btn="light" class="active" aria-pressed="true">Light</button>
      <button data-theme-btn="dark" aria-pressed="false">Dark</button>
    </span>
  </div>
</div></header>'''

COVER = '''<section class="cover col">
  <div class="eyebrow brand">Note · Small business</div>
  <h1>It's rational to ignore small business</h1>
  <p class="standfirst">Europe is rushing to make company formation easier. The numbers say the
  neglect was rational — and point somewhere unexpected for a fix.</p>
  <div class="byline">
    <div><div class="k">Author</div><div class="v">plvch</div></div>
    <div><div class="k">Published</div><div class="v">June 2026</div></div>
    <div><div class="k">Reading</div><div class="v">3 min</div></div>
    <div><div class="k">Data</div><div class="v">Destatis · Eurostat</div></div>
  </div>
</section>'''

def p(t): return f'<p>{t}</p>'
def srule(n, t): return f'<div class="section-rule col"><div class="n">{n}</div><div class="t">{t}</div></div>'

INTRO = f'''<section class="essay"><div class="col">
  {p("Europe is full of good initiatives right now to make starting a company easier. Good timing, given the viral notes about sitting through (and paying for) a 12-hour notary appointment in Germany to register a GmbH.")}
  {p("But I think a lot of the policy-versus-bureaucracy frustration is just a misunderstanding. Fiscally, ignoring small business is reasonable.")}
</div></section>'''

SEC1 = f'''{srule("01","The concentration")}
<section class="essay"><div class="col">
  {p("Micro firms aren't rare. Germany has around 7&nbsp;million VAT-registered businesses, and about 5&nbsp;million of them turn over less than €100k a year. Those 5&nbsp;million together make 1.2% of all turnover. The top 1% of firms make roughly 80%. Just 3,190 companies, 0.04% of the total, book more than half. Tax and social revenue track the same curve, by proxy.")}
</div>
<figure class="fig col-wide">
  <div class="fig-head"><div><div class="fig-num">Figure 1</div>
    <div class="fig-title">A few firms hold almost all the turnover</div></div>
    <div class="fig-source">Germany · 2021</div></div>
  <div class="fig-body">
    <div class="fig-legend">
      <span><i style="background:var(--oi-brand)"></i>corporate turnover</span>
      <span><i style="background:var(--oi-brand-2)"></i>personal income</span>
      <span><i style="background:var(--oi-ink-3)"></i>perfect equality</span>
    </div>
    {lorenz_svg()}
  </div>
  <figcaption>VAT-registered businesses sorted smallest to largest. Lorenz curves from Destatis
  Umsatzsteuerstatistik (73321) and Lohn- u. Einkommensteuerstatistik (73111). The corporate Gini
  (~0.96) is a grouped estimate; personal income is Gesamtbetrag der Einkünfte, pre-tax — not the
  household disposable Gini (~0.28).</figcaption>
</figure>
<div class="col">
  {p("Nothing on the personal side comes close. The corporate turnover Gini sits near 0.96; personal income is around 0.5. That's less a verdict on big firms than a map of where the money sits.")}
</div></section>'''

SEC2 = f'''{srule("02","Even by European standards")}
<section class="essay">
<figure class="fig col-wide">
  <div class="fig-head"><div><div class="fig-num">Figure 2</div>
    <div class="fig-title">Concentrated even by European standards</div></div>
    <div class="fig-source">Germany vs Europe</div></div>
  <div class="fig-body">{fig2_body()}</div>
  <figcaption>Germany is #1 on the turnover Gini but 6th on HHI — different metrics. Its turnover sits
  in large, efficient firms (low markups), not monopolies. Sources: IWH/CompNet (2021); Eurostat SBS (2023).</figcaption>
</figure>
<div class="col">
  {p("And Germany isn't middling here. On both common measures of corporate concentration it sits at or near the top, above France, Italy and Spain. So the neglect makes sense. If the small end is a rounding error in the base, leaving founders to the notary and the forms is the rational call. The concentration is hard, and it's set at the level of the whole economy.")}
</div></section>'''

SEC3 = f'''{srule("03","What would change it")}
<section class="essay"><div class="col">
  {p("This is where I keep coming back to Christensen. The prescription is to back the seemingly irrational low end early. Inside a company that happens because someone at the top believes in it and shields the bet. A state has no one in that chair, and tax revenue won't supply the reason: the payoff, if it lands, is decades out and credited to no one in office.")}
  {p("So maybe the move isn't more incentives. It's letting some risk into the system. American VC really took off once pension funds were allowed in, around 1979. Here that capital is still mostly steered away from risk. University spin-outs are the other obvious source, and they need endowments and funding rules that barely exist. None of that needs the state to pick winners or write cheques. Just looser rules on where existing capital can go.")}
  {p("Where the risk capital actually comes from, I haven't worked out. Pension reform seems like the obvious first move. I'm less sure what comes after.")}
</div></section>'''

FOOT = '''<footer class="essay-foot col-wide">
  <p>Data and code: Destatis (Umsatzsteuer-, Lohn-/Einkommensteuer-, Gewerbeanzeigen-, Unternehmensregister-Statistik),
  Eurostat (SBS, business demography, SILC), IWH/CompNet. Figures rebuilt from the published source tables.</p>
</footer>'''

DOC = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>It's rational to ignore small business — plvch</title>
<meta name="description" content="Germany barely taxes its small businesses. The data says the neglect was rational — and points somewhere unexpected for a fix."/>
<link rel="stylesheet" href="assets/plvch-tokens.css"/>
<style>{REF_CSS}
/* ---- chart additions ---- */
{CHART_CSS}</style>
</head>
<body>
{MAST}
<main class="wrap">
{COVER}
{INTRO}
{SEC1}
{SEC2}
{SEC3}
{FOOT}
</main>
<script>{REF_JS}</script>
</body>
</html>'''

open("index.html","w").write(DOC)
print(f"wrote index.html ({len(DOC):,} bytes) | reused CSS {len(REF_CSS):,} chars, JS {len(REF_JS):,} chars")
