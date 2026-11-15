# Deployment

## One-time GitHub set-up

### 1. Create the repository

1. Sign in to GitHub and open https://github.com/new
2. **Owner:** `David-Somers-Jupiter-6`
3. **Repository name:** `gm-early-years-app-iphone-guide` (exactly this, lower case with hyphens; the 404 page and README use this address)
4. **Description:** `GM Early Years App – iPhone sign-in guide for carers`
5. **Visibility:** Public. GitHub Pages on a free account needs a public repository.
6. Leave **Add a README**, **.gitignore** and **licence** switched off. The repository must start empty.
7. Select **Create repository**.

### 2. Upload the files

Either let Claude push them (add the repository to the Claude GitHub connection first), or from `C:\Projects\GM_Early_Years_App_iPhone_Guide\gm-early-years-app-iphone-guide` in PowerShell:

```
git init -b main
git add -A
git commit -m "Publish GM Early Years App iPhone guide v2.29"
git remote add origin https://github.com/David-Somers-Jupiter-6/gm-early-years-app-iphone-guide.git
git push -u origin main
```

### 3. Switch on GitHub Pages

1. Open https://github.com/David-Somers-Jupiter-6/gm-early-years-app-iphone-guide/settings/pages
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Nothing else needs changing. There is no Save button; the choice applies at once.

### 4. Run the first deployment

1. Open the **Actions** tab.
2. If the first run failed at "Configure GitHub Pages" (it will if it ran before step 3), open it and select **Re-run all jobs**. Otherwise choose **Deploy GM Early Years App iPhone Guide to GitHub Pages**, then **Run workflow**.
3. When both jobs show a green tick, the site is live at
   https://david-somers-jupiter-6.github.io/gm-early-years-app-iphone-guide/

## Publishing an update

See "Publishing a new version" in `README.md`. Every push to `main` validates and redeploys.

## Taking the site down

Settings → Pages → **Unpublish site**, or make the repository private.
