from unittest import TestCase, mock

import ddt

from nintendeals.commons.enumerates import Platforms
from nintendeals.noe.api import nintendo

LIMIT = 20


@ddt.ddt
class TestNintendo(TestCase):
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
        (Platforms.NINTENDO_SWITCH, "700", "HAC"),
    )
    @ddt.unpack
    def test_search_by_platform(self, platform, nsuid_prefix, playable_on):
        result = nintendo.search_by_platform(platform)

        for index, data in enumerate(result):
            if index > LIMIT:
                break

            nsuid = data.get("nsuid_txt", "")
            playable_ons = data.get("playable_on_txt", [])

            if nsuid:
                self.assertTrue(nsuid.startswith(nsuid_prefix))

            if playable_ons:
                self.assertIn(playable_on, " ".join(playable_ons))
