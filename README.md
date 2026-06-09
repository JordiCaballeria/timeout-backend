# TimeOut — Backend

> Sports club management platform · Django REST Framework API

TimeOut is a full-stack web platform built to help sports clubs manage their operations digitally: members, teams, events, ticket sales, merchandise, and more. This repository contains the **backend** — a REST API built with Django and Django REST Framework.

---

## Live Demo

La plataforma completa està desplegada i accessible a:

🔗 [timeout-project.vercel.app](https://timeout-project.vercel.app)

> Frontend: Vercel · Backend: Render · Base de dades: Aiven (MySQL)

---

## Features

- JWT authentication and role-based permission system
- Member (soci) management with automated subscription expiry via scheduled cron jobs
- Team and player management, including coaches and staff
- Event and match creation with configurable ticket capacity and pricing
- Ticket purchasing flow with QR code generation for entry validation
- Stripe payment integration for memberships, tickets, and shop orders
- Order management with PDF invoice generation
- Merchandise shop with product categories, sizes, and stock control
- News publishing system linked to events
- Sponsor management
- Automated transactional emails (account activation, ticket delivery, password reset, bulk newsletters) using Django + Jinja2 templates
- Shipping tracking for physical orders
- Swagger/OpenAPI documentation via `drf-yasg`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Django 4.1 + Django REST Framework 3.14 |
| Database | MySQL (via PyMySQL / mysqlclient) |
| Auth | JWT (`djangorestframework-simplejwt`) |
| Payments | Stripe |
| Email templates | Jinja2 |
| Task scheduling | `django-crontab` |
| Server | Gunicorn on Ubuntu Linux |
| API docs | drf-yasg (Swagger/OpenAPI) |

---

## Project Structure

```
timeoutbackend/
├── Botiga/            # Shop: products, sizes, orders, shipping
├── Equip/             # Teams, players, coaches, divisions, categories
├── Esdeveniment/      # Events, matches, tickets, event types
├── noticies/          # News articles
├── Patrocinadors/     # Sponsors
├── User/              # Users, roles, permissions
├── templates/         # HTML email templates (Jinja2)
├── uploads/           # User-uploaded media (profile photos, product images)
├── manage.py
└── unicorn.conf.py    # Gunicorn config
```

Each Django app follows the structure:

```
AppName/
├── api/
│   ├── routes.py
│   ├── serializers.py
│   └── views.py
├── migrations/
├── admin.py
├── models.py
└── __init__.py
```

---

## Running Tests

```bash
python manage.py test
```

The test suite covers key backend logic including automatic member deactivation on subscription expiry, the contact form email endpoint, and the mobile app's today's-events API endpoint.

---

## Related Repositories

| Repository | Description |
|---|---|
| [`timeout-frontend`](https://github.com/JordiCaballeria/timeout-frontend) | React + TypeScript web app (admin panel + public site) |
| `timeout-mobile` | React Native app for QR ticket scanning |

---

## Authors

- **Jordi Caballeria** — [github.com/JordiCaballeria](https://github.com/JordiCaballeria)
- **Isaac González**

---

## Awards

🏆 **1st Prize — Best Entrepreneurship Project**, 4th edition of the *Premios ImpulsFP* (2023)
