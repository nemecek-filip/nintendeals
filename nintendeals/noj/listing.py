from typing import Iterator

from nintendeals.commons.classes.games import Game
from nintendeals.commons.enumerates import Platforms
from nintendeals.noj.api import nintendo
from nintendeals.noj.util import build_game


def list_games(platform: Platforms) -> Iterator[Game]:
    for data in nintendo.search_by_platform(platform):
        yield build_game(data)


def list_switch_games() -> Iterator[Game]:
    """
    Get a list of Switch and Switch 2 games for the JP region.

    Available Features
    ------------------
        * AMIIBO
        * DLC
        * ONLINE_PLAY

    Yields
    -------
    nintendeals.classes.common.Game:
        Information of a game.
    """
    yield from list_games(Platforms.NINTENDO_SWITCH_2)

    yield from list_games(Platforms.NINTENDO_SWITCH)


def list_switch2_games() -> Iterator[Game]:
    yield from list_games(Platforms.NINTENDO_SWITCH_2)
