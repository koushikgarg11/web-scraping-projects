"""
Project 1: Quotes Scraper
Scrapes quotes from https://quotes.toscrape.com
Saves to CSV and JSON
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time


def scrape_quotes(max_pages=5):
    base_url = "https://quotes.toscrape.com"
    all_quotes = []
    page = 1

    while page <= max_pages:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping page {page}...")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.find_all("div", class_="quote")

        if not quote_blocks:
            print("No more quotes found.")
            break

        for block in quote_blocks:
            text = block.find("span", class_="text").get_text(strip=True)
            author = block.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in block.find_all("a", class_="tag")]
            all_quotes.append({"quote": text, "author": author, "tags": tags})

        page += 1
        time.sleep(1)  # Be polite – don't hammer the server

    return all_quotes


def save_to_csv(quotes, filename="quotes.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
        writer.writeheader()
        for q in quotes:
            writer.writerow({"quote": q["quote"], "author": q["author"], "tags": ", ".join(q["tags"])})
    print(f"Saved {len(quotes)} quotes to {filename}")


def save_to_json(quotes, filename="quotes.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(quotes)} quotes to {filename}")


if __name__ == "__main__":
    quotes = scrape_quotes(max_pages=5)
    save_to_csv(quotes)
    save_to_json(quotes)

    print(f"\nTotal quotes scraped: {len(quotes)}")
    print("\nSample:")
    print(f"  Quote : {quotes[0]['quote']}")
    print(f"  Author: {quotes[0]['author']}")
    print(f"  Tags  : {', '.join(quotes[0]['tags'])}")

