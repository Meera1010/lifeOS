# LifeOS — REST API Design Conventions & Standards

This document specifies the RESTful architectural standards used across LifeOS API endpoints.

## 1. Response Envelope Format

All REST responses return a standard JSON structure:

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": { ... },
  "errors": null
}
```

## 2. HTTP Status Code Conventions

- `200 OK`: Standard successful request.
- `201 Created`: Resource successfully created.
- `400 Bad Request`: Validation failure or missing parameters.
- `401 Unauthorized`: Missing or invalid Bearer token.
- `403 Forbidden`: Insufficient RBAC role privileges.
- `404 Not Found`: Resource does not exist.
- `500 Internal Server Error`: Server exception.
