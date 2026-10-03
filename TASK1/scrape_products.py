"""
scrape_products.py
CodeAlpha Data Analytics Internship - Task 1: Web Scraping

Scrapes product data (name, price, rating, reviews, availability)
using BeautifulSoup and saves it to a clean CSV dataset.

NOTE: This sandbox environment has no outbound internet access, so this
script scrapes a local HTML page (sample_page.html) that mimics a real
e-commerce listing page. The scraping logic itself is identical to what
you'd use on a live site - to point it at a real URL, just replace the
`load_local_html()` call with the `fetch_live_html(url)` function below
(requests + your target URL), which is already included and ready to use
on a machine with internet access.
"""

import re
import csv
import requests
from bs4 import BeautifulSoup

LOCAL_FILE = "sample_page.html"
OUTPUT_CSV = "scraped_products.csv"


def load_local_html(path=LOCAL_FILE):
    """Read HTML from a local file (used in this offline sandbox)."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def fetch_live_html(url, timeout=10):
    """
    Fetch HTML from a real website. Use this instead of load_local_html()
    when running with internet access, e.g.:
        html = fetch_live_html("https://example-shop.com/electronics")
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CodeAlphaBot/1.0)"}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_products(html):
    """Parse product cards out of the page HTML into a list of dicts."""
    soup = BeautifulSoup(html, "lxml")
    products = []

    for card in soup.select(".product-card"):
        name = card.select_one(".product-name").get_text(strip=True)

        price_text = card.select_one(".price").get_text(strip=True)
        price = float(re.sub(r"[^\d.]", "", price_text))

        rating = float(card.select_one(".rating").get_text(strip=True))

        reviews_text = card.select_one(".reviews-count").get_text(strip=True)
        review_count = int(re.sub(r"[^\d]", "", reviews_text))

        availability = card.select_one(".availability").get_text(strip=True)
        in_stock = availability.lower() != "out of stock"

        products.append({
            "product_name": name,
            "price": price,
            "rating": rating,
            "review_count": review_count,
            "availability": availability,
            "in_stock": in_stock,
        })

    return products


def save_csv(products, path=OUTPUT_CSV):
    if not products:
        print("No products found.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to {path}")


def main():
    html = load_local_html()
    # For a live site instead, use:
    # html = fetch_live_html("https://your-target-site.com/products")

    products = parse_products(html)
    save_csv(products)

    print("\nPreview:")
    for p in products[:5]:
        print(f"  {p['product_name']:<35} ${p['price']:<8} "
              f"rating={p['rating']} reviews={p['review_count']} "
              f"({p['availability']})")

    # quick summary stats, since raw scraped data is more useful once summarized
    prices = [p["price"] for p in products]
    ratings = [p["rating"] for p in products]
    print(f"\nTotal products scraped : {len(products)}")
    print(f"Average price          : ${sum(prices)/len(prices):.2f}")
    print(f"Average rating          : {sum(ratings)/len(ratings):.2f}")
    print(f"In stock                : {sum(p['in_stock'] for p in products)}/{len(products)}")


if __name__ == "__main__":
    main()
