import requests
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io"

def get_page(url):
    """Safely fetch a page, return None if failed"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Failed to load {url}: {e}")
        return None

def resolve_url(href):
    """Convert relative URL to absolute URL"""
    if not href:
        return None
    if href.startswith("http"):
        return href
    return BASE_URL + href

def clean_text(text):
    """Remove extra spaces and newlines"""
    if not text:
        return ""
    return text.strip()

def clean_price(price_text):
    """Convert price like '$12.99' to float 12.99"""
    try:
        return float(price_text.replace("$", "").strip())
    except:
        return 0.0

def deduplicate(products):
    """Remove duplicate products by URL"""
    seen = set()
    unique = []
    duplicates_removed = 0
    for product in products:
        url = product.get('product_url')
        if url not in seen:
            seen.add(url)
            unique.append(product)
        else:
            duplicates_removed += 1
    print(f"Duplicates removed: {duplicates_removed}")
    return unique