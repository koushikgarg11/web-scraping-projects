# 🕷️ Web Scraping & API Data Extraction Projects

A collection of 5 beginner-friendly Python projects covering web scraping and API data extraction.
Built as part of Task 1: Web Scraping & API Learning.

---

## 📁 Project Structure

```
web-scraping-projects/
├── requirements.txt
├── README.md
├── project1_quotes/        ← BeautifulSoup scraper (quotes.toscrape.com)
│   └── scraper.py
├── project2_weather/       ← REST API (Open-Meteo, no key needed)
│   └── weather_api.py
├── project3_books/         ← Multi-page scraper with data analysis
│   └── books_scraper.py
├── project4_hn_news/       ← JSON API (Hacker News Firebase API)
│   └── hn_scraper.py
└── project5_github_trending/  ← Advanced scraper with headers/filters
    └── github_trending.py
```

---

## 🐧 Ubuntu Step-by-Step Setup Guide

### Step 1 — Update your system

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2 — Install Python 3 and pip

```bash
sudo apt install python3 python3-pip python3-venv -y
python3 --version   # should print Python 3.10+ 
```

### Step 3 — Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/web-scraping-projects.git
cd web-scraping-projects
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 4 — Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` in your terminal — this means the environment is active.

### Step 5 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs: `requests`, `beautifulsoup4`, `lxml`

---

## 🚀 Running Each Project

### Project 1 — Quotes Scraper

```bash
cd project1_quotes
python3 scraper.py
```

**What it does:**
- Scrapes quotes from `https://quotes.toscrape.com` (a legal practice site)
- Collects: quote text, author name, and tags
- Saves results to `quotes.csv` and `quotes.json`
- Scrapes 5 pages (~50 quotes)

**Key concepts learned:**
- `requests.get()` to fetch HTML pages
- `BeautifulSoup` to parse HTML and find elements by class
- Pagination (looping through pages)
- Writing CSV and JSON files

---

### Project 2 — Weather API

```bash
cd ../project2_weather
python3 weather_api.py
```

**What it does:**
- Fetches current weather + 7-day forecast for Delhi, London, New York
- Uses **Open-Meteo** (free, no API key required!)
- First geocodes city names → coordinates, then fetches weather
- Saves each city's data to a JSON file

**Key concepts learned:**
- Working with REST APIs and query parameters
- Chaining two API calls (geocoding → weather)
- Parsing nested JSON responses
- `response.raise_for_status()` for error handling

---

### Project 3 — Books Price & Rating Scraper

```bash
cd ../project3_books
python3 books_scraper.py
```

**What it does:**
- Scrapes `https://books.toscrape.com` (10 pages, ~200 books)
- Collects: title, price (£), star rating, availability
- Shows top-rated books and cheapest books in terminal
- Saves to `books.csv`

**Key concepts learned:**
- Extracting data from CSS classes
- Converting word-based ratings ("Three") to numbers
- Sorting and filtering scraped data
- Polite scraping with `time.sleep()`

---

### Project 4 — Hacker News Top Stories

```bash
cd ../project4_hn_news
python3 hn_scraper.py
```

**What it does:**
- Uses the official Hacker News Firebase JSON API
- Fetches top 50 stories, filters by minimum score
- Shows: title, author, score, comment count, timestamp, URL
- Saves to both CSV and JSON

**Key concepts learned:**
- Using official public APIs (no scraping needed)
- Making multiple API calls efficiently
- Filtering and sorting API results
- `datetime.fromtimestamp()` to convert Unix timestamps

---

### Project 5 — GitHub Trending Scraper

```bash
cd ../project5_github_trending
python3 github_trending.py
```

**What it does:**
- Scrapes `https://github.com/trending` for all languages
- Also scrapes Python-specific trending repos (weekly)
- Collects: repo name, description, language, stars, forks, stars today
- Saves to CSV and JSON

**Key concepts learned:**
- Adding `User-Agent` headers to avoid blocks
- Scraping complex real-world HTML structures
- Parameterized URLs (language filter, time range)
- Handling missing data gracefully

---

## 📤 Pushing to GitHub

### First-time setup

```bash
# Configure git (only once)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Create a new repo on GitHub
1. Go to https://github.com/new
2. Name it `web-scraping-projects`
3. Keep it public, don't add README (we have one)
4. Click **Create repository**

### Push your code

```bash
cd ~/web-scraping-projects     # go to project root
git init
git add .
git commit -m "Add 5 web scraping projects - Task 1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/web-scraping-projects.git
git push -u origin main
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: requests` | Run `pip install -r requirements.txt` inside `(venv)` |
| `Permission denied` | Never use `sudo pip` — use venv instead |
| `ConnectionError` | Check internet; the target site may be down |
| `venv` not activating | Make sure you're in the right folder; try `python3 -m venv venv` again |
| GitHub push rejected | Run `git pull origin main --rebase` first |

---

## 🧠 Tools Used

| Tool | Purpose |
|---|---|
| `requests` | HTTP requests (GET pages/APIs) |
| `beautifulsoup4` | Parse and extract HTML content |
| `lxml` | Fast HTML parser used by BeautifulSoup |
| Open-Meteo API | Free weather API, no key needed |
| HN Firebase API | Official Hacker News JSON API |

---

## 📚 Learning Resources

- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Docs](https://requests.readthedocs.io/)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- [HN API Docs](https://github.com/HackerNews/API)
- [Web Scraping Ethics](https://www.zyte.com/learn/web-scraping-best-practices/)

---

## ⚖️ Legal & Ethics Note

All projects scrape **legal practice sites** (`toscrape.com`) or use **official public APIs**.
Always check a site's `robots.txt` and Terms of Service before scraping.
Use `time.sleep()` to avoid overloading servers.
