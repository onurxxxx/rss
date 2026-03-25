"""
TEK XML RSS ÜRETİCİ
Çıktı: feeds/combined.xml
"""

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone, timedelta
import re
import os
import time

OUTPUT_DIR = "feeds"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "tr-TR,tr;q=0.9",
}

ALL_ITEMS = []
SEEN = set()

# -------------------------------------------------
# YARDIMCI
# -------------------------------------------------

def get_page(url, timeout=20):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = "utf-8"
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print("Sayfa alınamadı:", url, e)
        return None


def parse_date(text):
    if not text:
        return datetime.now(timezone.utc)

    text = text.strip()

    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except:
            pass

    return datetime.now(timezone.utc)


def add_entry(title, url, date):
    if url in SEEN:
        return
    SEEN.add(url)

    ALL_ITEMS.append({
        "title": title,
        "url": url,
        "date": date
    })


# -------------------------------------------------
# BDDK TABLO SCRAPER (DÜZELTİLDİ)
# -------------------------------------------------

def scrape_bddk_table(url, tag):
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    rows = soup.select("table tr")
    count = 0

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        date_text = cols[0].get_text(strip=True)
        a = cols[1].find("a")

        if not a:
            continue

        title = a.get_text(strip=True)
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        date = parse_date(date_text)

        add_entry(f"[BDDK] {title}", full_url, date)
        count += 1

    print(f"BDDK {tag}: {count}")


def scrape_bddk_duyuru(url):
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    rows = soup.select("table tr")
    count = 0

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        date_text = cols[0].get_text(strip=True)
        a = cols[1].find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        date = parse_date(date_text)

        add_entry(f"[BDDK] {title}", full_url, date)
        count += 1

    print(f"BDDK Duyuru: {count}")


# -------------------------------------------------
# KGK
# -------------------------------------------------

def scrape_kgk(url, selector, tag):
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    count = 0

    for a in soup.select(selector):
        title = a.get_text(strip=True)
        if len(title) < 5:
            continue

        href = a["href"]
        full_url = base + href if href.startswith("/") else href

        raw = a.find_parent().get_text(" ", strip=True)
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)

        add_entry(f"[KGK] {title}", full_url, date)
        count += 1

    print(f"{tag}: {count}")


# -------------------------------------------------
# FEED
# -------------------------------------------------

def build_feed():
    fg = FeedGenerator()
    fg.title("Regülasyon Feed")
    fg.link(href="https://localhost/")
    fg.description("BDDK + KGK Tek Feed")

    items = sorted(ALL_ITEMS, key=lambda x: x["date"], reverse=True)

    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    items = [i for i in items if i["date"] >= cutoff]
    items = items[:300]

    for i in items:
        fe = fg.add_entry()
        fe.id(i["url"])
        fe.title(i["title"])
        fe.link(href=i["url"])
        fe.published(i["date"])
        fe.updated(i["date"])

    fg.rss_file("feeds/combined.xml", pretty=True)
    print("combined.xml oluşturuldu")


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():
    TASKS = [
        lambda: scrape_bddk_table("https://www.bddk.org.tr/Mevzuat/Liste/56", "Mevzuat56"),
        lambda: scrape_bddk_table("https://www.bddk.org.tr/Mevzuat/Liste/55", "Mevzuat55"),
        lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/39"),
        lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/40"),
        lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/48"),
        lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/197"),
        lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/1/0/Duyurular", "a[href*='/ContentAssignmentDetail/']", "KGK1"),
        lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/2/0/Son-Yayimlananlar", "a[href*='/ContentAssignmentDetail/']", "KGK2"),
    ]

    for task in TASKS:
        task()
        time.sleep(1)

    build_feed()


if __name__ == "__main__":
    main()
