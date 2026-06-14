# Spreetail Shared Expenses — Architectural Decisions

This document details key architectural decisions, rationale, and design choices made during development.

---

## 1. Web Architecture: Server-Rendered HTML (FastAPI + Jinja2 + HTMX)

### Decision
Use a server-rendered monolith rather than a separate Single Page Application (SPA).

### Rationale
- **Simplicity & Speed**: A unified codebase eliminates the overhead of managing separate API routes, build configurations, and client-side routers.
- **HTMX integration**: HTMX provides smooth, single-page-like dynamic updates (e.g., adding expense split inputs, removing members, inline audits) by exchanging raw HTML fragments, keeping state entirely on the server.
- **Reduced Bundle Size**: Eliminates heavy React or Vue runtimes.

---

## 2. Database Layer: Asynchronous SQLAlchemy 2.0 & PostgreSQL

### Decision
Use SQLAlchemy 2.0's async extension with `asyncpg` and standard PostgreSQL.

### Rationale
- **Concurrency**: Asyncio database sessions prevent blocking threads during slow DB lookups, ensuring high throughput.
- **Strict Data Integrity**: Implemented foreign keys, unique constraints, and check constraints at the database engine level (e.g., `uq_exchange_rates_currency_date`).
- **Native UUIDs**: Used standard UUIDs as primary keys to prevent ID enumeration vulnerabilities.

---

## 3. Decimal Arithmetic for Currency & Remainder Absorption

### Decision
Represent currency using Python's `Decimal` type and database `Numeric(12, 2)` / `Numeric(12, 6)` instead of floating-point representations.

### Rationale
- Floating-point representations introduce rounding errors (e.g., `0.1 + 0.2 != 0.3`).
- In split calculations, divisions can result in recurring decimals (e.g., $100 / 3 = 33.3333...$). We absorb the remaining fractional part into the user with the largest share to ensure the sum of splits matches the total amount exactly.

---

## 4. Date-Gated Active Membership

### Decision
Members are never permanently deleted from a group's history. Instead, membership is tracked with `joined_at` and `left_at` date columns.

### Rationale
- Permitting deletions would corrupt historical balance calculations and audit trails for past expenses.
- By checking `joined_at <= expense_date AND (left_at IS NULL OR left_at > expense_date)`, we ensure splits only include members who were active *at the exact date* the expense occurred.

---

## 5. Token-Based Authentication via Cryptographically Signed Cookies

### Decision
Use `itsdangerous.URLSafeTimedSerializer` to generate session tokens stored in secure `HttpOnly` cookies.

### Rationale
- **No Database Lookup on Every Token Parse**: The token cryptographically signs the user's email. We verify the signature and expiration without needing database validation on the token structure itself.
- **Session Expiry**: Implemented absolute session expiry of 24 hours.
- **CSRF Mitigation**: Cookies use the `HttpOnly` and `SameSite=Lax` properties to safeguard session persistence.
