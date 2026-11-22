# FORTLS roadmap (planning notes, not published)

## Tools (browser-only, no backend, no paid APIs)
1. **Compiler Flags Builder** - choose compiler (gfortran/ifx), build type (debug/release), checks, OpenMP; output flag string + fpm `[fortran]`/profile snippet. Data: a static JSON table of flags with one-line explanations. Track: tool_copy.
2. **GitHub Actions Generator** - fpm build/test workflow; inputs: OS matrix, compiler, caching. Output YAML. Verify action names against upstream docs before release.
3. **fortls Config Optimizer** - paste `.fortls`; rules suggest `excl_paths` for build dirs, `nthreads`, hover options. Ruleset lives in `fortls-tools/rules`.
4. **FPM Validator** - parse `fpm.toml` (small TOML subset parser or a vendored MIT library), check required keys, dependency forms, section names.
5. **Tool download tracking** - already wired in `site.js` (tool_copy / tool_download with tool_name); each new tool needs `section.tool` with an `id`.

## Downloads library (/downloads categories)
Cheat Sheets: Compiler Flags, Intrinsics, OpenMP, MPI. Templates: FPM Project, CI Workflow. Guides: VS Code Setup, fortls Configuration Handbook, FPM Developer Reference. Checklists: Modernization. Publish each as PDF with `data-category`; add to `DLS` in build.py so the feed and home block pick it up.

## Article queue (1200-2500 words each; Article + Breadcrumb schema, TOC, support box)
1 Installing fortls in Neovim - 2 Your first FPM project - 3 Modern Fortran modules - 4 fortls configuration reference - 5 VS Code settings explained - 6 Intel Fortran vs gfortran - 7 gfortran flags for debug and release - 8 Running Fortran on HPC clusters. Add each to `POSTS` and call `article()`; verify every command against official docs.

## Sponsorship
Bronze (listed), Silver (listed + one labelled newsletter mention), Featured Tool Partner ("Sponsored by" credit on one tool page). Manual only; no display ads, popups or ad networks; rel="sponsored"; no traffic promises.

## AI-agent workflow (human approval required)
Content as files + `POSTS/TOOLREL/DLS/ISSUES` registry -> agent opens a pull request -> automated checks (links, HTML, banned claims such as "verified/guaranteed", official-source citation for commands) -> human merges -> Cloudflare deploys. Newsletter drafts only via beehiiv; social posts drafted, never auto-posted. Note AI assistance where required.
