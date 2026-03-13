from .utils import get_page, resolve_url, clean_text, clean_price

def parse_product(product_info):
    """Visit product page and extract all details"""
    url = product_info['url']
    soup = get_page(url)

    if not soup:
        return None

    try:
        title = clean_text(
            soup.select_one("h4.price + h4, .caption h4")
            and soup.select_one(".caption h4").text
        )
        price_tag = soup.select_one("h4.price")
        price = clean_price(price_tag.text) if price_tag else 0.0

        desc_tag = soup.select_one("p.description")
        description = clean_text(desc_tag.text) if desc_tag else ""

        rating_tag = soup.select_one("div.ratings p:last-child")
        rating = clean_text(rating_tag.text) if rating_tag else ""

        review_tag = soup.select_one("div.ratings p.pull-right")
        reviews = clean_text(review_tag.text) if review_tag else ""

        img_tag = soup.select_one("img.thumbnail")
        image_url = resolve_url(
            img_tag.get("src")
        ) if img_tag else ""

        return {
            "category":     product_info['category'],
            "subcategory":  product_info['subcategory'],
            "title":        title,
            "price":        price,
            "description":  description,
            "rating":       rating,
            "reviews":      reviews,
            "image_url":    image_url,
            "product_url":  url,
            "page_num":     product_info['page_num']
        }

    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None