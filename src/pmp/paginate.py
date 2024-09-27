import math
from collections.abc import Callable
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any

import requests


def paginate(
    url: str,
    headers: dict[str, str],
    on_page_fetched: Callable[..., None],
    args: tuple[Any] = ((),),
):
    first_page = __fetch_page(url, 1, headers)
    assert first_page is not None

    total_pages = math.ceil(
        first_page["message_response"]["total"]
        / first_page["message_response"]["limit"]
    )

    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.submit(on_page_fetched, first_page, args)

        # since the first page is already fetched, we need to fetch one less page
        for i in range(total_pages - 1):
            # i is zero-based, so +1 to make it one-based, and another +1 to skip the first page
            executor.submit(
                __fetch_page,
                url,
                i + 2,
                headers,
                on_page_fetched,
                args,
            )


def __fetch_page(
    url: str,
    page: int,
    headers: dict[str, str],
    cb: Callable[..., None] | None = None,
    args: tuple[Any] = ((),),
):
    res = requests.get(f"{url}", params={"page": page}, headers=headers)
    page_json = res.json()
    print(f"page {page} fetched")
    if cb:
        cb(page_json, page, *args)
    else:
        return page_json
