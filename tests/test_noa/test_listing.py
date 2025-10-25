from unittest import TestCase

from nintendeals import noa
from nintendeals.commons.enumerates import Platforms, Regions
from nintendeals.noa.api.algolia import count_switch_games

LIMIT = 20


class TestListing(TestCase):
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

    def test_list_all_games(self):
        counter = 0

        for index, game in enumerate(noa.list_switch_games()):
            counter += 1

        print("Listed {0} games".format(counter))
