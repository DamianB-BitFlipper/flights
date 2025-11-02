from typing import Dict
import asyncio
from playwright.async_api import async_playwright


class DummyResponse:
    def __init__(self, body: str) -> None:
        self.status_code: int = 200
        self.text: str = body
        self.text_markdown: str = body


async def afetch_with_playwright(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Handle Google consent page if shown
        if page.url.startswith("https://consent.google.com"):
            await page.click('text="Accept all"')

        # Wait until page finishes all requests
        await page.wait_for_load_state("networkidle")

        # Extract the main HTML content
        body = await page.evaluate(
            "() => document.querySelector('[role=\"main\"]').innerHTML"
        )

        await browser.close()
        return body


async def alocal_playwright_fetch(params: Dict[str, str]) -> DummyResponse:
    url = "https://www.google.com/travel/flights?" + "&".join(f"{k}={v}" for k, v in params.items())
    body = await afetch_with_playwright(url)
    return DummyResponse(body)

def local_playwright_fetch(params: Dict[str, str]) -> DummyResponse:
    return asyncio.run(alocal_playwright_fetch(params))
