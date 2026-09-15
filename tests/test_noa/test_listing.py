from unittest import TestCase, mock, skip

from nintendeals import noa
from nintendeals.commons.enumerates import Platforms, Regions
from nintendeals.noa.api.algolia import count_switch_games

LIMIT = 20


class TestListing(TestCase):
    def test_list_recent_switch_games(self):
        data = {
            "platform": "Nintendo Switch 2",
            "title": "Recent Game",
            "nsuid": "70010000135065",
        }

        with mock.patch("nintendeals.noa.listing.algolia.search_recent_switch_games", return_value=iter([data])):
            games = list(noa.list_recent_switch_games(limit=500))

        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Recent Game")
        self.assertEqual(games[0].platform, Platforms.NINTENDO_SWITCH_2)
        self.assertEqual(games[0].region, Regions.NA)

    def test_list_switch_games(self):
        for index, game in enumerate(noa.list_switch_games()):
            if index > LIMIT:
                break

            # self.assertEqual(game.platform, Platforms.NINTENDO_SWITCH)
            self.assertEqual(game.region, Regions.NA)

            if game.nsuid:
                self.assertTrue(game.nsuid.startswith("700"))

    def test_list_switch2_games(self):
        for index, game in enumerate(noa.list_switch2_games()):
            if index > LIMIT:
                break

            print(game)

    @skip("Nintendo removed nsuid from the Algolia index's searchable attributes")
    def test_list_all_games(self):
        counter = 0

        for index, game in enumerate(noa.list_switch_games()):
            counter += 1

        print("Listed {0} games".format(counter))
