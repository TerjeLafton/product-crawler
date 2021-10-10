import asyncio
from typing import Union

import httpx
import typer
from bs4 import BeautifulSoup  # type: ignore

from product_crawler.config import base_url
from product_crawler.helpers.fetch_website_body import fetch_website_body
from product_crawler.storage.storage import db, update_json_database


async def start_scraper() -> None:
    while len(db["product_urls"]) > 0:
        tasks = []

        for i in range(50):
            try:
                tasks.append(asyncio.create_task(worker(url=db["product_urls"][i])))
            except IndexError:
                pass

        await asyncio.gather(*tasks)

        typer.echo(f"Scraped {len(db['products'])} so far, {len(db['product_urls'])} left!")

    typer.echo("\n\n" "Done! 🙌" "\n\n" f"Scraped {len(db['products'])} products! 🍔🍷🍌")


async def worker(url: Union[str, dict]) -> None:
    if isinstance(url, str):
        async with httpx.AsyncClient() as client:
            response = await fetch_website_body(url=base_url + url, client=client)
            if isinstance(response, httpx.Response):
                await parse_product_body(response.text)
                db["product_urls"].remove(url)
            else:
                if url not in db["product_urls"]:
                    db["product_urls"].append(url)


async def parse_product_body(body: str) -> None:
    parsed_body = BeautifulSoup(body, "html.parser")
    meta_tags = parsed_body.find_all("meta")

    product: dict = {}

    for meta_tag in meta_tags:
        meta_content = meta_tag.get("content")
        meta_property = meta_tag.get("property")

        if meta_property == "og:title":
            product["title"] = meta_content

        if meta_property == "og:description":
            product["description"] = meta_content

        if meta_property == "og:url":
            product["url"] = meta_content

        if meta_property == "product:price:amount":
            product["price"] = meta_content

    db["products"].append(product)
    update_json_database()
