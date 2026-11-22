# FORTLS.com - static site (v1.4)

Deploy: push to GitHub -> Cloudflare Pages. Build command: none. Output directory: `site`. Upload/commit the WHOLE `site/` folder each release.
Edit `build.py` (CONFIG, registries POSTS/TOOLREL/DLS/ISSUES) and `extra.py`, run `python3 build.py`, commit `site/`.

## After deploying v1.4
1. Open the site in a private window: no Google/Clarity requests before you click Accept (DevTools > Network).
2. Click Accept, then check GA4 Realtime. If NO hits appear, the GTM container (GTM-P54LMMLJ) has no GA4 tag: set `GA4_DIRECT = "true"` in build.py and rebuild. If hits appear twice, keep it "false".
3. In GTM, make sure tags fire on the custom events (affiliate_click, newsletter_click, github_sponsor_click, kofi_click, paypal_click, offer_click, file_download, tool_copy, tool_download) and mark the useful ones as key events in GA4.
4. Click every /go/ link once; confirm the Afternic link shows fortls.com with Make Offer.
5. Search Console: submit https://fortls.com/sitemap.xml and request indexing for /faq and /newsletter/archive.

## Folders
- `site/` deployed files - `fortls-tools/` MIT tool code for GitHub (FORTLS-HUB/fortls-tools) - `docs/` planning notes - `brand/` source logos (not published as a repo).
