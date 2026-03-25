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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "tr-TR,tr;q=0.9",
}

# ─────────────────────────────────────────────────────────────
# GLOBAL STORAGE
# ─────────────────────────────────────────────────────────────

ALL_ITEMS = []
SEEN = set()

# ─────────────────────────────────────────────────────────────
# YARDIMCI
# ─────────────────────────────────────────────────────────────

def get_page(url, timeout=20):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = "utf-8"
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  ⚠️  Sayfa çekilemedi: {url} → {e}")
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

    m = re.search(r"(\d{2})[./](\d{2})[./](\d{4})", text)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), tzinfo=timezone.utc)
        except:
            pass

    return datetime.now(timezone.utc)


def add_entry(title, url, date):
    if not title or not url:
        return
    if url in SEEN:
        return
    SEEN.add(url)

    ALL_ITEMS.append({
        "title": title.strip(),
        "url": url,
        "date": date
    })


def save_feed(fg, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fg.rss_file(path, pretty=True)
    print(f"  ✅ Kaydedildi: {path}")


# ─────────────────────────────────────────────────────────────
# SCRAPERS
# ─────────────────────────────────────────────────────────────

def scrape_bddk1():
    url = "https://www.bddk.org.tr/Mevzuat/Liste/56"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    count = 0
    for a in soup.select("a[href*='/DokumanGetir/']"):
        title = a.get_text(strip=True)
        if len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        raw = a.find_parent().get_text(" ", strip=True)
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(f"[BDDK] {title}", full_url, date)
        count += 1

    print(f" 📌 BDDK1: {count} öğe")


def scrape_bddk2():
    url = "https://www.bddk.org.tr/Mevzuat/Liste/55"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    count = 0
    for a in soup.select("a[href*='/DokumanGetir/']"):
        title = a.get_text(strip=True)
        if len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        raw = a.find_parent().get_text(" ", strip=True)
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(f"[BDDK] {title}", full_url, date)
        count += 1

    print(f" 📌 BDDK2: {count} öğe")


def scrape_bddk_duyuru(url):
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    count = 0
    for a in soup.select("a[href*='/Duyuru/Detay/']"):
        title = a.get_text(strip=True)
        if len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        raw = a.find_parent().get_text(" ", strip=True)
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(f"[BDDK] {title}", full_url, date)
        count += 1

    print(f" 📌 BDDK Duyuru: {count} öğe")


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

    print(f" 📌 {tag}: {count} öğe")


# ─────────────────────────────────────────────────────────────
# FEED BUILD
# ─────────────────────────────────────────────────────────────

def build_feed():
    fg = FeedGenerator()
    fg.title("Regülasyon & Bankacılık – Tüm Akış")
    fg.link(href="https://localhost/combined", rel="alternate")
    fg.description("Birleşik RSS Feed")

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

    save_feed(fg, "combined.xml")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    TASKS = [
        ("BDDK1", scrape_bddk1),
        ("BDDK2", scrape_bddk2),
        ("BDDK Duyuru 39", lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/39")),
        ("BDDK Duyuru 40", lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/40")),
        ("BDDK Duyuru 48", lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/48")),
        ("BDDK Duyuru 197", lambda: scrape_bddk_duyuru("https://www.bddk.org.tr/Duyuru/Liste/197")),
        ("KGK1", lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/1/0/Duyurular", "a[href*='/ContentAssignmentDetail/']", "KGK1")),
        ("KGK2", lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/1/0/Duyurular", "a[href*='/Portalv2Uploads/']", "KGK2")),
        ("KGK3", lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/2/0/Son-Yayimlananlar", "a[href*='/ContentAssignmentDetail/']", "KGK3")),
        ("KGK4", lambda: scrape_kgk("https://www.kgk.gov.tr/Assignments/2/0/Son-Yayimlananlar", "a[href*='/Portalv2Uploads/']", "KGK4")),
        ("KGK5", lambda: scrape_kgk("https://www.kgk.gov.tr/Activities/6748/1/Faaliyetlerimiz", "a[href*='/ActivityDetail/']", "KGK5")),
    ]

    print(f"🚀 {len(TASKS)} kaynak taranıyor...\n")

    for name, fn in TASKS:
        print(f"⏳ {name}")
        try:
            fn()
        except Exception as e:
            print(f"  ❌ Hata: {e}")
        time.sleep(1)

    build_feed()

    print("\n✅ Tamamlandı.")
    print("📁 Çıktı: feeds/combined.xml")


if __name__ == "__main__":
    main()
