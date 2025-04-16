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

### 📁 Projects

| Method    | Endpoint           | Description            | Accès                  |
|-----------|--------------------|------------------------|-------------------------|
| GET       | `/projects`        | List all projects      | `IsProjectContributor` |
| GET       | `/projects/{id}`   | Get a specific project | `IsProjectContributor` |
| POST      | `/projects`        | Create a new project   | `IsAuthenticated`      |
| PUT/PATCH | `/projects/{id}/`  | Update a project       | `IsAuthor`             |
| DELETE    | `/projects/{id}/`  | Delete a project       | `IsAuthor`             |


### 👥 Contributors

| Method | Endpoint                                  | Description                              | Accès           |
|--------|-------------------------------------------|------------------------------------------|------------------|
| GET    | `/projects/{projectId}/contributors/`     | List all contributors of a project       | `IsProjectContributor` |
| GET    | `/projects/{projectId}/contributors/{id}` | Get a specific contributor               | `IsProjectContributor` |
| POST   | `/projects/{projectId}/contributors`      | Add a user as contributor to a project   | `IsAuthor`       |
| DELETE | `/projects/{projectId}/contributors/{id}` | Remove a contributor from a project      | `IsAuthor`       |


### 🔧 Issues

| Méthode | Endpoint | Description | Accès |
|--------|----------|-------------|-------|
| **GET** | `/projects/{projectId}/issues/` | Liste tous les problèmes d’un projet | `IsProjectContributor` |
| **GET** | `/projects/{projectId}/issues/{id}/` | Récupère une issue spécifique | `IsProjectContributor`|
| **POST** | `/projects/{projectId}/issues/` | Crée une nouvelle issue | `IsProjectContributor` |
| **PUT** | `/projects/{projectId}/issues/{id}/` | Modifie une issue | `IsAuthor` |
| **DELETE** | `/projects/{projectId}/issues/{id}/` | Supprime une issue | `IsAuthor`  |



### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{projectId}/issues/{issueId}/comments` | List all comments of an issue |
| GET | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Get a specific comment |
| POST | `/projects/{projectId}/issues/{issueId}/comments` | Create a new comment |
| PUT | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Update a comment |
| DELETE | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Delete a comment |


## Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
` | `page[number]` | Page number for pagination | `?page[number]=2` |
| `page[size]` | Results per page | `?page[size]=20` |
