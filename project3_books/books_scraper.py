"""
Project 3: Books to Scrape - Price & Rating Scraper
Scrapes https://books.toscrape.com
Extracts title, price, rating, availability
Saves to CSV and shows top-rated books
"""

import requests
from bs4 import BeautifulSoup
import csv
import time


RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
BASE_URL = "https://books.toscrape.com/catalogue/"


def scrape_books(max_pages=10):
    books = []
    page = 1

    while page <= max_pages:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Scraping page {page}...")

        response = requests.get(url)
        if response.status_code == 404:
            print("Reached last page.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")

        for item in items:
            title = item.h3.a["title"]
            price = item.find("p", class_="price_color").get_text(strip=True).replace("Â", "")
            rating_word = item.p["class"][1]
            rating = RATING_MAP.get(rating_word, 0)
            availability = item.find("p", class_="instock availability")
            in_stock = "In stock" if availability and "In stock" in availability.get_text() else "Out of stock"

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": in_stock,
            })

        page += 1
        time.sleep(0.5)

    return books


def save_to_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "availability"])
        writer.writeheader()
        writer.writerows(books)
    print(f"\nSaved {len(books)} books to {filename}")


def show_top_rated(books, n=10):
    top = sorted(books, key=lambda x: x["rating"], reverse=True)[:n]
    print(f"\nTop {n} Highest-Rated Books:")
    print(f"{'#':<4} {'Rating':<8} {'Price':<10} Title")
    print("-" * 70)
    for i, book in enumerate(top, 1):
        print(f"{i:<4} {'★' * book['rating']:<8} {book['price']:<10} {book['title'][:50]}")


def show_cheapest(books, n=10):
    def parse_price(p):
        return float(p.replace("£", "").replace("Â", "").strip())

    cheapest = sorted(books, key=lambda x: parse_price(x["price"]))[:n]
    print(f"\nTop {n} Cheapest Books:")
    print(f"{'#':<4} {'Price':<10} {'Rating':<8} Title")
    print("-" * 70)
    for i, book in enumerate(cheapest, 1):
        print(f"{i:<4} {book['price']:<10} {'★' * book['rating']:<8} {book['title'][:50]}")


if __name__ == "__main__":
    books = scrape_books(max_pages=10)
    save_to_csv(books)
    show_top_rated(books)
    show_cheapest(books)
    print(f"\nTotal books scraped: {len(books)}")

