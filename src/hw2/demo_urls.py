"""Набор из 100 URL для демо-краулера.

40 HTML-страниц с scraping-песочниц (настоящий HTML, ссылки, пагинация)
и 60 эндпоинтов httpbin.org, покрывающих поведение, на котором обычно
ломаются краулеры: коды ответа, редиректы, задержки, content-type,
сжатие, размер тела, cookies, кэш.

Особые случаи (проверены реальным прогоном):

- 9 URL отвечают не-2xx: 201, 204, 400, 401, 403, 404, 418, 500, 503.
- 5 URL отдают цепочку редиректов; /status/301 тоже редиректит (301 -> 302).
- /delay/0.5, /delay/1, /delay/2 нужны, чтобы показать, что семафор реально
  параллелит: сумма задержек 3.5 с проходится быстрее.
- image/png, image/jpeg и bytes/102400 не декодируются через resp.text() —
  они проверяют, что краулер фильтрует по content-type.
- /brotli требует пакета Brotli (`uv add brotli`), иначе aiohttp падает
  с ClientResponseError. Это единственный URL, который не работает
  на голых зависимостях проекта.

Использование:

    from hw2.demo_urls import DEMO_URLS
    results = await crawler.fetch_urls(list(DEMO_URLS))
"""

from typing import Final

# --- books.toscrape.com: каталог, 10 страниц пагинации ----------------------

BOOKS_CATALOGUE: Final[tuple[str, ...]] = tuple(
    f"https://books.toscrape.com/catalogue/page-{i}.html" for i in range(1, 11)
)

# --- books.toscrape.com: 20 карточек книг (реальные слаги) ------------------

BOOKS_DETAIL: Final[tuple[str, ...]] = (
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html",
    "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
    "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
    "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html",
    "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html",
    "https://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html",
    "https://books.toscrape.com/catalogue/the-boys-in-the-boat-nine-americans-and-their-epic-quest-for-gold-at-the-1936-berlin-olympics_992/index.html",
    "https://books.toscrape.com/catalogue/the-black-maria_991/index.html",
    "https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html",
    "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html",
    "https://books.toscrape.com/catalogue/set-me-free_988/index.html",
    "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html",
    "https://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html",
    "https://books.toscrape.com/catalogue/our-band-could-be-your-life-scenes-from-the-american-indie-underground-1981-1991_985/index.html",
    "https://books.toscrape.com/catalogue/olio_984/index.html",
    "https://books.toscrape.com/catalogue/mesaerion-the-best-science-fiction-stories-1800-1849_983/index.html",
    "https://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html",
    "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html",
)

# --- quotes.toscrape.com: 10 страниц пагинации ------------------------------

QUOTES: Final[tuple[str, ...]] = tuple(
    f"https://quotes.toscrape.com/page/{i}/" for i in range(1, 11)
)

# --- httpbin.org: коды ответа -----------------------------------------------

HTTPBIN_STATUS: Final[tuple[str, ...]] = (
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/201",
    "https://httpbin.org/status/204",
    "https://httpbin.org/status/301",  # 301 -> 302 -> 200, history из двух шагов
    "https://httpbin.org/status/400",
    "https://httpbin.org/status/401",
    "https://httpbin.org/status/403",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/418",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/503",
)

# --- httpbin.org: редиректы -------------------------------------------------

HTTPBIN_REDIRECT: Final[tuple[str, ...]] = (
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/redirect/2",
    "https://httpbin.org/redirect/3",
    "https://httpbin.org/relative-redirect/2",
    "https://httpbin.org/absolute-redirect/2",
)

# --- httpbin.org: задержки (проверка, что семафор реально параллелит) ------

HTTPBIN_DELAY: Final[tuple[str, ...]] = (
    "https://httpbin.org/delay/0.5",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
)

# --- httpbin.org: content-type, сжатие, размер тела -------------------------

HTTPBIN_CONTENT: Final[tuple[str, ...]] = (
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/xml",
    "https://httpbin.org/robots.txt",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/svg",
    "https://httpbin.org/gzip",
    "https://httpbin.org/deflate",
    "https://httpbin.org/brotli",
    "https://httpbin.org/bytes/1024",
    "https://httpbin.org/bytes/102400",
)

# --- httpbin.org: заголовки, cookies, кэш -----------------------------------

HTTPBIN_META: Final[tuple[str, ...]] = (
    "https://httpbin.org/headers",
    "https://httpbin.org/user-agent",
    "https://httpbin.org/ip",
    "https://httpbin.org/uuid",
    "https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l",
    "https://httpbin.org/cookies",
    "https://httpbin.org/cookies/set?demo=1",
    "https://httpbin.org/cache/60",
    "https://httpbin.org/etag/demo-etag",
    "https://httpbin.org/response-headers?X-Demo=1",
)

# --- httpbin.org: echo с разными query, 19 штук -----------------------------

HTTPBIN_ECHO: Final[tuple[str, ...]] = tuple(
    f"https://httpbin.org/anything?i={i}" for i in range(19)
)

HTML_URLS: Final[tuple[str, ...]] = BOOKS_CATALOGUE + BOOKS_DETAIL + QUOTES

HTTPBIN_URLS: Final[tuple[str, ...]] = (
    HTTPBIN_STATUS
    + HTTPBIN_REDIRECT
    + HTTPBIN_DELAY
    + HTTPBIN_CONTENT
    + HTTPBIN_META
    + HTTPBIN_ECHO
)

DEMO_URLS: Final[tuple[str, ...]] = HTML_URLS + HTTPBIN_URLS

if len(DEMO_URLS) != 100:
    raise AssertionError(f"expected 100 urls, got {len(DEMO_URLS)}")
if len(set(DEMO_URLS)) != len(DEMO_URLS):
    raise AssertionError("duplicate urls in DEMO_URLS")
