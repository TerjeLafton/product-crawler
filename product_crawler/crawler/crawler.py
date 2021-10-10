import asyncio
from typing import Union

import httpx
import typer

from product_crawler.config import base_url
from product_crawler.crawler.parser import parse_website_body
from product_crawler.helpers.fetch_website_body import fetch_website_body
from product_crawler.storage.storage import db


async def start_crawler() -> None:
    """
    The main function for the the crawler command.
    It loops through URLs in a list of URLs, starts a worker for it and wait for the result.
    Repeat this process until all URLs found have been crawled.
    """
    # urls_to_crawl and crawled_urls are continuously updated
    # and when they are the same length, there are no other URLs to crawl.
    while len(db['urls_to_crawl']) != len(db['crawled_urls']):
        # Create a task for every URL that has not been crawled yet.
        tasks = [asyncio.create_task(worker(url=url)) for url in db['urls_to_crawl'] if url not in db['crawled_urls']]

        # Wait for all tasks to finish.
        await asyncio.gather(*tasks)

    typer.echo('\n\n' 'Done! 🙌' '\n\n' f"Found {len(db['product_urls'])} products! 🍔🍷🍌")


async def worker(url: Union[str, dict]) -> None:
    """
    Function for starting a single worker that requests the page of the given URL
    and parses its body.
    :param url: The URL the worker should use
    """
    if isinstance(url, str):

        async with httpx.AsyncClient() as client:
            response = await fetch_website_body(url=base_url + url, client=client)
            if isinstance(response, httpx.Response):

                await parse_website_body(response.text)

                # Append the url to crawled_urls to stop future workers from crawling it.
                db['crawled_urls'].append(url)

        typer.echo(
            f"Found {len(db['product_urls'])} "
            f"products🥐 in {len(db['category_urls'])} "
            f'different categories📁 so far!'
        )
