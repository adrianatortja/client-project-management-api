Client Project Management API

A production-style backend API built with Django and Django REST Framework for managing client projects and tasks, featuring JWT authentication and strict data ownership control.

Overview

This project simulates a real-world backend system where users can:

create and manage projects
create and manage tasks within those projects
securely access only their own data

The API is designed with scalability, security, and clean architecture in mind.

Features
Custom user model
JWT authentication (register, login, refresh)
Full Project CRUD (create, list, retrieve, update, delete)
Full Task CRUD
Ownership validation (users only access their own data)
Relational data modeling (projects → tasks)
Clean API structure using Django REST Framework generics
Improved API responses (includes project_title)
Endpoint testing with Postman
Tech Stack
Python
Django
Django REST Framework
SimpleJWT
SQLite
API Endpoints
Authentication

POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/

Use the returned access token:

Authorization: Bearer <access_token>

Projects

GET /api/projects/
POST /api/projects/
GET /api/projects/<id>/
PATCH /api/projects/<id>/
DELETE /api/projects/<id>/

Tasks

GET /api/projects/tasks/
POST /api/projects/tasks/
GET /api/projects/tasks/<id>/
PATCH /api/projects/tasks/<id>/
DELETE /api/projects/tasks/<id>/

Example Request

Create Task:

{
"project": 1,
"title": "Build task API",
"description": "Implement task endpoints with validation"
}

Example Response

Task Response:

{
"id": 2,
"project": 1,
"project_title": "Client Portal",
"title": "First task",
"description": "",
"completed": true,
"created_at": "2026-04-12T17:59:23.063141Z"
}

Security & Permissions
Authentication required for all endpoints
Users can only access their own projects
Users can only create tasks within their own projects
Query filtering prevents cross-user access

Example:

Task.objects.filter(project__user=request.user)

Unauthorized requests return:
401 Unauthorized

Project Structure

projects/
├── models.py
├── serializers.py
├── views.py
├── urls.py

Setup Instructions

Clone the repository:

git clone https://github.com/adrianatortja/client-project-management-api.git

cd client-project-management-api

Create virtual environment:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Run the server:

python manage.py runserver

Development Workflow
feature branches
pull requests
clean merges into main branch
incremental API improvements
Current Status

Completed:

JWT authentication (login, register, refresh)
Full Project CRUD
Full Task CRUD
Ownership validation across all endpoints
Clean DRF generic views
Improved API responses (project_title)
Full endpoint testing with Postman

This API is fully functional and ready for frontend integration.

Learning Focus
REST API design
authentication and authorization
relational database modeling
secure multi-user data handling
real-world backend structure
Git workflow (branching, PRs, merging)
Author

Adriana Tortja