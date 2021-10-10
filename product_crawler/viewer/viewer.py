import typer
from dominate import document  # type: ignore
from dominate.tags import h1, table, td, th, tr  # type: ignore

from product_crawler.storage.storage import db


def show_products_in_terminal() -> None:
    """
    Prints out all scraped products in the terminal.
    """
    for product in db['products']:
        try:
            typer.echo(f"      Title : {product['title']}")  # type: ignore
            typer.echo(f"Description : {product['description']}")  # type: ignore
            typer.echo(f"        URL : {product['url']}")  # type: ignore
            typer.echo(f"      Price : {product['price']}")  # type: ignore
            typer.echo('\n')
        except KeyError:
            pass


def show_products_in_html() -> None:
    """
    Creates a table of all scraped products in a HTML file.
    :return:
    """
    doc = document(title='Products')

    with doc:
        h1('Products')
        with table():
            with tr():
                th('Title'),
                th('URL'),
                th('Price'),
            try:
                for product in db['products']:
                    with tr():
                        td(product['title']),  # type: ignore
                        td(product['url']),  # type: ignore
                        td(product['price']),  # type: ignore
            except KeyError:
                pass

    with open('products.html', 'w') as file:
        file.write(doc.render())
