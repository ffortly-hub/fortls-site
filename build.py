#!/usr/bin/env python3
"""FORTLS.com static site generator.  Run: python3 build.py   -> writes ./site
Edit the CONFIG block, rebuild, commit. Deploy dir for Cloudflare Pages: site"""
import os, shutil, json
from PIL import Image, ImageDraw, ImageFont

# ---------------- CONFIG ----------------
DOM = "https://fortls.com"
NEWS = "https://fortls.beehiiv.com"
BMC = "https://buymeacoffee.com/fortls"
CLARITY = "zbdjwrsl12"
GTM = "GTM-P54LMMLJ"
GA4 = "G-1X1ZLKFJ9S"
GA4_DIRECT = "false"  # set "true" ONLY if the GTM container has no GA4 tag (see README)
UPDATED = "2026-11-22"
OUT = "site"
# affiliate redirects: replace the URL with your referral URL once approved (kept as plain homepages = no commission, no risk)
GO = {"cloudways": "https://www.cloudways.com/en/?id=2226421", "vultr": "https://www.vultr.com/?ref=9934870",
      "beehiiv": "https://fortls.beehiiv.com", "github-sponsors": "https://github.com/sponsors/FORTLS-HUB",
      "kofi": "https://ko-fi.com/fortls", "paypal": "https://www.paypal.com/paypalme/fortls",
      "afternic": "https://www.godaddy.com/en/domainsearch/find?premiumOnly=true&domainToCheck=fortls.com"}
# ----------------------------------------

def w(p, s, mode="w"):
    p = os.path.join(OUT, p); os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, mode, encoding="utf-8").write(s)

NAV = '<a href="/blog">Blog</a><a href="/tools">Tools</a><a href="/resources">Resources</a><a href="/downloads">Downloads</a><a href="/newsletter">Newsletter</a><a href="/support">Support</a><a href="/acquisition">For sale</a>'
HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>@T@</title><meta name="description" content="@D@">@R@<meta name="theme-color" content="#0d1117">
<link rel="canonical" href="@U@">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website"><meta property="og:site_name" content="FORTLS"><meta property="og:title" content="@T@"><meta property="og:description" content="@D@"><meta property="og:url" content="@U@"><meta property="og:image" content="@DOM@/og-image.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="@T@"><meta name="twitter:description" content="@D@"><meta name="twitter:image" content="@DOM@/og-image.png">
<link rel="alternate" type="application/rss+xml" title="FORTLS" href="/feed.xml"><link rel="stylesheet" href="/assets/css/site.css">@X@<script src="/assets/js/site.js" defer></script></head>
<body><div class="topline">FORTLS.com is available for acquisition. <a href="/acquisition">Details</a></div>
<header><div class="wrap nav"><a class="brand" href="/" aria-label="FORTLS home"><img src="/logo-horizontal.svg" alt="FORTLS" width="150" height="38"></a><nav aria-label="Main">@N@</nav></div></header>
'''
FOOT = '''<footer><div class="wrap foot"><div><strong>FORTLS</strong><p>Independent, free resources and tools for Fortran developers.</p>
<small>FORTLS is an independent community resource. It is not the official fortls project and is not affiliated with the fortls maintainers or the Fortran-lang organization. Product and project names belong to their owners.</small></div>
<div class="footlinks"><a href="/about">About</a><a href="/faq">FAQ</a><a href="/contact">Contact</a><a href="/partners">Partners</a><a href="/sponsors">Sponsors</a><a href="/status">Status</a><a href="/changelog">Changelog</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/resources#disclosure">Affiliate disclosure</a><a href="#" id="cs">Privacy choices</a><a class="star" href="https://github.com/FORTLS-HUB" target="_blank" rel="noopener"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>Star us on GitHub</a></div></div></footer></body></html>'''

def WP(u, t, d):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebPage", "@id": u, "url": u, "name": t, "description": d, "isPartOf": {"@type": "WebSite", "name": "FORTLS", "url": DOM + "/"}}) + '</script>'
PAGES = []
def page(slug, title, desc, body, extra="", noindex=False):
    url = DOM + ("/" if slug == "index" else "/" + slug)
    h = HEAD
    for k, v in {"@T@": title, "@D@": desc, "@U@": url, "@DOM@": DOM, "@N@": NAV, "@X@": extra + ("" if noindex else WP(url, title, desc)),
                 "@R@": '<meta name="robots" content="noindex">' if noindex else ""}.items():
        h = h.replace(k, v)
    w(slug + ".html", h + body + FOOT)
    if not noindex: PAGES.append(url)

def main_(s): return '<main class="wrap page">' + s + '</main>'
def aff(k, label): return f'<a href="/go/{k}" rel="sponsored nofollow noopener" target="_blank">{label}</a>'


