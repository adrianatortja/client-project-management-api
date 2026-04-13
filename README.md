# Client Project Management API

A backend API built with Django and Django REST Framework to manage client projects and tasks with secure JWT authentication and strict ownership control.

## Overview

This project simulates a real-world backend system where users can:

* create and manage projects
* create and manage tasks within those projects
* securely access only their own data

The focus is on building a structured, secure, and scalable REST API.

---

## Features

* Custom user model
* JWT authentication (register & login)
* Project management (create, list)
* Task management (create, list)
* Ownership validation (users only access their own data)
* Relational data modeling (projects → tasks)
* Clean API structure using Django REST Framework

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SimpleJWT
* SQLite

---

## API Structure

### Authentication

* `POST /api/register/`
* `POST /api/login/`

Use the returned access token in headers:

```
Authorization: Bearer <access_token>
```

---

### Projects

* `POST /projects/` → Create project
* `GET /projects/` → List user's projects

---

### Tasks

* `POST /tasks/` → Create task
* `GET /tasks/` → List user's tasks

---

## Example Request

### Create Task

```json
{
  "project": 1,
  "title": "Build task API",
  "description": "Implement task endpoints with validation"
}
```

---

## Security Design

This project enforces strict data ownership:

* Users can only see their own projects
* Users can only create tasks inside their own projects
* Query filtering prevents cross-user access

Example:

```python
Task.objects.filter(project__user=request.user)
```

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/adrianatortja/client-project-management-api.git
cd client-project-management-api
```

Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

---

## Current Status

Completed:

* Authentication (JWT)
* Project model and API
* Task model with enhanced fields
* Task create and list endpoints
* Ownership validation

In progress:

* Task update and delete endpoints
* API response improvements
* Endpoint testing

---

## Learning Focus

This project focuses on backend fundamentals:

* REST API design
* authentication and authorization
* relational database modeling
* handling migrations with existing data
* building real-world backend structure

---

## Author

Adriana Tortja

