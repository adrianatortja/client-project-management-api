# Client Project Management API

A Django REST API for managing client projects and tasks with JWT authentication and user-based data ownership.

---

## 🚀 Features

- JWT authentication (login, register, refresh)
- Full Project CRUD
- Full Task CRUD
- Ownership validation (users only access their own data)
- Clean DRF generic views
- Task responses include `project_title`
- Tested with Postman

---

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite

---

## 🔐 Authentication

- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/refresh/

Use token:

```
Authorization: Bearer <access_token>
```


## 📁 Projects API

- GET /api/projects/
- POST /api/projects/
- GET /api/projects/<id>/
- PATCH /api/projects/<id>/
- DELETE /api/projects/<id>/

---

## ✅ Tasks API

- GET /api/projects/tasks/
- POST /api/projects/tasks/
- GET /api/projects/tasks/<id>/
- PATCH /api/projects/tasks/<id>/
- DELETE /api/projects/tasks/<id>/

---

## 📌 Example Task

```json
{
  "id": 2,
  "project": 1,
  "project_title": "Client Portal",
  "title": "First task",
  "completed": true
}
```

## 🔒 Permissions

- Authentication required  
- Users only access their own data  

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

## 📊 Status

✔ Complete backend API
✔ Ready for frontend integration

## 👩‍💻 Author

Adriana Tortja
