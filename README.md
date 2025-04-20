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

### 👤 Users

<br>

| Method    | Endpoint           | Description         |
|:----------|:-------------------|:---------------------|
| **GET**       | `/users`           | List all users      |
| **GET**       | `/users/{id}`      | Get a specific user |
| **POST**      | `/users`           | Create a new user   |
| **PUT/PATCH** | `/users/{id}/`     | Update a user       |
| **DELETE**    | `/users/{id}/`     | Delete a user       |

### 📁 Projects

<br>

| Method    | Endpoint           | Description            |
|:----------|:-------------------|:------------------------|
| **GET**       | `/projects`        | List all projects      |
| **GET**       | `/projects/{id}`   | Get a specific project |
| **POST**      | `/projects`        | Create a new project   |
| **PUT/PATCH** | `/projects/{id}/`  | Update a project       |
| **DELETE**    | `/projects/{id}/`  | Delete a project       |

### 👥 Contributors

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| **GET** | `/projects/{projectId}/contributors/` | Liste tous les contributeurs d’un projet |
| **GET** | `/projects/{projectId}/contributors/{id}/` | Récupère un contributeur spécifique |
| **POST** | `/projects/{projectId}/contributors/` | Ajoute un utilisateur comme contributeur |
| **DELETE** | `/projects/{projectId}/contributors/{id}/` | Supprime un contributeur du projet |

### 🔧 Issues

| Méthode | Endpoint                         | Description                           |
|---------|----------------------------------|---------------------------------------|
| **GET** | `/projects/{projectId}/issues/`  | Liste tous les problèmes d’un projet  |
| **GET** | `/projects/{projectId}/issues/{id}/` | Récupère une issue spécifique        |
| **POST** | `/projects/{projectId}/issues/`  | Crée une nouvelle issue               |
| **PUT** | `/projects/{projectId}/issues/{id}/` | Modifie une issue                    |
| **DELETE** | `/projects/{projectId}/issues/{id}/` | Supprime une issue                   |




### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/projects/{projectId}/issues/{issueId}/comments` | List all comments of an issue |
| **GET** | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Get a specific comment |
| **POST** | `/projects/{projectId}/issues/{issueId}/comments` | Create a new comment |
| **PUT** | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Update a comment |
| **DELETE** | `/projects/{projectId}/issues/{issueId}/comments/{id}` | Delete a comment |


## Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
` | `page[number]` | Page number for pagination | `?page[number]=2` |
| `page[size]` | Results per page | `?page[size]=20` |
