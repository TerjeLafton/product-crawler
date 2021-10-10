import re

from bs4 import BeautifulSoup, ResultSet  # type: ignore

from product_crawler.storage.storage import db, update_json_database


async def parse_website_body(body: str) -> None:
    parsed_body = BeautifulSoup(body, "html.parser")
    tags = parsed_body.find_all("a")

    category_pattern: str = r"\/no\/categories\/\d+"
    product_pattern: str = r"\/no\/products\/\d+"

    categories: list[str] = await find_pattern_in_tags(pattern=category_pattern, tags=tags)
    products: list[str] = await find_pattern_in_tags(pattern=product_pattern, tags=tags)

    await filter_categories_and_products(categories=categories, products=products)


async def filter_categories_and_products(categories: list[str], products: list[str]) -> None:
    for url in categories:
        if url not in db["urls_to_crawl"]:
            db["urls_to_crawl"].append(url)

        if url not in db["category_urls"]:
            db["category_urls"].append(url)

    for url in products:
        if url not in db["product_urls"]:
            db["product_urls"].append(url)

    update_json_database()


async def find_pattern_in_tags(pattern: str, tags: ResultSet) -> list[str]:
    matches: list[str] = []

    for tag in tags:
        url: str = str(tag.get("href"))
        matches.append(url) if re.search(pattern=pattern, string=url) else None

    return matches
