from unittest import TestCase, mock

from nintendeals import noe
from nintendeals.commons.enumerates import Platforms, Regions

LIMIT = 20


class TestListing(TestCase):
    def test_list_recent_switch_games(self):
        data = {
            "title": "Recently changed",
            "nsuid_txt": "70010000124104",
            "product_code_txt": "BEE-P-TEST-A",
        }

        with mock.patch("nintendeals.noe.listing.nintendo.search_recent_switch_games", return_value=iter([data])):
            games = list(noe.list_recent_switch_games(limit=500))

        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Recently changed")
        self.assertEqual(games[0].platform, Platforms.NINTENDO_SWITCH_2)
        self.assertEqual(games[0].region, Regions.EU)

    def test_list_switch_games(self):
        for index, game in enumerate(noe.list_switch_games()):
            if index > LIMIT:
                break

            self.assertEqual(game.platform, Platforms.NINTENDO_SWITCH)
            self.assertEqual(game.region, Regions.EU)

            if game.nsuid:
                self.assertTrue(game.nsuid.startswith("700"))
