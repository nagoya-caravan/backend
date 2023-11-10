# endpoint

***

## 目次

```http request
GET /api
Content-Type: application/json
```

### response

[BaseUrls](object.md#baseurls)

***

## auth目次

```http request
GET /api/auth
Content-Type: application/json
```

### response

[AuthUrls](object.md#AuthUrls)

***

## ログインする

```http request
POST /api/auth/login
Content-Type: application/json
```

### body

[LoginInfo](object.md#logininfo)

### response

[Tokens](object.md#tokes)
***

## tokenをリフレッシュする

```http request
POST /api/auth/refresh
Content-Type: application/json
Authorization: Bearer ${refresh-token}
```

### response

[Tokens](object.md#tokes)
***

## user登録

```http request
POST /api/auth/register
Content-Type: application/json
```

### body

[User](object.md#user)
***

## カレンダーリスト

```http request
GET /api/calender?page=0&size=10
Content-Type: application/json
Authorization: Bearer ${access-token}
```

### query

| name | type | default | description   |
|------|------|---------|---------------|
| page | int  | 0       | カレンダーリストの表示位置 |   
| size | int  | 10      | 1ページの表示数      |

### response

[CalenderList](object.md#calenderlist)
***
## カレンダー取得

```http request
GET /api/calender/:calender-id
Content-Type: application/json
Authorization: Bearer ${access-token}
```
### response

[Calender](object.md#calender)

## イベントリスト

```http request
GET /api/calender/:calender-id/event?page=0&size=10
Content-Type: application/json
Authorization: Bearer ${access-token}
```

### query

| name | type | default | description  |
|------|------|---------|--------------|
| page | int  | 0       | イベントリストの表示位置 |   
| size | int  | 10      | 1ページの表示数     |

### response

[EventList](object.md#eventlist)
***
## イベント取得

```http request
GET /api/calender/:calender-id/event:event-id
Content-Type: application/json
Authorization: Bearer ${access-token}
```
### response

[Event](object.md#event)
