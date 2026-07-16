# Client Project Management SaaS

A multi-tenant Django REST API + React frontend for managing client projects and tasks, with organizations/teams, role-based access, Stripe subscription billing, JWT auth, and Docker deployment.

---

## 🚀 Features

- JWT authentication (register, login, refresh, `me`)
- **Organizations & teams** — every project belongs to an organization, not a single user
- **Roles**: owner / admin / member, enforced via a dedicated permission class
- Invite existing users into your organization by email
- Full Project & Task CRUD, scoped to the current organization
- Project filtering by `status`, search by `title`, ordering by `title`/`created_at`
- Task filtering by `completed`
- Project responses include task stats (`total_tasks`, `completed_tasks`, `pending_tasks`) and nested tasks
- **Stripe subscription billing** — Free / Pro plans, Checkout, Billing Portal, webhooks
- Free plan is capped at a configurable number of projects; Pro is unlimited
- Automated backend test suite (22 tests) using `factory_boy`
- Simple React (Vite) frontend exercising every feature above
- Dockerized: Postgres + Django (gunicorn/whitenoise) + React (nginx)

---

## 🛠 Tech Stack

**Backend:** Python, Django, Django REST Framework, SimpleJWT, django-filter, django-environ, django-cors-headers, Stripe SDK, Postgres (SQLite in local dev by default)
**Frontend:** React, Vite, react-router, axios
**Deployment:** Docker, docker-compose, gunicorn, whitenoise, nginx

---

## 🏢 Multi-tenancy model

- Every user gets a personal `Organization` automatically on registration (owner role).
- Users can create additional organizations and invite others (owner/admin only).
- `Project`s belong to an `Organization`; `Task`s belong to a `Project`.
- All project/task routes are scoped by organization slug: `/api/orgs/<org_slug>/projects/...`.
- A non-member gets `403` for any org they don't belong to — including nonexistent slugs, so org existence can't be enumerated.

---

## ⚙️ Backend setup (local, SQLite)

```bash
git clone https://github.com/adrianatortja/client-project-management-api.git
cd client-project-management-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

By default `manage.py`/`wsgi.py`/`asgi.py` use `config.settings.dev` (SQLite, permissive CORS for `localhost:5173`, `DEBUG=True`). Copy `.env.example` to `.env` to override any setting (see below).

### Environment variables

Copy `.env.example` to `.env` and fill in real values. Key variables:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key (required in prod) |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames (prod) |
| `DATABASE_URL` | e.g. `postgres://user:pass@host:5432/dbname` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins |
| `FRONTEND_URL` | Used to build Stripe Checkout/Portal redirect URLs |
| `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRO_PRICE_ID` | Stripe test-mode keys (see below) |

### Running tests

```bash
python manage.py test
```

---

## 💳 Stripe setup (test mode)

1. Create a free [Stripe account](https://dashboard.stripe.com/register) and switch to **test mode**.
2. Create a recurring **Price** for your "Pro" plan (Products → Add product), and copy its Price ID into `STRIPE_PRO_PRICE_ID`.
3. Copy your test **Secret key** and **Publishable key** from Developers → API keys into `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY`.
4. Forward webhooks to your local server with the [Stripe CLI](https://docs.stripe.com/stripe-cli):
   ```bash
   stripe listen --forward-to localhost:8000/api/billing/webhook/
   ```
   Copy the printed `whsec_...` value into `STRIPE_WEBHOOK_SECRET`.
5. Use a [Stripe test card](https://docs.stripe.com/testing) (e.g. `4242 4242 4242 4242`) at checkout.

Billing endpoints (all under `/api/orgs/<org_slug>/billing/`, owner/admin only for checkout/portal):
- `GET  billing/` — current plan, status, project limit
- `POST billing/checkout/` — create a Stripe Checkout session for the Pro plan
- `POST billing/portal/` — create a Stripe Billing Portal session (manage/cancel)
- `POST /api/billing/webhook/` — Stripe webhook receiver (signature-verified)

---

## 🔐 Auth endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET  /api/auth/me/`

## 🏢 Organization endpoints

- `GET/POST /api/orgs/` — list my orgs / create a new org (creator becomes owner)
- `GET /api/orgs/<slug>/` — org detail (members only)
- `GET /api/orgs/<slug>/members/` — list members
- `POST /api/orgs/<slug>/invite/` — invite an existing user by email (owner/admin only)

## 📁 Projects & ✅ Tasks (org-scoped)

- `GET/POST /api/orgs/<slug>/projects/`
- `GET/PATCH/DELETE /api/orgs/<slug>/projects/<id>/`
- `GET/POST /api/orgs/<slug>/projects/tasks/`
- `GET/PATCH/DELETE /api/orgs/<slug>/projects/tasks/<id>/`

Examples:

```http
GET /api/orgs/acme/projects/?status=active
GET /api/orgs/acme/projects/?search=client&ordering=-created_at
GET /api/orgs/acme/projects/tasks/?completed=false
```

---

## 🖥 Frontend setup

```bash
cd frontend
cp .env.example .env   # VITE_API_BASE_URL=http://localhost:8000
npm install
npm run dev
```

Visit `http://localhost:5173`. Pages: register/login → organization picker → project list → project detail (tasks) → billing/upgrade.

> **Note:** the frontend was written by hand against Vite/React conventions but has not been run in this environment (Node.js isn't installed here) — run `npm install && npm run dev` yourself and confirm the flow before relying on it.

---

## 🐳 Docker (Postgres + Django + React + nginx)

```bash
cp .env.example .env   # fill in real values, especially SECRET_KEY and Stripe keys
docker compose up --build
```

- `db` — Postgres 16
- `backend` — Django via gunicorn on :8000, runs migrations + collectstatic on start
- `frontend` — React build served by nginx on :80, reverse-proxies `/api/`, `/admin/`, `/static/` to `backend` (same-origin in prod, no CORS needed)

`docker compose config` was used to validate the compose file in this environment; the images themselves have not been built end-to-end here because Docker Desktop's engine wasn't running — build and walk through the app once before deploying.

---

## 🔒 Permissions summary

- Authentication required for all non-auth endpoints
- Org membership required for any org-scoped endpoint (403 otherwise, including for nonexistent org slugs)
- Only owner/admin roles can invite members or manage billing
- Free plan projects are capped (`max_projects`); Pro is unlimited

---

## 📊 Status

- Multi-tenant organizations with roles
- Stripe subscription billing (Checkout, Portal, webhooks, plan limits)
- Org-scoped REST API with full test coverage (22 tests)
- React frontend covering the full flow
- Dockerized for Postgres-backed deployment

---

## 👩‍💻 Author

Adriana Tortja
