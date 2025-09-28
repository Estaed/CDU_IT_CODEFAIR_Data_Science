# NT Stargazing — NLP Tier List Project Guide

Links: [CDU Data Science Challenge](https://itcodefair.cdu.edu.au/data-science-challenge)

## 1) Project Overview
- Objective: Build a domain‑specific recommendation assistant for Australian travel destinations. Predict 1–5 star sentiment for each review, build a retrieval system over reviews, and deliver recommendations via a RAG pipeline restricted to places in the dataset.
- Deliverables: Unified reviews CSV, reviews enriched with `stars`, fine‑tuned star classifier, FAISS index + retrieval, RAG recommendation service/notebook, evaluation metrics/figures, short slide deck.
- Tech: Python, Jupyter, pandas, PyTorch, Hugging Face Transformers, Sentence‑Transformers, FAISS, scikit‑learn, matplotlib/seaborn.

## 2) Unified Output (Single CSV)
- Required columns (exact):
  ```csv
  source,place,comment
  ```
- Location: `data/reviews_unified.csv`

## 3) Success Criteria
- Unified CSV created with only the three required columns (done)
- Cleaned comments (deduped, non‑empty, sensible text length) (done)
- Automatic 1–5 `stars` labels generated and saved to an enriched CSV
- Fine‑tuned star classifier trained with Accuracy/F1 and confusion matrix reported
- Retrieval returns relevant reviews for diverse queries (spot‑checked and measured)
- RAG recommendations grounded in retrieved reviews and restricted to dataset places
- 8–10 slides summarizing method, results, and takeaways

## 4) Data Sources (already collected)
- Three raw sources live under `raw_data/` (e.g., TripAdvisor/Google/Reddit/blogs). Use only text that complies with ToS and attribution where required.

## 5) Phases (simple & actionable)

### Phase 1 — Scope & Inventory (Completed)
- Tasks
  - List raw files and locate columns for website/source, place, and comment text.
  - Define canonical place names (e.g., "Uluru-Kata Tjuta", "Alice Springs Desert Park").
  - Draft mapping from each source's columns → `source,place,comment`.

### Phase 2 — Cleaning & Unification (Completed)
- Scripts (three independent cleaners)
  - `scripts/clean_tripadvisor.py` → outputs `data/interim/tripadvisor_clean.csv`
  - `scripts/clean_google_maps.py` → outputs `data/interim/google_clean.csv`
  - `scripts/clean_reddit.py` → outputs `data/interim/reddit_clean.csv`
- Schema rules (strict)
  - Keep only: `source,place,comment`.
  - `source` values:
    - TripAdvisor → `TripAdvisor`
    - Google Maps → `GoogleMaps`
    - Reddit → `Reddit/<subreddit>` (e.g., `Reddit/r/australia`)
  - `place`: normalized to canonical names.
  - `comment`: plain text; strip HTML/emoji/control chars; normalize whitespace.
- Cleaning tasks per script
  - Load raw → select/rename → clean text → drop empty/very short → save interim CSV.
- Merge & dedup
  - Concatenate interim CSVs, standardize `place` via canonical map, deduplicate on `source+place+comment`.
  - Save unified file: `data/processed/reviews_unified.csv`.
  - Run order: TripAdvisor → Google Maps → Reddit → Merge.

### Phase 3 — Automatic Star Label Generation (1–5)
- Model: `nlptown/bert-base-multilingual-uncased-sentiment` (or similar) to infer 1–5 stars per `comment`.
- Output: add integer `stars ∈ {1,2,3,4,5}` to each row; save as `data/processed/reviews_with_stars.csv`.
- Implementation notes:
  - Truncate/segment long comments to model max tokens; average or max‑pool predictions if segmented.
  - Batch inference; prefer GPU if available; set random seed and log model version.
  - Keep only rows with valid predictions; preserve `source,place,comment`.

### Phase 4 — Fine‑Tuning for Star Prediction
- Task: multi‑class classification over 5 classes using DistilBERT/RoBERTa.
- Data: `reviews_with_stars.csv` with stratified train/val/test split.
- Metrics: Accuracy, macro F1; export confusion matrix to `visualizations/star_confusion_matrix.png`.
- Artifacts: save model + tokenizer to `models/star_classifier/`; log training config and metrics.

### Phase 5 — Retrieval System (Semantic Search)
- Embeddings: generate with Sentence‑Transformers (e.g., `all-MiniLM-L6-v2`).
- Index: build FAISS index; store vectors + metadata (id, `place`, `source`, `stars`).
- Artifacts: `indices/review_faiss/` (index files) and `data/processed/review_metadata.parquet`.
- Functionality: given a user query, return top‑k most relevant reviews.

### Phase 6 — RAG Recommendations & Reporting
- LLM: lightweight model (e.g., Mistral/DistilGPT‑2) fine‑tuned on review‑style recommendations.
- System prompt: "You are a travel recommendation assistant. You can only suggest places from the dataset and must base your answers on provided reviews."
- Pipeline: user query → retrieve reviews (Phase 5) → format context → generate recommendation constrained to dataset places.
- Outputs:
  - Example recommendations and qualitative checks saved under `docs/examples/`.
  - Figures: star distribution per place, top places by average stars, retrieval quality snapshots → `visualizations/`.
  - Slide deck: problem, data, star labeling, classifier metrics, retrieval, RAG results, insights.

## 6) SOP & Quality
- Ethics/ToS: obey platform rules; attribute URLs if used; avoid prohibited scraping.
- Reproducibility: notebooks to cover key steps:
  - `notebooks/generate_stars.ipynb` (Phase 3)
  - `notebooks/train_star_classifier.ipynb` (Phase 4)
  - `notebooks/build_retrieval_index.ipynb` (Phase 5)
  - `notebooks/rag_recommender.ipynb` (Phase 6)
- Versioning: keep data writes in `data/processed/`; do not overwrite raw files.

## 7) File Map (minimal)
- Input: `raw_data/` (three sources)
- Interim: `data/interim/` (per‑source cleaned CSVs)
- Unified: `data/processed/reviews_unified.csv`
- Enriched: `data/processed/reviews_with_stars.csv`
- Retrieval index: `indices/review_faiss/`, metadata `data/processed/review_metadata.parquet`
- Models: `models/star_classifier/`
- Notebooks: `notebooks/generate_stars.ipynb`, `notebooks/train_star_classifier.ipynb`, `notebooks/build_retrieval_index.ipynb`, `notebooks/rag_recommender.ipynb`
- Figures: `visualizations/`
- Scripts: `scripts/clean_tripadvisor.py`, `scripts/clean_google_maps.py`, `scripts/clean_reddit.py`

## 8) Quick Implementation Notes
- Star inference: batch with `transformers` pipeline; cap length to model max tokens; prefer GPU if available.
- Fine‑tuning: use stratified split; early stopping; report Accuracy and macro F1; export confusion matrix.
- Retrieval: normalize/clean queries; store `place` and `source` in metadata; return citations with each result.
- Guardrails: only recommend places present in `reviews_unified.csv`; cite supporting reviews.
- Place merging: maintain canonical mapping from Phase 2 for consistency across all phases.
