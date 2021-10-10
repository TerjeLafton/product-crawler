from typing import Optional

import httpx
import typer


async def fetch_website_body(url: str, client: httpx.AsyncClient) -> Optional[httpx.Response]:
    """
    Fetches the website body from the given URL and returns the response.
    :param url: The URL to fetch
    :param client: An httpx AsyncClient to use for fetching
    :return: The response of the request, if any.
    """
    try:
        response = await client.get(url=url)
        return response
    except httpx.ReadTimeout:
        typer.echo(f'Timeout against {url}')
        return None