GH="https://github.com/FORTLS-HUB"
SOC=[("GitHub",GH),("LinkedIn","https://www.linkedin.com/in/fortls/"),("YouTube","https://www.youtube.com/@FORTLSHUB"),("X","https://x.com/FORTLSHUB"),("Bluesky","https://bsky.app/profile/fortls.bsky.social"),("Reddit","https://www.reddit.com/user/FORTLSHUB/")]
def ext(u,l,c=""): return f'<a class="btn {c}" href="{u}" target="_blank" rel="noopener noreferrer">{l}</a>'
def go(k,l,c=""): return f'<a class="btn {c}" href="/go/{k}" target="_blank" rel="noopener">{l}</a>'
ICO={'heart': '<path fill="currentColor" stroke="none" d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.58 20.58 0 0 0 8 13.393a20.58 20.58 0 0 0 3.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.749.749 0 0 1-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5Z"/>', 'cup': '<path d="M2 4h9v5a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V4Zm9 1h1.5a1.5 1.5 0 0 1 0 3H11"/>', 'card': '<rect x="1.5" y="3.5" width="13" height="9" rx="1.5"/><path d="M1.5 6.5h13"/>', 'mail': '<rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="m2 4 6 5 6-5"/>'}
def ic(k): return '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'+ICO[k]+'</svg>'
NL = '<section class="wrap section"><div class="callout" data-placement="newsletter-callout"><h2>Join the FORTLS Newsletter</h2><p>Receive tutorials, development guides, tooling resources, release updates, and future downloads.</p>' + go("beehiiv","Subscribe Free") + '<p class="muted">Subscription is handled by beehiiv; see our <a href="/privacy">privacy policy</a>.</p></div></section>'
COMM = '<section id="community" class="section"><h2>Community</h2><p class="lead">Find FORTLS elsewhere.</p><p>' + ext(DOM,"Website","secondary") + " ".join(ext(u,l,"secondary") for l,u in SOC) + '</p></section>'
SUPBTN = '<p data-placement="support-page">' + go("github-sponsors","GitHub Sponsors ↗") + " " + go("kofi","Ko-fi ↗","secondary") + " " + go("paypal","PayPal ↗","secondary") + '</p>'
SUPPORT_BOX = '<section class="wrap section"><aside class="fortls-support-box" data-placement="support-box" aria-label="Support FORTLS"><h2>Help keep FORTLS free</h2><p>FORTLS is independently maintained. Support helps fund tools, documentation, educational resources, and future development.</p><p class="sb-row">' + go("github-sponsors", ic("heart")+"GitHub Sponsors") + go("kofi", ic("cup")+"Ko-fi","secondary") + go("paypal", ic("card")+"PayPal","secondary") + go("beehiiv", ic("mail")+"Newsletter","secondary") + '</p><p class="muted"><strong>Related resources:</strong> <a href="/tools">Tools</a> · <a href="/downloads">Downloads</a> · <a href="/blog">Blog</a> · <a href="/faq">FAQ</a></p></aside></section>'
# content registry (newest first): (date, title, url, description) - drives home block and feed.xml
POSTS=[("2026-11-15","Installing fortls in VS Code","/blog/install-fortls-vscode","Python, fortls, the Modern Fortran extension, configuration and troubleshooting."),("2026-11-15","What is fortls?","/blog/what-is-fortls","The Language Server Protocol, why it matters, supported editors and a typical workflow.")]
TOOLREL=[("2026-11-15","VS Code settings generator","/tools#vscode","Generate Modern Fortran extension settings in your browser."),("2026-11-15","fortls validator","/tools#check","Check a .fortls file for syntax errors and unrecognised keys."),("2026-11-15","Advanced .fortls generator","/tools#fortls","Generate a .fortls configuration file."),("2026-11-15","fpm.toml generator","/tools#fpm","Create a starter Fortran Package Manager manifest.")]
DLS=[("2026-11-15","Modern Fortran Developer Cheat Sheet & Quick Start Guide","/downloads/fortran-developer-quick-reference.pdf","Two-page guide: arrays, modules, type-bound procedures, fpm and the fortls workflow.")]
ISSUES=[]  # add newsletter issues here: (date, title, beehiiv_url, description) - newest first
def latest():
    c=lambda tag,it,lab:f'<article class="card"><span class="tag">{tag}</span><h3>{it[1]}</h3><p>{it[3]}</p><a href="{it[2]}">{lab} →</a></article>'
    n=c("Latest Newsletter",ISSUES[0],"Read") if ISSUES else '<article class="card"><span class="tag">Latest Newsletter</span><h3>Newsletter archive</h3><p>Issues are listed in the archive as they are published.</p><a href="/newsletter/archive">Open archive →</a></article>'
    return '<section class="section"><h2>Latest activity</h2><div class="grid">'+c("Latest Article",POSTS[0],"Read")+c("Latest Tool",TOOLREL[0],"Open")+c("Latest Download",DLS[0],"Download")+n+'</div></section>'
LATEST=latest()

# ---------- pages ----------
JSONLD = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "name": "FORTLS", "url": DOM + "/", "description": "Independent free resources and browser-based tools for Fortran developers."},
    {"@type": "Organization", "name": "FORTLS", "url": DOM + "/", "logo": DOM + "/logo.png", "sameAs": [u for _, u in SOC]}]}) + '</script>'
page("index", "FORTLS — Free tools and resources for Fortran developers",
     "Free browser-based tools and curated resources for Fortran developers and the Fortran Language Server (fortls) ecosystem.",
     '''<section class="hero wrap"><div class="eyebrow">Fortran • Developer tooling • Scientific computing</div><h1>Free tools for Fortran developers.</h1>
<p>Generate and check fortls configuration, create an fpm manifest, and find trusted learning and tooling resources. Everything runs in your browser — nothing is uploaded.</p>
<div class="actions"><a class="btn" href="/tools">Open the free tools</a><a class="btn secondary" href="/resources">Browse resources</a></div></section>
<main class="wrap"><section class="section"><h2>What you’ll find here</h2><div class="grid">
<article class="card"><span class="tag">Tool</span><h3>.fortls generator</h3><p>Pick options, get a ready-to-use configuration file.</p><a href="/tools#fortls">Open →</a></article>
<article class="card"><span class="tag">Tool</span><h3>fortls validator</h3><p>Check a config for syntax errors and unrecognised keys.</p><a href="/tools#check">Open →</a></article>
<article class="card"><span class="tag">Tool</span><h3>fpm.toml generator</h3><p>Start a Fortran Package Manager project manifest.</p><a href="/tools#fpm">Open →</a></article>
<article class="card"><span class="tag">Tool</span><h3>VS Code settings</h3><p>Generate Modern Fortran extension settings.</p><a href="/tools#vscode">Open →</a></article>
<article class="card"><span class="tag">Download</span><h3>Quick reference (PDF)</h3><p>A free two-page modern Fortran cheat sheet and quick start guide.</p><a href="/downloads/fortran-developer-quick-reference.pdf">Download →</a></article>
</div></section>
@LATEST@<section class="section"><h2>Free, and kept running by the community</h2><p class="lead">The tools are free. Hosting is covered by voluntary support and clearly labelled affiliate links.</p>
<p><a class="btn secondary" href="/support">Support the project</a> <a class="btn secondary" href="/newsletter">Newsletter</a></p></section>
@NLCOMM@<section class="section"><div class="callout"><strong>FORTLS.com is for sale.</strong><p class="muted">A short .com domain connected to Fortran tooling, with the option to continue this resource hub.</p><a href="/acquisition">Acquisition information →</a></div></section></main>'''.replace('@NLCOMM@', NL + COMM).replace('@LATEST@', LATEST), JSONLD)

