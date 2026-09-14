from unittest import TestCase

from nintendeals import noe
from nintendeals.commons.enumerates import Features, Ratings, Regions, Platforms
from nintendeals.noe.util import build_game


class TestGameInfo(TestCase):
    def test_build_game_normalizes_english_locale_in_slug(self):
        game = build_game(
            {
                "title": "Super Smash Bros. Ultimate",
                "nsuid_txt": "70010000012331",
                "url": "/en-gb/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
                "playable_on_txt": ["HAC"],
            }
        )

        self.assertEqual(
            game.slug,
            "/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )
        self.assertEqual(
            game.eshop.uk_en,
            "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )
        self.assertEqual(
            game.eshop.za_en,
            "https://www.nintendo.com/en-za/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )

    def test_build_game_preserves_locale_neutral_slug(self):
        game = build_game(
            {
                "title": "Super Smash Bros. Ultimate",
                "nsuid_txt": "70010000012331",
                "url": "/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
                "playable_on_txt": ["HAC"],
            }
        )

        self.assertEqual(
            game.slug,
            "/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )

    def test_eshop_uses_consolidated_nintendo_locale_urls(self):
        game = build_game(
            {
                "title": "Example",
                "url": "/Games/example.html",
                "playable_on_txt": ["HAC"],
            }
        )
        locales = {
            "at_de": "de-at",
            "be_fr": "fr-be",
            "be_nl": "nl-be",
            "ch_de": "de-ch",
            "ch_fr": "fr-ch",
            "ch_it": "it-ch",
            "de_de": "de-de",
            "es_es": "es-es",
            "fr_fr": "fr-fr",
            "it_it": "it-it",
            "nl_nl": "nl-nl",
            "pt_pt": "pt-pt",
            "uk_en": "en-gb",
            "za_en": "en-za",
        }

        for property_name, locale in locales.items():
            with self.subTest(property_name=property_name):
                self.assertEqual(
                    getattr(game.eshop, property_name),
                    f"https://www.nintendo.com/{locale}/Games/example.html",
                )

    def test_build_game_exposes_application_id(self):
        game = build_game(
            {
                "title": "Swordship",
                "nsuid_txt": "70010000050444",
                "application_id_s": "01002c60178c4000",
                "playable_on_txt": ["HAC"],
            }
        )

        self.assertEqual(game.application_id, "01002c60178c4000")

    def test_build_game_infers_switch_2_from_product_code(self):
        game = build_game(
            {
                "title": "Switch 2 Game",
                "nsuid_txt": "70010000000000",
                "product_code_txt": "BEEPA123A",
            }
        )

        self.assertEqual(game.platform, Platforms.NINTENDO_SWITCH_2)

    def test_build_game_infers_switch_2_from_playable_on(self):
        game = build_game(
            {
                "title": "Switch 2 Download",
                "nsuid_txt": "70010000000000",
                "playable_on_txt": ["BEE"],
            }
        )

        self.assertEqual(game.platform, Platforms.NINTENDO_SWITCH_2)

    def test_game_info_non_existant(self):
        game = noe.game_info("60010000000000")
        self.assertIsNone(game)

    def test_game_info_switch(self):
        game = noe.game_info("70010000012331")

        self.assertEqual(game.platform, Platforms.NINTENDO_SWITCH)
        self.assertEqual(game.region, Regions.EU)
        self.assertEqual(game.title, "Super Smash Bros. Ultimate")
        self.assertEqual(game.nsuid, "70010000012331")
        self.assertEqual(game.unique_id, "AAAB")

        self.assertEqual(
            game.slug,
            "/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )

        self.assertEqual(game.players, 8)
        self.assertFalse(game.free_to_play)

        self.assertEqual(game.rating, (Ratings.PEGI, 12))

        self.assertEqual(game.release_date.year, 2018)
        self.assertEqual(game.release_date.month, 12)
        self.assertEqual(game.release_date.day, 7)

        self.assertIn("Nintendo", game.publishers)

        self.assertEqual(game.features.get(Features.AMIIBO), True)
        self.assertEqual(game.features.get(Features.DEMO), False)
        self.assertEqual(game.features.get(Features.DLC), True)
        self.assertEqual(game.features.get(Features.ONLINE_PLAY), True)
        self.assertEqual(game.features.get(Features.SAVE_DATA_CLOUD), True)
        self.assertEqual(game.features.get(Features.VOICE_CHAT), True)

        self.assertEqual(
            game.eshop.ru_ru,
            "https://www.nintendo.ru/-/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )
        self.assertEqual(
            game.eshop.uk_en,
            "https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )
        self.assertEqual(
            game.eshop.za_en,
            "https://www.nintendo.com/en-za/Games/Nintendo-Switch-games/Super-Smash-Bros-Ultimate-1395713.html",
        )
        self.assertEqual(game.eshop.au_en, "https://ec.nintendo.com/AU/en/titles/70010000012331")
        self.assertEqual(game.eshop.nz_en, "https://ec.nintendo.com/NZ/en/titles/70010000012331")
