# CodeAlpha_WebScraping

**Task:** Web Scraping (Task 1)
**Tools:** Python, BeautifulSoup, requests, lxml

## What this does
Extracts structured product data (name, price, rating, review count, availability)
from an HTML product listing page and saves it as a clean CSV file.

## ⚠️ About the data source
This script was built in a sandboxed environment with no outbound internet access,
so it scrapes `sample_page.html`, a local page structured just like a real
e-commerce listing (same tags/classes you'd find on an actual site).

The parsing logic (`parse_products()`) is written to work on any page with that
structure. To scrape a **real, live website**, do this:

1. Open `scrape_products.py`.
2. In `main()`, replace:
   ```python
   html = load_local_html()
   ```
   with:
   ```python
   html = fetch_live_html("https://your-target-site.com/products")
   ```
3. Update the CSS selectors in `parse_products()` (`.product-card`, `.product-name`,
   `.price`, etc.) to match the actual target site's HTML structure — open the
   page's DevTools (F12) to find the right class/tag names.
4. Always check the target site's `robots.txt` and terms of service before scraping.

## How to run
```bash
pip install beautifulsoup4 requests lxml
python scrape_products.py
```

## Output
`scraped_products.csv` — 8 products with price, rating, review count, and
stock status, plus a console summary (average price, average rating, stock %).

## Sample output
```
product_name,price,rating,review_count,availability,in_stock
Wireless Noise-Cancelling Headphones,149.99,4.5,2341,In Stock,True
27-inch 4K Monitor,329.0,4.7,1058,In Stock,True
...
```

---
*Submitted as part of the CodeAlpha Data Analytics Internship.*
