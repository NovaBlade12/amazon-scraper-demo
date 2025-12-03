#!/usr/bin/env python3
# src/scraper.py
# Simple demo scraper (educational). Use carefully and politely.

import time
import csv
import argparse
import requests
from bs4 import BeautifulSoup
from random import uniform

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

def fetch_html(url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            return r.text
        except Exception as e:
            if attempt == retries:
                print(f"[ERROR] Failed to fetch {url}: {e}")
                return ""
            wait = 1.0 * attempt + uniform(0, 0.5)
            time.sleep(wait)

def extract_title(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    # Try Amazon product title selector first
    title_tag = soup.select_one("#productTitle") or soup.select_one("h1") or soup.title
    if title_tag:
        return title_tag.get_text(strip=True)
    return ""

def scrape_urls(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["url", "title"])
        writer.writeheader()

        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] Scraping: {url}")
            html = fetch_html(url)
            title = extract_title(html)
            writer.writerow({"url": url, "title": title})
            # polite delay between requests
            time.sleep(uniform(1.5, 3.0))

    print(f"Done. Saved results to: {output_file}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Simple demo scraper")
    ap.add_argument("--input", default="examples/urls.txt", help="input file with one URL per line")
    ap.add_argument("--out", default="examples/sample_output.csv", help="output CSV file")
    args = ap.parse_args()
    scrape_urls(args.input, args.out)
