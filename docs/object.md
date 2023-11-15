# object

* [endpoint](endpoint.md)
* Typeは[object](object.md)を表す

## Calender

```json
{
  "calender_id": 0,
  "calender_name": "calender-name",
  "ical_url": "url"
}
```

***

## Event

```json
{
  "event_id": 0,
  "calender_id": 0,
  "is_show": true,
  "all_day": false,
  "event_title": "event-title",
  "description": "description",
  "start": "start-date",
  "end": "end-date",
  "location": "location",
  "ical_uid": "ica uid"
}
```

***

## EventEdit

```json
{
  "is_show": true
}
```

***

## Error

```json
{
  "error_id": "error id",
  "message": "message"
}
```

***

## datetime

```
YYYY-mm-dd-HH-MM-SS
```

***

## User

```json
{
  "user_id": 0,
  "user_name": "user name",
  "user_token": "user token"
}
```

***

## UserId

```json
{
  "user_id": 1
}
```

