import asyncio
from typing import Union

import httpx
import typer

from product_crawler.config import base_url
from product_crawler.crawler.parser import parse_website_body
from product_crawler.helpers.fetch_website_body import fetch_website_body
from product_crawler.storage.storage import db


async def start_crawler() -> None:
    while len(db["urls_to_crawl"]) != len(db["crawled_urls"]):
        tasks = [asyncio.create_task(worker(url=url)) for url in db["urls_to_crawl"] if url not in db["crawled_urls"]]

        await asyncio.gather(*tasks)

    typer.echo("\n\n" "Done! 🙌" "\n\n" f"Found {len(db['product_urls'])} products! 🍔🍷🍌")


async def worker(url: Union[str, dict]) -> None:
    if isinstance(url, str):
        db["crawled_urls"].append(url)

        async with httpx.AsyncClient() as client:
            response = await fetch_website_body(url=base_url + url, client=client)
            if isinstance(response, httpx.Response):
                await parse_website_body(response.text)
            else:
                db["crawled_urls"].remove(url)

        typer.echo(
            f"Found {len(db['product_urls'])} "
            f"products🥐 in {len(db['category_urls'])} "
            f"different categories📁 so far!"
        )
