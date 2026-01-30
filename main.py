import json
from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI(title="IMDb Async Scraper")

IMDB_SEARCH_URL = "https://www.imdb.com/title/"


async def extract_json_ld(page):
    """Extract title and description via JSON-LD"""
    json_ld_handle = await page.query_selector('script[type="application/ld+json"]')
    if json_ld_handle:
        text = await json_ld_handle.text_content()
        try:
            data = json.loads(text)
            return {"title": data.get("name"), "description": data.get("description")}
        except json.JSONDecodeError:
            return None
    return None


@app.get("/movies/{title}")
async def get_movie(imdbId: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            )
        )
        # Search by imdb id
        search_url = IMDB_SEARCH_URL + imdbId
        await page.goto(search_url)

        html = await page.content()

        data = await extract_json_ld(page)

        return data
