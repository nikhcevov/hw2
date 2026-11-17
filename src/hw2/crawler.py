import asyncio

from aiohttp import (
    ClientError,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    TCPConnector,
)

from .logger import CrawlerLogger


class AsyncCrawler:
    def __init__(
        self,
        max_concurrent: int = 10,
        timeout: ClientTimeout | None = None,
    ) -> None:
        if max_concurrent < 1:
            raise ValueError("max_concurrent must be >= 1")
        self._max_concurrent: int = max_concurrent
        self._timeout: ClientTimeout = timeout or ClientTimeout(total=30, connect=15, sock_read=15)
        self._session: ClientSession | None = None
        self._logger = CrawlerLogger()

    def _make_session(self) -> ClientSession:
        if self._session and not self._session.closed:
            return self._session

        connector: TCPConnector = TCPConnector(
            limit=self._max_concurrent,
        )
        self._session = ClientSession(connector=connector, timeout=self._timeout)
        return self._session

    async def fetch_url(self, url: str) -> str | None:
        session = self._make_session()
        try:
            self._logger.log(
                message=f"Loading start for url: {url}",
                severity="info",
                tags=["loading_start"],
            )
            async with session.get(url, raise_for_status=True) as resp:
                data = await resp.text()
                self._logger.log(
                    message=f"Loading success for url: {url} [HTTP: {resp.status}]",
                    severity="info",
                    tags=["loading_success"],
                )
                return data
        except ClientResponseError as exc:
            self._logger.log(
                message=f"response error for url: {url}: {exc!r}",
                severity="error",
                tags=["response_error"],
            )
        except TimeoutError as exc:
            self._logger.log(
                message=f"timeout error for url: {url}: {exc!r}",
                severity="error",
                tags=["timeout_error"],
            )
        except ClientError as exc:
            self._logger.log(
                message=f"client error for url: {url}: {exc!r}",
                severity="error",
                tags=["client_error"],
            )

    async def fetch_urls(self, urls: list[str]) -> dict[str, str]:
        results = await asyncio.gather(
            *(self.fetch_url(url) for url in urls),
            return_exceptions=True,
        )
        pages: dict[str, str] = {}
        for url, result in zip(urls, results, strict=True):
            if isinstance(result, BaseException):
                self._logger.log(
                    message=f"unexpected failure for url: {url}: {result!r}",
                    severity="error",
                    tags=["unexpected_failure"],
                )
            elif result is not None:
                pages[url] = result
        return pages

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
