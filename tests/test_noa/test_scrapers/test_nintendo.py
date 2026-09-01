import json
from unittest import TestCase, mock

import ddt

from nintendeals.noa.scrapers import nintendo


@ddt.ddt
class TestNintendo(TestCase):
    @mock.patch("nintendeals.noa.scrapers.nintendo.requests.get")
    def test_scrap_exposes_application_id(self, get):
        sku = "70010000050443"
        product = {
            "urlKey": "swordship-switch",
            "name": "Swordship",
            "nsuid": sku,
            "productCode": "HACPA7T4A",
            "applicationId": "01002c60178c4000",
            "supportedLanguages": ["English"],
            "playersMaxLocal": 1,
            "playersMaxOnline": None,
            "downloadableContents": [],
        }
        next_data = {
            "props": {
                "pageProps": {
                    "linkedData": {"sku": sku},
                    "initialApolloState": {f'Product:{{"sku":"{sku}"}}': product},
                }
            }
        }
        get.return_value.status_code = 200
        get.return_value.text = f'<script id="__NEXT_DATA__">{json.dumps(next_data)}</script>'

        result = nintendo.scrap("swordship-switch")

        self.assertEqual(result["application_id"], "01002c60178c4000")

    @ddt.data(
        (
            "the-legend-of-zelda-breath-of-the-wild-switch",
            "70010000000025",
            "HACPAAAAA",
            "The Legend of Zelda™: Breath of the Wild",
        ),
        (
            "the-legend-of-zelda-links-awakening-switch",
            "70010000020033",
            "HACPAR3NA",
            "The Legend of Zelda™: Link’s Awakening",
        ),
    )
    @ddt.unpack
    def test_search_by_nsuid(self, slug, nsuid, product_code, title):
        result = nintendo.scrap(slug)

        self.assertEqual(nsuid, result["nsuid"])
        self.assertEqual(product_code, result["product_code"])
        self.assertEqual(slug, result["slug"])
        self.assertEqual(title, result["title"])
