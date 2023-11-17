# event endpoint

## イベント編集

```http request
PUT /api/event/<id>
Content-Type: application/json
```

**body**

```json
{
  "is_show": "bool"
}
```

## イベントリスト

```http request
GET /api/calender/<calender-id>/event?start,end
Content-Type: application/json
```

**response**

```json
[
  {
    "event_id": "int",
    "calender_id": "int",
    "is_show": "bool",
    "all_day": "bool",
    "event_title": "str",
    "description": "str, null",
    "start": "start-date",
    "end": "end-date",
    "location": "location",
    "ical_uid": "ica uid"
  }
]
```

## 公開イベントリスト

```http request
GET /api/calender/<calender-id>/public-event?start,end
Content-Type: application/json
```

**response**

```json
[
  {
    "event_id": "int",
    "calender_id": "int",
    "is_show": "bool",
    "all_day": "bool",
    "event_title": "str",
    "description": "str, null",
    "start": "start-date",
    "end": "end-date",
    "location": "location",
    "ical_uid": "ica uid"
  }
]
```

***
