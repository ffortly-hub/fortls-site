# executed inside build.py (shares its namespace)
CSS_EXTRA = '''
.badge{display:inline-block;font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:99px;background:#1f2a44;color:#a5b4fc;margin-bottom:8px}.badge.soon{background:#222b38;color:#9aa8b8}
.meta{color:var(--muted);font-size:.88rem}main.page pre{overflow:auto;background:#0b111a;border:1px solid var(--line);border-radius:8px;padding:14px;font-size:.85rem}
.crumbs{font-size:.85rem;color:var(--muted);margin-bottom:14px}ul.status{list-style:none;padding:0}ul.status li{display:flex;justify-content:space-between;border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin:8px 0;background:#121923}.up{color:var(--green);font-weight:700}
.entry{border-left:3px solid var(--violet);padding-left:16px;margin:26px 0}
.fortls-support-box{border:1px solid #3c4265;background:#171a2c;border-radius:12px;padding:24px}.fortls-support-box h2{margin-top:0}.fortls-support-box .btn svg,a.star svg{width:16px;height:16px;vertical-align:-3px;margin-right:6px}.sb-row .btn{margin:4px 8px 4px 0}a.star{display:inline-flex;align-items:center}
'''
def crumbs(items):
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(f'<a href="{u}">{n}</a>' for n, u in items[:-1]) + " › " + items[-1][0] + '</nav>'
def bc_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOM + u} for i, (n, u) in enumerate(items)]}
def article(slug, title, desc, body, mins):
    url = "/blog/" + slug
    items = [("Home", "/"), ("Blog", "/blog"), (title, url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc, "datePublished": "2026-11-15", "dateModified": "2026-11-15",
         "mainEntityOfPage": DOM + url, "author": {"@type": "Organization", "name": "FORTLS", "url": DOM},
         "publisher": {"@type": "Organization", "name": "FORTLS", "logo": {"@type": "ImageObject", "url": DOM + "/logo.png"}}}, bc_ld(items)]}
    page("blog/" + slug, title + " — FORTLS", desc,
         main_(crumbs(items) + f'<article><h1>{title}</h1><p class="meta">Published 15 November 2026 · {mins} min read · FORTLS</p>' + body +
               '<p class="notice">FORTLS.com is an independent community resource, not the official fortls project. Verify commands against the official documentation for your versions.</p></article>') + SUPPORT_BOX,
         '<script type="application/ld+json">' + json.dumps(ld) + '</script>')

