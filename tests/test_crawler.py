import time

from aiohttp import ClientTimeout


async def test_valid_urls(site, make_crawler):
    urls = [f"{site}/ok/{i}" for i in range(5)]

    pages = await make_crawler(max_concurrent=5).fetch_urls(urls)

    assert set(pages) == set(urls)
    assert pages[f"{site}/ok/0"] == "ok:0"
    assert pages[f"{site}/ok/4"] == "ok:4"


async def test_dead_url_is_dropped(site, dead_url, make_crawler):
    crawler = make_crawler(max_concurrent=5)
    good = f"{site}/ok/1"

    pages = await crawler.fetch_urls([good, dead_url])

    assert set(pages) == {good}
    errors = [e.tags[0] for e in crawler._logger.drain() if e.severity == "error"]
    assert "client_error" in errors


async def test_timeout_returns_none(site, make_crawler):
    crawler = make_crawler(
        max_concurrent=2,
        timeout=ClientTimeout(total=0.1, connect=0.1),
    )

    assert await crawler.fetch_url(f"{site}/slow/1") is None
    tags = [e.tags[0] for e in crawler._logger.drain()]
    assert "timeout_error" in tags


async def test_parallel_is_faster_than_sequential(site, make_crawler):
    crawler = make_crawler(max_concurrent=4)
    urls = [f"{site}/slow/0.2?i={i}" for i in range(4)]

    started = time.perf_counter()
    for url in urls:
        await crawler.fetch_url(url)
    sequential = time.perf_counter() - started

    started = time.perf_counter()
    pages = await crawler.fetch_urls(urls)
    parallel = time.perf_counter() - started

    assert set(pages) == set(urls)
    assert sequential > 0.7, "сервер должен был отработать 4 x 0.2s подряд"
    assert parallel < sequential / 2
