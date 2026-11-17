from dataclasses import dataclass
from typing import Literal

LogSeverity = Literal["info", "warning", "error"]


@dataclass
class CrawlerLog:
    message: str
    tags: list[str] | None
    severity: LogSeverity | None


class CrawlerLogger:
    def __init__(self) -> None:
        self._log_queue: list[CrawlerLog] = []

    def log(
        self,
        message: str,
        tags: list[str] | None = None,
        severity: LogSeverity | None = None,
    ) -> None:
        self._log_queue.append(
            CrawlerLog(message=message, tags=tags, severity=severity)
        )

    def drain(self) -> list[CrawlerLog]:
        return self._log_queue
