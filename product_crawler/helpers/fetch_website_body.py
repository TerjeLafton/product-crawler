import httpx
import typer


async def fetch_website_body(url: str, client: httpx.AsyncClient) -> httpx.Response:
    try:
        response = await client.get(url=url)
        return response
    except httpx.ReadTimeout:
        typer.echo(f"Timeout against {url}")
