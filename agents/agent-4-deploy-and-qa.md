# Agent 4 - Deploy and QA

## Status: ❌ NOT STARTED — Priority for next session

## Exact Deploy Commands (copy-paste ready)

```powershell
cd "c:\Users\andrew.neuburger\OneDrive - International Space University\Bureau\Marketing\AI WORLD\AI Training\AI Challenge Arena\Round 3"
git init -b main
git add .
git commit -m "Round 3: launch tracker + research brief – ready for competition"
git remote add origin https://github.com/<your-username>/ai-challenge-round3.git
git push -u origin main
```

Then on GitHub: Settings → Pages → Branch: `main`, Folder: `/site` → Save.

## Security check before push

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "sk-|tvly-|api_key" | Format-Table
```
Expected result: 0 matches.

## QA Checklist (run after Pages is live)

- [ ] `https://<user>.github.io/<repo>/` loads landing page
- [ ] `/launch-tracker.html` — table rows visible with mission/rocket/site/UTC data
- [ ] Countdown ticks every second for the next launch
- [ ] `/research-brief.html` — 6 DOI links all open to real papers
- [ ] Mobile view (< 860px): no horizontal scroll
- [ ] `.env` file does NOT appear in GitHub repo files

## Judge URL Submission

After passing QA, paste:
- **Launch Tracker**: `https://<user>.github.io/<repo>/launch-tracker.html`
- **Research Brief**: `https://<user>.github.io/<repo>/research-brief.html`
