from datetime import datetime
from typing import Dict

from nintendeals.commons.classes.games import Game
from nintendeals.commons.enumerates import Features, Platforms, Ratings, Regions

NSUIDS = {
    "700": Platforms.NINTENDO_SWITCH,
}

PLATFORMS = {
    "HAC": Platforms.NINTENDO_SWITCH,
    "BEE": Platforms.NINTENDO_SWITCH_2,
}


def build_game(data: Dict) -> Game:
    nsuid = data.get("nsuid_txt")
    product_code = data.get("product_code_txt")
    original_platform = (data.get("originally_for_t") or "").upper()
    slug = data.get("url")

    if slug and slug.startswith("/en-gb/"):
        slug = slug[len("/en-gb") :]

    if not product_code:
        product_code = None

    if product_code and product_code[:3] in PLATFORMS:
        platform = PLATFORMS[product_code[:3]]
    elif any(playable_on in PLATFORMS for playable_on in data.get("playable_on_txt", [])):
        platform = next(PLATFORMS[playable_on] for playable_on in data["playable_on_txt"] if playable_on in PLATFORMS)
    elif original_platform in PLATFORMS:
        platform = PLATFORMS[original_platform]
    elif nsuid:
        platform = NSUIDS[nsuid[:3]]
    else:
        platform = PLATFORMS[data["playable_on_txt"][0]]

    game = Game(
        platform=platform,
        region=Regions.EU,
        title=data["title"],
        nsuid=nsuid,
        product_code=product_code,
    )

    game.description = data.get("excerpt")
    game.slug = slug
    game.application_id = data.get("application_id_s")
    game.content_type = data.get("type")
    game.players = data.get("players_to", 0)
    game.free_to_play = data.get("price_regular_f") == 0.0

    # Release Date
    try:
        game.release_date = datetime.strptime(data.get("pretty_date_s"), "%d/%m/%Y")
    except (ValueError, TypeError):
        game.release_date = None

    # Categories
    game.categories = data.get("game_categories_txt", [])

    # Developer
    developer = data.get("developer")
    game.developers = [developer] if developer else []

    # Languages
    languages = data.get("language_availability")
    game.languages = list(map(str.title, languages[0].split(","))) if languages else []

    # Publisher
    publisher = data.get("publisher")
    game.publishers = [publisher] if publisher else []

    # Rating (PEGI)
    age_rating = data.get("age_rating_sorting_i")
    if age_rating is None:
        age_rating = data.get("age_rating_value")
    game.rating = (Ratings.PEGI, age_rating)

    # Features
    game.features = {
        Features.AMIIBO: data.get("near_field_comm_b", False),
        Features.DEMO: data.get("demo_availability", False),
        Features.DLC: data.get("add_on_content_b", False),
        Features.GAME_VOUCHER: data.get("switch_game_voucher_b", False),
        Features.ONLINE_PLAY: data.get("paid_subscription_required_b", False),
        Features.SAVE_DATA_CLOUD: data.get("cloud_saves_b", False),
        Features.VOICE_CHAT: data.get("voice_chat_b", False),
    }

    return game
