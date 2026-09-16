from typing import Iterator

from nintendeals.commons.classes.games import Game
from nintendeals.commons.enumerates import Platforms
from nintendeals.noe.api import nintendo
from nintendeals.noe.util import build_game


def list_games(platform: Platforms) -> Iterator[Game]:
    for data in nintendo.search_by_platform(platform):
        yield build_game(data)


def list_recent_switch_games(limit: int = 1000) -> Iterator[Game]:
    """
    Get recently added or updated Nintendo Switch records for the EU region.

    Results are ordered by Nintendo Europe's catalog modification timestamp.

    Parameters
    ----------
    limit: int
        Number of games to return, between 1 and 1,000.
    """
    for data in nintendo.search_recent_switch_games(limit=limit):
        yield build_game(data)


def list_switch_games() -> Iterator[Game]:
    """
    Get a list of Nintendo Switch games for the EU region.

    Available Features
    ------------------
        * AMIIBO
        * DEMO
        * DLC
        * GAME_VOUCHER
        * ONLINE_PLAY
        * SAVE_DATA_CLOUD
        * VOICE_CHAT

    Yields
    -------
    nintendeals.classes.common.Game:
        Information of a game.
    """
    yield from list_games(Platforms.NINTENDO_SWITCH)
