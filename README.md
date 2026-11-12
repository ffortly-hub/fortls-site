# FORTLS.com — static site

Deploy: push this repo to GitHub (FORTLSHub/fortls-site) → Cloudflare Pages → Build command: *(none)* · Output directory: `site`.
Then add custom domain `fortls.com` and a redirect from `www` to the apex (Cloudflare dashboard → Rules → Redirect Rules).

Edit `build.py` (CONFIG block / page text), run `python3 build.py`, commit `site/`.

## Before launch (5 minutes)
1. Replace the plain provider URLs in `GO` (build.py) with your approved referral links → rebuild. Until then /go/* sends to the providers' homepages (no commission).
2. Check hello@, support@, offers@fortls.com actually forward (Cloudflare Email Routing).
3. In Search Console, submit https://fortls.com/sitemap.xml.

## Legal-risk decisions built in
- Analytics (Clarity) loads only after the visitor accepts the consent banner.
- No claims about escrow, traffic, "verified", "premium", partners or sponsors that can't be proven.
- Affiliate links carry rel="sponsored nofollow" and a disclosure on /resources.
- "Not the official fortls project" disclaimer on every page; original logo (not the upstream project's).
- Privacy, Terms, copyright/takedown route and a domain-sale due-diligence note are included.
- Newsletter and donations are plain links to beehiiv / Buy Me a Coffee (no embedded forms collecting data here).
