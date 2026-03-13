from scraper.crawler import crawl_all_products
from scraper.parsers import parse_product
from scraper.exporters import export_products, export_summary
from scraper.utils import deduplicate

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def main():
    print("🚀 Starting scraper...")

    # Step 1 - Crawl all product links
    print("\n📂 Discovering categories and products...")
    product_links = crawl_all_products(BASE_URL)
    print(f"\nTotal product links found: {len(product_links)}")

    # Step 2 - Visit each product page
    print("\n🔍 Scraping product details...")
    products = []
    for i, link in enumerate(product_links):
        print(f"  Scraping {i+1}/{len(product_links)}: {link['url']}")
        product = parse_product(link)
        if product:
            products.append(product)

    # Step 3 - Deduplicate
    print("\n🧹 Removing duplicates...")
    products = deduplicate(products)

    # Step 4 - Export
    print("\n💾 Saving data...")
    export_products(products)
    export_summary(products)

    print("\n✅ All done!")

if __name__ == "__main__":
    main()