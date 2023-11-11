# object

* Typeは[object](object.md)を表す

## Calender

```json
{
  "calender_id": "uuid",
  "calender_name": "calender-name",
  "ical_urls": [
    "url",
    "url"
  ]
}
```

***

## Event

```json
{
  "event_id": "uuid",
  "calender_id": "uuid",
  "is_show": true,
  "event_title": "event-title",
  "description": "description",
  "start": "start-date",
  "end": "end-date",
  "location": "location"
}
```