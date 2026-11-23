# Job Discovery

Minimal job feed built with React, Vite, and Anime.js. GitHub Pages hosting; no API key required.

### Publishing
Open **Settings → Pages → Build and deployment → Source → GitHub Actions**. Pushing to main starts the deployment workflow. Site URL: https://akhauber.github.io/job-discovery/

### Importing reviewed jobs
Save a reviewed shortlist to a JSON file with a `jobs` array. Then:
```bash
python3 scripts/import_jobs.py reviewed.json
git add public/data/jobs.json
git commit -m "Import reviewed jobs"
git push
```
The importer preserves job IDs and first-seen dates across repeat imports. It does **not** scrape jobs, call ChatGPT, or automatically synchronize the existing ChatGPT scheduled task.

### Data
Fields: company, title, season (spring/summer/both), location, work_mode (remote/hybrid/onsite/unverified), apply_url, overview, why_fit, relevant_experiences (array), gaps (array), fit_score (0–10). Optional: posted_at, start_date, end_date, compensation, hourly_pay, hours, source, status (active/unverified/closed), eligibility, freshness. Never publish private résumé text or credentials.

### Privacy
This is a public website. Saved/dismissed/seen preferences live in the **current browser only**. Do not put secrets in source or public/data/jobs.json.