page("resources", "Fortran & fortls resources — FORTLS", "Curated official links for fortls, Fortran learning, compilers, build tools, plus labelled hosting partners.",
 main_('''<div class="eyebrow">Reference library</div><h1>Fortran ecosystem resources</h1>
<p class="lead">Links go to their official maintainers. This list is informational and not an endorsement; check current compatibility and licences yourself.</p>
<h2>fortls and editors</h2><ul>
<li><a href="https://github.com/fortran-lang/fortls" target="_blank" rel="noopener noreferrer">fortls — official repository</a></li>
<li><a href="https://fortls.fortran-lang.org/" target="_blank" rel="noopener noreferrer">fortls documentation</a></li>
<li><a href="https://pypi.org/project/fortls/" target="_blank" rel="noopener noreferrer">fortls on PyPI</a></li>
<li><a href="https://marketplace.visualstudio.com/items?itemName=fortran-lang.linter-gfortran" target="_blank" rel="noopener noreferrer">Modern Fortran extension for VS Code</a></li>
<li><a href="https://github.com/neovim/nvim-lspconfig" target="_blank" rel="noopener noreferrer">nvim-lspconfig (Neovim)</a></li>
<li><a href="https://microsoft.github.io/language-server-protocol/" target="_blank" rel="noopener noreferrer">Language Server Protocol specification</a></li></ul>
<h2>Learn and build</h2><ul>
<li><a href="https://fortran-lang.org/" target="_blank" rel="noopener noreferrer">Fortran-lang community</a> · <a href="https://fortran-lang.org/learn/" target="_blank" rel="noopener noreferrer">Learn</a></li>
<li><a href="https://fpm.fortran-lang.org/" target="_blank" rel="noopener noreferrer">Fortran Package Manager (fpm)</a></li>
<li><a href="https://stdlib.fortran-lang.org/" target="_blank" rel="noopener noreferrer">Fortran standard library (stdlib)</a></li>
<li><a href="https://fortran-lang.discourse.group/" target="_blank" rel="noopener noreferrer">Fortran Discourse forum</a></li></ul>
<h2>Compilers</h2><ul><li><a href="https://gcc.gnu.org/fortran/" target="_blank" rel="noopener noreferrer">GNU Fortran (gfortran)</a></li>
<li><a href="https://www.intel.com/content/www/us/en/developer/tools/oneapi/fortran-compiler.html" target="_blank" rel="noopener noreferrer">Intel Fortran Compiler</a></li></ul>
<h2>Free download</h2><ul><li><a href="/downloads/fortran-developer-quick-reference.pdf">Modern Fortran developer quick reference (PDF)</a></li></ul>
<h2 id="disclosure">Hosting &amp; domain partners</h2>
<p class="notice"><strong>Affiliate disclosure:</strong> links to Cloudways and Vultr are affiliate links. If you sign up through them, FORTLS may earn a commission at no extra cost to you. The other providers below are editorial references only and are not affiliate links. We have not tested every service; verify pricing and terms on the provider’s site.</p>
<h3>Affiliate partners</h3><ul><li>''' + aff("vultr", "Vultr — cloud compute") + '</li><li>' + aff("cloudways", "Cloudways — managed cloud hosting") + '''</li></ul>
<h3>Editorial references (not affiliate links)</h3><ul><li><a href="https://www.digitalocean.com/" target="_blank" rel="noopener">DigitalOcean — cloud servers</a></li><li><a href="https://www.hostinger.com/" target="_blank" rel="noopener">Hostinger — web hosting</a></li><li><a href="https://www.namecheap.com/" target="_blank" rel="noopener">Namecheap — domains</a></li></ul>'''))

