from typing import Iterator

from nintendeals.commons.classes.games import Game
from nintendeals.commons.enumerates import Platforms
from nintendeals.noa.api import algolia
from nintendeals.noa.util import build_game


def list_games() -> Iterator[Game]:
    for data in algolia.search_by_prefixes():
        yield build_game(data)


def list_switch2_games() -> Iterator[Game]:
    for data in algolia.search_by_platform_new(Platforms.NINTENDO_SWITCH_2):
        yield build_game(data)


def list_recent_switch_games(limit: int = 1000) -> Iterator[Game]:
    """
    Get recent Nintendo Switch and Switch 2 games for the NA region.

    Results are ordered by descending release date. Nintendo does not expose
    the date on which a record was added to its catalog, so this is intended
    for frequent incremental imports rather than complete catalog discovery.

    Parameters
    ----------
    limit: int
        Number of games to return, between 1 and 1,000.
    """
    for data in algolia.search_recent_switch_games(limit=limit):
        yield build_game(data)


def list_switch_games() -> Iterator[Game]:
    """
    Get a list of Nintendo Switch and Switch 2 games for the NA region.

    Note: game.product_code is unavailable with this method, to get it use the
    method noa.game_info(nsuid).

    Available Features
    ------------------
        * DEMO
        * GAME_VOUCHER
        * ONLINE_PLAY
        * SAVE_DATA_CLOUD

    Yields
    -------
    nintendeals.classes.common.Game:
        Information of a game.
    """
    yield from list_switch2_games()

    yield from list_games()


def list_missing_switch_games(existing_nsuids: set) -> Iterator[Game]:
    for data in algolia.search_missing_by_nsuid(existing_nsuids=existing_nsuids):
        yield build_game(data)
