# API Endpoints (MVP)

> Note: This documentation is for the MVP phase and will be updated as endpoints are implemented.

## Health Check

```
GET /api/health
```

Returns the API health status.

## Bird Sightings

```
GET /api/sightings
```

Returns bird sightings within a specified radius of given coordinates.

### Parameters

- `lat` (required): Latitude of center point
- `lng` (required): Longitude of center point
- `radius` (optional): Search radius in kilometers (default: 50)

## Xeno-canto Integration

```
GET /api/recordings/{id}
```

Retrieves bird recording details from xeno-canto.

### Parameters

- `id` (required): Xeno-canto recording ID

---

Additional endpoints will be documented as they are implemented during the MVP development phase.