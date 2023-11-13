# endpoint

structure
![structure](img/structure.png)

***

## カレンダー登録

```http request
POST /api/calender
Content-Type: application/json
```

**body**

> [Calender](object.md#calender)

**response**

```json
{
  "calender_id": 0
}
```

***

## カレンダー編集

```http request
PUT /api/calender/:calender-id
Content-Type: application/json
```

**body**

> [Calender](object.md#calender)

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

> [
> [Calender](object.md#calender)
> ]

***

## カレンダー取得

```http request
GET /api/calender/<calender-id>
Content-Type: application/json
```

**response**

> [Calender](object.md#calender)

***

## カレンダー更新

```http request
GET /api/calender/<calender-id>/refresh
Content-Type: application/json
```

***

## イベント編集

```http request
PUT /api/event/<id>
Content-Type: application/json
```

**body**

> [EventEdit](./object.md#eventedit)

## イベントリスト

```http request
GET /api/calender/<calender-id>/event?start,end
Content-Type: application/json
```

**response**
[
[Event](object.md#event)
]

## 公開イベントリスト

```http request
GET /api/calender/<calender-id>/public-event?start,end
Content-Type: application/json
```

**response**
[
[Event](object.md#event)
]

