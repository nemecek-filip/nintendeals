# Nintendo of America upstream API notes

Last verified: 2026-09-15

This document records observations about Nintendo's unofficial, public-facing
services. It is engineering context, not a promise that `nintendeals` currently
uses or supports every endpoint described here.

## Algolia

Index: `store_game_en_us`

Nintendo removed `nsuid` from the index's searchable attributes in September
2026. Searching or prefix-probing that attribute now fails, and searching for
an NSUID without restricting attributes returns no matching hit.

Known NSUIDs can still be retrieved by exact object ID. For a validated
14-digit NSUID:

```python
object_id = nsuid[0] + nsuid[3:5] + nsuid[7:]
```

Verified examples:

| NSUID | Object ID | Product type |
| --- | --- | --- |
| `70010000050443` | `7100050443` | Game |
| `70050000056961` | `7500056961` | Switch 2 upgrade |
| `70070000013113` | `7700013113` | Bundle |

Exact lookup returns HTTP 404 when an object does not exist. Other request
errors should not be treated as missing products.

The primary index cannot provide full catalog enumeration through the public
key:

- Ordinary search exposes at most the first 1,000 matching records.
- The browse endpoint returns HTTP 403 because the key lacks the `browse` ACL.
- Partitioning by title or facets would not guarantee complete coverage.

The `store_game_en_us_release_des` replica still lists `nsuid` as searchable
and accepted exact and prefix NSUID queries during live verification. It also
provides release-date-descending search results, subject to the same 1,000-hit
pagination limit. Because this replica may simply retain older index settings,
clients should not assume that NSUID search will remain available indefinitely.

## Nintendo store sitemap

Nintendo publishes the US store sitemap at:

```text
https://www.nintendo.com/us/store/sitemap.xml
```

It contained 37,604 store URLs, of which roughly 35,208 matched Switch software
URL patterns. It mixes software and merchandise. Its `lastmod` values were all
generated within the same 70-millisecond interval, so they cannot identify
recently changed products; incremental consumers must instead compare URL sets.

## Nintendo mobile-app API (ZNEJ)

The npm package `@maixio/nintendo-eshop-tool` 0.2.1 uses Nintendo's mobile-app
API at:

```text
https://app-api.znej.nintendo.com/api/v2.0
```

The package was published on 2026-06-18. Its linked GitHub repository was not
available when these notes were written, so the published npm tarball was used
as the reference implementation.

### Product details

The `POST /product_details` endpoint accepted multiple products in one request
during live verification. The npm implementation sends groups of 20.

For US products, the API expects a product ID derived by product type:

| NSUID prefix | Type | Product ID |
| --- | --- | --- |
| `7001` | Base title | `71` plus the final eight NSUID digits |
| `7005` | AOC/DLC | `75` plus the final eight NSUID digits |
| `7007` | Bundle | `77` plus the final eight NSUID digits |

The live endpoint returned structured values including:

- The exact NSUID and one or more application title IDs.
- HAC/BEE platform information.
- Short and long descriptions.
- Store URL, images, screenshots, and videos.
- Bundle members and their application IDs.
- Release, upgrade, stock, preorder, and purchase information.

It did not expose all fields currently obtained from the Nintendo product page,
including product code, languages, and player count. It should therefore be
considered an enrichment or fallback source, not a direct scraper replacement.

### Search and enumeration

`GET /products:search` supports text and empty queries and reports `totalCount`
and `hasNextPage`. An empty US query reported 35,802 products with 20 hits per
page. Only pages 1 through 50 returned hits; page 51 and later returned empty
arrays while `hasNextPage` remained true. This is another effective 1,000-item
limit and does not restore complete NOA catalog enumeration.

The results also include hardware and physical products. The tested
`productType` values did not narrow the live response.

## Application title ID resolver

Nintendo exposes a redirect-based regional resolver:

```text
https://ec.nintendo.com/apps/{application_title_id}/{country}
```

It may help map a base game's application ID to a regional product page or
NSUID. It is not a documented JSON API and may fail for DLC, bundles,
region-specific IDs, unavailable products, or Queue-it-protected destinations.

## Actionable follow-ups

These are candidates, not implemented features:

1. Add explicit timeouts and bounded retry handling for Nintendo HTTP calls,
   especially HTTP 429 and transient 5xx responses.
2. Add a small ZNEJ adapter as an optional fallback for known-NSUID detail
   lookup and application-ID enrichment.
3. Add a batched known-NSUID API that uses ZNEJ product-detail groups and only
   scrapes individual product pages for fields still missing.
4. Model multiple application IDs, product type, and bundle members while
   retaining the singular `Game.application_id` property for compatibility.
5. Add a health check for NSUID prefix searching on the release-date replica
   and use the store sitemap as an independent discovery fallback.

Because these endpoints are undocumented, implementations should use fixture-
based unit tests plus a small, separately runnable network smoke-test suite.