TOOLS = '''<div class="eyebrow">Free browser tools</div><h1>Fortran developer tools</h1>
<p class="lead">All tools run locally in your browser. Nothing is sent to a server. Outputs are starting points: review them against the official documentation for your versions.</p>
<section id="fortls" class="tool"><h2>Advanced .fortls generator</h2><p class="muted">Only options you enable are written. Leave blank to use fortls defaults. One path per line (or comma-separated).</p>
<div class="cols"><div>
<label>source_dirs<textarea id="g-src" rows="2" placeholder="src/**"></textarea></label>
<label>ext_source_dirs<textarea id="g-ext" rows="1"></textarea></label>
<label>excl_paths<textarea id="g-exp" rows="1" placeholder="build"></textarea></label>
<label>excl_suffixes<textarea id="g-exs" rows="1"></textarea></label>
<label>include_dirs<textarea id="g-inc" rows="1"></textarea></label>
<label>Project size (suggested thread count, adjust to your machine)<select id="g-size"><option value="">Default</option><option value="2">Small</option><option value="4">Medium</option><option value="8">Large</option></select></label>@CHK@</div><div><label>Output<textarea id="g-out" rows="16" readonly spellcheck="false"></textarea></label>
<button data-copy="g-out">Copy</button><button class="alt" data-dl="g-out" data-name=".fortls">Download .fortls</button><output class="ok" id="g-st"></output></div></div></section>
<section id="check" class="tool"><h2>fortls validator</h2><p class="muted">Paste a config. Comments (JSONC) are accepted. Checks syntax, key names and value types against options known to this tool — not full semantics.</p>
<textarea id="l-in" rows="9" spellcheck="false" placeholder='{ "source_dirs": ["src"] }'></textarea><button id="l-go">Check</button><button class="alt" id="l-fmt">Format (removes comments)</button><output id="l-out" style="white-space:pre-wrap"></output></section>
<section id="fpm" class="tool"><h2>fpm.toml generator</h2><p class="muted">Creates a starter manifest for the Fortran Package Manager.</p>
<div class="cols"><div><label>name<input id="f-name" value="my_project"></label><label>version<input id="f-ver" value="0.1.0"></label><label>license<input id="f-lic" value="MIT"></label><label>author<input id="f-au"></label><label>maintainer<input id="f-mt"></label>
<label>dependencies (one per line: <code>name</code> or <code>name git-url</code>)<textarea id="f-dep" rows="3" placeholder="stdlib https://github.com/fortran-lang/stdlib"></textarea></label>
<div class="chk"><label><input type="checkbox" id="f-ae" checked> auto-executables</label><label><input type="checkbox" id="f-at" checked> auto-tests</label><label><input type="checkbox" id="f-ax" checked> auto-examples</label><label><input type="checkbox" id="f-lib"> install library</label></div></div>
<div><label>Output<textarea id="f-out" rows="16" readonly spellcheck="false"></textarea></label><button data-copy="f-out">Copy</button><button class="alt" data-dl="f-out" data-name="fpm.toml">Download fpm.toml</button></div></div></section>
<section id="vscode" class="tool"><h2>VS Code settings generator</h2><p class="muted">Creates settings for the Modern Fortran extension. Paste the result into <code>.vscode/settings.json</code>, merging with existing settings.</p>
<div class="cols"><div><label>fortran.fortls.path<input id="v-path" value="fortls"></label>
<label>fortran.linter.compiler<select id="v-cc"><option>gfortran</option><option>ifx</option><option>ifort</option><option>Disabled</option></select></label>
<label>fortran.formatting.formatter<select id="v-fmt"><option>Disabled</option><option>fprettify</option><option>findent</option></select></label>
<label>fortran.linter.includePaths<textarea id="v-inc" rows="2"></textarea></label><label>fortran.fortls.directories<textarea id="v-dir" rows="2" placeholder="src/**"></textarea></label>
<div class="chk"><label><input type="checkbox" id="v-sync"> fortran.fortls.incrementalSync</label></div></div>
<div><label>Output<textarea id="v-out" rows="14" readonly spellcheck="false"></textarea></label><button data-copy="v-out">Copy</button><button class="alt" data-dl="v-out" data-name="settings.json">Download settings.json</button></div></div></section>
<p class="notice">Config options change between releases; see the <a href="https://github.com/fortran-lang/fortls" target="_blank" rel="noopener noreferrer">official fortls documentation</a> and <a href="https://fpm.fortran-lang.org/" target="_blank" rel="noopener noreferrer">fpm documentation</a>. Provided as-is without warranty (see <a href="/terms">Terms</a>).</p>'''
BOOLS = [("autocomplete_no_prefix", "Don’t filter autocomplete by prefix"), ("autocomplete_no_snippets", "No snippet placeholders in autocomplete"),
 ("autocomplete_name_only", "Complete procedure names only"), ("lowercase_intrinsics", "Lowercase intrinsics/keywords"),
 ("use_signature_help", "Signature help instead of snippets"), ("variable_hover", "Hover info for variables"),
 ("hover_signature", "Signature info on hover"), ("enable_code_actions", "Enable code actions"),
 ("symbol_skip_mem", "Skip type members in symbols"), ("incremental_sync", "Incremental document sync"),
 ("preserve_keyword_order", "Keep keyword order on hover"), ("debug_log", "Write fortls_debug.log")]
chk = '<div class="chk">' + "".join(f'<label><input type="checkbox" id="b-{k}"> {d}</label>' for k, d in BOOLS) + '</div>'
page("tools", "Free Fortran tools — fortls config, checker, fpm.toml — FORTLS", "Free browser-based tools: fortls validator, .fortls generator, fpm.toml generator and VS Code settings generator. Runs locally; nothing is uploaded.",
     main_(TOOLS.replace("@CHK@", chk)).replace('class="wrap page"', 'class="wrap page wide"') + SUPPORT_BOX, '<script src="/assets/js/tools.js" defer></script>')

page("newsletter", "Newsletter — FORTLS", "Occasional notes and resources for Fortran developers, delivered by beehiiv.",
 main_(f'''<h1>FORTLS newsletter</h1><p>Occasional guides and ecosystem notes for Fortran developers. Subscription is handled by beehiiv.</p>
<p>{go("beehiiv","Subscribe on beehiiv ↗")}</p><p><a href="/newsletter/archive">Browse the newsletter archive →</a></p>
<p class="notice">Your email is submitted to beehiiv, not to this site, and is subject to beehiiv’s privacy policy. You can unsubscribe from any email.</p>
<h2>Free download</h2><p><a href="/downloads/fortran-developer-quick-reference.pdf">Modern Fortran developer quick reference (PDF)</a> — available to everyone, no sign-up needed.</p>'''))

page("support", "Support FORTLS", "Voluntary support for the free FORTLS tools and resources.",
 main_(f'''<h1>Support the project</h1><p>FORTLS is independently maintained. Support helps fund tools, documentation, educational resources, and future development. The tools and guides stay free.</p>
{SUPBTN}
<p class="notice">Support is voluntary, handled by a third-party platform, and does not buy services, advertising or influence over content. It is not a charitable donation and may not be tax-deductible. FORTLS.com may also earn commissions from labelled <a href="/resources#disclosure">affiliate links</a>.</p>'''))

page("sponsors", "Sponsors — FORTLS", "Manually managed, clearly labelled sponsorships for FORTLS.",
 main_('''<h1>Sponsors</h1><p>FORTLS offers a small number of manually managed sponsorships for companies serving Fortran, HPC, scientific-computing and developer-tooling audiences. There are no display ads, popups or programmatic ad networks.</p>
<div class="grid"><article class="card"><span class="tag">Bronze Sponsor</span><h3>Listed sponsor</h3><p>Name, logo and link on this page for a fixed term.</p></article>
<article class="card"><span class="tag">Silver Sponsor</span><h3>Listed + newsletter</h3><p>Everything in Bronze, plus one clearly labelled mention in the FORTLS newsletter.</p></article>
<article class="card"><span class="tag">Featured Tool Partner</span><h3>Tool credit</h3><p>A “Sponsored by” credit on one tool page for a fixed term, plus Silver benefits.</p></article></div>
<h2>Rules</h2><ul><li>Every paid placement is labelled “Sponsored” and its link uses rel="sponsored".</li><li>Sponsors do not influence editorial content or tool outputs.</li><li>No traffic, audience size or performance is promised.</li><li>We may decline any sponsor; terms and rates are agreed by email.</li></ul>
<p>Email <a href="mailto:hello@fortls.com">hello@fortls.com</a> with your organisation and goal.</p><p class="notice">There are currently no active sponsors.</p>'''))

