"""
Project 5: GitHub Trending Repositories Scraper
Scrapes https://github.com/trending
Extracts repo name, description, language, stars, forks
Supports filtering by language
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_trending(language="", time_range="daily"):
    """
    language   : e.g. 'python', 'javascript', '' for all
    time_range : 'daily', 'weekly', 'monthly'
    """
    url = f"https://github.com/trending/{language}?since={time_range}"
    print(f"Fetching: {url}")

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    repo_list = soup.find_all("article", class_="Box-row")

    repos = []
    for repo in repo_list:
        # Repo full name
        name_tag = repo.find("h2")
        full_name = name_tag.get_text(strip=True).replace("\n", "").replace(" ", "") if name_tag else ""

        # Description
        desc_tag = repo.find("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Language
        lang_tag = repo.find("span", itemprop="programmingLanguage")
        language_used = lang_tag.get_text(strip=True) if lang_tag else "Unknown"

        # Stars
        stars_tags = repo.find_all("a", class_="Link--muted")
        stars = stars_tags[0].get_text(strip=True).replace(",", "") if len(stars_tags) > 0 else "0"
        forks = stars_tags[1].get_text(strip=True).replace(",", "") if len(stars_tags) > 1 else "0"

        # Stars gained today
        stars_today_tag = repo.find("span", class_="d-inline-block float-sm-right")
        stars_today = stars_today_tag.get_text(strip=True) if stars_today_tag else ""

        repos.append({
            "full_name": full_name,
            "description": description,
            "language": language_used,
            "stars": stars,
            "forks": forks,
            "stars_today": stars_today,
            "url": f"https://github.com/{full_name}",
        })

    return repos


def save_csv(repos, filename="github_trending.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["full_name", "description", "language", "stars", "forks", "stars_today", "url"])
        writer.writeheader()
        writer.writerows(repos)
    print(f"Saved {len(repos)} repos to {filename}")


def save_json(repos, filename="github_trending.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2)
    print(f"Saved to {filename}")


def display_repos(repos):
    print(f"\n{'='*70}")
    print(f"  GitHub Trending  |  {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}")
    print(f"{'#':<4} {'Stars':>8} {'Forks':>7}  {'Language':<14} Repo")
    print(f"{'-'*70}")
    for i, r in enumerate(repos, 1):
        name = r["full_name"][:35]
        print(f"{i:<4} {r['stars']:>8} {r['forks']:>7}  {r['language'][:13]:<14} {name}")
        if r["description"]:
            print(f"       {r['description'][:65]}")
        if r["stars_today"]:
            print(f"       ⭐ {r['stars_today']}")
        print()


if __name__ == "__main__":
    # Scrape all languages
    all_repos = scrape_trending(language="", time_range="daily")
    display_repos(all_repos)
    save_csv(all_repos)
    save_json(all_repos)

    # Also scrape Python-specific trending
    print("\n--- Python Trending ---")
    python_repos = scrape_trending(language="python", time_range="weekly")
    display_repos(python_repos)
    save_csv(python_repos, "github_trending_python.csv")

