# GM Early Years App – iPhone sign-in guide (Carer role)

A screen-by-screen guide for parents and primary carers who are having trouble signing in to their GM Early Years App account on an iPhone. It helps them find out what is stopping them and shows what to do next.

**Website:** https://david-somers-jupiter-6.github.io/gm-early-years-app-iphone-guide/

| | |
|---|---|
| Current version | 2.41 (review draft, iPhone edition) |
| Pages | 69, in four sections: Checklist, Signing in, Troubleshooting, Contact & support |
| Owner | GMDP Support Team, GMCA |
| Hosting | GitHub Pages, deployed by GitHub Actions |

## How the site works

The whole guide is one self-contained file, `index.html`. Fonts, images and scripts are embedded, so it loads nothing from other websites and collects no information about the reader. The only outside links go to NHS login's own help pages.

## What is in this repository

| File | Purpose |
|---|---|
| `index.html` | The published guide |
| `preview/` (when present) | A trial version for review, published at `/preview/`. Not the live guide. |
| `404.html` | "Page not found" page that points back to the guide |
| `releases/` | A named copy of each published version |
| `scripts/validate_site.py` | Checks run before every deployment (structure, links, alt text, self-containment) |
| `scripts/check_javascript.py` | Checks the guide's embedded JavaScript for syntax errors |
| `.github/workflows/deploy-pages.yml` | Validates, then publishes to GitHub Pages |
| `DEPLOYMENT.md` | One-time GitHub set-up and how to publish a new version |
| `CHANGELOG.md` | What changed in each published version |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## Publishing a new version

1. Save the new guide as `releases/GM_Early_Years_App_iPhone_vX.XX.html`.
2. Copy the same file over `index.html`.
3. Add a line to `CHANGELOG.md`.
4. Commit and push to `main`. GitHub Actions validates the guide and publishes it, usually within two minutes.

Run the checks locally first with:

```
python3 scripts/validate_site.py
python3 scripts/check_javascript.py
```

## Support

For help with a GM Early Years App account, contact the GMDP Support Team. GMDP Support cannot set up or troubleshoot NHS login accounts; the guide points to NHS login's own support for those.