page("about", "About — FORTLS", "About the independent FORTLS resource hub.",
 main_('''<h1>About FORTLS</h1><p>FORTLS.com is an independent hub of free tools and curated links for Fortran developers, with a focus on the Fortran Language Server ecosystem.</p>
<h2>Independence</h2><p>This site is not the official fortls project and is not affiliated with, endorsed by or maintained by its maintainers or the Fortran-lang community. Names and trademarks belong to their respective owners. The official project is on <a href="https://github.com/fortran-lang/fortls" target="_blank" rel="noopener noreferrer">GitHub</a>.</p>
<h2>How it’s funded</h2><p>Voluntary <a href="/support">support</a>, labelled affiliate links and, in future, labelled sponsorships. Editorial content does not depend on them.</p>
<h2>The domain</h2><p>The FORTLS.com domain is <a href="/acquisition">available for acquisition</a>.</p>
<h2>Corrections</h2><p>Spot an error or want a link changed or removed? Email <a href="mailto:hello@fortls.com">hello@fortls.com</a>.</p>'''))

page("acquisition", "Acquire FORTLS.com", "FORTLS.com is available for acquisition. Send proposals to offers@fortls.com.",
 main_('''<div class="eyebrow">Domain acquisition</div><h1>FORTLS.com is available</h1>
<p class="lead">A short, memorable .com connected to Fortran language-server tooling, with an optional working resource hub.</p>
<div class="callout"><h2>Enquiries</h2><p>Email <a href="mailto:offers@fortls.com">offers@fortls.com</a> with your intended use and preferred transaction method.</p><p>''' + go("afternic","Make an offer (Afternic) ↗") + '''</p><p class="muted">No price is published. Any sale would use a written agreement, ideally through a reputable escrow or marketplace service.</p></div>
<h2>What’s included</h2><p>The domain name. Website files, content, tools or third-party accounts are included only if listed in a written agreement.</p>
<h2>Due diligence</h2><p>“fortls” is also the name of an open-source project that is not affiliated with this site. Buyers are responsible for their own review of naming and trademark considerations. No warranty is given beyond what is stated in a signed agreement.</p>'''))

page("contact", "Contact — FORTLS", "Contact FORTLS for questions, corrections, partnerships or domain offers.",
 main_('''<h1>Contact</h1><ul><li>General, corrections, privacy, partnerships: <a href="mailto:hello@fortls.com">hello@fortls.com</a></li><li>Help with a tool: <a href="mailto:support@fortls.com">support@fortls.com</a></li><li>Domain offers: <a href="mailto:offers@fortls.com">offers@fortls.com</a></li></ul>
<p class="notice">This is a part-time project; replies may take a while. Please don’t send passwords or sensitive personal data.</p>
<h2>Copyright or content concerns</h2><p>If you believe content here infringes your rights, email hello@fortls.com with the page address and details and we will review it promptly.</p>'''))

page("privacy", "Privacy — FORTLS", "How FORTLS.com handles visitor data, analytics consent and third-party services.",
 main_(f'''<h1>Privacy policy</h1><p class="muted">Last updated {UPDATED}</p>
<p>FORTLS.com is run by its owner, reachable at <a href="mailto:hello@fortls.com">hello@fortls.com</a>. We keep data collection minimal.</p>
<h2>What we don’t collect</h2><p>No accounts, no forms, no comments. The tools run in your browser; the text you enter is not sent to us.</p>
<h2>Cloudflare</h2><p>The site is served by Cloudflare (hosting, DNS and security), which may process technical data such as IP address and request details under its own <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">privacy policy</a>. Email sent to @fortls.com addresses is handled by Cloudflare Email Routing, forwarded to the owner’s mailbox and used only to reply.</p>
<h2>Analytics (only with your consent)</h2><p>A single banner asks whether we may use Google Tag (Google Tag Manager), Google Analytics 4 and Microsoft Clarity. Nothing from these services loads until you click Accept; Google Consent Mode v2 is set to “denied” by default. If you accept, they collect pages viewed, clicks on key links and buttons (for example affiliate, newsletter, support, download and tool copy/download events), device and browser information, approximate location, and, for Clarity, session recordings and heatmaps with sensitive content masked. They set the cookies _ga, _ga_*, _clck and _clsk. Google and Microsoft process this data under the <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a> and <a href="https://privacy.microsoft.com/privacystatement" target="_blank" rel="noopener">Microsoft Privacy Statement</a>, and it may be transferred outside your country, including to the United States. We do not use analytics for advertising or personalisation.</p>
<p><strong>Withdrawing consent:</strong> click “Privacy choices” in the footer. This revokes your consent, deletes those cookies and shows the banner again. Your choice is stored in your browser’s local storage and is asked again after about a year.</p>
<h2>Newsletter</h2><p>Subscription is handled by beehiiv. Your email address is submitted to beehiiv, not to this site, under <a href="https://www.beehiiv.com/privacy" target="_blank" rel="noopener">beehiiv’s privacy policy</a>.</p>
<h2>Support platforms</h2><p>GitHub Sponsors, Ko-fi and PayPal are operated by third parties. Payments and supporter details are handled by them under their own policies; we do not receive card details.</p>
<h2>Affiliate partners</h2><p>Links to Cloudways and Vultr go through a redirect on this site (/go/…), which does not store personal data, and then to the partner’s site. The partner may set cookies or track referrals, and we may earn a commission. See the <a href="/resources#disclosure">affiliate disclosure</a>.</p>
<h2>Other links</h2><p>Links to the Afternic/GoDaddy domain marketplace, GitHub, social platforms and other sites lead to services with their own privacy policies.</p>
<h2>Legal bases and your rights</h2><p>We rely on your consent for analytics and on legitimate interests for hosting and security. Depending on where you live (for example the EU/UK), you may have rights to access, correct, delete or object to processing of personal data, to withdraw consent at any time, and to complain to a data-protection authority. Email hello@fortls.com. We don’t knowingly collect data from children.</p>
<h2>Changes</h2><p>We may update this page; the date above shows the latest version.</p>'''))

