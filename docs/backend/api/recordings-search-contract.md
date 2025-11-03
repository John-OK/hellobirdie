# Recordings Search API Contract (MVP)

Date: 2025-09-25
Status: Draft (agreed for MVP)
Audience: Backend (DRF) and Frontend (React/TypeScript)

## Overview

- JSON keys use camelCase throughout.
- This endpoint returns bird recordings around a given coordinate with pagination, caching metadata, and optional name filtering.
- The API layer (DRF) returns consistent success and error shapes. The service layer raises domain exceptions; DRF maps them to HTTP.

## Endpoint

- Method: GET
- Path: `/api/v1/recordings/search`

## Query Parameters

- `lat` (number, required): Latitude in decimal degrees. Range: [-90, 90].
- `lon` (number, required): Longitude in decimal degrees. Range: [-180, 180].
- `radiusKm` (number, optional): Radius in kilometers. Default: 50. Must be > 0.
- `en` (string, optional): English name contains filter. Case-insensitive contains.
- `gen` (string, optional): Scientific genus filter. When provided without `sp`, returns all species in the genus.
- `sp` (string, optional): Scientific species filter. May be a full scientific name in quotes (e.g., "Falco columbarius"), a specific epithet (e.g., "fuscus"), or used together with `gen`. `sp` alone is allowed.
- `perPage` (integer, optional): Items per page. Default: 200. Min: 50. Max: 500.
- `page` (integer, optional): 1-based page index for this endpoint. Default: 1.

Rules:
- Scientific filters: `gen` alone is allowed (genus-level search); `sp` alone is allowed; `gen` + `sp` targets a single species.
- Combining `en` with scientific filters applies logical AND (further narrows results).
- The backend always filters to birds using `grp:birds` upstream.
 - Subspecies filtering (`ssp`) is not supported in the MVP. The response item may include `ssp`, but there is no `ssp` query parameter.

## Success Response (200)

Top-level shape:
```
{
  "data": [ Recording, ... ],
  "meta": {
    "page": number,
    "perPage": number,
    "pagesFetched": number,
    "hasNextPage": boolean,
    "servedFromCache": boolean,
    "refreshedAt": "ISO-8601 timestamp",
    "isStale": boolean
  }
}
```

Recording item (fields included in MVP):
- `id` (number): xeno-canto recording id.
- `en` (string|null): English name.
- `gen` (string|null): Genus.
- `sp` (string|null): Species epithet.
- `ssp` (string|null): Subspecies epithet, if any.
- `lat` (number|null): Latitude (normalized to float), if available.
- `lon` (number|null): Longitude (normalized to float), if available.
- `url` (string|null): Recording page URL, normalized to `https://`.
- `file` (string|null): Audio file URL, normalized to `https://`.
- `lic` (string|null): License URL, normalized to `https://`.
- `q` (string|null): Quality rating.
- `date` (string|null): Recording date (YYYY-MM-DD), if provided upstream.
- `cnt` (string|null): Country label.
- `loc` (string|null): Location label.
- `distanceKm` (number|null): Great-circle distance from (`lat`,`lon`) to the query center in kilometers; null if coordinates are missing.

Meta field semantics:
- `page`: The page requested on this endpoint (not the upstream page number).
- `perPage`: The requested items per page for this endpoint.
- `pagesFetched`: How many upstream pages were fetched to assemble this page (bounded by configuration).
- `hasNextPage`: True if more results are available (based on upstream `numPages` and configured caps).
- `servedFromCache`: True if this response was served from cache (fresh or stale).
- `refreshedAt`: ISO-8601 timestamp when this response’s data was last refreshed from upstream (time of last successful fetch).
- `isStale`: True if the cached data is older than TTL at the time of serving (SWR); use for "Update" affordances.
- Response pagination semantics: each API response returns at most `perPage` items. The service may fetch multiple upstream pages to assemble this single response (bounded by configuration); `pagesFetched` reports how many upstream pages were used. If `hasNextPage` is true, the client can request the next API page (`page + 1`) to continue.

Notes:
- `distanceKm` enables proximity sorting and display without extra client work.
- `refreshedAt` enables UI to show "as of" timestamps for data freshness; `isStale` quickly indicates SWR state.

## Error Responses

Uniform shape regardless of error cause:
```
{
  "error": {
    "code": "validation_error | rate_limited | upstream_timeout | upstream_unavailable | upstream_bad_response | unexpected",
    "message": "Human-readable, safe to show",
    "details": { "field": "explanation" },
    "retryAfterSeconds": number
  }
}
```

HTTP status mapping:
- validation_error → 400
- rate_limited → 429 (respect `Retry-After` header when present; include `retryAfterSeconds` in JSON)
- upstream_timeout → 504
- upstream_unavailable → 503
- upstream_bad_response → 502
- unexpected → 500

## Behavior & Semantics

- The backend constructs an outward-rounded bounding box (0.01°) around the center to query xeno-canto via `box:` and always includes `grp:birds`.
- Results are post-filtered to a true 50 km circle by geodesic distance.
- Pagination aggregates upstream pages up to configured caps to produce `perPage` items.
- Caching uses TTL=15m with stale-while-revalidate; `servedFromCache`, `refreshedAt`, and `isStale` reflect cache state.
- URLs returned by xeno-canto that start with `//` are normalized to `https://`.

### Upstream Query Construction Rules (deterministic)

- Tag order (when present) is stable for determinism and cache-key consistency:
  1. `grp:birds`
  2. `box:LAT_MIN,LON_MIN,LAT_MAX,LON_MAX`
  3. `gen:<genus>`
  4. `sp:<species>`
  5. `en:<substring>`
- Query assembly: the service layer joins tags with `+` and quotes multi-word values (e.g., `en:"lesser black-backed gull"`). QueryBuilder returns a list of tags only.
- `box:` formatting:
  - No spaces; exactly three commas.
  - Exactly two decimal places for each coordinate.
  - Outward rounding to 0.01°: mins rounded down; maxes rounded up.
  - Order is `LAT_MIN,LON_MIN,LAT_MAX,LON_MAX`.
- Antimeridian handling: if the true (unrounded) box crosses ±180°, the request is executed as two `box:` queries that wrap the antimeridian; results are merged before circle post-filtering.

## Naming & Versioning

- JSON keys are camelCase.
- Path is versioned: `/api/v1/recordings/search`. Future breaking changes will bump the version (e.g., `/api/v2/...`).

## TDD Acceptance Checklist (for this endpoint)

- Valid inputs produce a 200 with the shape above; fields have correct types and semantics.
- Invalid inputs produce 400 with `error.code=validation_error` and `details`.
- Scientific filters: `gen` alone is accepted (genus-level results); `sp` alone is accepted; `gen+sp` narrows to a single species.
- Upstream timeouts/5xx: retries with backoff+jitter, then mapped to 503/504 accordingly.
- Pagination fields (`page`, `perPage`, `pagesFetched`, `hasNextPage`) are consistent.
- `servedFromCache`, `refreshedAt`, and `isStale` are present and correct when caching is involved.
- Recording fields are normalized (types; URLs; `lon` handling) and include `distanceKm`.
