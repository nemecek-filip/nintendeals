from unittest import TestCase

from nintendeals import noj
from nintendeals.commons.enumerates import Platforms, Regions

LIMIT = 20


class TestListing(TestCase):
    def test_list_switch_games(self):
        for index, game in enumerate(noj.list_switch_games()):
            if index > LIMIT:
                break

            self.assertIn(game.platform, (Platforms.NINTENDO_SWITCH, Platforms.NINTENDO_SWITCH_2))
            self.assertEqual(game.region, Regions.JP)

            if game.nsuid:
                self.assertTrue(game.nsuid.startswith("700"))