page("terms", "Terms — FORTLS", "Terms of use for FORTLS.com resources and tools.",
 main_(f'''<h1>Terms of use</h1><p class="muted">Last updated {UPDATED}</p>
<p>By using FORTLS.com you agree to these terms.</p>
<h2>As-is</h2><p>Content, links and tools are provided for general information “as is”, without warranties of accuracy, fitness or availability. Review any generated file and check official documentation for your software versions before relying on it.</p>
<h2>Liability</h2><p>To the fullest extent permitted by law, the site owner is not liable for any loss or damage arising from use of the site, its tools or third-party sites. Nothing here limits liability that cannot be limited by law.</p>
<h2>Generated output</h2><p>The tools generate .fortls files, fpm.toml manifests, VS Code settings, CI workflows, compiler flags and other configuration. All generated output is provided “as is”, without warranty of any kind. It is a starting point only: review, test and adapt it to your project and software versions before relying on it. We are not responsible for any loss or damage resulting from its use.</p>
<h2>Third parties</h2><p>External sites and services have their own terms. Some links are affiliate links (see <a href="/resources#disclosure">disclosure</a>). Names and marks belong to their owners; no affiliation or endorsement is implied, including with the fortls project.</p>
<h2>Content</h2><p>Site text and design are owned by the site owner. Output you generate with the tools is yours. Don’t misuse the site or interfere with its operation.</p>
<h2>Concerns and changes</h2><p>Report content issues to hello@fortls.com. We may change or remove the site or these terms at any time. If any provision is unenforceable, the rest remains in effect.</p>'''))

w("404.html", HEAD.replace("@T@", "Page not found — FORTLS").replace("@D@", "Page not found.").replace("@U@", DOM + "/404").replace("@DOM@", DOM).replace("@N@", NAV).replace("@X@", "").replace("@R@", '<meta name="robots" content="noindex">')
  + main_('<h1>Page not found</h1><p>The page may have moved.</p><a class="btn" href="/">Back to FORTLS</a>') + FOOT)

exec(open("extra.py", encoding="utf-8").read())

