from .utils import get_page, resolve_url

def get_categories(base_url):
    """Find all categories from main page"""
    soup = get_page(base_url)
    if not soup:
        return []

    categories = []
    nav_items = soup.select("ul.nav-second-level li a")

    for item in nav_items:
        href = item.get("href")
        name = item.text.strip()
        if href and "/test-sites/e-commerce/static" in href:
            categories.append({
                "name": name,
                "url": resolve_url(href)
            })

    return categories

def get_product_links(url, category, subcategory, page_num=1):
    """Get all product links from a listing page"""
    soup = get_page(url)
    if not soup:
        return [], None

    links = []
    products = soup.select("div.thumbnail")

    for product in products:
        a_tag = product.select_one("a.title")
        if a_tag:
            links.append({
                "url": resolve_url(a_tag.get("href")),
                "category": category,
                "subcategory": subcategory,
                "page_num": page_num
            })

    # Check for next page
    next_btn = soup.select_one("li.next a")
    next_url = resolve_url(next_btn.get("href")) if next_btn else None

    return links, next_url

def crawl_all_products(base_url):
    """Crawl entire site and return all product links"""
    all_links = []
    categories = get_categories(base_url)

    print(f"Found {len(categories)} categories/subcategories")

    for cat in categories:
        print(f"Crawling: {cat['name']} → {cat['url']}")
        page_url = cat['url']
        page_num = 1

        # detect category vs subcategory from URL depth
        parts = cat['url'].rstrip('/').split('/')
        if len(parts) >= 8:
            category = parts[-2]
            subcategory = parts[-1]
        else:
            category = parts[-1]
            subcategory = parts[-1]

        while page_url:
            links, next_url = get_product_links(
                page_url, category, subcategory, page_num
            )
            all_links.extend(links)
            print(f"  Page {page_num}: {len(links)} products found")
            page_url = next_url
            page_num += 1

    return all_links