# Changelog

Notable package changes and upstream compatibility discoveries are recorded here.

## Unreleased

### Fixed

- Replace Nintendo of America Algolia NSUID searches with exact object lookups.
  Nintendo removed `nsuid` from the index's searchable attributes in September
  2026. For a 14-digit NSUID, the Algolia object ID is derived as
  `nsuid[0] + nsuid[3:5] + nsuid[7:]`.
- Validate NOA NSUIDs before making a request, verify that the returned record
  contains the requested NSUID, and treat only HTTP 404 as a missing game.
  Other Algolia request failures continue to propagate.

### Known limitations

- NOA catalog enumeration by NSUID prefix no longer works because `nsuid` is
  not searchable. This affects `noa.list_switch_games()` and
  `noa.list_missing_switch_games()`.
- Empty-query platform searches are not a complete replacement. Nintendo's
  Algolia index exposes more than 1,000 records per platform, while ordinary
  search pagination makes only the first 1,000 results accessible.
- Algolia's browse endpoint would support complete enumeration, but Nintendo's
  public search key currently returns HTTP 403 for browse requests.

### Previously completed related work

- Preserve NOE NSUID/product-code array alignment without mutating source
  documents.
- Recognize HAC and BEE product codes and expose Nintendo application IDs on
  `Game` objects for both NOE and NOA detail lookups.
