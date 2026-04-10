# Deploy Round 3 to GitHub Pages

## 1. Initialize repository

```powershell
cd "c:\Users\andrew.neuburger\OneDrive - International Space University\Bureau\Marketing\AI WORLD\AI Training\AI Challenge Arena\Round 3"
git init -b main
git add .
git commit -m "Round 3: launch tracker + research brief"
```

## 2. Create GitHub repository

Create an empty repo on GitHub (for example: `ai-challenge-round3`) and add remote:

```powershell
git remote add origin https://github.com/<your-username>/ai-challenge-round3.git
git push -u origin main
```

## 3. Enable GitHub Pages

1. Open repository Settings -> Pages
2. Source: `Deploy from a branch`
3. Branch: `main` and folder `/site`
4. Save and wait 1-3 minutes

## 4. Validate live URLs

- `https://<your-username>.github.io/ai-challenge-round3/`
- `https://<your-username>.github.io/ai-challenge-round3/launch-tracker.html`
- `https://<your-username>.github.io/ai-challenge-round3/research-brief.html`

## 5. Judge submission paste-ready URLs

- Launch Tracker URL: the `launch-tracker.html` URL above
- Research Brief URL: the `research-brief.html` URL above

## 6. Security check before push

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "sk-|tvly-|api_key|API_KEY"
```

If any secret appears, rotate the key and remove it before final push.
