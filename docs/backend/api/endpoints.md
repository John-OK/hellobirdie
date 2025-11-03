# Backend API Endpoints (MVP)

This document summarizes the backend API endpoints that are in-scope for the xeno-canto integration MVP. See `docs/backend/api/recordings-search-contract.md` for the full response contract.

## Health Check

```
GET /api/health-check
```

Returns the API health status. (Implementation unchanged.)

## Recordings Search (xeno-canto)

```
GET /api/v1/recordings/search
```

Returns bird recordings near a coordinate, backed by the xeno-canto API.

### Query Parameters

- `lat` (number, required): Latitude in decimal degrees (range: -90 to 90).
- `lon` (number, required): Longitude in decimal degrees (range: -180 to 180).
- `radiusKm` (number, optional): Radius in kilometers (default: 50; must be > 0).
- `en` (string, optional): English name contains filter.
- `gen` (string, optional): Scientific genus filter (genus-level search when provided without `sp`).
- `sp` (string, optional): Scientific species filter. May be a full scientific name in quotes (e.g., "Falco columbarius") or a specific epithet (e.g., "fuscus"). Can be used alone or together with `gen`.
- `perPage` (integer, optional): Items per page (default 200; min 50; max 500).
- `page` (integer, optional): Page index for this endpoint (default 1).

### Response Shape (200)

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

Each `Recording` item includes:

- `id`, `en`, `gen`, `sp`, `ssp`
- `lat`, `lon`
- `url`, `file`, `lic`
- `q`, `date`, `cnt`, `loc`
- `distanceKm` (null when coordinates are missing)

### Error Responses

```
{
  "error": {
    "code": "validation_error | rate_limited | upstream_timeout | upstream_unavailable | upstream_bad_response | unexpected",
    "message": "...",
    "details": { ... },
    "retryAfterSeconds": number
  }
}
```

HTTP status mapping:

- 400 → `validation_error`
- 429 → `rate_limited`
- 504 → `upstream_timeout`
- 503 → `upstream_unavailable`
- 502 → `upstream_bad_response`
- 500 → `unexpected`

### Notes

- Upstream queries always include `grp:birds` and an outward-rounded (0.01°) `box:`.
- Results are post-filtered to a true 50 km circle using Haversine distance.
- Caching uses TTL=15 minutes with stale-while-revalidate semantics; meta fields surface cache status.
- Pagination aggregates up to three upstream pages (perPage 200) per API response.

---

Additional endpoints will be documented here as they are implemented.
