import time

from typing import Iterator, Optional

from algoliasearch.search_client import SearchClient

from nintendeals.commons.enumerates import Platforms

APP_ID = "U3B6GR4UA3"
API_KEY = "a29c6927638bfd8cee23993e51e721c9"

INDEX_NAME = "store_game_en_us"
INDEX = None


PLATFORMS = {
    Platforms.NINTENDO_SWITCH: "Nintendo Switch",
    Platforms.NINTENDO_SWITCH_2: "Nintendo Switch 2"
}

PLATFORM_CODES = {
    Platforms.NINTENDO_SWITCH: "7001",
}


def _search_index(query, **options):
    global INDEX

    if not INDEX:
        client = SearchClient.create(APP_ID, API_KEY)
        INDEX = client.init_index(INDEX_NAME)

    response = INDEX.search(query, request_options=options)
    return response.get("hits", [])


def search_by_nsuid(nsuid: str) -> Optional[dict]:
    hits = _search_index(nsuid, restrictSearchableAttributes=["nsuid"])
    return (hits or [{}])[0]


def search_by_platform_new(platform: Platforms) -> Iterator[dict]:
    platform_label = PLATFORMS[platform]

    options = {
        "filters": f'(corePlatforms:"{platform_label}")',
        "hitsPerPage": 100,
    }

    page = -1

    while True:
        page += 1
        options["page"] = page

        items = _search_index("", **options)

        if not items:
            break

        for item in items:
            yield item

        if len(items) < options["hitsPerPage"]:
            break


def search_by_platform(platform: Platforms) -> Iterator[dict]:
    empty_pages = 0

    platform_code = PLATFORM_CODES[platform]

    options = {
        "allowTyposOnNumericTokens": False,
        "queryType": "prefixAll",
        "restrictSearchableAttributes": ["nsuid"],
        "hitsPerPage": 500,
    }

    current = -1

    while True:
        current += 1
        query = f"{platform_code}{current:07}"
        items = _search_index(query, **options)

        if not items:
            empty_pages += 1

        if empty_pages == 5:
            break

        for item in items:
            if item["platform"] != platform:
                continue

            yield item


def search_by_query(query: str, platform: Platforms = None) -> Iterator[dict]:
    hits_per_page = 50

    options = {
        "hitsPerPage": hits_per_page,
    }

    page = -1

    while True:
        page += 1
        options["page"] = page

        items = _search_index(query, **options)

        for item in items:
            if item["topLevelCategoryCode"] != "GAMES":
                continue

            if platform:
                if item["platform"] != platform:
                    continue

            yield item

        if len(items) < hits_per_page:
            break


def count_switch_games():
    global INDEX

    if not INDEX:
        client = SearchClient.create(APP_ID, API_KEY)
        INDEX = client.init_index(INDEX_NAME)

    response = INDEX.search("", {
        "filters": '(corePlatforms:"Nintendo Switch" OR corePlatforms:"Nintendo Switch 2")',
        "hitsPerPage": 1,
    })
    print("Total hits according to Algolia:", response.get("nbHits"))


def search_by_prefixes() -> Iterator[dict]:
    """
    Brute-force search for Nintendo Switch games using NSUID prefix probing.

    This version does NOT skip existing nsuids — filtering should be done
    by the call site. It simply yields all results found under known prefixes.
    """

    prefixes = ("7001", "7005", "7007")  # US eShop observed prefixes
    suffix_len = 7
    sleep_time = 0.1   # seconds between requests
    max_empty = 5      # stop after this many consecutive empty queries

    options = {
        "allowTyposOnNumericTokens": False,
        "queryType": "prefixAll",
        "restrictSearchableAttributes": ["nsuid"],
        "hitsPerPage": 500,
    }

    for prefix in prefixes:
        print(f"🔎 Scanning prefix {prefix}...")
        empty_pages = 0
        current = -1

        while True:
            current += 1
            query = f"{prefix}{current:0{suffix_len}d}"
            items = _search_index(query, **options)

            if not items:
                empty_pages += 1
                if empty_pages >= max_empty:
                    print(f"⏹️  Done scanning {prefix} after {empty_pages} empty pages.")
                    break
                time.sleep(sleep_time * 2)
                continue

            empty_pages = 0

            for item in items:
                yield item

            time.sleep(sleep_time)


def search_missing_by_nsuid(existing_nsuids: set) -> Iterator[dict]:
    """
    Incrementally search for new Nintendo Switch games by probing nsuid patterns,
    skipping any nsuids already present in `existing_nsuids`.

    This uses the same brute-force discovery logic as `search_by_platform`, but
    avoids re-querying known ids. It’s useful for incremental syncs.
    """

    platform_code = "7001"  # US eShop code
    suffix_len = 7

    options = {
        "allowTyposOnNumericTokens": False,
        "queryType": "prefixAll",
        "restrictSearchableAttributes": ["nsuid"],
        "hitsPerPage": 500,
    }

    empty_pages = 0
    current = -1

    # Extract the numeric suffixes from known nsuids for faster skipping
    known_suffixes = set()
    for nsuid in existing_nsuids:
        if nsuid.startswith(platform_code) and len(nsuid) >= len(platform_code) + suffix_len:
            try:
                known_suffixes.add(int(nsuid[len(platform_code):]))
            except ValueError:
                pass

    while True:
        current += 1
        query = f"{platform_code}{current:0{suffix_len}d}"

        # Skip if we already have this id
        if current in known_suffixes:
            continue

        items = _search_index(query, **options)

        if not items:
            empty_pages += 1
            if empty_pages >= 5:
                break
            continue

        empty_pages = 0

        for item in items:
            nsuid = item.get("nsuid")
            if not nsuid or nsuid in existing_nsuids:
                continue

            existing_nsuids.add(nsuid)
            yield item
