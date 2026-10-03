"""
sentiment_analysis.py
CodeAlpha Data Analytics Internship - Task 4: Sentiment Analysis

Classifies product reviews as Positive / Negative / Neutral using a custom
lexicon-based NLP approach (no external ML/NLP library required):
  - word-level positive/negative lexicon
  - negation handling ("not good" -> negative)
  - intensifier handling ("very good" -> stronger positive)
  - simple polarity scoring -> Positive / Negative / Neutral label

This mirrors how classic tools like VADER work, built from scratch so it
runs anywhere without extra dependencies.
"""

import re
import csv
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set_style("whitegrid")

# --------------------------------------------------------------------------
# 1. LEXICON
# --------------------------------------------------------------------------
POSITIVE_WORDS = {
    "love": 2.5, "loved": 2.5, "amazing": 2.5, "excellent": 2.5, "perfect": 2.5,
    "perfectly": 2.2, "great": 2.0, "fantastic": 2.5, "wonderful": 2.2,
    "best": 2.3, "superb": 2.4, "impressed": 2.0, "happy": 1.8, "recommend": 1.6,
    "good": 1.5, "nice": 1.3, "fine": 0.8, "decent": 0.8, "okay": 0.4, "ok": 0.4,
    "fast": 1.0, "quality": 0.8, "lovely": 1.8, "beautiful": 1.6, "value": 0.7,
    "helpful": 1.2, "acceptable": 0.5, "functional": 0.5, "works": 0.5,
}

NEGATIVE_WORDS = {
    "hate": -2.5, "terrible": -2.5, "awful": -2.5, "worst": -2.6, "broke": -2.0,
    "broken": -2.0, "waste": -2.2, "disappointed": -2.0, "disappointing": -2.0,
    "poor": -1.8, "cheaply": -1.5, "cheap": -1.0, "flimsy": -1.6, "slow": -1.2,
    "buggy": -1.5, "frustrating": -1.8, "damaged": -1.8, "unhelpful": -1.6,
    "late": -0.8, "bad": -1.6, "plain": -0.5, "stopped": -1.0, "complaints": -0.8,
    "complaint": -0.8, "issue": -0.9, "problem": -0.9,
}

NEGATIONS = {"not", "no", "never", "n't", "don't", "doesn't", "isn't", "wasn't",
             "wouldn't", "won't", "didn't"}

INTENSIFIERS = {"very": 1.5, "really": 1.4, "absolutely": 1.6, "completely": 1.5,
                 "totally": 1.4, "extremely": 1.6, "quite": 1.2, "pretty": 1.15,
                 "honestly": 1.1}


def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    return text.split()


def score_review(text, window=3):
    """
    Returns a polarity score for a review.
    Handles negation by flipping the polarity of a sentiment word if a
    negation word appears within `window` tokens before it, and boosts
    the score if an intensifier immediately precedes the sentiment word.
    """
    tokens = tokenize(text)
    score = 0.0
    matched_words = []

    for i, tok in enumerate(tokens):
        polarity = POSITIVE_WORDS.get(tok, NEGATIVE_WORDS.get(tok))
        if polarity is None:
            continue

        # check for negation in the preceding window
        preceding = tokens[max(0, i - window):i]
        negated = any(w in NEGATIONS or w.endswith("n't") for w in preceding)

        # check for intensifier immediately before
        intensity = 1.0
        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            intensity = INTENSIFIERS[tokens[i - 1]]

        word_score = polarity * intensity
        if negated:
            word_score *= -0.8  # flip and soften slightly (negation isn't a perfect mirror)

        score += word_score
        matched_words.append((tok, round(word_score, 2), negated))

    return score, matched_words


def classify(score, pos_threshold=0.5, neg_threshold=-0.5):
    if score >= pos_threshold:
        return "Positive"
    elif score <= neg_threshold:
        return "Negative"
    return "Neutral"