article("what-is-fortls", "What is fortls? A plain-English guide to the Fortran Language Server",
 "What fortls is, how the Language Server Protocol works, which editors support it, and how a typical Fortran workflow looks.", '''
<p>If you write Fortran in a modern editor and get autocompletion, hover documentation and “go to definition”, there is a good chance a program called <strong>fortls</strong> is doing the work in the background. This guide explains what it is, why it matters and how it fits into a normal development workflow.</p>
<h2>What fortls is</h2>
<p>fortls is an open-source <em>language server</em> for Fortran. It is a separate program, written in Python and installed with <code>pip</code>, that reads your Fortran source files and answers the questions an editor asks: what does this name refer to, which members does this derived type have, which procedures start with these letters. It is developed in the open by the fortran-lang community on <a href="https://github.com/fortran-lang/fortls" target="_blank" rel="noopener noreferrer">GitHub</a>. This website is independent and has no connection with that project.</p>
<h2>The Language Server Protocol in two minutes</h2>
<p>Editor features such as completion and navigation used to be built separately for every language and every editor, so a language needed a new plugin for each editor it wanted to support. The <a href="https://microsoft.github.io/language-server-protocol/" target="_blank" rel="noopener noreferrer">Language Server Protocol (LSP)</a> removes that duplication. It defines a common set of messages exchanged between an editor (the client) and a language-specific program (the server).</p>
<p>In practice the editor starts the server, opens your project folder, and sends small requests such as “the cursor is on line 40, column 12; what is here?”. The server analyses the code and replies with hover text, a list of completions or a file location. Any editor that speaks LSP can use any server that speaks LSP, which is why one Fortran server can serve many editors.</p>
<h2>Why it matters for Fortran</h2>
<p>Fortran projects are often long-lived and large. Code is split across many modules and files, derived types carry procedures, and legacy fixed-form files sit beside modern free-form ones. Finding where something is defined with plain text search is slow and error-prone. A language server understands the structure instead of matching text.</p>
<p>The features you typically get are:</p>
<ul>
<li><strong>Autocompletion</strong> for variables, procedures, modules and type members.</li>
<li><strong>Hover information</strong> showing declarations and signatures.</li>
<li><strong>Go to definition</strong> and <strong>find references</strong> across files.</li>
<li><strong>Symbol outlines</strong> for the current file and the whole workspace.</li>
<li><strong>Signature help</strong> while you type the arguments of a call.</li>
<li><strong>Some diagnostics</strong> for common mistakes. For full compiler errors, pair it with a compiler-based linter.</li>
</ul>
<h2>Supported editors</h2>
<p>Because fortls speaks LSP, it works with any editor that has an LSP client. Commonly used combinations include:</p>
<ul>
<li><strong>Visual Studio Code</strong> through the Modern Fortran extension, which can also lint with a compiler.</li>
<li><strong>Neovim</strong> through the built-in LSP client with <a href="https://github.com/neovim/nvim-lspconfig" target="_blank" rel="noopener noreferrer">nvim-lspconfig</a>.</li>
<li><strong>Vim</strong>, <strong>Emacs</strong> and <strong>Sublime Text</strong> through their respective LSP plugins.</li>
</ul>
<p>Plugin names and setup steps change over time, so check each editor’s documentation. Our <a href="/resources">resources page</a> lists official starting points.</p>
<h2>A typical workflow</h2>
<ol>
<li><strong>Install fortls</strong>, for example with <code>pip install fortls</code>, and confirm it runs with <code>fortls --version</code>.</li>
<li><strong>Install the editor integration</strong> for your editor (see the next article for VS Code).</li>
<li><strong>Open the project folder</strong>, not a single file, so the server can index the whole workspace.</li>
<li><strong>Add a <code>.fortls</code> file</strong> in the project root if the defaults do not suit your layout. It is a small JSON file, for example:</li>
</ol>
<pre>{
  "source_dirs": ["src/**"],
  "excl_paths": ["build"],
  "lowercase_intrinsics": true
}</pre>
<p>The <code>source_dirs</code> option says where your sources live, <code>excl_paths</code> keeps build output out of the index, and <code>lowercase_intrinsics</code> controls the case of completed intrinsic names. You can create and check such a file with our free <a href="/tools#fortls">generator</a> and <a href="/tools#check">validator</a>; both run in your browser.</p>
<h2>Benefits</h2>
<ul>
<li><strong>Faster navigation</strong> in unfamiliar code, which is valuable when joining a research code base.</li>
<li><strong>Fewer typos and mismatched arguments</strong> thanks to completion and signature help.</li>
<li><strong>Editor choice</strong>: you keep the editor you like instead of being tied to one IDE.</li>
<li><strong>Free and open source</strong>, with settings kept in a plain text file you can commit to version control.</li>
</ul>
<h2>Limitations to know about</h2>
<p>fortls is not a compiler. It analyses source text on its own, so unusual preprocessor use, generated sources or very dynamic build setups may need extra configuration, such as include directories or preprocessor definitions. It also cannot replace compiler diagnostics. Treat it as a navigation and productivity layer and keep building with your compiler.</p>
<h2>Conclusion</h2>
<p>fortls brings the everyday conveniences of modern editors to Fortran without locking you into one tool. Install it, connect your editor, add a small <code>.fortls</code> file when needed, and you get faster navigation and fewer mistakes. Ready to try it? Read <a href="/blog/install-fortls-vscode">how to install fortls in VS Code</a>, or open the <a href="/tools">free tools</a>.</p>''', 6)

