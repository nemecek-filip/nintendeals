from datetime import datetime
from typing import Iterator

import requests

from nintendeals.classes.games import Game
from nintendeals.constants import EU, SWITCH

LISTING_URL = 'https://search.nintendo-europe.com/en/select'

SYSTEM_NAMES = {
    SWITCH: "Switch",
}


def list_games(platform: str) -> Iterator[Game]:
    assert platform in SYSTEM_NAMES
    system_name = SYSTEM_NAMES[platform]

    rows = 200
    start = -rows

    while True:
        start += rows

        params = {
            "q": "*",
            "wt": "json",
            "sort": "title asc",
            "start": start,
            "rows": rows,
            "fq": f"type:GAME AND system_names_txt:\"{system_name}\""
        }

        response = requests.get(url=LISTING_URL, params=params)
        json = response.json().get('response').get('docs', [])

        if not len(json):
            break

        for data in json:
            game = Game(
                title=data["title_extras_txt"][0],
                region=EU,
                platform=platform,
                nsuid=data.get("nsuid_txt", [None])[0],
                product_code=data.get("product_code_txt", [None])[0],
            )

            game.genres = data.get("pretty_game_categories_txt", [])
            game.players = data.get("players_to")
            game.languages = list(map(
                lambda lang: lang.title(),
                data.get("language_availability", [])
            ))

            try:
                release_date = data["dates_released_dts"][0].split("T")[0]
                game.release_date = datetime.strptime(release_date, '%Y-%m-%d')
            except ValueError:
                pass

            game.amiibo = data.get("near_field_comm_b", False)
            game.demo = data.get("demo_availability", False)
            game.developer = data.get("developer")
            game.dlc = data.get("dlc_shown_b", False)
            game.free_to_play = data.get("price_regular_f") == 0.0
            game.game_vouchers = data.get("switch_game_voucher_b", False)
            game.local_multiplayer = data.get("local_play", False)
            game.online_play = data.get("internet", False)
            game.publisher = data.get("publisher")
            game.save_data_cloud = data.get("cloud_saves_b", False)
            game.voice_chat = data.get("voice_chat_b", False)

            yield game
