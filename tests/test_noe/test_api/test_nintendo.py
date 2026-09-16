from unittest import TestCase, mock

import ddt

from nintendeals.commons.enumerates import Platforms
from nintendeals.noe.api import nintendo

LIMIT = 20


@ddt.ddt
class TestNintendo(TestCase):
    def test_search_respects_limit_after_expanding_document(self):
        response = mock.Mock(status_code=200)
        response.json.return_value = {
            "response": {
                "docs": [
                    {
                        "nsuid_txt": ["70010000000001", "70010000000002"],
                        "product_code_txt": ["HAC-P-ONE-A", "HAC-P-TWO-A"],
                    }
                ]
            }
        }

        with mock.patch.object(nintendo.requests, "get", return_value=response) as get:
            result = list(nintendo._search(limit=1))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["nsuid_txt"], "70010000000001")
        self.assertEqual(get.call_args.kwargs["params"]["rows"], 1)

    def test_search_recent_switch_games_uses_change_date_order(self):
        items = iter([{"title": "Recently changed"}])

        with mock.patch.object(nintendo, "_search", return_value=items) as search:
            result = list(nintendo.search_recent_switch_games(limit=500))

        self.assertEqual(result, [{"title": "Recently changed"}])
        search.assert_called_once_with(
            platform=Platforms.NINTENDO_SWITCH,
            sort="change_date desc, sorting_title asc",
            limit=500,
        )

    @ddt.data(0, 1001, -1, 1.5, True, None)
    def test_search_recent_switch_games_rejects_invalid_limit(self, limit):
        with self.assertRaises(ValueError):
            list(nintendo.search_recent_switch_games(limit=limit))

    def test_expand_document_preserves_nsuid_product_code_alignment(self):
        data = {
            "nsuid_txt": ["bundle", "game"],
            "product_code_txt": ["HAC-YA3FE-E", "HAC-PA3FE-B"],
        }

        items = list(nintendo._expand_document(data))

        self.assertEqual(items[0]["nsuid_txt"], "bundle")
        self.assertEqual(items[0]["product_code_txt"], "HACYA3FEE")
        self.assertEqual(items[1]["nsuid_txt"], "game")
        self.assertEqual(items[1]["product_code_txt"], "HACPA3FEB")
        self.assertIsNot(items[0], items[1])
        self.assertEqual(data["nsuid_txt"], ["bundle", "game"])

    def test_expand_document_does_not_shift_or_reuse_product_codes(self):
        data = {
            "nsuid_txt": ["unsupported", "switch-2", "missing"],
            "product_code_txt": ["CTR-P-TEST", "BEE-P-A123-A"],
        }

        items = list(nintendo._expand_document(data))

        self.assertIsNone(items[0]["product_code_txt"])
        self.assertEqual(items[1]["product_code_txt"], "BEEPA123A")
        self.assertIsNone(items[2]["product_code_txt"])

    def test_search_by_nsuid_selects_matching_expanded_item(self):
        items = iter(
            [
                {"nsuid_txt": "70070000015111", "product_code_txt": "HACYA3FEE"},
                {"nsuid_txt": "70010000049963", "product_code_txt": "HACPA3FEB"},
            ]
        )

        with mock.patch.object(nintendo, "_search", return_value=items):
            result = nintendo.search_by_nsuid("70010000049963")

        self.assertEqual(result["nsuid_txt"], "70010000049963")
        self.assertEqual(result["product_code_txt"], "HACPA3FEB")

    @ddt.data(
        (Platforms.NINTENDO_SWITCH, "700", ("HAC", "BEE")),
    )
    @ddt.unpack
    def test_search_by_platform(self, platform, nsuid_prefix, allowed_playable_on):
        result = nintendo.search_by_platform(platform)

        for index, data in enumerate(result):
            if index > LIMIT:
                break

            nsuid = data.get("nsuid_txt", "")
            playable_ons = data.get("playable_on_txt", [])

            if nsuid:
                self.assertTrue(nsuid.startswith(nsuid_prefix))

            if playable_ons:
                self.assertTrue(set(playable_ons).intersection(allowed_playable_on))