article("install-fortls-vscode", "Installing fortls in VS Code: a step-by-step guide",
 "Install Python, fortls, VS Code and the Modern Fortran extension, configure them, and fix the most common problems.", '''
<p>This guide takes you from a clean machine to working Fortran autocompletion, hover and go-to-definition in Visual Studio Code. It covers Python, fortls, VS Code, the Modern Fortran extension, configuration and troubleshooting. If you are new to the idea, start with <a href="/blog/what-is-fortls">What is fortls?</a>.</p>
<h2>Step 1: Install Python</h2>
<p>fortls is a Python package, so you need Python 3 first. Download it from <a href="https://www.python.org/downloads/" target="_blank" rel="noopener noreferrer">python.org</a> or use your system package manager. On Windows, tick the option to add Python to <code>PATH</code> in the installer. Then check it in a terminal:</p>
<pre>python3 --version     # Linux / macOS
py --version          # Windows
python3 -m pip --version</pre>
<h2>Step 2: Install fortls</h2>
<p>The simplest way is pip:</p>
<pre>python3 -m pip install fortls</pre>
<p>If you prefer to keep command-line tools isolated from your other Python packages, <code>pipx install fortls</code> works well too, and conda users can install it from the conda-forge channel. Confirm the installation:</p>
<pre>fortls --version
fortls --help</pre>
<p>If the command is not found, the folder that holds Python scripts is probably not on your <code>PATH</code>; see the troubleshooting section below.</p>
<h2>Step 3: Install a compiler (optional, for linting)</h2>
<p>fortls provides navigation and completion; compiler errors come from a compiler. To see them as you type, install gfortran (for example <code>sudo apt install gfortran</code> on Debian or Ubuntu, or the GCC package from Homebrew on macOS) or Intel’s <code>ifx</code>. See the <a href="/resources">resources page</a> for compiler links.</p>
<h2>Step 4: Install VS Code and the extension</h2>
<p>Download <a href="https://code.visualstudio.com/" target="_blank" rel="noopener noreferrer">Visual Studio Code</a>. Open the Extensions view (<code>Ctrl+Shift+X</code>), search for <strong>Modern Fortran</strong> published by fortran-lang, and install it. From a terminal you can run:</p>
<pre>code --install-extension fortran-lang.linter-gfortran</pre>
<p>The extension integrates fortls for hover, completion, symbols and go-to-definition, and it offers to install fortls with pip if it cannot find it.</p>
<h2>Step 5: Open your project</h2>
<p>Use <em>File → Open Folder</em> on the root of your Fortran project, then open a <code>.f90</code> file. Open the Output panel and choose the Modern Fortran channel; you should see fortls start. Hover over a variable or press <code>F12</code> on a procedure call to test it.</p>
<h2>Step 6: Configure</h2>
<p>You can pass options to fortls in two ways, and the extension watches both. The first is VS Code’s <code>settings.json</code> (workspace file <code>.vscode/settings.json</code>):</p>
<pre>{
  "fortran.fortls.path": "fortls",
  "fortran.fortls.directories": ["src/**"],
  "fortran.linter.compiler": "gfortran",
  "fortran.linter.includePaths": ["build/include"]
}</pre>
<p>The second is a <code>.fortls</code> file in the project root, which also works in other editors:</p>
<pre>{
  "source_dirs": ["src/**"],
  "excl_paths": ["build"],
  "hover_signature": true,
  "variable_hover": true
}</pre>
<p>Our <a href="/tools#fortls">.fortls generator</a> and <a href="/tools#vscode">VS Code settings generator</a> create these files for you and run entirely in your browser. Set <code>fortran.linter.compiler</code> to <code>ifx</code>, <code>ifort</code> or <code>Disabled</code> if you do not use gfortran.</p>
<h2>Troubleshooting</h2>
<ul>
<li><strong>“fortls not found”.</strong> Set <code>fortran.fortls.path</code> to the full path of the executable (find it with <code>which fortls</code> on Linux and macOS or <code>where fortls</code> on Windows), or add the Python scripts folder to <code>PATH</code> and restart VS Code.</li>
<li><strong>Nothing happens or the wrong version runs.</strong> You may have two installations, for example one in a virtual environment and one global. Run <code>fortls --version</code> in the same terminal VS Code uses and compare it with the version in the Modern Fortran log.</li>
<li><strong>“Module not found in project”.</strong> The module’s folder is not indexed. Add it to <code>source_dirs</code> (or <code>fortran.fortls.directories</code>) and, for external libraries, to <code>ext_source_dirs</code> or the include paths.</li>
<li><strong>Slow indexing or high CPU.</strong> Exclude build and dependency folders with <code>excl_paths</code>, and avoid pointing <code>source_dirs</code> at your whole home directory.</li>
<li><strong>Hover shows too little.</strong> Enable <code>variable_hover</code> and <code>hover_signature</code> in your configuration.</li>
<li><strong>Odd results in older code.</strong> Check that fixed-form files use a <code>.f</code> style extension and free-form files use <code>.f90</code>, or adjust the suffix options.</li>
<li><strong>Still stuck?</strong> Reload the window (<em>Developer: Reload Window</em>), read the Modern Fortran output channel, and search the upstream issue trackers on GitHub.</li>
</ul>
<h2>Conclusion</h2>
<p>With Python, fortls and the Modern Fortran extension installed, VS Code becomes a capable Fortran environment. Keep a small <code>.fortls</code> file in each project, exclude build folders, and use the output channel when something misbehaves. Next, try the free <a href="/tools">configuration tools</a> or download the <a href="/downloads">quick reference</a>.</p>''', 7)

