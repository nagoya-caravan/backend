# object

* Typeは[object](object.md)を表す

## BaseUrls

```json
{
  "base_url": "https://localhost/api",
  "auth_urls": "Type: AuthUrls",
  "calenders_url": "https://localhost/api/calender"
}
```

* [AuthUrls](#authurls)

***

## AuthUrls

```json
{
  "auth_url": "https://localhost/api/auth",
  "login_url": "https://localhost/api/auth/login",
  "refresh_url": "https://localhost/api/auth/refresh",
  "user_url": "https://localhost/api/auth/user"
}
```

***

## LoginInfo

```json
{
  "username": "user-name",
  "password": "plain-password"
}
```

***

## Tokes

```json
{
  "refresh_token": "refresh token",
  "access_token": "access token"
}
```

***

## User

```json
{
  "username": "user name",
  "password": "password"
}
```

***

## CalenderList

```json
[
  "Type: Calender"
]
```

***

## Calender

```json
{
  "calender_url": "resource-url",
  "calender_id": "resource-id",
  "calender_name": "calender-name",
  "event_list_url": "event-list-url"
}
```
***

## EventList

```json
[
  "Type: Event"
]
```

***

## Event

```json
{
  "event_url": "event-url",
  "event_id": "event-id",
  "is_show": true,
  "event_title": "event-title",
  "description": "description",
  "start": "start-date",
  "end": "end-date",
  "location": "location"
}
```