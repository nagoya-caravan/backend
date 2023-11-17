# calender endpoint

## カレンダー登録

```http request
POST /api/calender
Content-Type: application/json
```

**body**

```json
{
  "calender_name": "str",
  "ical_url": "str"
}
```

**response**

```json
{
  "calender_id": "int"
}
```

***

## カレンダー編集

```http request
PUT /api/calender/:calender-id
Content-Type: application/json
```

**body**

```json
{
  "calender_name": "str",
  "ical_url": "str"
}
```

***

## カレンダーリスト

```http request
GET /api/calender?page,size
Content-Type: application/json
```

**query**

| name | type | default | description |
|------|------|---------|-------------|
| page | int  | 0       | 表示位置        |   
| size | int  | 10      | 1ページの表示数    |

**response**

```json
[
  {
    "calender_id": "int",
    "calender_name": "str",
    "ical_url": "str"
  }
]
```

***

## カレンダー取得

```http request
GET /api/calender/<calender-id>
Content-Type: application/json
```

**response**

```json
{
  "calender_id": "int",
  "calender_name": "str",
  "ical_url": "str"
}
```

***

## カレンダー削除

```http request
DELETE /api/calender/<calender-id>
Content-Type: application/json
```

***

## カレンダー更新

```http request
GET /api/calender/<calender-id>/refresh
Content-Type: application/json
```

***
