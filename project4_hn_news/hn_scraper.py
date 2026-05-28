"""
Project 4: Hacker News Top Stories API
Uses the official HN Firebase API (no scraping needed, fully legal)
Fetches top stories, filters by score, saves results
"""

import requests
import json
import csv
from datetime import datetime
import time


HN_API = "https://hacker-news.firebaseio.com/v0"


def get_top_story_ids(limit=50):
    url = f"{HN_API}/topstories.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[:limit]


def get_story_details(story_id):
    url = f"{HN_API}/item/{story_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_top_stories(limit=50, min_score=100):
    print(f"Fetching top {limit} HN stories (min score: {min_score})...")
    ids = get_top_story_ids(limit)

    stories = []
    for i, story_id in enumerate(ids, 1):
        print(f"  Fetching story {i}/{len(ids)}...", end="\r")
        try:
            story = get_story_details(story_id)
            if story and story.get("type") == "story":
                score = story.get("score", 0)
                if score >= min_score:
                    stories.append({
                        "id": story_id,
                        "title": story.get("title", ""),
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "score": score,
                        "by": story.get("by", ""),
                        "comments": story.get("descendants", 0),
                        "time": datetime.fromtimestamp(story.get("time", 0)).strftime("%Y-%m-%d %H:%M"),
                    })
        except Exception as e:
            print(f"\nError fetching story {story_id}: {e}")
        time.sleep(0.05)

    # Sort by score
    stories.sort(key=lambda x: x["score"], reverse=True)
    print(f"\nFound {len(stories)} stories with score >= {min_score}")
    return stories


def save_to_csv(stories, filename="hn_top_stories.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "url", "score", "by", "comments", "time"])
        writer.writeheader()
        writer.writerows(stories)
    print(f"Saved to {filename}")


def save_to_json(stories, filename="hn_top_stories.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2)
    print(f"Saved to {filename}")


def display_stories(stories, n=20):
    print(f"\n{'='*70}")
    print(f"  Hacker News Top Stories  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")
    print(f"{'#':<4} {'Score':>6} {'Cmts':>5}  Title")
    print(f"{'-'*70}")
    for i, s in enumerate(stories[:n], 1):
        title = s["title"][:55] + "..." if len(s["title"]) > 55 else s["title"]
        print(f"{i:<4} {s['score']:>6} {s['comments']:>5}  {title}")
        print(f"       by {s['by']} | {s['time']}")
        print(f"       {s['url'][:65]}")
        print()


if __name__ == "__main__":
    stories = fetch_top_stories(limit=50, min_score=50)
    display_stories(stories, n=15)
    save_to_csv(stories)
    save_to_json(stories)