def main():
    df = pd.read_csv("reviews.csv")

    scores, labels, matched_all = [], [], []
    for text in df["review_text"]:
        s, matched = score_review(text)
        scores.append(round(s, 2))
        labels.append(classify(s))
        matched_all.append(matched)

    df["sentiment_score"] = scores
    df["sentiment"] = labels
    df.to_csv("reviews_with_sentiment.csv", index=False)

    print("=" * 60)
    print("SENTIMENT CLASSIFICATION RESULTS")
    print("=" * 60)
    counts = df["sentiment"].value_counts()
    print(counts.to_string())
    print(f"\nTotal reviews: {len(df)}")
    for label in ["Positive", "Negative", "Neutral"]:
        pct = counts.get(label, 0) / len(df) * 100
        print(f"  {label}: {pct:.1f}%")

    print("\nSample classifications:")
    for _, row in df.sample(8, random_state=3).iterrows():
        print(f"  [{row['sentiment']:>8} | score={row['sentiment_score']:>5}] {row['review_text']}")

    # word frequency of matched sentiment words (for a quick "top words" view)
    all_words = Counter()
    for matched in matched_all:
        for word, wscore, negated in matched:
            all_words[word] += 1
    top_words = all_words.most_common(15)
    print("\nTop sentiment-bearing words detected:")
    for w, c in top_words:
        print(f"  {w}: {c}")

    # -----------------------------------------------------------------
    # Visualizations
    # -----------------------------------------------------------------
    # 1. Sentiment distribution (bar)
    plt.figure(figsize=(7, 5))
    order = ["Positive", "Neutral", "Negative"]
    colors = {"Positive": "#16a34a", "Neutral": "#94a3b8", "Negative": "#dc2626"}
    counts_ordered = counts.reindex(order).fillna(0)
    plt.bar(counts_ordered.index, counts_ordered.values,
            color=[colors[l] for l in order])
    plt.title("Review Sentiment Distribution", fontsize=13, fontweight="bold")
    plt.ylabel("Number of Reviews")
    for i, v in enumerate(counts_ordered.values):
        plt.text(i, v + 1, int(v), ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig("charts/01_sentiment_distribution.png")
    plt.close()

    # 2. Sentiment share (pie)
    plt.figure(figsize=(6, 6))
    plt.pie(counts_ordered.values, labels=counts_ordered.index, autopct="%1.1f%%",
            colors=[colors[l] for l in order], startangle=90)
    plt.title("Sentiment Share", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("charts/02_sentiment_share.png")
    plt.close()

    # 3. Score distribution histogram
    plt.figure(figsize=(9, 5))
    sns.histplot(df["sentiment_score"], bins=30, kde=True, color="#2563eb")
    plt.axvline(0.5, color="green", linestyle="--", label="Positive threshold")
    plt.axvline(-0.5, color="red", linestyle="--", label="Negative threshold")
    plt.title("Distribution of Sentiment Scores", fontsize=13, fontweight="bold")
    plt.xlabel("Sentiment Score")
    plt.legend()
    plt.tight_layout()
    plt.savefig("charts/03_score_distribution.png")
    plt.close()

    # 4. Average sentiment by product
    prod_sentiment = df.groupby("product")["sentiment_score"].mean().sort_values()
    plt.figure(figsize=(9, 6))
    bar_colors = ["#dc2626" if v < 0 else "#16a34a" for v in prod_sentiment.values]
    plt.barh(prod_sentiment.index, prod_sentiment.values, color=bar_colors)
    plt.title("Average Sentiment Score by Product", fontsize=13, fontweight="bold")
    plt.xlabel("Average Sentiment Score")
    plt.axvline(0, color="black", linewidth=0.8)
    plt.tight_layout()
    plt.savefig("charts/04_sentiment_by_product.png")
    plt.close()

    print("\n4 charts saved to charts/ folder.")
    print("Full labeled dataset saved to reviews_with_sentiment.csv")


if __name__ == "__main__":
    main()
