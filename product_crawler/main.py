import asyncio

import typer

from product_crawler.crawler.crawler import start_crawler
from product_crawler.scraper.scraper import start_scraper
from product_crawler.storage.storage import db, delete_json_database, load_json_database

app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    A tool for crawling through all of Oda's categories and scrape metadata from their products.

    Use find-products first to find all products and then scrape-products to gather metadata.
    """


@app.command()
def find_products(delete_db: bool = typer.Option(..., prompt="Delete current database?")) -> None:
    """
    Crawls through all categories on Oda.com to find all products and stores the product URLs in a database.
    Progress can be stopped halfway through and continue later.

    Use --delete-db option to start with a clean database.
    """
    if delete_db:
        delete_json_database()
    else:
        load_json_database(database=db)

    asyncio.run(start_crawler())


@app.command()
def scrape_products() -> None:
    """
    Scrapes every product url gathered for metadata and stores it in a database. saves
    Progress can be stopped halfway through and continue later.
    """
    load_json_database(database=db)

    asyncio.run(start_scraper())
