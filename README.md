# SOFTDESK - Documentation

## Flake8

```
    flake8 --max-line-length=120 --exclude=.venv . > flake8_errors.log
```

## URL
```
http://127.0.0.1:8000/api
```

## Authentication
Les requêtes sont protégées par une authentification JWT token

## API Endpoints

### Users

|      Method       |   Endpoint    |     Description     |
|:-----------------:|:-------------:|:-------------------:|
|        GET        |   `/users`    |   List all users    |
|        GET        | `/users/{id}` | Get a specific user |
|       POST        |   `/users`    |  Create a new user  |
|        PUT        | `/users/{id}` |    Update a user    |
|      DELETE       | `/users/{id}` |    Delete a user    |

#### Exemple
```json
{
    "id": 2,
    "username": "Manon",
    "first_name": "",
    "last_name": "",
    "email": "",
    "birth_date": "1991-11-12",
    "can_be_contacted": false,
    "can_data_be_shared": false
}
```

### Projects

| Method | Endpoint          | Description |
|--------|-------------------|-------------|
| GET | `/projects`       | List all projects |
| GET | `/projects/{id}`  | Get a specific project |
| POST | `/projects`       | Create a new project |
| DELETE | `/projects/{id}/` | Delete a project |

#### Exemple
```json
{
  "id": 1,
  "tilte": "",
  "description": "",
  "type_project": "back",
  "created_at": "2025-03-29T13:38:33.812592Z",
  "link": {
    "contributors": "http://127.0.0.1:8000/api/projects/1/contributors",
    "issues": "http://127.0.0.1:8000/api/projects/1/issues"
 }
}
```

### Contributors

| Method | Endpoint                                  | Description |
|--------|-------------------------------------------|-------------|
| GET | `/projects/{projectId}/contributors/`     | List all contributors of a project |
| GET | `/projects/{projectId}/contributors/{id}` | Get a specific contributor |
| POST | `/projects/{projectId}/contributors`      | Add a user as contributor to a project |
| DELETE | `/projects/{projectId}/contributors/{id}` | Remove a contributor from a project |

#### Exemple
```json
 {
        "id": 3,
        "user": {
            "id": 3,
            "username": "Clément",
            "first_name": "",
            "last_name": "",
            "email": "",
            "birth_date": "2024-01-29",
            "can_be_contacted": false,
            "can_data_be_shared": false
        }
}
```

### Issues

| Method | Endpoint                             | Description |
|--------|--------------------------------------|-------------|
| GET | `/projects/{projectId}/issues/`      | List all issues of a project |
| GET | `/projects/{projectId}/issues/{id}/` | Get a specific issue |
| POST | `/projects/{projectId}/issues/`      | Create a new issue |
| PUT | `/projects/{projectId}/issues/{id}/` | Update an issue |
| DELETE | `/projects/{projectId}/issues/{id}/` | Delete an issue |

#### Exemple
```json
{
        "id": 3,
        "title": "title",
        "description": "description",
        "status": "todo",
        "priority": "low",
        "author": 1,
        "type_issue": "bug",
        "created_at": "2025-03-30T15:32:25.655233Z",
        "link": "http://127.0.0.1:8000/api/projects/1/issues/3/comments/"‡
},
```

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{projectId}/issues/{issueId}/comments` | List all comments of an issue |
| GET | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Get a specific comment |
| POST | `/projects/{projectId}/issues/{issueId}/comments` | Create a new comment |
| PUT | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Update a comment |
| DELETE | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Delete a comment |

#### Exemple
```json
{
  "id": 1,
  "issueId": 1,
  "content": "I can reproduce this issue on iPhone 13.",
  "createdBy": 5,
  "createdAt": "2025-03-02T14:45:00Z"
}
```

## Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
` | `page[number]` | Page number for pagination | `?page[number]=2` |
| `page[size]` | Results per page | `?page[size]=20` |
