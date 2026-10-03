"""
generate_reviews.py
Creates a synthetic dataset of product reviews (text only, no pre-labeled
sentiment) for Task 4 - Sentiment Analysis. sentiment_analysis.py then
classifies these reviews using a custom lexicon.
"""

import random
import csv

random.seed(7)

positive_templates = [
    "I absolutely love this {p}, it works perfectly!",
    "This {p} exceeded my expectations, highly recommend.",
    "Great quality {p} for the price, very happy with it.",
    "Fast shipping and the {p} is fantastic.",
    "Best {p} I've ever bought, excellent value.",
    "Superb build quality, this {p} is amazing.",
    "The {p} works great and looks wonderful.",
    "Really impressed with this {p}, will buy again.",
    "Excellent customer service and a lovely {p}.",
    "This {p} is a perfect fit for my needs, love it.",
]

negative_templates = [
    "This {p} broke after two days, terrible quality.",
    "Very disappointed with this {p}, waste of money.",
    "The {p} arrived damaged and customer service was unhelpful.",
    "Awful experience, this {p} does not work as advertised.",
    "I hate this {p}, it stopped working almost immediately.",
    "Poor quality {p}, would not recommend to anyone.",
    "The {p} is cheaply made and feels flimsy.",
    "Worst purchase ever, this {p} is a complete waste.",
    "This {p} is slow, buggy, and frustrating to use.",
    "Terrible {p}, arrived late and completely broken.",
]

neutral_templates = [
    "The {p} is okay, does what it says, nothing special.",
    "This {p} works fine, average quality for the price.",
    "The {p} arrived on time, packaging was standard.",
    "It's a decent {p}, does the job but nothing more.",
    "The {p} is fine, not great but not bad either.",
    "Received the {p} as described, no complaints so far.",
    "This {p} is functional but a bit plain looking.",
    "An acceptable {p} for casual use.",
]

# a few reviews with negation / mixed sentiment to test the lexicon's robustness
tricky_templates = [
    "This {p} is not bad at all, pretty good actually.",
    "I don't love this {p}, but it's not terrible either.",
    "Not the best {p} I've owned, but it's decent.",
    "This {p} isn't great, honestly quite disappointing.",
    "I wouldn't say this {p} is amazing, but it's not awful.",
]

products = ["headphones", "blender", "laptop bag", "office chair", "phone case",
            "coffee maker", "backpack", "desk lamp", "wireless mouse", "water bottle",
            "yoga mat", "bluetooth speaker", "running shoes", "tablet stand", "keyboard"]

rows = []
review_id = 1

for template_group, count in [(positive_templates, 60), (negative_templates, 55),
                                (neutral_templates, 40), (tricky_templates, 25)]:
    for _ in range(count):
        template = random.choice(template_group)
        product = random.choice(products)
        text = template.format(p=product)
        rows.append({"review_id": review_id, "product": product, "review_text": text})
        review_id += 1

random.shuffle(rows)
for i, row in enumerate(rows, start=1):
    row["review_id"] = i

with open("reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["review_id", "product", "review_text"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} reviews -> reviews.csv")
