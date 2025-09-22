# Dark Sky Explorer NT — Project Guide

Links: [CDU Data Science Challenge](https://itcodefair.cdu.edu.au/data-science-challenge) • [Open‑Meteo API Docs](https://open-meteo.com/en/docs)

## 1) Project Overview
- Objective: Analyze weather + tourist reviews to rank NT stargazing sites and provide 5–7 actionable recommendations with indicative economic impact.
- Deliverables: Clean dataset, Python notebook(s), slide deck, 10‑minute presentation.
- Tech: Python; Jupyter; Open‑Meteo for weather; reviews from TripAdvisor, Google Maps, blogs, Reddit.

## 2) Success Criteria
- ≥500 total reviews (≥80/site)
- ≥3 figures (sentiment by site, top pain points, Stargazing Score ranking)
- 5–7 recommendations; clear, actionable, and grounded in findings

## 3) Team & Workflow
- Solo developer: You own all coding (collection, cleaning, EDA, modeling, visuals)
- Teammates: Support data sourcing/validation and presentation
- GitHub only; shared drive and Kanban not used

## 4) ## Selected Dark-Sky Sites (6 locations)

1. Uluru-Kata Tjuta National Park — (-25.3444, 131.0369): Remote, iconic landscape, minimal light pollution
2. Alice Springs Desert Park — (-23.6980, 133.8807): Central hub, education facilities, strong accessibility
3. Devils Marbles (Karlu Karlu) — (-20.7539, 134.2692): Exceptional darkness, unique geology, camping
4. Kakadu NP – Gunlom Falls Lookout — (-13.4269, 132.4117): UNESCO site, elevated views, cultural heritage
5. West MacDonnell – Ormiston Gorge — (-23.6386, 132.7289): Dark skies, natural amphitheater, camping
6. Nitmiluk (Katherine Gorge) — (-14.2531, 132.4236): Remote Top End site, cultural tourism opportunities

Rationales: remote/dark skies, iconic landscapes, accessibility, cultural value.

## 5) Data Sources & Access
- Weather: Open‑Meteo Archive API (no key). Example (Uluru):
  ```
  https://archive-api.open-meteo.com/v1/archive?latitude=-25.3444&longitude=131.0369&start_date=2015-01-01&end_date=2024-12-31&hourly=temperature_2m,cloud_cover,precipitation
  ```
  Typical hourly vars: temperature_2m, cloud_cover, precipitation
- Reviews: TripAdvisor, Google Maps, travel blogs, Reddit
  - Reddit subreddits: r/australia, r/travel, r/AustraliaTravel, r/Darwin, r/northernterritory, r/camping, r/Astronomy
  - Query strings: "<place> night sky", "<place> stars", "<place> stargazing", "Milky Way"
- Light pollution (VIIRS): Deferred to Phase 5

.env (optional, for future Reddit):
```
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=
```

## 6) Data Templates (CSV)
- Reviews (required):
  ```csv
  platform,location_name,review_id,review_text,rating,review_date,reviewer_home,url
  ```
  Optional: `source_id,collected_at,lang`
- Weather:
  ```csv
  location,date,cloud_cover_percent,temperature_night,rainfall_mm,wind_speed
  ```
- Unified schema (target):
  ```csv
  location,lat,lon,date,sky_brightness,cloud_cover,temperature,sentiment_score,review_count,avg_rating
  ```

## 7) Data Dictionary (to be finalized later)
- Reviews: types for each column, dedup by `platform+review_id`
- Weather: units km/h
- Light pollution: `viirs_radiance`, `sky_brightness_index` (0–100 inverse)

## 8) Phases & Tasks (condensed)
- Phase 2 — Data Collection (Active)
  - Weather: Pull Open‑Meteo for all 6 sites; save CSV
  - Reviews: Collect TripAdvisor/Google/Reddit/blogs to reach ≥500 reviews, standardize fields
  - Note: VIIRS deferred
- Phase 3 — Cleaning & Preprocessing
  - Standardize dates/units; drop empty reviews; dedup
  - Sentiment (TextBlob/VADER), Topic Modeling (LDA)
  - Build unified dataset
- Phase 4 — EDA
  - Weather seasonality charts; sentiment distributions; word clouds; pain points
- Phase 5 — Modeling & Indices
  - Weather Index (cloud cover 60% + temp 40%)
  - Darkness Index (from VIIRS; deferred)
  - Sentiment Index (% positive)
  - Stargazing Score = 0.4*Weather + 0.3*Darkness + 0.3*Sentiment
  - Normalize to 0–100; rank sites
- Phase 6 — Recommendations & Economic Value
  - 5–7 actions; estimate impact = visitors × nights × spend
- Phase 7 — Presentation
  - 8–10 slides; visuals first; timed 10 min

## 9) Reviews SOP (quick)
- Platforms: TripAdvisor, Google Maps, Reddit, blogs
- De‑dup: `platform+review_id`
- Date range: last 3 years preferred
- Ethics: obey ToS; attribute URLs; do not scrape where prohibited

## Reviews Collection Strategy (simple & ToS‑safe)
- Reddit (API via PRAW)
  - Use environment variables: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
  - Search subreddits: r/australia, r/travel, r/AustraliaTravel, r/Darwin, r/northernterritory, r/camping, r/Astronomy
  - Queries: `<place> night sky`, `<place> stars`, `<place> stargazing`, `Milky Way`
  - CSV mapping:
    - platform=Reddit, location_name, review_id=(post_id/comment_id), review_text=(title+selftext or comment), rating=, review_date, reviewer_home=, url=permalink, source_id=subreddit, collected_at, lang
  - Output: `raw_data/reviews/reddit_<slug>.csv`
- TripAdvisor + Google Maps
  - Start with manual CSV exports to avoid ToS issues; include source URLs
  - Fields must match the Reviews template; add optional `source_id,collected_at,lang`
  - Optional later: Selenium (slow, respectful delays) or Google Places API (limited reviews)
  - Output: `raw_data/reviews/{tripadvisor|google}_<slug>.csv`
- Blogs
  - Manual extraction with citation; store URLs in `url` column
- Merge step
  - Script plan: `scripts/reviews_merge.py` to load all platform CSVs, normalize columns, dedup on `platform+review_id`, write `raw_data/reviews/reviews_all.csv`
- Targets
  - ≥500 total reviews; aim ≥80 per site; focus on last 3 years

## 10) Notes & Links
- Repo: https://github.com/Estaed/CDU_IT_CODEFAIR_Data_Science
- Challenge brief: https://itcodefair.cdu.edu.au/data-science-challenge
- Weather API: https://open-meteo.com/en/docs

---

## Charter (Merged)
- Success Criteria: ≥500 total reviews; ≥3 figures; 5–7 recommendations; 10‑minute presentation
- Key Deliverables: Clean dataset + dictionary; Python notebook; slide deck; live pitch
- Tooling & Links: GitHub only (shared drive/Kanban not used)
- Data Schema (core):
  - Reviews: platform, location_name, review_id, review_text, rating, review_date, reviewer_home, url
  - Unified: location, lat, lon, date, sky_brightness, cloud_cover, temperature, sentiment_score
- Timeline Overview: Days 1–2 (data), 3–4 (EDA), 5 (model), 6 (slides), 7 (rehearsal)

## Phases — AI‑Ready Playbook (Detailed)

### Phase 2 — Data Collection
- Weather (Open‑Meteo)
  - Task: For each site, fetch hourly `temperature_2m,cloud_cover,precipitation` (2015‑01‑01 → 2024‑12‑31)
  - Output CSV per site: `raw_data/weather/<slug>_weather.csv`
  - Helper (suggested): `scripts/fetch_open_meteo.py` with `fetch_site_weather(lat, lon, start_date, end_date) -> DataFrame`
- Reviews (TripAdvisor, Google, Reddit, Blogs)
  - Create schema CSV: `raw_data/reviews/reviews_schema.csv` (header only from Reviews template)
  - Collect links per site; export CSVs per platform: `raw_data/reviews/<platform>_<slug>.csv`
  - Ensure columns match template; add optional `source_id,collected_at,lang`
  - Deduplicate on `platform+review_id`

### Phase 3 — Cleaning & Preprocessing
- Weather
  - Convert timestamps → date; aggregate nightly/cloud cover % by date; unify columns
- Reviews
  - Drop empty reviews; normalize ratings to 1–5; parse dates to ISO
  - Sentiment (VADER/TextBlob): add `sentiment_score` (‑1..1 or 0..1), and label (pos/neu/neg)
  - Topic modeling (LDA): extract top keywords per site
- Unified Dataset
  - Join weather + reviews by site/date; final columns: `location,lat,lon,date,cloud_cover,temperature,sentiment_score`
  - Save to `data/processed/unified.csv`

### Phase 4 — EDA
- Weather: histograms (cloud cover % by season), line charts (seasonal trends)
- Reviews: sentiment distribution per site; word clouds (pos vs neg); top pain points
- Maps (optional later): site scatter map
- Save figures to `visualizations/` with descriptive filenames

### Phase 5 — Modeling & Indices
- Weather Index = 0.6×(inverse cloud cover) + 0.4×(temperature comfort)
- Darkness Index = inverse of VIIRS radiance (deferred to later)
- Sentiment Index = % positive reviews per site
- Stargazing Score = 0.4×Weather + 0.3×Darkness + 0.3×Sentiment → normalize 0–100
- Output: `data/processed/stargazing_scores.csv` + ranking plot

### Phase 6 — Recommendations & Economic Value
- Derive 5–7 actions tied to findings (e.g., promote top sites in dry season)
- Economic estimate = Visitors uplift × Nights × Spend/night (document assumptions)
- Create 1–2 slides summarizing impact ranges

### Phase 7 — Presentation
- 8–10 slides: background, data sources, cleaning, EDA highlights, score results, recommendations, economic value
- Keep text minimal; emphasize charts, maps, rankings; rehearse to 10 min