page("blog", "FORTLS Blog — Fortran tooling tutorials and guides", "Articles, tutorials and developer resources for the Fortran Language Server and modern Fortran tooling.",
 main_(crumbs([("Home", "/"), ("Blog", "/blog")]) + '''<h1>FORTLS Blog</h1><p class="lead">Articles, tutorials, ecosystem updates, and developer resources.</p>
<div class="grid"><article class="card"><span class="tag">Guide · 6 min</span><h3>What is fortls?</h3><p>The Language Server Protocol, why it matters, supported editors and a typical workflow.</p><a href="/blog/what-is-fortls">Read the article →</a></article>
<article class="card"><span class="tag">Tutorial · 7 min</span><h3>Installing fortls in VS Code</h3><p>Python, fortls, the Modern Fortran extension, configuration and troubleshooting.</p><a href="/blog/install-fortls-vscode">Read the article →</a></article></div>''') + NL,
 '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Blog", "name": "FORTLS Blog", "url": DOM + "/blog"}) + '</script>')

page("downloads", "Free Downloads & Developer Resources — FORTLS", "Free quick-reference guides and educational materials for modern Fortran developers.",
 main_(crumbs([("Home", "/"), ("Downloads", "/downloads")]) + '''<h1>Free Downloads &amp; Developer Resources</h1>
<p class="lead">FORTLS provides free resources for modern Fortran developers, including quick-reference guides, configuration examples, and educational materials.</p>
<div class="grid"><article class="card"><span class="badge">Featured Resource</span><h3>Modern Fortran Developer Cheat Sheet &amp; Quick Start Guide</h3><p>A two-page guide with program structure, language habits, arrays, modules and type-bound procedures, fpm commands and the fortls and VS Code workflow.</p><a class="btn" href="/downloads/fortran-developer-quick-reference.pdf">Download PDF</a></article>
<article class="card"><span class="badge soon">Planned</span><h3>VS Code Setup Guide</h3><p>A longer companion to our <a href="/blog/install-fortls-vscode">installation article</a>.</p></article>
<article class="card"><span class="badge soon">Planned</span><h3>fortls Configuration Handbook</h3><p>Until then, use the <a href="/tools#fortls">generator</a>.</p></article>
<article class="card"><span class="badge soon">Planned</span><h3>FPM Developer Reference</h3><p>Until then, use the <a href="/tools#fpm">fpm.toml generator</a>.</p></article></div>
<p class="notice">Downloads are provided as-is. Check commands against the official documentation for your versions.</p>''') + SUPPORT_BOX)

page("partners", "Recommended Infrastructure & Development Partners — FORTLS", "Hosting and cloud providers commonly used by Fortran and scientific-computing developers, with affiliate disclosure.",
 main_(crumbs([("Home", "/"), ("Partners", "/partners")]) + '''<h1>Recommended Infrastructure &amp; Development Partners</h1>
<p class="lead">Providers that developers in scientific computing commonly use for hosting, development environments and CI. We list them for convenience; we have not benchmarked them, so compare pricing and terms yourself.</p>
<p class="notice"><strong>Disclosure:</strong> the links to Cloudways and Vultr on this page are affiliate links. If you sign up through them, FORTLS may earn a commission at no additional cost to you.</p>
<h2>Cloudways</h2><p>Managed cloud hosting that sits on top of infrastructure providers, aimed at simpler server management and application deployments.</p><p>''' + aff("cloudways", "Visit Cloudways") + '''</p>
<h2>Vultr</h2><p>Cloud infrastructure offering virtual machines and other compute options that developers use for test servers, build machines and CI runners.</p><p>''' + aff("vultr", "Visit Vultr") + '''</p>
<h2>Future partners</h2><p>More ecosystem partners may be added over time. See also the full list on <a href="/resources#disclosure">resources</a>, or <a href="/sponsors">sponsor FORTLS</a>.</p>'''))

page("status", "FORTLS Status", "Status of the FORTLS website, guides, downloads and newsletter.",
 main_(crumbs([("Home", "/"), ("Status", "/status")]) + '''<h1>FORTLS Status</h1><p class="lead">System status, platform availability, and operational updates.</p>
<ul class="status"><li><span>Website</span><span class="up">Operational</span></li><li><span>Guides &amp; blog</span><span class="up">Online</span></li><li><span>Newsletter</span><span class="up">Available</span></li><li><span>Downloads</span><span class="up">Available</span></li><li><span>Community channels</span><span><a href="/#community">Listed here</a></span></li></ul>
<p><strong>Last reviewed:</strong> 22 November 2026. <strong>No known platform issues.</strong></p>
<p class="notice">This page is reviewed by hand, not by automated monitoring. The site is static and hosted by Cloudflare; see <a href="https://www.cloudflarestatus.com/" target="_blank" rel="noopener noreferrer">Cloudflare Status</a> for live infrastructure information. Report problems to <a href="mailto:support@fortls.com">support@fortls.com</a>.</p>'''))

page("changelog", "FORTLS Changelog", "Platform updates, feature releases and improvements for FORTLS.com.",
 main_(crumbs([("Home", "/"), ("Changelog", "/changelog")]) + '''<h1>FORTLS Changelog</h1><p class="lead">Track platform updates, feature releases, and improvements.</p>
<div class="entry"><h2>Version 1.0 — Official Public Launch</h2><p class="meta">November 2026</p><ul><li>Website launched</li><li>Resource hub launched</li><li>Newsletter launched</li></ul></div>
<div class="entry"><h2>Version 1.1 — Community Expansion</h2><p class="meta">November 2026</p><ul><li>Social channels established</li><li>GitHub Sponsors enabled</li><li>Ko-fi support enabled</li></ul></div>
<div class="entry"><h2>Version 1.2 — Resource Library</h2><p class="meta">November 2026</p><ul><li>Cheat sheet added</li><li>Download center added</li></ul></div>
<div class="entry"><h2>Version 1.3 — Learning &amp; Tools</h2><p class="meta">November 2026</p><ul><li>Blog with two guides</li><li>VS Code settings generator, validator and advanced .fortls generator</li><li>Partners, status and changelog pages</li></ul></div>
<div class="entry"><h2>Version 1.4 — Privacy, Tracking &amp; Discovery</h2><p class="meta">November 2026</p><ul><li>Single consent banner for Google Tag, Google Analytics 4 and Microsoft Clarity, with Consent Mode v2</li><li>Event tracking for affiliate, newsletter, support, download and tool actions</li><li>FAQ, newsletter archive and RSS feed</li><li>Support box on articles, tools and downloads; latest-activity block on the home page</li><li>Updated privacy policy, terms and affiliate disclosure</li></ul></div>'''))


# ---------- v1.4: FAQ, newsletter archive, feed ----------
FAQS = [
 ("What is fortls?", 'fortls is an open-source language server for Fortran. It gives editors features such as autocompletion, hover information and go-to-definition. The upstream project is developed by the fortran-lang community on <a href="https://github.com/fortran-lang/fortls" target="_blank" rel="noopener">GitHub</a>. Read our <a href="/blog/what-is-fortls">plain-English guide</a>.'),
 ("Is FORTLS official?", "No. FORTLS is an independent community resource. It is not the official fortls project and is not affiliated with the fortls maintainers or the Fortran-lang organization."),
 ("Which editors are supported?", 'Any editor with a Language Server Protocol client can use fortls, including Visual Studio Code (Modern Fortran extension), Neovim, Vim, Emacs and Sublime Text. See <a href="/blog/install-fortls-vscode">installing fortls in VS Code</a>.'),
 ("What is FPM?", 'The Fortran Package Manager (fpm) builds Fortran projects and manages dependencies. Our <a href="/tools#fpm">fpm.toml generator</a> creates a starter manifest. Official documentation: <a href="https://fpm.fortran-lang.org/" target="_blank" rel="noopener">fpm.fortran-lang.org</a>.'),
 ("What tools are available?", 'Four free browser tools: the .fortls generator, the fortls validator, the fpm.toml generator and the VS Code settings generator. They run locally and nothing is uploaded. <a href="/tools">Open the tools</a>.'),
 ("Is everything free?", "Yes. The tools, guides and downloads are free. The site is kept running by voluntary support, labelled affiliate links (Cloudways and Vultr) and, in future, labelled sponsorships."),
 ("How can I support the project?", 'Through GitHub Sponsors, Ko-fi or PayPal on the <a href="/support">support page</a>, by subscribing to the <a href="/newsletter">newsletter</a>, or by starring us on GitHub.'),
 ("Can I advertise on FORTLS?", 'We offer a small number of manually managed, clearly labelled sponsorships. There are no display ads, popups or programmatic ad networks. See <a href="/sponsors">sponsors</a>.'),
 ("Is the domain available for acquisition?", 'Yes. FORTLS.com is for sale. Make an offer through Afternic or email offers@fortls.com. See <a href="/acquisition">acquisition</a>.'),
]
_faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
page("faq", "FAQ — FORTLS", "Answers about fortls, FORTLS.com, the free tools, support, sponsorship and the domain.",
 main_(crumbs([("Home", "/"), ("FAQ", "/faq")]) + '<h1>Frequently asked questions</h1>' + "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in FAQS)) + SUPPORT_BOX,
 '<script type="application/ld+json">' + json.dumps(_faq_ld) + '</script>')

_arch = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> <span class="muted">· {d}</span></li>' for d, t, u, _ in ISSUES)
page("newsletter/archive", "Newsletter archive — FORTLS", "Past issues of the FORTLS newsletter, hosted on beehiiv.",
 main_(crumbs([("Home", "/"), ("Newsletter", "/newsletter"), ("Archive", "/newsletter/archive")]) + '<h1>Newsletter archive</h1><p class="lead">Past issues of the FORTLS newsletter. Issues open on beehiiv.</p>' +
       ("<ul>" + _arch + "</ul>" if ISSUES else "<p>No issues are listed here yet.</p>") + '<p>' + go("beehiiv", "Browse all issues on beehiiv ↗") + '</p>') + NL)

from email.utils import format_datetime
from datetime import datetime, timezone
from xml.sax.saxutils import escape
def _rfc(d): return format_datetime(datetime.strptime(d, "%Y-%m-%d").replace(hour=12, tzinfo=timezone.utc))
_items = [("Article", p) for p in POSTS] + [("Tool", p) for p in TOOLREL] + [("Download", p) for p in DLS] + [("Newsletter", p) for p in ISSUES]
_items.sort(key=lambda t: t[1][0], reverse=True)
_xml = "".join(f'<item><title>{escape(k + ": " + it[1])}</title><link>{escape(it[2] if it[2].startswith("http") else DOM + it[2])}</link><guid isPermaLink="false">fortls-{k.lower()}-{escape(it[2])}</guid><pubDate>{_rfc(it[0])}</pubDate><category>{k}</category><description>{escape(it[3])}</description></item>' for k, it in _items)
w("feed.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>FORTLS</title><link>' + DOM + '/</link><description>Free tools and resources for Fortran developers.</description><language>en</language><lastBuildDate>' + _rfc(UPDATED) + '</lastBuildDate><atom:link href="' + DOM + '/feed.xml" rel="self" type="application/rss+xml"/>' + _xml + '</channel></rss>\n')
