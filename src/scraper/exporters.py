import csv
from collections import defaultdict

def export_products(products, filepath="data/products.csv"):
    """Save all products to CSV"""
    if not products:
        print("No products to export!")
        return

    fieldnames = [
        "category", "subcategory", "title", "price",
        "description", "rating", "reviews",
        "image_url", "product_url", "page_num"
    ]

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"✅ Saved {len(products)} products to {filepath}")

def export_summary(products, filepath="data/category_summary.csv"):
    """Generate and save category summary CSV"""
    summary = defaultdict(lambda: {
        "total": 0, "prices": [],
        "missing_desc": 0, "duplicates": 0
    })

    seen_urls = set()
    for p in products:
        key = (p['category'], p['subcategory'])
        url = p['product_url']

        if url in seen_urls:
            summary[key]["duplicates"] += 1
        else:
            seen_urls.add(url)
            summary[key]["total"] += 1
            summary[key]["prices"].append(p['price'])
            if not p['description']:
                summary[key]["missing_desc"] += 1

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            "category", "subcategory", "total_products",
            "avg_price", "min_price", "max_price",
            "missing_descriptions", "duplicates_removed"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for (cat, subcat), data in summary.items():
            prices = data["prices"]
            writer.writerow({
                "category":             cat,
                "subcategory":          subcat,
                "total_products":       data["total"],
                "avg_price":            round(sum(prices)/len(prices), 2) if prices else 0,
                "min_price":            min(prices) if prices else 0,
                "max_price":            max(prices) if prices else 0,
                "missing_descriptions": data["missing_desc"],
                "duplicates_removed":   data["duplicates"]
            })

    print(f"✅ Saved summary to {filepath}")