# MentorByte — Backend (Django REST Framework)

A production-ready REST API for the MentorByte online education platform.

## Tech Stack
- **Django 5** + **Django REST Framework 3.15**
- **PostgreSQL** (via psycopg2 + dj-database-url)
- **SimpleJWT** for access/refresh token authentication
- **WhiteNoise** for static file serving
- **Gunicorn** WSGI server
- Deployed on **Render**

## Payments

This project does **not** integrate a live payment gateway. Checkout confirms
the order and grants enrollment immediately on the backend — see the
comment at the top of `apps/orders/views.py` for the reasoning and for
notes on where to plug in a real gateway later (e.g. SSLCommerz, bKash, or
Stripe, if your country is supported). This keeps the project fully
deployable everywhere while still exercising the complete Order /
Enrollment data model, which is what matters for a portfolio piece.

## Project Structure
```
config/          Django project config (settings, urls, wsgi)
apps/
  accounts/      Custom User model, JWT register/login/me endpoints
  courses/       Course, Category, Instructor, Module, Lesson, Review, Enrollment
  cart/          Per-user cart with price snapshot on add
  orders/        Order creation + instant confirmation + enrollment
  blog/          Blog Post + Tag
```

## API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | `/api/auth/register/` | ❌ | Sign up |
| POST | `/api/auth/login/` | ❌ | Sign in → returns access + refresh token |
| POST | `/api/auth/logout/` | ✅ | Blacklist refresh token |
| POST | `/api/auth/token/refresh/` | ❌ | Get new access token |
| GET/PATCH | `/api/auth/me/` | ✅ | My profile |
| GET | `/api/courses/` | ❌ | List courses (filter, search, paginate) |
| GET | `/api/courses/featured/` | ❌ | Featured courses (home page) |
| GET | `/api/courses/categories/` | ❌ | All categories |
| GET | `/api/courses/<slug>/` | ❌ | Course detail + curriculum |
| POST | `/api/courses/<slug>/reviews/` | ✅ | Post a review |
| GET | `/api/courses/<slug>/enrolled/` | ✅ | Check enrollment status |
| GET | `/api/courses/my/enrollments/` | ✅ | My enrolled courses |
| GET/POST/DELETE | `/api/cart/` | ✅ | View / add to / clear cart |
| DELETE | `/api/cart/<item_id>/` | ✅ | Remove one item |
| POST | `/api/orders/checkout/` | ✅ | Confirm order + grant enrollment instantly |
| GET | `/api/orders/` | ✅ | My order history |
| GET | `/api/orders/<id>/` | ✅ | Single order detail |
| GET | `/api/blog/` | ❌ | Blog posts (search, tag filter) |
| GET | `/api/blog/tags/` | ❌ | All tags |
| GET | `/api/blog/<slug>/` | ❌ | Blog post detail |

## Local Setup

### 1. Clone & create virtual environment
```bash
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create PostgreSQL database
```sql
CREATE DATABASE mentorbyte;
```

### 3. Configure environment

`.env.example` is committed to this repo as a template — it contains no
real secrets. Copy it to your own local `.env` file, which is listed in
`.gitignore` and will never be pushed to GitHub:

```bash
cp .env.example .env
# Edit .env — fill in SECRET_KEY and DATABASE_URL for your machine
```

### 4. Run migrations and seed data
```bash
python manage.py migrate
python manage.py seed_data        # creates admin + sample courses + blog posts
```

### 5. Start the dev server
```bash
python manage.py runserver
# API available at http://localhost:8000
# Admin panel at http://localhost:8000/admin  (admin@mentorbyte.com / Admin@1234)
```

## Deploy to Render

1. Push this folder to a GitHub repository.
2. Create a new **Web Service** on [render.com](https://render.com) connected to your repo.
3. Create a **PostgreSQL** database on Render and copy the internal connection string.
4. Set environment variables directly in the Render dashboard (see `render.yaml`
   for the full list) — there is no `.env` file involved in production;
   Render injects these as real environment variables at runtime.
5. Render auto-runs migrations via the build command.

See `DEPLOYMENT_GUIDE.md` (in the project root, alongside both zips) for the
full step-by-step walkthrough.
