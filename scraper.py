"""
Çok Kaynaklı RSS Üretici
Kullanım: python scraper.py
Çıktı: feeds/ klasöründe her site için ayrı .xml dosyası
"""

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import re
import os
import time
import urllib3
session = requests.Session()
session.headers.update(HEADERS)


OUTPUT_DIR = "feeds"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9",
}


# ── Yardımcı fonksiyonlar ─────────────────────────────────────────────────────

def get_page(url, timeout=20):
    try:
        r = session.get(url, timeout=timeout, verify=False)
        r.encoding = "utf-8"
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  ⚠️  Sayfa çekilemedi: {url} → {e}")
        return None


def parse_date(text):
    """Çeşitli Türkçe tarih formatlarını datetime'a çevirir."""
    if not text:
        return datetime.now(timezone.utc)
    text = text.strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%d %B %Y"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    m = re.search(r"(\d{2})[./](\d{2})[./](\d{4})", text)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), tzinfo=timezone.utc)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def make_feed(title, url, desc, lang="tr"):
    fg = FeedGenerator()
    fg.id(url)
    fg.title(title)
    fg.link(href=url, rel="alternate")
    fg.description(desc)
    fg.language(lang)
    fg.lastBuildDate(datetime.now(timezone.utc))
    return fg


def add_entry(fg, title, url, date):
    if not title or not url:
        return
    fe = fg.add_entry()
    fe.id(url)
    fe.title(title.strip())
    fe.link(href=url)
    fe.published(date)
    fe.updated(date)


def save_feed(fg, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fg.rss_file(path, pretty=True)
    print(f"  ✅ Kaydedildi: {path}")


# ── Scraper fonksiyonları ─────────────────────────────────────────────────────



def scrape_bddk1():
    """BDDK 1."""
    url = "https://www.bddk.org.tr/Mevzuat/Liste/56"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK1", url, "BDDK1")
    count = 0
    for a in soup.select("a[href*='/DokumanGetir/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

    print(f" 📌 {count} öğe bulundu.")
    save_feed(fg, "bddk1.xml")

def scrape_bddk2():
    """BDDK 2."""
    url = "https://www.bddk.org.tr/Mevzuat/Liste/55"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK2", url, "BDDK2")
    count = 0
    for a in soup.select("a[href*='/DokumanGetir/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

    print(f" 📌 {count} öğe bulundu.")
    save_feed(fg, "bddk2.xml")


def scrape_bddk3():
    """BDDK 3."""
    url = "https://www.bddk.org.tr/Duyuru/Liste/39"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK3", url, "BDDK3")
    count = 0
    for a in soup.select("a[href*='/Duyuru/Detay/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "bddk3.xml")




def scrape_bddk4():
    """BDDK 4."""
    url = "https://www.bddk.org.tr/Duyuru/Liste/40"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK4", url, "BDDK4")
    count = 0
    for a in soup.select("a[href*='/Duyuru/Detay/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "bddk4.xml")


def scrape_bddk5():
    """BDDK 5."""
    url = "https://www.bddk.org.tr/Duyuru/Liste/48"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK5", url, "BDDK5")
    count = 0
    for a in soup.select("a[href*='/Duyuru/Detay/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "bddk5.xml")


def scrape_bddk6():
    """BDDK 6."""
    url = "https://www.bddk.org.tr/Duyuru/Liste/197"
    base = "https://www.bddk.org.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("BDDK6", url, "BDDK6")
    count = 0
    for a in soup.select("a[href*='/Duyuru/Detay/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "bddk6.xml")



def scrape_kgk1():
    """KGK 1."""
    url = "https://www.kgk.gov.tr/Assignments/1/0/Duyurular"
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("KGK1", url, "KGK1")
    count = 0
    for a in soup.select("a[href*='/ContentAssignmentDetail/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "kgk1.xml")


def scrape_kgk2():
    """KGK 2."""
    url = "https://www.kgk.gov.tr/Assignments/1/0/Duyurular"
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("KGK2", url, "KGK2")
    count = 0
    for a in soup.select("a[href*='/Portalv2Uploads/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "kgk2.xml")


def scrape_kgk3():
    """KGK 3."""
    url = "https://www.kgk.gov.tr/Assignments/2/0/Son-Yayimlananlar"
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("KGK3", url, "KGK3")
    count = 0
    for a in soup.select("a[href*='/ContentAssignmentDetail/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "kgk3.xml")

def scrape_kgk4():
    """KGK 4."""
    url = "https://www.kgk.gov.tr/Assignments/2/0/Son-Yayimlananlar"
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("KGK4", url, "KGK4")
    count = 0
    for a in soup.select("a[href*='/Portalv2Uploads/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "kgk4.xml")

def scrape_kgk5():
    """KGK 5."""
    url = "https://www.kgk.gov.tr/Activities/6748/1/Faaliyetlerimiz"
    base = "https://www.kgk.gov.tr"
    soup = get_page(url)
    if not soup:
        return

    fg = make_feed("KGK5", url, "KGK5")
    count = 0
    for a in soup.select("a[href*='/ActivityDetail/']"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = a["href"]
        full_url = base + href if href.startswith("/") else href
        parent = a.find_parent()
        raw = parent.get_text(" ", strip=True) if parent else ""
        m = re.search(r"\d{2}[./]\d{2}[./]\d{4}", raw)
        date = parse_date(m.group() if m else None)
        add_entry(fg, title, full_url, date)
        count += 1

        print(f" 📌 {count} öğe bulundu.")
        save_feed(fg, "kgk5.xml")

# ── Ana akış ─────────────────────────────────────────────────────────────────

TASKS = [
 
        ("BDDK1",                  scrape_bddk1),
        ("BDDK2",                  scrape_bddk2),
        ("BDDK3",                  scrape_bddk3),
        ("BDDK4",                  scrape_bddk4),
        ("BDDK5",                  scrape_bddk5),
        ("BDDK6",                  scrape_bddk6),
("KGK1",                  scrape_kgk1),
("KGK2",                  scrape_kgk2),
("KGK3",                  scrape_kgk3),
("KGK4",                  scrape_kgk4),
("KGK5",                  scrape_kgk5),
]


def main():
    print(f"🚀 {len(TASKS)} kaynak taranıyor...\n")
    basarili = 0
    for name, fn in TASKS:
        print(f"⏳ {name}")
        try:
            fn()
            basarili += 1
        except Exception as e:
            print(f"  ❌ Hata: {e}")
        time.sleep(1)  # Sitelere aşırı yük bindirmemek için

    print(f"\n✅ Tamamlandı: {basarili}/{len(TASKS)} kaynak işlendi.")
    print(f"📁 Feed dosyaları: ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
