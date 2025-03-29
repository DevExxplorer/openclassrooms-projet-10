# SOFTDESK - Documentation

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
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "createdAt": "2025-01-15T14:30:00Z"
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
  "tilte": "TITLE",
  "description": "DESCRIPTION",
  "type_project": "back",
  "created_at": "2025-03-29T13:38:33.812592Z",
  "link": {
    "contributors": "http://127.0.0.1:8000/api/projects/1/contributors",
    "issues": "http://127.0.0.1:8000/api/projects/1/issues"
 }
}
```

### Contributors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{projectId}/contributors` | List all contributors of a project |
| GET | `/projects/{projectId}/contributors/{id}` | Get a specific contributor |
| POST | `/projects/{projectId}/contributors` | Add a user as contributor to a project |
| PUT | `/projects/{projectId}/contributors/{id}` | Update a contributor's role |
| DELETE | `/projects/{projectId}/contributors/{id}` | Remove a contributor from a project |

#### Exemple
```json
{
  "id": 1,
  "userId": 5,
  "projectId": 1,
  "username": "mariemartin",
  "role": "developer",
  "joinedAt": "2025-02-15T10:00:00Z"
}
```

#### Exemple
```json
// POST /api/projects/1/contributors
{
  "userId": 5,
  "role": "developer"
}
```

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{projectId}/issues` | List all issues of a project |
| GET | `/projects/{projectId}/issues/{id}` | Get a specific issue |
| POST | `/projects/{projectId}/issues` | Create a new issue |
| PUT | `/projects/{projectId}/issues/{id}` | Update an issue |
| DELETE | `/projects/{projectId}/issues/{id}` | Delete an issue |

#### Exemple
```json
{
  "id": 1,
  "projectId": 1,
  "title": "Login page not responsive",
  "description": "The login page doesn't render correctly on mobile devices",
  "status": "open",
  "createdBy": 5,
  "assignedTo": 3,
  "createdAt": "2025-03-01T11:30:00Z",
  "links": {
    "comments": "/api/projects/1/issues/1/comments"
  }
}
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
