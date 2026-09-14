from unittest import TestCase, mock, skip

import ddt
from algoliasearch.exceptions import RequestException

from nintendeals.commons.enumerates import Platforms
from nintendeals.noa.api import algolia

LIMIT = 20


@ddt.ddt
class TestAlgolia(TestCase):
    @ddt.data(
        ("70010000050443", "7100050443"),
        ("70070000013113", "7700013113"),
        ("70050000056961", "7500056961"),
    )
    @ddt.unpack
    def test_search_by_nsuid_fetches_derived_object_id(self, nsuid, object_id):
        index = mock.Mock()
        index.get_object.return_value = {"nsuid": nsuid, "urlKey": "game-switch"}

        with mock.patch.object(algolia, "_get_index", return_value=index):
            result = algolia.search_by_nsuid(nsuid)

        self.assertEqual(result["nsuid"], nsuid)
        index.get_object.assert_called_once_with(object_id)

    @ddt.data(None, 70010000050443, "", "7001000005044", "700100000504433", "7001000005044x")
    def test_search_by_nsuid_rejects_invalid_input(self, nsuid):
        with mock.patch.object(algolia, "_get_index") as get_index:
            result = algolia.search_by_nsuid(nsuid)

        self.assertIsNone(result)
        get_index.assert_not_called()

    def test_search_by_nsuid_returns_none_for_missing_object(self):
        index = mock.Mock()
        index.get_object.side_effect = RequestException("ObjectID does not exist", 404)

        with mock.patch.object(algolia, "_get_index", return_value=index):
            result = algolia.search_by_nsuid("70010000050443")

        self.assertIsNone(result)

    def test_search_by_nsuid_propagates_other_request_errors(self):
        index = mock.Mock()
        index.get_object.side_effect = RequestException("Rate limit exceeded", 429)

        with mock.patch.object(algolia, "_get_index", return_value=index):
            with self.assertRaises(RequestException):
                algolia.search_by_nsuid("70010000050443")

    def test_search_by_nsuid_rejects_mismatched_record(self):
        index = mock.Mock()
        index.get_object.return_value = {"nsuid": "70010000000000"}

        with mock.patch.object(algolia, "_get_index", return_value=index):
            result = algolia.search_by_nsuid("70010000050443")

        self.assertIsNone(result)

    @ddt.data(
        ("70010000000025", "the-legend-of-zelda-breath-of-the-wild-switch"),
        ("70010000020033", "the-legend-of-zelda-links-awakening-switch"),
    )
    @ddt.unpack
    def test_search_by_nsuid(self, nsuid, slug):
        result = algolia.search_by_nsuid(nsuid)
        self.assertEqual(slug, result["urlKey"])

    @ddt.data(
        (Platforms.NINTENDO_SWITCH, "700", "Nintendo Switch"),
    )
    @ddt.unpack
    def test_search_by_query(self, platform, nsuid_prefix, playable_on):
        result = algolia.search_by_query(query="Zelda", platform=platform)

        for index, data in enumerate(result):
            if index > LIMIT:
                break

            self.assertIn("Zelda", data.get("title"))
            self.assertIn(playable_on, data.get("platform"))

            nsuid = data.get("nsuid")

            if nsuid:
                self.assertIn(nsuid_prefix, nsuid)

    @ddt.data(
        (Platforms.NINTENDO_SWITCH, "7001", "Nintendo Switch"),
    )
    @ddt.unpack
    @skip("Nintendo removed nsuid from the Algolia index's searchable attributes")
    def test_search_by_platform(self, platform, nsuid_prefix, playable_on):
        result = algolia.search_by_platform(platform)

        for index, data in enumerate(result):
            if index > LIMIT:
                break

            self.assertIn(nsuid_prefix, data.get("nsuid"))
            self.assertIn(playable_on, data.get("platform"))
