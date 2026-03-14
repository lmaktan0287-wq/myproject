from .utils import get_page, resolve_url

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

# Known correct structure of the website
SITE_STRUCTURE = {
    "Computers": {
        "url": f"{BASE_URL}/computers",
        "subcategories": {
            "Laptops": f"{BASE_URL}/computers/laptops",
            "Tablets": f"{BASE_URL}/computers/tablets",
        }
    },
    "Phones": {
        "url": f"{BASE_URL}/phones",
        "subcategories": {
            "Touch": f"{BASE_URL}/phones/touch",
        }
    }
}

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
            href = a_tag.get("href", "")
            if href:
                links.append({
                    "url": resolve_url(href),
                    "category": category,
                    "subcategory": subcategory,
                    "page_num": page_num
                })

    # Check for next page button
    next_btn = soup.select_one("a[rel=next]")
    next_url = resolve_url(next_btn.get("href")) if next_btn else None

    return links, next_url

def crawl_all_products(base_url):
    """Crawl entire site using known structure"""
    all_links = []

    for category_name, category_data in SITE_STRUCTURE.items():
        print(f"\n📂 Category: {category_name}")

        for subcat_name, subcat_url in category_data["subcategories"].items():
            print(f"  📁 Subcategory: {subcat_name}")
            page_url = subcat_url
            page_num = 1

            while page_url:
                links, next_url = get_product_links(
                    page_url,
                    category_name,
                    subcat_name,
                    page_num
                )
                all_links.extend(links)
                print(f"    Page {page_num}: {len(links)} products found")
                page_url = next_url
                page_num += 1

    return all_links