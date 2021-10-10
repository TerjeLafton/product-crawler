import json
import os

from pathlib import Path

db = {
    "urls_to_crawl": ["/"],
    "crawled_urls": [],
    "category_urls": [],
    "product_urls": [],
    "products": [],
}


def update_json_database() -> None:
    with open("database.json", "w") as database_file:
        json.dump(db, database_file)


def check_if_json_database_exists() -> bool:
    path = Path("database.json")
    if path.exists():
        return True

    return False


def delete_json_database() -> None:
    if check_if_json_database_exists():
        os.remove("database.json")


def load_json_database(database: dict) -> None:
    if check_if_json_database_exists():
        with open("database.json", "r") as database_file:
            loaded_database = json.load(database_file)

            database["urls_to_crawl"] = loaded_database["urls_to_crawl"]
            database["crawled_urls"] = loaded_database["crawled_urls"]
            database["category_urls"] = loaded_database["category_urls"]
            database["product_urls"] = loaded_database["product_urls"]
            database["products"] = loaded_database["products"]
