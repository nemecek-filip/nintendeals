from typing import Iterator, Optional

import requests

from nintendeals.commons.enumerates import Platforms

SEARCH_URL = "https://search.nintendo-europe.com/en/select"

SYSTEM_NAMES = {
    Platforms.NINTENDO_SWITCH: "Switch",
}

PRODUCT_CODE_PREFIXES = ("HAC", "BEE")
NSUIDS_PREFIXES = "700"


def _expand_document(data: dict) -> Iterator[dict]:
    nsuids = data.get("nsuid_txt", [])
    raw_product_codes = data.get("product_code_txt", [])
    product_codes = [code.replace("-", "") if code[:3] in PRODUCT_CODE_PREFIXES else None for code in raw_product_codes]

    for index in range(max(len(nsuids), len(product_codes))):
        item = data.copy()
        item["nsuid_txt"] = nsuids[index] if index < len(nsuids) else None
        item["product_code_txt"] = product_codes[index] if index < len(product_codes) else None
        yield item


def _search(
    query: str = "*",
    nsuid: str = None,
    platform: Platforms = None,
    sort: str = "title asc",
    limit: int = None,
) -> Iterator[dict]:
    rows = min(limit, 200) if limit else 200

    params = {
        "fq": "type:GAME",
        "q": query,
        "rows": rows,
        "sort": sort,
        "start": -rows,
        "wt": "json",
    }

    if platform:
        system_name = SYSTEM_NAMES[platform]
        params["fq"] += f' AND system_names_txt:"{system_name}"'

    if nsuid:
        params["fq"] += f' AND nsuid_txt:"{nsuid}"'

    yielded = 0

    while limit is None or yielded < limit:
        params["start"] += rows
        response = requests.get(url=SEARCH_URL, params=params)

        if response.status_code != 200:
            break

        json = response.json()["response"].get("docs", [])

        if not len(json):
            break

        for data in json:
            for item in _expand_document(data):
                if limit is not None and yielded >= limit:
                    return

                yield item
                yielded += 1


def search_by_nsuid(nsuid: str) -> Optional[dict]:
    return next((item for item in _search(nsuid=nsuid) if item.get("nsuid_txt") == nsuid), None)


def search_by_platform(platform: Platforms) -> Iterator[dict]:
    yield from _search(platform=platform)


def search_by_query(query: str, platform: Platforms = None) -> Iterator[dict]:
    yield from _search(query=query, platform=platform)


def search_recent_switch_games(limit: int = 1000) -> Iterator[dict]:
    """Yield recently changed Switch records from Nintendo Europe's catalog."""
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 1000:
        raise ValueError("limit must be an integer between 1 and 1000")

    yield from _search(
        platform=Platforms.NINTENDO_SWITCH,
        sort="change_date desc, sorting_title asc",
        limit=limit,
    )
