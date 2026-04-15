# Client Project Management API

A Django REST API for managing client projects and tasks with JWT authentication, user-based data ownership, filtering, search, ordering, project statistics, and nested task data.

---

## 🚀 Features

- JWT authentication (login, register, refresh)
- Full Project CRUD
- Full Task CRUD
- Ownership validation (users only access their own data)
- Clean DRF generic views
- Task responses include `project_title`
- Project filtering by `status`
- Project search by `title`
- Project ordering by `title` and `created_at`
- Task filtering by `completed`
- Project responses include task statistics:
  - `total_tasks`
  - `completed_tasks`
  - `pending_tasks`
- Project responses include nested task data
- Automated API tests
- Tested with Postman

---

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- django-filter
- SQLite

---

## 🔐 Authentication

### Endpoints
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

### Use token

```text
Authorization: Bearer <access_token>
```

---

## 📁 Projects API

- `GET /api/projects/`
- `POST /api/projects/`
- `GET /api/projects/<id>/`
- `PATCH /api/projects/<id>/`
- `DELETE /api/projects/<id>/`

---

## ✅ Tasks API

- `GET /api/projects/tasks/`
- `POST /api/projects/tasks/`
- `GET /api/projects/tasks/<id>/`
- `PATCH /api/projects/tasks/<id>/`
- `DELETE /api/projects/tasks/<id>/`

---

## 🔎 Filtering, Search, and Ordering

### Projects

You can filter, search, and order projects using query parameters.

Examples:

```http
GET /api/projects/?status=active
GET /api/projects/?search=client
GET /api/projects/?ordering=title
GET /api/projects/?ordering=-created_at
```

### Tasks

You can filter and order tasks using query parameters.

Examples:

```http
GET /api/projects/tasks/?completed=true
GET /api/projects/tasks/?completed=false
GET /api/projects/tasks/?ordering=-created_at
```

---

## 📌 Example Task Response

```json
{
  "id": 2,
  "project": 1,
  "project_title": "Client Portal Updated",
  "title": "First task",
  "description": "",
  "completed": true,
  "created_at": "2026-04-12T17:59:23.063141Z"
}
```

---

## 📌 Example Project Response

```json
[
  {
    "id": 1,
    "title": "Client Portal Updated",
    "description": "Backend for managing client projects",
    "status": "active",
    "created_at": "2026-04-10T11:30:39.340348Z",
    "total_tasks": 3,
    "completed_tasks": 1,
    "pending_tasks": 2,
    "tasks": [
      {
        "id": 2,
        "project": 1,
        "project_title": "Client Portal Updated",
        "title": "First task",
        "description": "",
        "completed": true,
        "created_at": "2026-04-12T17:59:23.063141Z"
      },
      {
        "id": 6,
        "project": 1,
        "project_title": "Client Portal Updated",
        "title": "Second task",
        "description": "",
        "completed": false,
        "created_at": "2026-04-12T17:59:23.063141Z"
      },
      {
        "id": 7,
        "project": 1,
        "project_title": "Client Portal Updated",
        "title": "Hack",
        "description": "",
        "completed": false,
        "created_at": "2026-04-12T17:59:23.063141Z"
      }
    ]
  }
]
```

---

## 🔒 Permissions

- Authentication required
- Users only access their own data
- Users cannot create tasks for projects they do not own

---

## ⚙️ Setup

```bash
git clone https://github.com/adrianatortja/client-project-management-api.git
cd client-project-management-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Running Tests

Run project tests with:

```bash
python manage.py test projects
```

Current test coverage includes:
- authenticated project list access
- project task statistics in API response
- nested task data in project response
- ownership filtering so users only see their own projects

---

## 📊 Status

- Complete backend API
- Filtering, search, and ordering added
- Project stats added
- Nested task data added
- Automated tests added
- Ready for frontend integration

---

## 👩‍💻 Author

Adriana Tortja