"""Фикстуры: локальный сервер вместо интернета, чтобы тесты были быстрыми и детерминированными."""

import asyncio
import socket
from collections.abc import Iterator

import pytest
import pytest_asyncio
from aiohttp import web

from hw2.crawler import AsyncCrawler


@pytest_asyncio.fixture
async def site():
    async def ok(request: web.Request) -> web.Response:
        return web.Response(text=f"ok:{request.match_info['i']}")

    async def slow(request: web.Request) -> web.Response:
        await asyncio.sleep(float(request.match_info["sec"]))
        return web.Response(text="slow")

    app = web.Application()
    app.router.add_get("/ok/{i}", ok)
    app.router.add_get("/slow/{sec}", slow)

    runner = web.AppRunner(app, shutdown_timeout=0.1)
    await runner.setup()
    await web.TCPSite(runner, "127.0.0.1", 0).start()
    host, port = runner.addresses[0]
    try:
        yield f"http://{host}:{port}"
    finally:
        await runner.cleanup()


@pytest.fixture
def dead_url() -> Iterator[str]:
    """URL на порт, где никто не слушает: гарантированный ConnectionError.

    Сокет держим открытым до конца теста (без listen), чтобы ОС не отдала
    этот порт кому-то другому и отказ был детерминированным.
    """
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    try:
        yield f"http://127.0.0.1:{port}/gone"
    finally:
        sock.close()


@pytest_asyncio.fixture
async def make_crawler():
    created: list[AsyncCrawler] = []

    def factory(**kwargs) -> AsyncCrawler:
        crawler = AsyncCrawler(**kwargs)
        created.append(crawler)
        return crawler

    try:
        yield factory
    finally:
        for crawler in created:
            await crawler.close()
