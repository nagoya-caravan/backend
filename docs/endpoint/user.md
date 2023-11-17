# user endpoint


## ユーザー作成

```http request
POST http://localhost:5000/api/user
Content-Type: application/json
```

**body**

```json
{
  "user_name": "str",
  "user_token": "str"
}
```

**response**

```json
{
  "user_id": "int"
}
```

***

## ユーザー取得

```http request
GET http://localhost:5000/api/user
Content-Type: application/json
Authorization: token
```

**response**

```json
{
  "user_id": "int",
  "user_name": "str",
  "user_token": "null"
}
```

## 他ユーザー取得

```http request
GET http://localhost:5000/api/user/<int: user_id>
Content-Type: application/json
Authorization: token
```

**response**

```json
{
  "user_id": "int",
  "user_name": "str",
  "user_token": "null"
}
```

## ユーザー編集

```http request
PUT http://localhost:5000/api/user
Content-Type: application/json
Authorization: token
```

**body**

```json
{
  "user_name": "str",
  "user_token": "str, null"
}
```
