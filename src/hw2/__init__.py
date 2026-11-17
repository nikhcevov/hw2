import asyncio

from .crawler import AsyncCrawler
from .demo_urls import DEMO_URLS
from .logger import CrawlerLog


async def _crawl(
    urls: list[str], concurrency: int
) -> tuple[dict[str, str], list[CrawlerLog]]:
    crawler = AsyncCrawler(max_concurrent=concurrency)
    try:
        results = await crawler.fetch_urls(urls)
    finally:
        await crawler.close()
    return results, crawler._logger.drain()


CONCURRENCY = 10


def main():
    urls = list(DEMO_URLS)
    print(f"Demo: {len(urls)} urls, concurrency={CONCURRENCY}")

    results, logs = asyncio.run(_crawl(urls, CONCURRENCY))

    print(f"Загружено {len(results)} страниц, {len(logs)} логов")
