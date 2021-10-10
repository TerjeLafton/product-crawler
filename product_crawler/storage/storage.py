import json
import os
from pathlib import Path
from typing import Union

# The object representing the database of the application.
# This is dumped into a JSON file to be stored between runs.
db: dict[str, Union[list[Union[str, dict]]]] = {
    'urls_to_crawl': ['/'],
    'crawled_urls': [],
    'category_urls': [],
    'product_urls': [],
    'products': [],
}


def update_json_database() -> None:
    """
    Updates the database with the content of the db above.
    File is created if it doesn't exist.
    """
    with open('database.json', 'w') as database_file:
        json.dump(db, database_file)


def check_if_json_database_exists() -> bool:
    """
    Check if the JSON database exists by looking for the path.
    :return: A boolean to indicate if the JSON database exists or not.
    """
    path = Path('database.json')
    if path.exists():
        return True

    return False


def delete_json_database() -> None:
    """
    Delete the JSON database if it exists.
    """
    if check_if_json_database_exists():
        os.remove('database.json')


def load_json_database(database: dict) -> None:
    """
    Load the JSON database into the database variable.
    :param database: The variable to load the JSON database into.
    """
    if check_if_json_database_exists():
        with open('database.json') as database_file:
            loaded_database = json.load(database_file)

            database['urls_to_crawl'] = loaded_database['urls_to_crawl']
            database['crawled_urls'] = loaded_database['crawled_urls']
            database['category_urls'] = loaded_database['category_urls']
            database['product_urls'] = loaded_database['product_urls']
            database['products'] = loaded_database['products']
