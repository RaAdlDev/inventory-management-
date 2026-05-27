# 📦 Inventory API

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A REST API for inventory management built with **FastAPI** and **SQLAlchemy 2.0**. Supports product management, stock tracking, user authentication with JWT, role-based access control, and webhook notifications for low stock alerts.

---

## 📁 Project Structure

```
INVENTORY/
├── core/
│   ├── security.py       # JWT, password hashing, auth dependencies
│   └── settings.py       # Environment-based configuration
├── database/
│   ├── connection.py     # SQLAlchemy engine and session
│   └── models.py         # ORM models
├── routers/
│   ├── products.py       # Product and stock endpoints
│   ├── users.py          # User and auth endpoints
│   └── webhook.py        # Webhook receiver endpoint
├── schemas/
│   ├── movements_schemas.py
│   ├── products_schemas.py
│   ├── stock_schemas.py
│   ├── user_schemas.py
│   └── webhook_schemas.py
├── services/
│   ├── products_services.py
│   ├── users_services.py
│   └── webhook_services.py
├── .env
├── main.py
└── requirements.txt
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/RaAdlDev/inventory-management-.git
cd inventory-management-
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secret_key_here
DATABASE_URL=sqlite:///./inventory.db
TOKEN_DURATION=30
ALGORITHM=HS256
DEBUG=False
WEBHOOK_URL=http://localhost:8000/webhook/
```

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | JWT signing key | `mysecretkey123` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./inventory.db` |
| `TOKEN_DURATION` | Token expiry in minutes | `30` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `DEBUG` | Debug mode | `False` |
| `WEBHOOK_URL` | Webhook endpoint URL | `http://localhost:8000/webhook/` |

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## 🔐 Authentication

This API uses **JWT Bearer tokens** and **role-based access control**.

| Role | Access |
|---|---|
| `admin` | Full access to all endpoints |
| `employee` | Can view products and perform stock transactions |

> **Note:** The first registered user is automatically assigned the `admin` role. No token is required for the first registration.

### Login

```http
POST /user/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secret123
```

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests:

```http
Authorization: Bearer <your_token>
```

---

## 📋 Endpoints

### 👤 Users

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/user/register` | Admin | Register a new user |
| `POST` | `/user/login` | None | Login and get JWT token |
| `GET` | `/user/employees` | Admin | List all employees |
| `PATCH` | `/user/promote/{id}` | Admin | Promote employee to admin |
| `DELETE` | `/user/delete/{id}` | Admin | Delete a user |

#### Register a user
```http
POST /user/register
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "johndoe",
  "phone": "+1234567890",
  "password": "securepass123"
}
```

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "phone": "+1234567890",
  "role": "employee"
}
```

---

### 📦 Products

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/products/` | Employee+ | List all products (supports `?name=` search) |
| `POST` | `/products/add` | Admin | Add a new product |
| `PATCH` | `/products/update/{id}` | Admin | Update a product |
| `DELETE` | `/products/delete/{id}` | Admin | Delete a product |
| `GET` | `/products/low_stock` | Admin | List products below threshold |
| `PATCH` | `/products/transaction` | Employee+ | Add or subtract stock |
| `GET` | `/products/movements` | Admin | List all stock movements (supports `?id=` filter) |

#### Add a product
```http
POST /products/add
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Laptop",
  "description": "15-inch business laptop",
  "unit_price": 999.99,
  "threshold": 5
}
```

```json
{
  "product_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "name": "Laptop",
  "description": "15-inch business laptop",
  "unit_price": 999.99,
  "threshold": 5
}
```

#### Perform a stock transaction
```http
PATCH /products/transaction
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "quantity": 10,
  "operation": "add"
}
```

```json
{
  "stock": 10
}
```

> **Note:** When stock drops below the product's `threshold`, a webhook notification is triggered automatically in the background.

---

### 🔔 Webhooks

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/webhook/` | None | Receive low stock webhook notification |

#### Webhook payload (sent automatically on low stock)
```json
{
  "id": "uuid",
  "name": "Laptop",
  "product_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "threshold": 5,
  "stock": 3
}
```

---

## 🗄️ Database Models

```
Users
├── user_id (PK, UUID)
├── username (unique)
├── phone (unique)
├── password (hashed)
└── role (admin | employee)

Products
├── product_id (PK, UUID)
├── name (unique)
├── description (optional)
├── unit_price (Decimal)
├── threshold
└── stock → Stock (1:1, cascade delete)

Stock
├── product_id (PK, FK → Products)
└── stock
    └── transactions → Transactions (1:N)

Transactions
├── transactions_id (PK, UUID)
├── product_id (FK → Stock)
├── movement (add | subtract)
├── quantity
└── movement_date

WebHooks
├── id (PK, UUID)
├── name
├── product_id
├── threshold
└── stock
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | ORM |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation |
| [python-jose](https://github.com/mpdavis/python-jose) | JWT tokens |
| [passlib](https://passlib.readthedocs.io/) | Password hashing (bcrypt) |
| [httpx](https://www.python-httpx.org/) | Async HTTP client (webhooks) |
| [SQLite](https://www.sqlite.org/) | Database |

---

## 📄 License

MIT License. Feel free to use and modify this project.