# ---------- assets ----------
css = open("src/site.base.css").read()
css += '''
main.page.wide{max-width:1000px}.tool{border:1px solid var(--line);border-radius:12px;padding:22px;margin:26px 0;background:#121923}.tool h2{margin-top:0}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px}label{display:block;font-size:.88rem;color:#c2cddd;margin-bottom:12px}
input[type=text],input:not([type]),textarea{width:100%;margin-top:4px;background:#0b111a;color:#e6edf3;border:1px solid #39465a;border-radius:8px;padding:9px 11px;font:13px/1.5 "Fira Code",monospace}
.chk{display:grid;gap:4px}.chk label{margin:0;display:flex;gap:8px;align-items:center}.chk input{width:auto;margin:0}
output.warn{color:#e3b341}output.bad{color:#ff7b72}output.ok{color:var(--green)}
.consent{position:fixed;left:12px;right:12px;bottom:12px;z-index:20;max-width:620px;margin:auto;background:#161b22;border:1px solid #43516a;border-radius:10px;padding:12px 16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.9rem}.consent p{margin:0;flex:1 1 280px}.consent button{margin:0}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
w("assets/css/site.css", css + CSS_EXTRA)

SITE_JS = r'''(()=>{const GTM="@GTM@",GA4="@GA4@",CL="@CL@",K="fortls-consent",DIRECT=@GA4D@;
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}
gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied",wait_for_update:500});
const rd=()=>{try{const j=JSON.parse(localStorage.getItem(K));if(j&&Date.now()-j.t<31536e6)return j.v}catch(e){}return null};
const wr=v=>{try{localStorage.setItem(K,JSON.stringify({v:v,t:Date.now()}))}catch(e){}};
let on=false;
const loadGA=()=>{on=true;gtag("consent","update",{analytics_storage:"granted"});
(function(w,d,s,l,i){w[l].push({"gtm.start":Date.now(),event:"gtm.js"});const f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=1;j.src="https://www.googletagmanager.com/gtm.js?id="+i;f.parentNode.insertBefore(j,f)})(window,document,"script","dataLayer",GTM);
if(DIRECT){gtag("js",new Date());gtag("config",GA4);const s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id="+GA4;document.head.appendChild(s)}};
const loadCL=()=>{(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script",CL);window.clarity("consentv2",{ad_Storage:"denied",analytics_Storage:"granted"})};
const purge=()=>{const h=location.hostname,p=h.split(".").slice(-2).join(".");document.cookie.split(";").forEach(c=>{const n=c.split("=")[0].trim();if(!/^(_ga|_ga_.+|_gid|_gat.*|_clck|_clsk)$/.test(n))return;const x="=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";document.cookie=n+x;[h,"."+h,"."+p,p].forEach(d=>{document.cookie=n+x+";domain="+d})})};
const track=(ev,p)=>{if(!on)return;p.page_path=location.pathname;dataLayer.push(Object.assign({event:ev},p));if(window.clarity){window.clarity("event",ev);for(const k in p)window.clarity("set",k,String(p[k]))}};
const EV={cloudways:"affiliate_click",vultr:"affiliate_click",beehiiv:"newsletter_click","github-sponsors":"github_sponsor_click",kofi:"kofi_click",paypal:"paypal_click",afternic:"offer_click"};
document.addEventListener("click",e=>{const t=e.target.closest("a,button");if(!t)return;const pe=t.closest("[data-placement]"),pl=pe?pe.dataset.placement:t.closest("footer")?"footer":t.closest("header")?"header":"content";
if(t.dataset.copy||t.dataset.dl){const s=t.closest("section.tool");track(t.dataset.copy?"tool_copy":"tool_download",{tool_name:s?s.id:"unknown",placement:pl});return}
const h=t.getAttribute("href")||"",m=h.match(/^\/go\/([a-z-]+)/);
if(m){const ev=EV[m[1]];if(ev){const p={placement:pl};if(ev==="affiliate_click")p.partner_name=m[1];else p.destination=m[1];track(ev,p)}return}
if(/\.pdf$/i.test(h))track("file_download",{file_name:h.split("/").pop(),file_category:t.dataset.category||"cheat-sheet",placement:pl})});
const cs=document.getElementById("cs");
if(cs)cs.onclick=e=>{e.preventDefault();gtag("consent","update",{analytics_storage:"denied"});purge();try{localStorage.removeItem(K)}catch(x){}location.reload()};
const v=rd();
if(v==="yes"){loadGA();loadCL();return}
if(v==="no")return;
const b=document.createElement("div");b.className="consent";b.setAttribute("role","dialog");b.setAttribute("aria-label","Analytics consent");
b.innerHTML='<p>We use Google Analytics and Microsoft Clarity to improve FORTLS. Nothing loads unless you accept. <a href="/privacy">Privacy</a>.</p><button>Accept</button><button class="alt">Decline</button>';
document.body.appendChild(b);const [y,n]=b.querySelectorAll("button");
y.onclick=()=>{wr("yes");b.remove();loadGA();loadCL()};n.onclick=()=>{wr("no");b.remove()}})();
'''
w("assets/js/site.js", SITE_JS.replace("@GTM@", GTM).replace("@GA4@", GA4).replace("@CL@", CLARITY).replace("@GA4D@", GA4_DIRECT))

TOOLS_JS = r'''(()=>{const $=i=>document.getElementById(i),list=v=>v.split(/\n|,/).map(s=>s.trim()).filter(Boolean);
const B=%s,ARR=["source_dirs","ext_source_dirs","excl_paths","excl_suffixes","incl_suffixes","pp_suffixes","include_dirs"];
const T={pp_defs:"object",nthreads:"number",max_line_length:"number",max_comment_line_length:"number",hover_language:"string",config:"string",notify_init:"boolean",disable_diagnostics:"boolean"};
ARR.forEach(k=>T[k]="array");B.forEach(k=>T[k]="boolean");
const strip=s=>{let o="",q=0,i=0;while(i<s.length){const c=s[i],n=s[i+1];if(q){o+=c;if(c==="\\"){o+=n||"";i++}else if(c==='"')q=0}else if(c==='"'){q=1;o+=c}else if(c==="/"&&n==="/"){while(i<s.length&&s[i]!=="\n")i++;continue}else if(c==="/"&&n==="*"){i+=2;while(i<s.length&&!(s[i]==="*"&&s[i+1]==="/"))i++;i++}else o+=c;i++}return o};
const gen=()=>{if(!$("g-out"))return;const o={};[["source_dirs","g-src"],["ext_source_dirs","g-ext"],["excl_paths","g-exp"],["excl_suffixes","g-exs"],["include_dirs","g-inc"]].forEach(([k,id])=>{const l=list($(id).value);if(l.length)o[k]=l});B.forEach(k=>{if($("b-"+k).checked)o[k]=true});if($("g-size").value)o.nthreads=+$("g-size").value;$("g-out").value=JSON.stringify(o,null,2)+"\n"};
const q=s=>'"'+s.replace(/\\/g,"\\\\").replace(/"/g,'\\"')+'"',g=i=>$(i).value.trim();
const fpm=()=>{if(!$("f-out"))return;let o="name = "+q(g("f-name")||"my_project")+"\nversion = "+q(g("f-ver")||"0.1.0")+"\n";[["license","f-lic"],["author","f-au"],["maintainer","f-mt"]].forEach(([k,i])=>{if(g(i))o+=k+" = "+q(g(i))+"\n"});
o+="\n[build]\nauto-executables = "+$("f-ae").checked+"\nauto-tests = "+$("f-at").checked+"\nauto-examples = "+$("f-ax").checked+"\n";if($("f-lib").checked)o+="\n[install]\nlibrary = true\n";
o+='\n[fortran]\nimplicit-typing = false\nimplicit-external = false\nsource-form = "free"\n';const d=list($("f-dep").value.replace(/\n/g,",").replace(/,\s*(?=\S)/g,"\n")).map(l=>l.split(/\s+/)).filter(a=>a[0]);
if(d.length){o+="\n[dependencies]\n";d.forEach(a=>{o+=a[0]+" = "+(a[1]?"{ git = "+q(a[1])+" }":'"*"')+"\n"})}$("f-out").value=o};
const lint=()=>{const s=$("l-out");let j;try{j=JSON.parse(strip($("l-in").value))}catch(e){s.className="bad";s.textContent="Invalid JSON: "+e.message;return null}
if(!j||typeof j!=="object"||Array.isArray(j)){s.className="bad";s.textContent="Top level must be a JSON object.";return null}const m=[];
for(const[k,v]of Object.entries(j)){const t=T[k];if(!t){m.push('? "'+k+'" is not in this tool\'s list (a typo, or an option from a newer fortls).');continue}const a=Array.isArray(v)?"array":v===null?"null":typeof v;if(a!==t)m.push('! "'+k+'" should be '+t+", found "+a+".")}
s.className=m.length?"warn":"ok";s.textContent=m.length?m.join("\n"):"Valid syntax; all keys recognised with the expected types.";return j};
const vsc=()=>{if(!$("v-out"))return;const o={};if(g("v-path")&&g("v-path")!=="fortls")o["fortran.fortls.path"]=g("v-path");o["fortran.linter.compiler"]=$("v-cc").value;const i=list($("v-inc").value);if(i.length)o["fortran.linter.includePaths"]=i;const d=list($("v-dir").value);if(d.length)o["fortran.fortls.directories"]=d;o["fortran.formatting.formatter"]=$("v-fmt").value;if($("v-sync").checked)o["fortran.fortls.incrementalSync"]=true;$("v-out").value=JSON.stringify(o,null,2)+"\n"};
const flash=(id,t)=>{const s=$("g-st")||$("l-out");const o=s.textContent;s.textContent=t;setTimeout(()=>{s.textContent=o},1200)};
document.addEventListener("input",()=>{gen();fpm();vsc()});document.addEventListener("change",()=>{gen();fpm();vsc()});
document.addEventListener("click",e=>{const t=e.target;if(t.dataset.copy){const v=$(t.dataset.copy).value;(navigator.clipboard?navigator.clipboard.writeText(v):Promise.reject()).then(()=>flash(0,"Copied."),()=>{$(t.dataset.copy).select();document.execCommand("copy")})}
if(t.dataset.dl){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([$(t.dataset.dl).value],{type:"text/plain"}));a.download=t.dataset.name;a.click();URL.revokeObjectURL(a.href)}
if(t.id==="l-go")lint();if(t.id==="l-fmt"){const j=lint();if(j)$("l-in").value=JSON.stringify(j,null,2)+"\n"}});
gen();fpm();vsc()})();
''' % json.dumps([k for k, _ in BOOLS])
w("assets/js/tools.js", TOOLS_JS)

# ---------- logos / icons ----------
def draw(d, s, ox=0, oy=0):
    k = s / 100.0; P = lambda x, y: (ox + x * k, oy + y * k)
    d.polygon([P(50, 4), P(92, 27), P(92, 73), P(50, 96), P(8, 73), P(8, 27)], fill="#161b22", outline="#58a6ff", width=max(2, int(4 * k)))
    for r, c in (((34, 30, 43, 70), "#e6edf3"), ((34, 30, 66, 39), "#e6edf3"), ((34, 46, 58, 54), "#e6edf3"), ((62, 62, 72, 70), "#a78bfa")):
        d.rectangle([P(r[0], r[1]), P(r[2], r[3])], fill=c)
SVG_ICON = '<polygon points="50,4 92,27 92,73 50,96 8,73 8,27" fill="#161b22" stroke="#58a6ff" stroke-width="4"/><rect x="34" y="30" width="9" height="40" fill="#e6edf3"/><rect x="34" y="30" width="32" height="9" fill="#e6edf3"/><rect x="34" y="46" width="24" height="8" fill="#e6edf3"/><rect x="62" y="62" width="10" height="8" fill="#a78bfa"/>'
ico_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' + SVG_ICON + '</svg>'
hor_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 76" width="300" height="76"><g transform="scale(.76)">' + SVG_ICON + '</g><text x="86" y="52" font-family="Inter,Segoe UI,Arial,sans-serif" font-weight="800" font-size="40" letter-spacing="2" fill="#e6edf3">FORTLS</text></svg>'
for n in ("logo.svg", "logo-icon.svg", "favicon.svg"): w(n, ico_svg)
w("logo-horizontal.svg", hor_svg)
def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
def icon_png(s, bg=None):
    im = Image.new("RGBA", (s, s), bg or (0, 0, 0, 0)); draw(ImageDraw.Draw(im), s); return im
def save(im, name): os.makedirs(OUT, exist_ok=True); im.save(os.path.join(OUT, name))
for n, s in (("logo.png", 512), ("logo-icon.png", 512), ("favicon-16x16.png", 16), ("favicon-32x32.png", 32), ("favicon-64x64.png", 64),
             ("android-chrome-192x192.png", 192), ("android-chrome-512x512.png", 512)): save(icon_png(s), n)
save(icon_png(180, (13, 17, 23, 255)), "apple-touch-icon.png")
icon_png(256).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
def banner(wd, ht, name, sub):
    im = Image.new("RGB", (wd, ht), "#0d1117"); d = ImageDraw.Draw(im); s = int(ht * .55)
    draw(d, s, int(wd * .08), (ht - s) // 2); x = int(wd * .08) + s + int(ht * .08)
    d.text((x, int(ht * .26)), "FORTLS", font=font(int(ht * .2)), fill="#e6edf3"); d.text((x, int(ht * .56)), sub, font=font(int(min(ht * .075, (wd - x - 40) / (len(sub) * .68)))), fill="#9aa8b8"); save(im, name)
save_ = banner
banner(1200, 630, "og-image.png", "Free tools for Fortran developers")
banner(1600, 400, "cover-newsletter.png", "Fortran tooling notes")
banner(1600, 400, "cover-support.png", "Support free Fortran tools")
hs = Image.new("RGBA", (800, 200), (0, 0, 0, 0)); hd = ImageDraw.Draw(hs); draw(hd, 190, 5, 5); hd.text((230, 55), "FORTLS", font=font(90), fill="#e6edf3"); save(hs, "logo-horizontal.png")

for f in ("logo.png", "logo-horizontal.png", "logo-icon.png"):
    if os.path.exists("brand/" + f): shutil.copy("brand/" + f, os.path.join(OUT, f))
# ---------- config files ----------
w("site.webmanifest", json.dumps({"name": "FORTLS", "short_name": "FORTLS", "start_url": "/", "display": "standalone", "theme_color": "#0d1117", "background_color": "#0d1117",
   "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOM}/sitemap.xml\n")
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod></url>\n" for u in PAGES) + "</urlset>\n")
w("_redirects", "# Affiliate links: replace the target with your referral URL once approved. 302 = temporary, so changes take effect.\n" + "".join(f"/go/{k} {v} 302\n" for k, v in GO.items()))
w("_headers", "/*\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n/go/*\n  X-Robots-Tag: noindex, nofollow\n")
os.makedirs(os.path.join(OUT, "downloads"), exist_ok=True)
import make_pdf; make_pdf.build(os.path.join(OUT, "downloads", "fortran-developer-quick-reference.pdf"))
print("built", len(PAGES), "pages")
