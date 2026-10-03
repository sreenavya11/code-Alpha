# CodeAlpha_SentimentAnalysis

**Task:** Sentiment Analysis (Task 4)
**Tools:** Python, pandas, custom NLP lexicon (built from scratch), matplotlib, seaborn
**Dataset:** `reviews.csv` — 180 synthetic product reviews across 15 product types

## Approach
Rather than relying on an external NLP package (this sandbox has no internet
access to install one), this project implements a **lexicon-based sentiment
engine from scratch** — the same core technique tools like VADER use:

1. **Positive/negative word lexicon** — ~65 hand-scored words with polarity
   weights (e.g. `amazing: +2.5`, `terrible: -2.5`, `decent: +0.8`).
2. **Negation handling** — flips polarity when a negation word ("not", "never",
   "isn't", etc.) appears in the 3 words before a sentiment word, so
   *"not the best"* correctly scores negative instead of positive.
3. **Intensifier handling** — words like "very", "absolutely", "extremely"
   boost the strength of the sentiment word that follows them.
4. **Scoring & classification** — each review gets a summed polarity score,
   then is labeled **Positive** (≥ 0.5), **Negative** (≤ -0.5), or **Neutral**
   (in between).

## How to run
```bash
pip install pandas matplotlib seaborn
python generate_reviews.py     # creates reviews.csv
python sentiment_analysis.py   # classifies + generates charts
```

## Output
- `reviews_with_sentiment.csv` — every review with its score and label
- `charts/01_sentiment_distribution.png` — count of Positive/Neutral/Negative
- `charts/02_sentiment_share.png` — pie chart of sentiment share
- `charts/03_score_distribution.png` — histogram of raw polarity scores
- `charts/04_sentiment_by_product.png` — average sentiment per product type

## Results
On the 180-review dataset: **49.4% Positive, 35.6% Negative, 15.0% Neutral**.
The negation handling correctly re-classifies tricky phrasing like
*"Not the best keyboard I've owned, but it's decent"* as Negative rather than
naively matching on "best" and "decent" alone — this is the key NLP technique
the task asks for.

## Notes / next steps
- The lexicon is intentionally compact and transparent (easy to extend —
  just add words to `POSITIVE_WORDS` / `NEGATIVE_WORDS` in `sentiment_analysis.py`).
- With internet access, swapping in `vaderSentiment` or `TextBlob` would give
  a larger pre-built lexicon; the pipeline structure (load → score → label →
  visualize) stays the same.
- To use with real reviews (e.g. Amazon, Twitter/X), just replace
  `reviews.csv` with your own CSV containing a `review_text` column.

---
*Submitted as part of the CodeAlpha Data Analytics Internship.*
